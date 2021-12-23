from flask import Flask, request, redirect, url_for, render_template,flash,session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os
from db import *
from models import User,Student
from views import *
from forms import *

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
        "title":"管理页面",
        "username":query_UserById(current_user.get_id()).username,
        "fields":get_Students_Fields(),
        "students":get_Students()
    }
    return render_template('index.html',data=data)




@app.route('/login', methods=['GET', 'POST'])
def login():
    # 处理一个非预期的情况：假设用户已经登录，却导航到应用的*/login* URL。需要导航到/index URL
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
            
            login_user(user,remember=remember)
            return redirect(url_for('index'))


    # GET 请求
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '登出成功！'

@app.route('/add/student', methods=['POST'])
@login_required
def student_add():
    if request is None:
        flash("添加失败，请重新填写。")
    id = int(request.form.get('id'))
    name = request.form.get('name')
    age = int(request.form.get('age'))
    funds = float(request.form.get('funds'))
    addr = request.form.get('addr')
    if name == '':
        flash("添加失败，请输入姓名。")
        return redirect(url_for('index'))
    add_Student(Student(id=id, name=name, age=age,funds= funds,addr=addr))
    flash("添加成功。")
    return redirect(url_for('index'))


# @app.teardown_request
# def shutdown_session(exception=None):
#     db.remove()

#防止被引用后执行，只有在当前模块中才可以使用
if __name__=='__main__':
    app.debug=True
    app.run()