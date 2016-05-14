#!/usr/bin/env python3

from flask import Flask, render_template
from app.database import db_session

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
