from flask import Flask, render_template, request, session, abort
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

import os

from config import Config
from CosmosClient import CosmosClient

config = Config()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.mysql_uri
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = config.mysql_connect_args
bcrypt = Bcrypt(app)
app.secret_key = "recipe secret key"

app.config['SESSION_TYPE'] = 'filesystem'
server_session = Session(app)

CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
cosmos_client = CosmosClient(config)

from models import *
from utils import *


@app.route("/hello")
def hello():
    version = db.engine.execute("select VERSION()").all()[0][0]
    return "Hello RecipePad in Cloud with MySQL " + str(version)


@app.route("/auth")
def get_current_user():
    # uid = session.get('uid')
    # if not uid:
    #     return {"error": "Unathorized"}, 401
    # TODO figure out how to work on cloud
    return {"isAuth": True}, 200


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

    tags = get_tags_from_description_and_title(description, title, ingredients)
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
        'base_url': config.blob_url,
        'cover_image_id': cover_imgid,
        'step_image_id': step_imgids
    }

    return response, 200



# input: {"success":True, "rid":int(rid), "title":str(title), "cover_imgid":str(imgid), "description":str,
#         "ingredients":json, "steps":json, "tags":json"}   See models.py class Recipe for examples.
# if success: return {"success": True}
# if failure: return {"success": False, "error": error msg}
@app.route('/recipe', methods=['PUT'])
def edit_recipe():
    data = request.json
    required_fields = ['rid', 'title', 'description', 'ingredients', 'steps']
    for field in required_fields:
        if field not in data:
            abort(400, f"{field} not found in the form")

    rid = data['rid']
    title = data['title']
    description = data['description']
    ingredients = data['ingredients']
    steps = data['steps']
    tags = get_tags_from_description_and_title(description, title, ingredients)

    if db.session.query(Recipe).filter_by(rid=rid).first() is None:
        return {'success': False, 'error': 'rid not exists in Recipe table'}, 400
    db.session.query(Recipe).filter_by(rid=rid).update(
        {'rid': rid, 'title': title, 'description': description, 'ingredients': ingredients, 'steps':steps, 'tags':tags})
    db.session.commit()
    return {'success': True}, 200



# input: {"uid":uid, "rid":rid}
# if success: return {"success":True}
# if failure: return {"success":False, "error":error msg}
@app.route('/bookmark', methods=['POST'])
def create_bookmark():
    data = request.json

    required_fields = ['uid', 'rid']
    for field in required_fields:
        if field not in data:
            abort(400, f"{field} not found in the form")

    uid = data['uid']
    rid = data['rid']

    try:
        if db.session.query(UserAccount).filter_by(uid=uid).first() is None:
            return {'success':False, 'error':"Uid not Found"}, 400
        elif db.session.query(Recipe).filter_by(rid=rid).first() is None:
            return {'success':False, 'error':"Rid not Found"}, 400
        else:
            bookmark = UserBookmark(uid=uid, rid=rid)
            db.session.add(bookmark)
            db.session.commit()
    except IntegrityError:
        return {'success':False, 'error':"Bookmark already existed"}, 400

    return {'success':True}, 200


# input: {"uid":uid, "rid":rid}
# if success: return {"success":True}
# if failure: return {"success":False, "error":error msg}
@app.route('/bookmark', methods=['DELETE'])
def delete_bookmark():
    data = request.json

    required_fields = ['uid', 'rid']
    for field in required_fields:
        if field not in data:
            abort(400, f"{field} not found in the form")

    uid = data['uid']
    rid = data['rid']

    try:
        if db.session.query(UserBookmark).filter_by(uid=uid,rid=rid).first() is None:
            return {'success':False, 'error':"Bookmark not existed"}, 400

        db.session.query(UserBookmark).filter_by(uid=uid,rid=rid).delete()
        db.session.commit()
    except Exception as e:
        return {'success':False, 'error': e}, 400

    return {'success':True}, 200


# input: uid from URL
# if success: return {"success":True, "rids":list of int(rid)}
# if failure: return {"success":False, "error":error msg}
@app.route('/bookmark/<int:uid>', methods=['GET'])
def get_bookmark(uid):
    if db.session.query(UserAccount).filter_by(uid=uid).first() is None:
        return {'success':False, 'error':"Uid Not Found"}, 400

    results = db.session.query(UserBookmark.rid).filter_by(uid=uid).all()
    results = [r[0] for r in results]
    return {'success':True, 'rids':results}, 200



# input: uid from URL
# if success: return {"uid":int(uid), "nickname":str(nickname), "email":str(email), "avatar_imgid":str(imgid)}
# if failure: return {"success":False, "error": error msg}
@app.route('/profile/<int:uid>', methods=['GET'])
def get_profile(uid):
    if db.session.query(UserAccount).filter_by(uid=uid).first() is None:
        return {'success': False, 'error':"Uid not Found"}, 400
    result = db.session.query(UserProfile).filter_by(uid=uid).first()
    result = result.to_dict()
    result['success'] = True
    return result, 200


# input: {"uid":int(uid), "nickname":str(nickname), "email":str(email), "avatar_imgid":str(imgid)}
# if success: return {"success": True}
# if failure: return {"success": False, "error": error msg}
@app.route('/profile', methods=['POST'])
def edit_profile():
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
        return {'success': False, 'error':"Uid not Found"}, 400
    db.session.query(UserProfile).filter_by(uid=uid).update(
        {'uid': uid, 'nickname': nickname, 'email': email, 'avatar_imgid': avatar_imgid})
    db.session.commit()
    return {'success': True}, 200


# input: uid from URL
# if success: return {"success":True, "rids":list of int(rid)}
# if failure: return {"success":False, "error":error msg}
@app.route('/user/<int:uid>/recipes', methods=['GET'])
def user_recipes(uid):
    if db.session.query(UserAccount).filter_by(uid=uid).first() is None:
        return {'success':False, 'error':"Uid Not Found"}, 400

    results = db.session.query(UserRecipe.rid).filter_by(uid=uid).all()
    results = [r[0] for r in results]
    return {'success':True, 'rids':results}, 200



# input: rid from URL
# if success: return {"success":True, "rid":int(rid), "title":str(title), "cover_imgid":str(imgid), "description":str,
#                     "ingredients":json, "steps":json, "tags":json"}   See models.py class Recipe for examples.
# if failure: return {"success":False, "error": error msg}
@app.route('/recipe/<int:rid>', methods=['GET'])
def get_recipe(rid):
    result = db.session.query(Recipe).filter_by(rid=rid).first()
    if result is None:
        return {'success': False, 'error': 'rid not exists in Recipe table'}, 400
    result = result.to_dict()
    result['success'] = True
    return result, 200


# input: rids from URL (separated by ";")
# if success: return {"success":True, "recipes":list of jsons (list of recipes)}
# if failure: return {"success":False, "error": error msg}
@app.route('/recipes/<rids>', methods=['GET'])
def get_recipes(rids):
    rids = rids.split(';')
    try:
        results = db.session.query(Recipe).filter(Recipe.rid.in_(rids)).all()
        results = [r.to_dict() for r in results]
    except Exception as e:
        return {'success':False, 'error':e}, 400

    result = {'recipes':results, 'success':True}
    return result, 200


# input: {"rid":int(rid)}
# if success: return {"success":True}
# if failure: return {"success":False, "error": error msg}
@app.route('/recipe', methods=['DELETE'])
def delete_recipe():
    data = request.json

    required_fields = ['rid']
    for field in required_fields:
        if field not in data:
            abort(400, f"{field} not found in the form")

    rid = data['rid']

    try:
        if db.session.query(Recipe).filter_by(rid=rid).first() is None:
            return {'success':False, 'error':"Rid not existed in Recipe Table"}, 400
        if db.session.query(UserRecipe).filter_by(rid=rid).first() is None:
            return {'success':False, 'error':"Rid not existed in UserRecipe Table"}, 400

        db.session.query(Recipe).filter_by(rid=rid).delete()
        db.session.query(UserRecipe).filter_by(rid=rid).delete()
        db.session.commit()
    except Exception as e:
        return {'success':False, 'error': e}, 400

    return {'success':True}, 200


# keywords separated by `;`
@app.route('/search/<keywords>', methods=['GET'])
def search_recipe_ids_by_keywords(keywords):
    keywords = keywords.split(';')
    rids = []
    for keyword in keywords:
        rids.extend(cosmos_client.get_rids(keyword))

    return {"rids": rids}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
