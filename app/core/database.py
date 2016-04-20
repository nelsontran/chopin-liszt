#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import json

with open("config.json") as c:
    config = json.load(c)
    engine = create_engine("mysql+pymysql://" + \
                           config["user"] + ":" + \
                           config["password"] + "@" + \
                           config["host"] + ":" + \
                           config["port"] + "/" + \
                           config["database"])

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # Import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise
    # you will have to import them first before calling init_db().
    import core.models
    Base.metadata.create_all(bind=engine)