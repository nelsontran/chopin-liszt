#!/usr/bin/env python3

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        _username = request.form["username"]
        _password = request.form["password"]
        _email = request.form["email"]

        print("user: " + _username)
        print("pass: " + _password)
        print("email: " + _email)

    return render_template("index.html", display_register_form=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        _username = request.form["username"];
        _password = request.form["password"];

        print("user: " + _username)
        print("pass: " + _password)

    return render_template("index.html", display_register_form=False)

if __name__ == "__main__":
    app.run(debug=True)
