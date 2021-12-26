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

app = Flask(__name__, static_url_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/pkd.sqlite3'
init_db(app)

# login 密钥
app.config['SECRET_KEY'] = os.urandom(24)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = '请登录。'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_stage_and_region():
    return dict(siteName="PKD")


@app.route('/')
@app.route('/index')
@login_required
def index():
    data = {
        "title": "学生信息管理",
        "username": query_UserById(current_user.get_id()).username,
        "fields": query_Students_Fields(),
        "students": query_Students()
    }
    return render_template('index.html', data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 处理一个非预期的情况：假设用户已经登录，却导航到/login URL。需要导航到/index URL
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    if request.method == 'POST':
        user = query_User(username)
        if user is None or not user.check_password(password):
            flash('账号或用户名错误！')
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        return redirect(url_for('index'))

    # GET 请求
    return render_template('login.html')


@app.route('/charts')
@login_required
def charts():
    return render_template('charts.html')


@app.route('/coupon')
@login_required
def coupon():
    data = {
        "title": "优惠券",
        "username": query_UserById(current_user.get_id()).username
    }
    return render_template('coupon.html', data=data)


@app.route('/ajax/coupon/del', methods=['GET', 'POST'])
@login_required
def coupon_del_ajax():
    jsonData = ""
    if request.method == 'POST':
        coupons = request.form.getlist('couponID')  # 获取优惠券 couponID
        for coupon in coupons:
            del_KeyById(coupon)
        jsonData = json.dumps({
            "status": 200,
            "msg": f"删除全部优惠券成功。",
            "data": coupons
        })

    elif request.method == 'GET':
        del_KeyAll()
        jsonData = json.dumps({
            "status": 200,
            "msg": f"删除全部优惠券成功。"
        })
    return jsonData, 200


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


@app.route('/ajax/coupon/data')
@login_required
def coupon_data_ajax():
    keys = query_Keys()
    fields = query_Keys_Fields()
    keysList = query2List(fields, keys)
    return json.dumps({
        "status": 200,
        "msg": "优惠券获取成功。",
        "data": keysList,
        "fields": fields
    }, indent=4, sort_keys=True, default=str), 200


@app.route('/ajax/login', methods=['GET', 'POST'])
def login_ajax():
    # 处理一个非预期的情况：假设用户已经登录，却导航到/login URL。需要导航到/index URL
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    if request.method == 'POST':
        user = query_User(username)
        if user is None or not user.check_password(password):
            return json.dumps({"status": 400, "msg": "账号或用户名错误！"}), 400

        next = request.form.get('next')

        if not utils.is_safe_url(next, request):
            return abort(400)

        login_user(user, remember=remember)
        # 如果 URL 中带有 next 参数则跳转到 next 页面
        if(next):  # next 不为空
            next = next
        else:  # next 空
            next = url_for('index')
        return json.dumps({"status": 200, "msg": "登录成功", "next": next}), 200
    # GET 请求
    return json.dumps({"status": 400, "msg": "请使用Post请求。"}), 400


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')


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


@app.route('/students/list', methods=['get'])
@login_required
def get_students_list():
    return json.dumps(query_StudentsList())


@app.route('/student/add', methods=['POST'])
@login_required
def student_add():
    if request is None:
        return json.dumps({"status": 400, "msg": "添加失败，请重新填写。"}), 400
    id = request.form.get('id', type=int)
    name = request.form.get('name', type=str)
    age = request.form.get('age', type=int, default=None)
    funds = request.form.get('funds', type=float, default=None)
    addr = request.form.get('addr', type=int, default=None)
    honor = request.form.get('honor', type=str, default=None)
    if name == '':
        return json.dumps({"status": 400, "msg": "添加失败，请输入姓名。"}), 400
    add_Student(Student(id=id, name=name, age=age,
                        funds=funds, addr=addr, honor=honor))
    return json.dumps({"status": 200, "msg": f"添加用户 {name} 成功。"}), 200


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


@app.route('/student/edit', methods=['POST'])
@login_required
def student_edit():
    if request is None:
        return json.dumps({"status": 400, "msg": "修改失败，请刷新重试。"}), 400

    id = request.form.get('id', type=int)
    name = request.form.get('name', type=str)
    age = request.form.get('age', type=int, default=None)
    funds = request.form.get('funds', type=float, default=None)
    addr = request.form.get('addr', type=int, default=None)
    honor = request.form.get('honor', type=str, default=None)
    if id == None:
        return json.dumps({"status": 400, "msg": "修改失败，请刷新重试。"}), 400
    edit_Student(Student(id=id, name=name, age=age,
                         funds=funds, addr=addr, honor=honor))
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
