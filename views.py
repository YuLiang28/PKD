
from models import *

# 增加学生
def add_Student(stu):
    db.session.add(stu)
    db.session.commit()

# 增加用户
def add_User(user):
    db.session.add(user)
    db.session.commit()

# 增加优惠券
def add_key(k):
    if(db.session.query(Key).filter(Key.code == k.code).first() is None):
        db.session.add(k)
        db.session.commit()
        return True
    else:
        return False

# 删
# 删除学生指定 id
def del_StudentById(student_id):
    db.session.query(Student).filter(Student.id == student_id).delete()
    db.session.commit()

# 删除优惠券指定 id
def del_KeyById(key_id):
    db.session.query(Key).filter(Key.id == key_id).delete()
    db.session.commit()

# 清空 Key 表
def del_KeyAll():
    db.session.query(Key).delete()
    db.session.commit()

# 改
# 修改学生信息
def edit_Student(stu):
    b = Student2Dict(stu,query_Students_Fields())
    db.session.query(Student).filter(
        Student.id == stu.id).update(b)
    db.session.commit()

# 设置优惠券状态
def set_key_status(code,status):
    db.session.query(Key).filter(
        Key.code == code).update({"status":status},synchronize_session=False)
    db.session.commit()

### 查
# 查询全部优惠券
def query_Keys():
    return Key.query.all()
# 查询优惠券是否存在
def keyIsExist(code):
    return Key.query.filter(Key.code == code).first() is not None

# 查询优惠券是否有用
def keyIsUseful(code):
    return Key.query.filter(Key.code == code).first().status == False # 查询返回 False == 没用过的优惠券

# 获取用户
def query_User(username):
    return User.query.filter_by(username=username).first()

# 用户 id 获取用户名
def query_UserById(user_id):
    return User.query.filter_by(id=user_id).first()

# 获取 Student
def query_StudentUser(name):
    return Student.query.filter_by(name=name).first()

# 获取 Student
def query_StudentById(student_id):
    return Student.query.filter_by(id=student_id).first()

# 获取 Student 字段
def query_Students_Fields():
    columns = Student.query.statement.columns.keys()
    return columns

# 获取 Student 字段，除开密码列
def query_Students_FieldsNotPwd():
    columns = Student.query.statement.columns.keys()
    columns.remove("password")
    return columns

# 获取 Key 字段
def query_Keys_Fields():
    return Key.query.statement.columns.keys()

# 获取全部用户
def query_Students():
    return Student.query.all()

# 获取全部用户的指定字段
def query_StudentsSpColumn(fields):
    query = db.session.query()
    for field in fields:
        # add_column 加一列对应的查询字段
        query = query.add_column(getattr(Student, field))
    return query

# 查询学生信息 返回二维表
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

# 查询学生列表，不包括密码列
def query_StudentsListNotPwd():
    fields = query_Students_FieldsNotPwd()
    students = query_Students()
    l = []
    for stu in students:
        l1 = []
        for field in fields:
            l1.append(getattr(stu, field))
        l.append(l1)
    return l

# 查询转列表
# fields : 字段
# dataOBJ : 查询对象
def query2List(fields,dataOBJ):
    l = []
    for data in dataOBJ:
        l1 = []
        for field in fields:
            l1.append(getattr(data, field))
        l.append(l1)
    return l

# 查询学生信息 返回字典
def query_StudentDict(stu_id):
    fields = query_Students_FieldsNotPwd()
    student = query_StudentById(stu_id)
    d = {}
    for field in fields:
        d[field] = student.__dict__[field]
    return d

# 学生对象转字典
def Student2Dict(student,fields):
    d = {}
    for field in fields:
        d[field] = student.__dict__[field]
    return d


# 将生成的激活码添加到数据库中
def keySet2DB(keyset):
    count = 0
    for k in keyset: # 逐个添加
        add_key(Key(k))
        count += 1
    return count

# 生成激活码
def generate_keys(total):
    import string
    import random
    keySet = set()
    while len(keySet) != total:
        keyStr = ''
        for i in range(16):
            point = random.randint(0, 4)
            if point == 0 or point == 1:
                lowKey = str(random.sample(string.ascii_lowercase, 1))
                keyStr = keyStr+lowKey
            elif point == 2 or point == 3:
                upKey = str(random.sample(string.ascii_uppercase, 1))
                keyStr = keyStr + upKey
            elif point == 4:
                dKey = str(random.sample(string.digits, 1))
                keyStr = keyStr + dKey
            keyStr = keyStr.replace('[', '').replace(']', '')
            keyStr = keyStr.replace("'", '')

        keyStr = keyStr[0:4]+'-'+keyStr[5:9]+'-'+keyStr[8:12]+'-'+keyStr[12:]
        keySet.add(keyStr)
    return keySet

# 查询是否为管理员
def isAdmin(session):
    return session.get('user_type') == "admin"
