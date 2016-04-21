#!/usr/bin/env python3

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(16), unique=True)
    password = Column(String(128))
    email = Column(String(256), unique=True)

    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User %r>" % (self.name)
