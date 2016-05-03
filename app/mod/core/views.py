#!/usr/bin/env python3

from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.mod.core.models import Project, ProjectPermission
from app.mod.auth.views import User
from app.database import db_session

core = Blueprint("core", __name__, template_folder="../../templates/core")

@core.route("/projects", methods=["GET"])
@login_required
def projects():
    admin_data = Project.get_projects(current_user, "admin")
    user_data = Project.get_projects(current_user, "user")

    return render_template("projects.html", admin_data=admin_data, user_data=user_data)

@core.route("/projects/<int:project_id>", methods=["GET", "POST"])
@login_required
def tasks(project_id):
    return render_template("tasks.html")

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

@core.route("/projects/<int:project_id>/create")
@login_required
def create_task(project_id):
    return render_template("create_task.html")

@core.route("/remove_project")
def remove_project():
    
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
