#!/usr/bin/env python3

from flask import Flask, jsonify, render_template, request
from flask.ext.login import LoginManager
from app.database import db_session
from app.models import User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    try:
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        password = request.json['password']
    except KeyError:
        return jsonify(success=False)

    # check if email exists in the database
    if User.get_user(email) is not None:
        return jsonify(success=False, email_taken=True)

    try:
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db_session.add(user)
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
