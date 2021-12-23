from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import User


class LoginForm(FlaskForm):
    username=StringField(label=u'用户名:',validators=[DataRequired(u'用户名不能为空'),validators.Length(3,20,u'用户名长度必须3~64位字符')])
    password=PasswordField(label=u'密码:',validators=[DataRequired(),validators.Length(0,24,u'密码必须位0~24字符')])