#!/usr/bin/env python3

from flask import Flask, render_template, request
from sqlalchemy.exc import IntegrityError
from core.database import db_session
from core.models import User

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
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

    return render_template("index.html", display_register_form=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        _username = request.form["username"];
        _password = request.form["password"];

        user = db_session.query(User) \
                         .filter(User.username.like(_username)) \
                         .first()

        if user.check_password(_password) is True:
            print("Login successful!")
        else:
            print("Login failed...")

    return render_template("index.html", display_register_form=False)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(debug=True)
