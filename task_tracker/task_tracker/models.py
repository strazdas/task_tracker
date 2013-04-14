from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    stories = relationship("Story", backref="created_by")
    tasks = relationship("Task", backref="assigned")

    def __repr__(self):
        return self.username


class Story(Base):
    __tablename__ = 'story'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text, nullable=True)
    estimated = Column(Text, nullable=True)
    created = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    tasks = relationship('Task', backref="story")


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text, nullable=True)
    estimated = Column(Text, nullable=True)
    created = Column(DateTime)
    assigned_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    story_id = Column(Integer, ForeignKey('story.id'))
    times_spent = relationship("TimeSpent", backref="task")


class TimeSpent(Base):
    __tablename__ = 'time_spent'
    id = Column(Integer, primary_key=True)
    duration = Column(Text)
    task_id = Column(Integer, ForeignKey('task.id'))

    def __repr__(self):
        return self.duration
