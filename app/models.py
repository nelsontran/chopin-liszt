#!/usr/bin/env python3

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from flask.ext.login import UserMixin
from app.database import Base, db_session

class User(Base, UserMixin):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    def __init__(self, first_name=None, last_name=None, email=None, password=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get(id):
        return User.query.get(int(id))

    def get_id(self):
        return self.user_id

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
        return "<User %r>" % (self.username)
