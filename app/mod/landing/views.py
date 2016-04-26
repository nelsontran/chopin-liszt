#!/usr/bin/env python3

from flask import Blueprint, render_template
from flask.ext.login import login_required

landing = Blueprint("landing", __name__, template_folder="../../templates/landing")

@landing.route("/")
def index():
    return render_template("landing.html")
