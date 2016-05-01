#!/usr/bin/env python3

from flask import Blueprint, redirect, render_template, request, url_for
from flask.ext.login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from app.database import db_session
from app.mod.auth.models import User
from app.mod.landing.views import landing

auth = Blueprint("auth", __name__, template_folder="../../templates/auth")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            _username = request.form["username"]
            _password = request.form["password"]
            _email = request.form["email"]

            user = User(_username, _password, _email)
            db_session.add(user)
            db_session.commit()

            print("Register successful!")

        except IntegrityError as e:
            print("Username or email already in use.")

    return render_template("login.html", display_register_form=True)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        _username = request.form["username"];
        _password = request.form["password"];

        user = db_session.query(User) \
                         .filter(User.username.like(_username)) \
                         .first()

        if user is not None and user.check_password(_password) is True:
            login_user(user)
            return redirect(url_for("landing.index"))

    return render_template("login.html", display_register_form=False)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("landing.index"))
