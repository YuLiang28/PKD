from db import db
from flask_login import UserMixin
from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from datetime import datetime

import enum
class UserTypeEnum(enum.Enum):
    Admin = 1
    Student = 2

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    type = db.Column(db.Enum(UserTypeEnum), nullable=False)

    def __init__(self, username, password,type):
        self.username = username
        self.set_password_hash(password)
        self.type = type

    def __repr__(self):
        return '<User %r>' % (self.username)

    def set_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    age =db.Column(db.Integer)
    funds = db.Column(db.Float)
    addr = db.Column(db.String(32))
    honor = db.Column(db.String(32))

    def __repr__(self):
        return '<Student %r>' % (self.name)

class Key(db.Model):
    __tablename__ = 'keys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Boolean,default=False) # 激活码是否被使用
    createDt = db.Column(db.DateTime,default=datetime.now())
    activeDt = db.Column(db.DateTime)

    def __init__(self,code):
        self.code = code

    def __repr__(self):
        return '<Keys %r>' % (self.name)

