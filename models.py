from db import db
from flask_login import UserMixin
from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password_hash(password)
    
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
