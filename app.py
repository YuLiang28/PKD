from flask import Flask, request, redirect, url_for, render_template,flash,session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os
from db import *
from models import User,Student
from views import *
from forms import *
import json

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
        "fields":query_Students_Fields(),
        "students":query_Students()
    }
    return render_template('index.html',data=data)




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
            
            login_user(user,remember=remember)
            return redirect(url_for('index'))


    # GET 请求
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '登出成功！'


@app.route('/students/list', methods=['get'])
@login_required
def get_students_list():
    return json.dumps(query_StudentsList())

@app.route('/student/add', methods=['POST'])
@login_required
def student_add():
    if request is None:
        return json.dumps({"status":400,"msg":"添加失败，请重新填写。"})
    id = request.form.get('id',type=int)
    name = request.form.get('name',type=str)
    age = request.form.get('age',type=int,default=None)
    funds = request.form.get('funds',type=float,default=None)
    addr = request.form.get('addr',type=int,default=None)
    honor = request.form.get('honor',type=str,default=None)
    if name == '':
        return json.dumps({"status":400,"msg":"添加失败，请输入姓名。"})
    add_Student(Student(id=id, name=name, age=age,funds= funds,addr=addr,honor=honor))
    return json.dumps({"status":200,"msg":f"添加用户 {name} 成功。"})

@app.route('/student/del', methods=['POST'])
@login_required
def student_del():
    if request is None:
        return json.dumps({"status":400,"msg":"删除失败，请刷新重试。"})
    id = request.form.get('id',type=int)
    if id == None:
        return json.dumps({"status":400,"msg":"删除失败，请刷新重试。"})
    del_StudentById(id)
    return json.dumps({"status":200,"msg":f"删除 ID 为 {id} 的用户成功。"})

@app.route('/student/edit', methods=['POST'])
@login_required
def student_edit():
    if request is None:
        return json.dumps({"status":400,"msg":"修改失败，请刷新重试。"})
    
    id = request.form.get('id',type=int)
    name = request.form.get('name',type=str)
    age = request.form.get('age',type=int,default=None)
    funds = request.form.get('funds',type=float,default=None)
    addr = request.form.get('addr',type=int,default=None)
    honor = request.form.get('honor',type=str,default=None)
    if id == None:
        return json.dumps({"status":400,"msg":"修改失败，请刷新重试。"})
    edit_Student(Student(id=id, name=name, age=age,funds= funds,addr=addr,honor=honor))
    return json.dumps({"status":200,"msg":f"修改 ID 为 {id} 的用户成功。"})

# @app.teardown_request
# def shutdown_session(exception=None):
#     db.remove()

#防止被引用后执行，只有在当前模块中才可以使用
if __name__=='__main__':
    app.debug=True
    app.run()