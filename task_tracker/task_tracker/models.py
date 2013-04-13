from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    stories = relationship("Story", backref="created_by")


class Story(Base):
    __tablename__ = 'story'
    id = Column(Integer, primary_key=True)
    title = Column(Text)  # TODO: use unique=True and create form validator
    estimated = Column(Text, nullable=True)
    created = Column(DateTime, nullable=True)
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=True)
