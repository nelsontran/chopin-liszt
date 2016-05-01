#!/usr/bin/env python3

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.mod.auth.models import User
from app.database import Base

class Project(Base):
    __tablename__ = "project"
    project_id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    status = Column(Enum("active", "archived", name='project_status'))

class ProjectPermission(Base):
    __tablename__ = "project_permission"
    project_id = Column (Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    group = Column (Enum("admin", "member"), nullable=False)

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
    project_id = Column(Integer, ForeignKey("project.project_id"), unique=True, nullable=False)
    status = Column (Enum("Open","Closed", name='tasks_status'))
    description = Column(String(150), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    tags = relationship("Tag", backref="task")

class Tag(Base):
    __tablename__ = "tag"
    tag_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.task_id"), unique=True, nullable=False)
    task_name = Column(String(32))
