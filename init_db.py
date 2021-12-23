from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/pkd.sqlite3'
db = SQLAlchemy(app)



db.create_all()
db.session.add(User("admin","admin"))
db.session.add(Student(id=1,name="张三",age=18,funds=5000,addr="美国洛圣都花园银行塔25楼1号"))
db.session.commit()