#!/usr/bin/env python3

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from flask.ext.login import UserMixin
from app.database import Base, db_session

class User(Base, UserMixin):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(32))
    last_name = Column(String(32))
    username = Column(String(32), unique=True)
    password = Column(String(128))
    email = Column(String(256), unique=True)

    def __init__(self, first_name=None, last_name=None, username=None, password=None, email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get(id):
        return User.query.get(int(id))

    def get_id(self):
        return self.user_id

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_user(email):
        user = db_session.query(User) \
                         .select_from(User) \
                         .filter(User.email == email) \
                         .first()

        return user

    def __repr__(self):
        return "<User %r>" % (self.username)
