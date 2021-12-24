from models import *

# 增加用户
def add_Student(stu):
    db.session.add(stu)
    db.session.commit()

# 删
def del_StudentById(student_id):
    db.session.query(Student).filter(Student.id == student_id).delete()
    db.session.commit()

# 改
def edit_Student(stu):
    db.session.query(Student).filter(Student.id == stu.id).update(Student2Dict(stu))
    db.session.commit()

# 获取用户
def query_User(username):
    return User.query.filter_by(username=username).first()

# 用户 id 获取用户名
def query_UserById(user_id):
    return User.query.filter_by(id=user_id).first()

# 获取 Student
def query_StudentById(student_id):
    return Student.query.filter_by(id=student_id).first()

# 获取 Student 字段
def query_Students_Fields():
    return Student.query.statement.columns.keys()

# 获取全部用户
def query_Students():
    return Student.query.all()


def query_StudentsList():
    fields = query_Students_Fields()
    students = query_Students()
    l = []
    for stu in students:
        l1 = []
        for field in fields:
            l1.append(getattr(stu, field))
        l.append(l1)
    return l


def query_StudentDict(stu_id):
    fields = query_Students_Fields()
    student = query_StudentById(stu_id)
    d = {}
    for field in fields:
        d[field] = student.__dict__[field]
    return d


def Student2Dict(student):
    fields = query_Students_Fields()
    d = {}
    for field in fields:

        d[field] = student.__dict__[field]
    return d