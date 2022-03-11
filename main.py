from time import sleep
from tkinter import DISABLED
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZHJ0125-bushu-dev'

name = 'ZHJ0125'

class MyForm(FlaskForm):
    username = StringField('小米账号（手机号）', validators=[DataRequired(), Regexp('^1[35789]\d{9}$')], render_kw={'type':'number', 'class':"input", 'placeholder':"a"})
    password = StringField('密码', validators=[DataRequired()], render_kw={'type':'password', 'class':"input", 'placeholder':"a"})
    steps = StringField('步数（建议2000~40000）', validators=[DataRequired()], render_kw={'type':'number', 'class':"input", 'placeholder':"a"})
    submit = SubmitField('提交', render_kw={'type':"submit", 'class':"submitBtn"})

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # 数据格式正确，获取表单数据
            print("username = " + form.username.data)
            print("password = " + form.password.data)
            print("steps = " + form.steps.data)
            if(int(form.steps.data) <= 0 or int(form.steps.data) > 40000):
                flash('步数超出范围，请重新输入步数', 'error')
                return render_template('index.html', form=form)
            flash('正在请求刷新步数，请稍等...')
            form.submit.render_kw = {'type':"submit", 'class':"submitBtn_disable", 'disabled': 'disabled'}  # 禁用submit
            
            sleep(5)  # 此处用来留作API请求
            
            form.submit.render_kw = {'type':"submit", 'class':"submitBtn"}  # 启用submit
        else:
            flash('输入的数据格式有误，请重新输入账号和密码', 'error')  # 显示错误提示
            return render_template('index.html', form=form)
    # 默认GET请求，返回主页面
    return render_template('index.html', form=form)

@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html', user=name), 404  # 返回模板和状态码