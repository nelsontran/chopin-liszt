#!/usr/bin/env python3

from sqlalchemy import Column, update, DateTime, Enum, ForeignKey, Integer, String, text, update
from sqlalchemy.orm import relationship
from app.mod.auth.models import User
from app.database import Base, db_session, engine
from datetime import datetime

class Project(Base):
    __tablename__ = "project"
    project_id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    status = Column(Enum("active", "archived"))

    def __init__(self, name=None, status="active"):
        self.name = name
        self.status = status

    def get(id):
        Project.query.get(int(id))

    def get_id(self):
        return self.project_id

    def get_projects(user, group):
        sql = text('select distinct p.name, p.project_id, pp.group ' + \
                   'from project p, user u, project_permission pp ' + \
                   'where p.project_id=pp.project_id and pp.user_id=' + \
                   str(user.get_id()) + ' and pp.group="' + group + '"')

        result = engine.execute(sql)
        print ("result: ", result)
        projects = { "name": [], "id": [] }


        for row in result:
            projects["name"].append(row[0])
            projects["id"].append(row[1])
            print ("Project: ", row[0],'\t',row[1])

        return projects

    def remove_project(id):
        db_session.query(Project).filter(Project.project_id == id)\
                          .delete(synchronize_session='evaluate')
        db_session.commit()

    def __repr__(self):
        return "<Project %r>" % (self.name)

class ProjectPermission(Base):
    __tablename__ = "project_permission"
    project_id = Column (Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    group = Column(Enum("admin", "user"), nullable=False)

    def __init__(self, user_id=None, project_id=None, group=None):
        self.user_id = user_id
        self.project_id = project_id
        self.group = group

    def get(id):
        return ProjectPermission.query.get(int(id))

    def get_pid(self):
        return self.project_id

    def get_uid(self):
        return self.user_id

    def __repr__(self):
        return "<ProjectPermission %r>" % (self.project_id)

class TimeEntry(Base):
    __tablename__ = "time_entry"
    task_entry_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.task_id"), unique=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), unique=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

class Task(Base):
    __tablename__ = "task"
    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.project_id"), nullable=False)
    status = Column (Enum("Open","Closed", name='tasks_status'))
    description = Column(String(150), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    tags = relationship("Tag", backref="task")

    def __init__(self, project_id=None, description=None, status=None, start_time=None, end_time=None):
        self.description = description
        self.project_id = project_id

        if self.status is None:
            self.status = "Open"
        else:
            self.status = status

        if start_time is not None:
            self.start_time = datetime.strptime(start_time[:15], '%Y-%m-%dT%H:%M')

        if end_time is not None:
            self.end_time = datetime.strptime(end_time[:15], '%Y-%m-%dT%H:%M')

        print("Status: " + self.status)

    def get(id):
        return Task.query.get(int(id))

    def get_id(self):
        return self.task_id

    def get_status(self):
        return self.status

    def get_active_tasks(project_id):
        sql = text('select task_id, description from task where task.project_id=' + str(project_id) + ' and task.status="Open"')
        result = engine.execute(sql)
        return result

    def get_completed_tasks(project_id):
        sql = text('select task_id, description from task where task.project_id=' + str(project_id) + ' and task.status="Closed"')
        result = engine.execute(sql)
        return result

    def remove_task(id):
        db_session.query(Task).filter(Task.task_id == id) \
                          .delete(synchronize_session='evaluate')
        db_session.commit()

    def change_status(id):
        sql = text ('select t.status from task t \
                     where t.task_id="' + str(id) + '"')

        result = engine.execute(sql)
        for i in result:
            print(i[0])
            status = i[0]

        if status == "Open":
            sql = text('update task set status="Closed" where task.task_id="' + str(id) + '"')
            result = engine.execute(sql)
        else:
            sql = text('update task set status="Open" where task.task_id="' + str(id) + '"')
            result = engine.execute(sql)

    def __repr__(self):
        return "<Task %r>" % (self.task_id)

class Tag(Base):
    __tablename__ = "tag"
    tag_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.task_id"), nullable=False)
    tag_name = Column(String(32))

    def __init__(self, task_id=None, tag_name=None):
        self.task_id = task_id
        self.tag_name = tag_name

    def get_id(self):
        return self.tag_id

    def __repr__(self):
        return "<Tag %r>" % (self.tag_id)
