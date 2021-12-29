from flask import Flask, request, redirect, url_for, render_template, flash, session, request, abort
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os
from db import *
from models import User, Student
from views import *
from forms import *
import json
import utils


# 初始化 Flask App 设置静态路径访问路径为
app = Flask(__name__, static_url_path='')



# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/pkd.sqlite3'
init_db(app) # 初始化数据库

# login 密钥
app.config['SECRET_KEY'] = os.urandom(24)

# 登陆管理器配置
login_manager = LoginManager()
login_manager.login_view = 'login' # 若用户未登录，则自动跳转到指定页面，而不是提示
login_manager.login_message_category = 'info' # 自定义消息分类
login_manager.login_message = '请登录。' # 自定义消息
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    if(isAdmin(session)):
        return User.query.get(int(user_id))
    else:
        return Student.query.get(int(user_id))

# 模板全局变量 设置站点名称为PKD
@app.context_processor
def inject_stage_and_region():
    return dict(siteName="PKD")



# 主页路由
@app.route('/')
@app.route('/index')
@login_required
def index():
    # 判断用户类型
    if(isAdmin(session)):
        username = query_UserById(current_user.get_id()).username
    else:
        return redirect(url_for('coupon'))
    data = {
        "title": "学生信息管理",
        "username": username,
        "fields": query_Students_FieldsNotPwd(),
        "students": query_Students(),
        "user_type": session.get("user_type")
    }
    return render_template('index.html', data=data)



@app.route('/login', methods=['GET'])
def login():
    # 处理一个非预期的情况：假设用户已经登录，却导航到/login URL。需要导航到/index URL
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')
    # username = request.form.get('username')
    # password = request.form.get('password')
    # remember = True if request.form.get('remember') else False
    # if request.method == 'POST':
    #     user = query_User(username)
    #     if user is None or not user.check_password(password):
    #         flash('账号或用户名错误！')
    #         return redirect(url_for('login'))

    #     login_user(user, remember=remember)
    #     return redirect(url_for('index'))

    # # GET 请求
    # return render_template('login.html')

# 弃用
@app.route('/charts')
@login_required
def charts():
    return render_template('charts.html')

# 优惠券路由
@app.route('/coupon')
@login_required
def coupon():
    username = None
    if(isAdmin(session)):
        username = query_UserById(current_user.get_id()).username
    else:
        username = query_StudentById(current_user.get_id()).name
    data = {
        "title": "优惠券",
        "username": username,
        "user_type": session.get('user_type')
    }
    return render_template('coupon.html', data=data)

# 删除/清空优惠券
@app.route('/ajax/coupon/del', methods=['GET', 'POST'])
@login_required
def coupon_del_ajax():
    jsonData = ""
    if request.method == 'POST':
        coupons = request.form.getlist('couponID')  # 获取优惠券 couponID
        for coupon in coupons:
            del_KeyById(coupon) # 删除指定优惠券
        jsonData = json.dumps({
            "status": 200,
            "msg": f"删除全部优惠券成功。",
            "data": coupons
        })

    elif request.method == 'GET':
        del_KeyAll() # 删除全部优惠券
        jsonData = json.dumps({
            "status": 200,
            "msg": f"删除全部优惠券成功。"
        })
    return jsonData, 200


# 添加优惠券
@app.route('/ajax/coupon/add')
@login_required
def coupon_add_ajax():
    args = request.args
    total = args.get("total", type=int, default=10)  # 获取要添加优惠券的总数
    if(total <= 0):
        return json.dumps({
            "status": 400,
            "msg": f"添加失败，提交参数错误。"
        }), 400
    keyset = generate_keys(total)  # 生成 n 张优惠券
    count = keySet2DB(keyset)  # 生成的优惠券加入数据库
    return json.dumps({
        "status": 200,
        "msg": f"添加成功，共添加 {count} 张优惠券。"
    }), 200

# 获取优惠券数据
@app.route('/ajax/coupon/data')
@login_required
def coupon_data_ajax():
    keys = query_Keys()
    fields = query_Keys_Fields() # 获取 Key 全部字段
    keysList = query2List(fields, keys) # 对象转列表
    return json.dumps({
        "status": 200,
        "msg": "优惠券获取成功。",
        "data": keysList,
        "fields": fields
    }, indent=4, sort_keys=True, default=str), 200

# 检查优惠券是否有效
@app.route('/ajax/coupon/check', methods=['POST'])
def coupon_check_ajax():
    code = request.form.get('code', type=str)

    # 如果优惠券存在且有效
    if(keyIsExist(code) and keyIsUseful(code)):
        set_key_status(code, True)  # 设置优惠券已使用
        return json.dumps({
            "status": 200,
            "msg": "优惠券可用。",
            "status": True
        }), 200
    else:
        return json.dumps({
            "status": 200,
            "msg": "优惠券不可用。",
            "status": False
        }), 200

# ajax 登录
@app.route('/ajax/login', methods=['GET', 'POST'])
def login_ajax():

    errorPWD = json.dumps({"status": 400, "msg": "账号或用户名错误！"})

    # 处理一个非预期的情况：假设用户已经登录，却导航到/login URL。需要导航到/index URL
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    userType = request.form.get('userType', default='admin')
    if request.method == 'POST':
        user = None
        if(userType == "admin"):
            user = query_User(username)
        elif(userType == "student"):
            user = query_StudentUser(username)
        else:
            return errorPWD, 400

        if user is None or not user.check_password(password):
            return errorPWD, 400

        next = request.form.get('next')

        if not utils.is_safe_url(next, request):
            return abort(400)

        login_user(user, remember=remember)
        session['user_type'] = userType

        # 如果 URL 中带有 next 参数则跳转到 next 页面
        # URL = 127.0.0.1/login?next=/index
        if(next):  # next 不为空
            next = next
        else:  # next 空
            next = url_for('index')
        return json.dumps({"status": 200, "msg": "登录成功", "next": next}), 200
    # GET 请求
    return json.dumps({"status": 400, "msg": "请使用Post请求。"}), 400

# 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')

# ajax 登出
@app.route('/ajax/logout')
@login_required
def logout_ajax():
    logout_user()
    next = request.args.get('next')
    # 如果 URL 中带有 next 参数则跳转到 next 页面
    if(next):  # next 不为空
        next = next
    else:  # next 空
        next = url_for('index')
    return json.dumps({"status": 200, "msg": "已注销。", "next": next}), 200

# 列出学生信息
@app.route('/students/list', methods=['get'])
@login_required
def get_students_list():
    # 返回不包含密码的其他记录
    return json.dumps(query_StudentsListNotPwd())

# 添加学生信息
@app.route('/student/add', methods=['POST'])
@login_required
def student_add():
    if request is None:
        return json.dumps({"status": 400, "msg": "添加失败，请重新填写。"}), 400
    id = request.form.get('id', type=int)
    name = request.form.get('name', type=str)
    age = request.form.get('age', type=int, default=None)
    funds = request.form.get('funds', type=float, default=None)
    addr = request.form.get('addr', type=str, default=None)
    honor = request.form.get('honor', type=str, default=None)
    password = request.form.get('password', type=str, default=None)

    if name == '':
        return json.dumps({"status": 400, "msg": "添加失败，请输入姓名。"}), 400

    stu = Student(id=id, name=name, age=age,funds=funds, addr=addr, honor=honor)
    stu.set_password_hash(password) # 密码 hash 加密
    add_Student(stu)
    return json.dumps({"status": 200, "msg": f"添加用户 {name} 成功。"}), 200

# 删除学生
@app.route('/student/del', methods=['POST'])
@login_required
def student_del():
    if request is None:
        return json.dumps({"status": 400, "msg": "删除失败，请刷新重试。"}), 400
    id = request.form.get('id', type=int)
    if id == None:
        return json.dumps({"status": 400, "msg": "删除失败，请刷新重试。"}), 400
    del_StudentById(id)
    return json.dumps({"status": 200, "msg": f"删除 ID 为 {id} 的用户成功。"}), 200

# 编辑学生
@app.route('/student/edit', methods=['POST'])
@login_required
def student_edit():
    if request is None:
        return json.dumps({"status": 400, "msg": "修改失败，请刷新重试。"}), 400

    id = request.form.get('id', type=int)
    name = request.form.get('name', type=str)
    age = request.form.get('age', type=int, default=None)
    funds = request.form.get('funds', type=float, default=None)
    addr = request.form.get('addr', type=str, default=None)
    honor = request.form.get('honor', type=str, default=None)
    password = request.form.get('password', type=str, default=None)
    stu = query_StudentById(id)
    if id is None or stu is None:
        return json.dumps({"status": 400, "msg": "修改失败，请刷新重试。"}), 400
    stuEdit = Student(id=id, name=name, age=age,funds=funds, addr=addr, honor=honor)
    if(password!=None and password!=""):
        stuEdit.set_password_hash(password)
    else:
        stuEdit.password=stu.password
    edit_Student(stuEdit)
    return json.dumps({"status": 200, "msg": f"修改 ID 为 {id} 的用户成功。"}), 200


@app.route('/student/columns', methods=['POST'])
@login_required
def student_columns():
    # fields = query_Students_Fields()
    pass

# @app.teardown_request
# def shutdown_session(exception=None):
#     db.remove()


# 防止被引用后执行，只有在当前模块中才可以使用
if __name__ == '__main__':
    app.debug = True
    app.run()
