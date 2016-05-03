#!/usr/bin/env python3

from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.mod.core.models import Project, ProjectPermission, Task, Tag, TimeEntry
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

    active_tasks_results = Task.get_active_tasks(project_id)
    completed_tasks_results = Task.get_completed_tasks(project_id)

    active_tasks = {
        "id": [],
        "description": [],
        "time_spent": []
    }

    completed_tasks = {
        "id": [],
        "description": [],
        "time_spent": []
    }

    for row in active_tasks_results:
        active_tasks["id"].append(row[0])
        active_tasks["description"].append(row[1])

        # get time entries for task and calculate time spent
        results = TimeEntry.get_times(row[0])
        time_spent = None
        for row2 in results:
            delta_time = row2[1] - row2[0]
            if time_spent is None:
                time_spent = delta_time
            else:
                time_spent = time_spent + delta_time

        active_tasks["time_spent"].append(time_spent)

    for row in completed_tasks_results:
        completed_tasks["id"].append(row[0])
        completed_tasks["description"].append(row[1])

        # get time entries for task and calculate time spent
        results = TimeEntry.get_times(row[0])
        time_spent = None
        for row2 in results:
            delta_time = row2[1] - row2[0]
            if time_spent is None:
                time_spent = delta_time
            else:
                time_spent = time_spent + delta_time

        completed_tasks["time_spent"].append(time_spent)

    return render_template("tasks.html", project_id=project_id, active_tasks=active_tasks, completed_tasks=completed_tasks)

@core.route("/projects/create", methods=["GET", "POST"])
@login_required
def create_project():
    if request.method == "POST":
        try:
            _project_name = request.form["name"]
            _collaborator_emails = request.form.getlist("emails[]")

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
                    permission = ProjectPermission(user_id=c.user_id, project_id=p_id, group="user")
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
        _description = request.form["description"]
        _tl = request.form ["tags"]
        _start_time = request.form["start_time"]
        _end_time = request.form["end_time"]

        print(project_id)

        task = Task(project_id=project_id, description=_description, start_time=_start_time, end_time=_end_time)

        db_session.add(task)
        db_session.commit()

        _tags_list = [x.strip() for x in _tl.split(",")]

        for t in _tags_list:
            tag = Tag(task_id=task.task_id, tag_name=t)
            db_session.add(tag)
            db_session.commit()

        return redirect(url_for("core.tasks", project_id=project_id))

    return render_template("create_task.html", project_id=project_id)

@core.route("/projects/<int:project_id>/log/<int:task_id>")
@login_required
def time_entries(project_id, task_id):
    time_entries_results = TimeEntry.get_entries(task_id)

    time_entry_id = []
    name = []
    start_time = []
    end_time = []

    for row in time_entries_results:
        time_entry_id.append(row[0])
        name.append(User.get(row[1]).get_full_name())
        start_time.append(row[2])
        end_time.append(row[3])

    entries = {
        "id": time_entry_id,
        "name": name,
        "start_time": start_time,
        "end_time": end_time
    }

    print(entries)

    return render_template("timeentry.html", project_id=project_id, task_id=task_id, entries=entries)

@core.route("/remove_project")
def remove_project():
    _project_id = request.args.get('id', 0, type=int)
    _user_id = current_user.get_id()

    group = ProjectPermission.get_permission(_user_id, _project_id)

    if group == 'admin':
        Project.remove_project(_project_id)
    else:
        ProjectPermission.del_user(_user_id, _project_id)

    return jsonify(result=True)

@core.route("/remove_task")
def remove_task():
    task_id = request.args.get('id', 0, type=int)
    Task.remove_task(task_id)
    return jsonify(result=True)

@core.route("/remove_entry")
def remove_entry():
    entry_id = request.args.get('id', 0, type=int)
    TimeEntry.remove_entry(entry_id)
    return jsonify(result=True)

@core.route("/complete_task")
def complete_task():
    task_id = request.args.get('id', 0, type=int)
    Task.change_status(task_id)
    return jsonify(result=True)

@core.route("/uncomplete_task")
def uncomplete_task():
    task_id = request.args.get('id', 0, type=int)
    Task.change_status(task_id)
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
    _task_id = request.args.get('task_id', 0, type=int)
    _date = request.args.get('date', 0, type=str)
    _start_time = request.args.get('start_time', 0, type=str)
    _end_time = request.args.get('end_time', 0, type=str)

    _user_id = current_user.get_id()
    time_entry = TimeEntry(task_id=_task_id, user_id=_user_id, date=_date, start_time=_start_time, end_time=_end_time)
    db_session.add(time_entry)
    db_session.commit()

    return jsonify(result=True)
