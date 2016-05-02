#!/usr/bin/env python3

from flask import Blueprint, render_template
from flask.ext.login import login_required

core = Blueprint("core", __name__, template_folder="../../templates/core")

@core.route("/projects", methods=["GET", "POST"])
@login_required
def projects():
    return render_template("projects.html")

@core.route("/projects/<int:project_id>", methods=["GET", "POST"])
@login_required
def tasks(project_id):
    return render_template("tasks.html")

@core.route("/projects/create", methods=["GET", "POST"])
@login_required
def create_project():
    return render_template("create_project.html")

@core.route("/projects/<int:project_id>/create")
@login_required
def create_task(project_id):
    return render_template("create_task.html")
