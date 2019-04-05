# -*- encoding: utf-8 -*-

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from constants.definitions import DATE_FORMAT

from db.db_config import DB_config

engine = create_engine('db_engine://{user}:{passwd}@{host}:{port}/{db_name}'.format(
        user=DB_config['user'],
        passwd=DB_config['password'],
        host=DB_config['host'],
        port=DB_config['port'],
        db_name=DB_config['db_name'],
    ))

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Action(Base):
    __tablename__ = 'action'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return '[{name} : {description}]'.format(
            name=self.name,
            description=self.description,
        )

    def __repr__(self):
        return '{{[{classname} - {id}] {name}, {description}}}'.format(
            classname=self.__class__.__name__,
            id=self.id,
            name=self.name,
            description=self.description,
        )


class Appointment(Base):
    '''
    Only can be one appointment for a date and time, but because
    exists a soft delete, that will be checked by app
    '''
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    time = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False)
    is_deleted = Column(Boolean)

    def __init__(self, date, time, email, is_deleted=False):
        self.date = date
        self.time = time
        self.email = email
        self.is_deleted = is_deleted

    def __str__(self):
        return '[{is_deleted} [{id}] {date} - {time}:00 : {email}]'.format(
            is_deleted='[DELETED] ' if self.is_deleted else '',
            id=self.id,
            date=self.date.strftime(DATE_FORMAT),
            time=self.time,
            email=self.email,
        )

    def __repr__(self):
        return '{{[{classname} - {id}] {date}, {time}, {email}, {is_deleted}}}'.format(
            classname=self.__class__.__name__,
            id=self.id,
            date=self.date,
            time=self.time,
            email=self.email,
            is_deleted=self.is_deleted,
        )

    def __eq__(self, other):
        return self.id == other.id


class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True)

    time = Column(DateTime, nullable=False)
    appointment_id = Column(Integer, ForeignKey('appointment.id', ondelete="CASCADE", onupdate="CASCADE"))
    action_id = Column(Integer, ForeignKey('action.id',ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    appointment = relationship(Appointment, backref=backref('log', cascade="all, delete"))
    action = relationship(Action, backref=backref('log', cascade="all, delete"))

    old_date = Column(Date)
    old_time = Column(Integer)
    old_email = Column(String(255))

    new_date = Column(Date)
    new_time = Column(Integer)
    new_email = Column(String(255))

    def __init__(
                    self,
                    time,
                    appointment,
                    action,
                    old_date=None,
                    old_time=None,
                    old_email=None,
                    new_date=None,
                    new_time=None,
                    new_email=None,
                ):
        self.time = time
        self.appointment = appointment
        self.action = action
        self.old_date = old_date
        self.old_time = old_time
        self.old_email = old_email
        self.new_date = new_date
        self.new_time = new_time
        self.new_email = new_email

    def __str__(self):
        return '[{time} : {action} {appointment}]'.format(
            time=self.time,
            action=self.action.name,
            appointment=str(self.appointment),
        )

    def __repr__(self):
        return '{{[{classname} - {id}] {time} {appointment} {action} {old_date} {old_time} {old_email} {new_date} {new_time} {new_email}}}'.format(
            classname=self.__class__.__name__,
            id=self.id,
            time = self.time,
            appointment = repr(self.appointment),
            action = repr(self.action),
            old_date = self.old_date,
            old_time = self.old_time,
            old_email = self.old_email,
            new_date = self.new_date,
            new_time = self.new_time,
            new_email = self.new_email,
        )
