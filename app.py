from flask import Flask, render_template, request, session, redirect, url_for, abort, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

import os

from config import Config

config = Config()
app = Flask(__name__)
app.secret_key = "recipe secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = config.mysql_uri
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = config.mysql_connect_args
db = SQLAlchemy(app)

from models import *
from utils import *


@app.route("/hello")
def hello():
    version = db.engine.execute("select VERSION()").all()[0][0]
    return "Hello RecipePad in Cloud with MySQL " + str(version)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        account = UserAccount.query.filter_by(username=username).first()
        if account is None:
            msg = "Username not exists"
        elif password != account.password:
            msg = "Incorrect password"
        else:
            session['loggedin'] = True
            session['username'] = username
            session['uid'] = account.uid
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('uid', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        try:
            account = UserAccount(username=username, password=password)
            db.session.add(account)
            db.session.commit()
            session['loggedin'] = True
            session['username'] = username
            session['uid'] = account.uid
            msg = 'You have successfully registered !'
            return render_template('index.html', msg=msg)
        except IntegrityError:
            msg = 'Error: user name has been registered'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/recipe', methods=['POST'])
def create_recipe():
    print("---------")
    print(request.json)
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

    tags = get_tags_from_description_and_title(description, title)  # JSON
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





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
