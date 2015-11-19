# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, ValidationError, TextAreaField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from ..models import User

class LoginForm(Form):
    email = StringField(u'E-mail', validators=[Required(), Length(1,64), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'登录')

class RegisterForm(Form):
    username = StringField(u'用户名', validators=[
        Required(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, '
                                         'numbers, dots or underscores')])
    email = StringField(u'E-mail', validators=[Required(), Length(1,64), Email()])
    password = PasswordField(u'密码', validators=[Required(), Length(4,64), EqualTo('password_confirm', message=u'两次密码不匹配')])
    password_confirm = PasswordField(u'密码(确认)')
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已被注册')

class CreateForm(Form):
    title = StringField(u'主题', validators=[Required()])
    content = TextAreaField(u'正文', validators=[Required()])
    submit = SubmitField(u'立即创建')

class ReplyForm(Form):
    content = TextAreaField(u'回复内容', validators=[Required()])
    submit = SubmitField(u'立即回复')


# class EditTopicForm(Form):
