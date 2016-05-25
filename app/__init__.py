#!/usr/bin/env python3

from flask import Flask, jsonify, render_template, \
                  redirect, request, url_for
from flask.ext.login import current_user, LoginManager, \
                            login_required, login_user, logout_user
from app.database import db_session
from app.models import User, Project

import os
import uuid

app = Flask(__name__)

# store uploaded project images in static/img/uploads
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/img/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    try:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        email = request.json["email"]
        password = request.json["password"]
    except KeyError:
        return jsonify(success=False)

    # check if email exists in the database
    if User.get_user(email) is not None:
        return jsonify(success=False, email_taken=True)

    try:
        user = User(first_name=first_name, last_name=last_name, \
                    email=email, password=password)
        db_session.add(user)
        db_session.commit()
    except Exception:
        return jsonify(success=False)

    return jsonify(success=True)

@app.route("/login", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        password = request.json["password"]
    except KeyError:
        return jsonify(success=False)

    user = db_session.query(User) \
                     .filter(User.email.like(email)) \
                     .first()

    if user is not None and user.check_password(password):
        user.authenticated = True
        db_session.add(user)
        db_session.commit()
        login_user(user)
        return jsonify(success=True)

    return jsonify(success=False)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db_session.add(user)
    db_session.commit()
    logout_user()

    if request.method == "GET":
        return redirect(url_for("index"))

@app.route("/logged_in", methods=["POST"])
def logged_in():
    return jsonify(authenticated=bool(current_user.is_authenticated))

@app.route("/create_project", methods=["POST"])
def create_project():
    name = request.form["project-name"]
    tags = request.form["project-tags"]
    image = request.files["project-image"]

    # save image to disk
    filename = str(uuid.uuid4()) + ".svg"
    image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    # parse comma separated tag list
    tags = [tag.strip() for tag in tags.split(",")]

    try:
        project = Project(name=name, tags=tags, image=filename)
        db_session.add(project)
        db_session.commit()
    except Exception:
        return jsonify(success=False)

    return jsonify(success=True)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
