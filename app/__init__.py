#!/usr/bin/env python3

from flask import Flask, render_template
from flask.ext.login import LoginManager
from app.database import db_session
from app.models import User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
