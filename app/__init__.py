#!/usr/bin/env python3

from flask import Flask, render_template
from flask.ext.login import LoginManager
from app.database import db_session
from app.mod.auth.views import auth
from app.mod.core.views import core
from app.mod.auth.models import User
from app.mod.landing.views import landing

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(core)
app.register_blueprint(landing)

login_manager = LoginManager()
login_manager.init_app(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
