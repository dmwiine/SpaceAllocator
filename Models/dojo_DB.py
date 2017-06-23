import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Models.models import *


class DojoDB(object):
    def __init__(self):
        self.db_name = None
        self.engine = None
        self.session = None

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_db(self, db_name):
        self.db_name = db_name
        self.engine = create_engine('sqlite:///' + self.db_name + '.db')
        Base.metadata.create_all(self.engine)
        self.create_session()
        return self

    def read_db(self, db_name):
        self.db_name = db_name
        self.engine = create_engine('sqlite:///' + self.db_name + '.db')
        self.create_session()
        return self
