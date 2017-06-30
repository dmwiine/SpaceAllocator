from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class FellowModel(Base):
    """"""
    __tablename__ = "fellow"

    fellow_id = Column(Integer, primary_key=True)
    living_space_id = Column('living_space_id', Integer,
                             ForeignKey("living_space.living_space_id"), nullable=True)
    office_id = Column('office_id', Integer, ForeignKey("office.office_id"), nullable=True)
    name = Column(String)

    def __init__(self, living_space_id, office_id, name):
        """"""
        self.living_space_id = living_space_id
        self.office_id = office_id
        self.name = name

class LivingSpaceModel(Base):
    """"""
    __tablename__ = "living_space"
    living_space_id = Column(Integer, primary_key=True)
    name = Column(String)
    spaces_available = Column(Integer)

    fellows = relationship("FellowModel", backref="living_space")

    def __init__(self, name, spaces_available):
        """"""
        self.name = name
        self.spaces_available = spaces_available

class OfficeModel(Base):
    """"""
    __tablename__ = "office"

    office_id = Column(Integer, primary_key=True)
    name = Column(String)
    spaces_available = Column(Integer)
    fellows = relationship("FellowModel", backref="office")
    staff = relationship("StaffModel", backref="office")

    def __init__(self, name, spaces_available):
        """"""
        self.name = name
        self.spaces_available = spaces_available

class StaffModel(Base):
    """"""
    __tablename__ = "staff"

    staff_id = Column(Integer, primary_key=True)
    office_id = Column('office_id', Integer, ForeignKey("office.office_id"), nullable=True)
    name = Column(String)

    def __init__(self, office_id, name):
        """"""
        self.office_id = office_id
        self.name = name

