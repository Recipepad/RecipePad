from flask import Flask, render_template, request, session, redirect, url_for, abort, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

import os

from config import Config
from CosmosClient import CosmosClient

config = Config()
app = Flask(__name__)
app.secret_key = "recipe secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = config.mysql_uri
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = config.mysql_connect_args
CORS(app)
db = SQLAlchemy(app)
cosmos_client = CosmosClient(config)

from models import *
from utils import *


@app.route("/hello")
def hello():
    version = db.engine.execute("select VERSION()").all()[0][0]
    return "Hello RecipePad in Cloud with MySQL " + str(version)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.json and 'password' in request.json:
        username = request.json['username']
        password = request.json['password']

        account = UserAccount.query.filter_by(username=username).first()
        if account is None:
            msg = "Username not exists"
        elif password != account.password:
            msg = "Incorrect password"
        else:
            session['loggedin'] = True
            session['username'] = username
            session['uid'] = account.uid
            return {'uid': account.uid}, 200
    return {'error': msg}, 400


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('uid', None)
    return {"status": 200}, 200


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.json and 'password' in request.json:
        username = request.json['username']
        password = request.json['password']
        try:
            account = UserAccount(username=username, password=password)
            db.session.add(account)
            db.session.commit()
            session['loggedin'] = True
            session['username'] = username
            session['uid'] = account.uid
            profile = UserProfile(uid=account.uid)
            db.session.add(profile)
            db.session.commit()
            return {"uid": account.uid}, 200
        except IntegrityError:
            msg = 'Error: user name has been registered'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return {'error': msg}, 400


@app.route('/recipe', methods=['POST'])
def create_recipe():
    # Validate form
    required_fields = ['title', 'uid', 'description', 'ingredients', 'steps']
    for field in required_fields:
        if field not in request.json:
            abort(400, f"{field} not found in the form")

    title = request.json['title']
    uid = request.json['uid']
    description = request.json['description']
    ingredients = request.json['ingredients']  # JSON
    steps = request.json['steps']  # JSON

    tags = get_tags_from_description_and_title(description, title)
    step_img_cnt = get_image_count_from_steps(steps)
    cover_imgid = get_cover_image_id(uid)
    step_imgids = get_step_image_ids(uid, step_img_cnt)
    steps = get_updated_steps_with_image_ids(steps, step_imgids)

    recipe = Recipe(
        title=title,
        cover_imgid=cover_imgid,
        description=description,
        ingredients=ingredients,
        steps=steps,
        tags=tags,
    )

    db.session.add(recipe)
    db.session.commit()

    user_recipe = UserRecipe(uid=uid, rid=recipe.rid)
    db.session.add(user_recipe)
    db.session.commit()

    response = {
        'cover_image_url': f'fake/cover/url/{cover_imgid}',
        'step_image_urls': [f'fake/step/url/{rid}' for rid in step_imgids]
    }

    return response, 200


@app.route('/bookmark', methods=['GET', 'POST'])
def bookmark():
    msg = ''

    if request.method == 'POST':
        # TODO: change data from form to json
        data = request.form

        required_fields = ['uid', 'rid']
        for field in required_fields:
            if field not in data:
                abort(400, f"{field} not found in the form")

        uid = data['uid']
        rid = data['rid']

        try:
            if db.session.query(UserAccount).filter_by(uid=uid).first() is None:
                msg = 'fail to bookmark ({uid}, {rid}), uid {uid} not found'.format(uid=uid, rid=rid)
            elif db.session.query(Recipe).filter_by(rid=rid).first() is None:
                msg = 'fail to bookmark ({uid}, {rid}), rid {rid} not found'.format(uid=uid, rid=rid)
            else:
                bookmark = UserBookmark(uid=uid, rid=rid)
                db.session.add(bookmark)
                db.session.commit()
                msg = 'successful bookmark ({uid}, {rid})'.format(uid=uid, rid=rid)
        except IntegrityError:
            msg = 'fail to bookmark ({uid}, {rid}): Already bookmarked'.format(uid=uid, rid=rid)
        except Exception as e:
            msg = str(e)

        # TODO: redirect to recipe(rid) page
        return render_template('bookmark_test.html', msg=msg)

    return render_template('bookmark_test.html', msg=msg)


# TODO: change the naming
@app.route('/get_bookmark', methods=['GET', 'POST'])
def get_bookmark():
    if request.method == 'GET':
        return render_template('get_bookmark_test.html')

    # TODO: change data from form to json
    data = request.form

    required_fields = ['uid']
    for field in required_fields:
        if field not in data:
            abort(400, f"{field} not found in the form")

    uid = data['uid']

    try:
        if db.session.query(UserAccount).filter_by(uid=uid).first() is None:
            msg = 'Fail: uid {uid} not found'.format(uid=uid)
        else:
            results = db.session.query(UserBookmark.rid).filter_by(uid=uid).all()
            results = [r[0] for r in results]
            msg = str(results)
    except Exception as e:
        msg = str(e)

    return render_template('get_bookmark_test.html', msg=msg)


@app.route('/profile/<int:uid>', methods=['GET'])
def get_profile(uid):
    if db.session.query(UserAccount).filter_by(uid=uid).first() is None:
        return {'success': False}, 400
    result = db.session.query(UserProfile).filter_by(uid=uid).first()
    result = result.to_dict()
    result['success'] = True
    return result, 200


@app.route('/profile', methods=['POST'])
def profile():
    data = request.json
    required_fields = ['uid', 'nickname', 'email', 'avatar_imgid']
    for field in required_fields:
        if field not in data:
            abort(400, f"{field} not found in the form")

    uid = data['uid']
    nickname = data['nickname']
    email = data['email']
    avatar_imgid = data['avatar_imgid']

    if db.session.query(UserAccount).filter_by(uid=uid).first() is None:
        return {'success': False}, 400
    db.session.query(UserProfile).update(
        {'uid': uid, 'nickname': nickname, 'email': email, 'avatar_imgid': avatar_imgid})
    db.session.commit()
    return {'success': True}, 200


@app.route('/recipe/<int:rid>', methods=['GET'])
def get_recipe(rid):
    result = db.session.query(Recipe).filter_by(rid=rid).first()
    if result is None:
        return {'success': False, 'error': 'rid not exists in Recipe table'}, 400
    result = result.to_dict()
    result['success'] = True
    return result, 200


# keywords separated by `:`
@app.route('/search/<keywords>', methods=['GET'])
def search_recipe_ids_by_keywords(keywords):
    keywords = keywords.split(':')
    rids = []
    for keyword in keywords:
        rids.extend(cosmos_client.get_rids(keyword))

    return {"rids": rids}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
