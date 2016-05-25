#!/usr/bin/env python3

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Boolean, Column, Enum, \
                       Integer, ForeignKey, String, \
                       Table, Text, DateTime
from sqlalchemy.orm import relationship
from flask.ext.login import UserMixin
from app.database import Base, db_session

tag_association_table = Table("project_tag", Base.metadata,
    Column("project_id", Integer, ForeignKey("project.id")),
    Column("tag_name", String(16), ForeignKey("tag.name"))
)

class User(Base, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    timezone = Column(Integer, nullable=False)
    authenticated = Column(Boolean, nullable=False, default=False)
    projects = relationship("ProjectMember", back_populates="member")
    entries = relationship("TimeEntry")

    def __init__(self, first_name=None, last_name=None, email=None, \
                 password=None, timezone=0, authenticated=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.timezone = timezone
        self.authenticated = authenticated

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get(id):
        return User.query.get(int(id))

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email;

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_user(email):
        user = db_session.query(User) \
                         .select_from(User) \
                         .filter(User.email == email) \
                         .first()

        return user

    def __repr__(self):
        return "<User %r>" % (self.email)

class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String(40))
    members = relationship("ProjectMember", back_populates="project")
    tasks = relationship("Task")
    tags = relationship("Tag", \
                        secondary=tag_association_table, \
                        back_populates="projects")

    def __init__(self, name=None, description="", tags=[], image=None):
        self.name = name
        self.description = description
        self.image = image

        for n in tags:
            tag = Tag(name=n, project_id=self.id)
            self.tags.append(tag)

    def get(id):
        Project.query.get(int(id))

    def __repr__(self):
        return "<Project %r>" % (self.id)

class ProjectMember(Base):
    __tablename__ = "project_member"
    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Enum("owner", "admin", "member", "invited", name="member_role"), nullable=False)

    project = relationship("Project", back_populates="members")
    member = relationship("User", back_populates="projects")

class Tag(Base):
    __tablename__ = "tag"
    name = Column(String(16), primary_key=True)
    projects = relationship("Project", \
                            secondary=tag_association_table, \
                            back_populates="tags")

    def __init__(self, name=None, project_id=None):
        self.name = name
        self.project_id = project_id

    def __repr__(self):
        return "<Tag %r>" % (self.name)

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    description = Column(String(128))
    status = Column(Enum("active", "completed", name="task_status"), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"))
    entries = relationship("TimeEntry")

    def __init__(self, description=description, status="active", project_id=None):
        self.description = description
        self.status = status
        self.project_id = project_id

    def __repr__(self):
        return "<Task %r>" % (self.id)

class TimeEntry(Base):
    __tablename__ = "time_entry"
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("user.id"))
    task_id = Column(Integer, ForeignKey("task.id"))

    def __init__(self, start_time=None, end_time=None):
        self.start_time = start_time
        self.end_time = end_time

    @hybrid_property
    def delta_time(self):
        if end_time is not None:
            return end_time - start_time
        else:
            return 0

    def __repr__(self):
        return "<Time Entry %r>" % (self.id)

class Invitation(Base):
    __tablename__ = "invitation"
    id = Column(Integer, primary_key=True)
    inviter_id = Column(Integer, ForeignKey("user.id"))
    invitee_id = Column(Integer, ForeignKey("user.id"))
    project_id = Column(Integer, ForeignKey("project.id"))

    def __init__(self, inviter_id=None, invitee_id=None, project_id=None):
        self.inviter_id = inviter_id
        self.invitee_id = invitee_id
        self.project_id = project_id

    def __repr__(self):
        return "<Invitation %r>" % (self.id)
