#!/usr/bin/env python3

from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.mod.core.models import Project, ProjectPermission
from app.mod.auth.views import User
from app.database import db_session

core = Blueprint("core", __name__, template_folder="../../templates/core")

@core.errorhandler(401)
def page_not_found(e):
    return redirect(url_for('auth.login'), 401)

@core.route("/projects", methods=["GET"])
@login_required
def projects():
    admin_data = Project.get_projects(current_user, "admin")
    user_data = Project.get_projects(current_user, "user")

    return render_template("projects.html", admin_data=admin_data, user_data=user_data)

@core.route("/projects/<int:project_id>", methods=["GET", "POST"])
@login_required
def tasks(project_id):
    active_tasks = {}
    completed_tasks = {}

    dummy_data = {
        "id": [1, 2, 3, 4, 5],
        "name": ["Task #1", "Task #2", "Task #3", "Task #4", "Task #5"],
        "description": ["Hello World", "Practice Etudes", "Lorem Ipsum", "Practice Tchaikovsky", "Practice Beethoven"],
        "time_spent": [12, 14, 51, 64, 74]
    }

    dummy_data2 = {
        "id": [1],
        "name": ["Task #0"],
        "description": ["Drink Water"],
        "time_spent": [154]
    }

    return render_template("tasks.html", project_id=project_id, active_tasks=dummy_data, completed_tasks=dummy_data2)

@core.route("/projects/create", methods=["GET", "POST"])
@login_required
def create_project():
    if request.method == "POST":
        try:
            _project_name = request.form["name"]
            _collaborator_emails = request.form.getlist("emails[]")
            _permissions = request.form.getlist("permissions[]")

            project = Project(name=_project_name)
            db_session.add(project)
            db_session.commit()

            # Getting the id for the project after the project has been added to the db
            p_id = project.get_id()
            print ('Project id: ', project.project_id)

            # Adding on the admin user (user who created the project)
            permission = ProjectPermission(user_id=current_user.get_id(), project_id=p_id, group="admin")
            db_session.add(permission)
            db_session.commit()

            # looping through and getting the collaborators to add to permission
            i = 0
            for email in _collaborator_emails:
                c = db_session.query(User) \
                              .filter(User.email.like(email)) \
                              .first()

                if c is not None:
                    permission = ProjectPermission(user_id=c.user_id, project_id=p_id, group=_permissions[i])
                    db_session.add(permission)
                    db_session.commit()
                    print("Permission added for collaborator!", c.get_full_name())
                i += 1

        except IntegrityError as e:
            print("User not found in database.")

        return redirect(url_for("core.projects"))

    return render_template("create_project.html")

@core.route("/projects/<int:project_id>/create", methods=["GET", "POST"])
@login_required
def create_task(project_id):
    if request.method == "POST":
        _name = request.form["name"]
        _description = request.form["description"]
        _start_time = request.form["start_time"]
        _end_time = request.form["end_time"]

        print(_name)
        print(_description)
        print(_start_time)
        print(_end_time)

    return render_template("create_task.html", project_id=project_id)

@core.route("/remove_project")
def remove_project():
    project_id = request.args.get('id', 0, type=int)
    Project.remove_project(project_id)
    return jsonify(result=True)

@core.route("/remove_task")
def remove_task():
    return jsonify(result=True)

@core.route("/complete_task")
def complete_task():
    return jsonify(result=True)

@core.route("/uncomplete_task")
def uncomplete_task():
    return jsonify(result=True)

@core.route("/get_collaborator")
def get_collaborator():
    email = request.args.get('email', 0, type=str)
    user = User.get_user(email)

    if user is not None:
        fullname = user.get_full_name()
        return jsonify(fullname=fullname, email=email, result=True)
    else:
        return jsonify(result=False)

@core.route("/remove_collaborator")
def remove_collaborator():
    email = request.args.get('email', 0, type=str)
    return jsonify(result=True)

@core.route("/record_time_entry")
def record_time_entry():
    project_id = request.args.get('project_id', 0, type=int)
    date = request.args.get('date', 0, type=str)
    start_time = request.args.get('start_time', 0, type=str)
    end_time = request.args.get('end_time', 0, type=str)

    print(project_id)
    print(date)
    print(start_time)
    print(end_time)

    return jsonify(result=True)
