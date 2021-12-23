from models import *

# 增加用户
def add_Student(student):
    db.session.add(student)
    db.session.commit()

# 删

# 改

# 获取用户
def query_User(username):
    return User.query.filter_by(username=username).first()

# 用户id获取用户名
def query_UserById(user_id):
    return User.query.filter_by(id=user_id).first()

# 获取 Student 字段
def get_Students_Fields():
    return Student.query.statement.columns.keys()


# 获取全部用户
def get_Students():
    return Student.query.all()





