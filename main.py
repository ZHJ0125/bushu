from flask import Flask, render_template, request, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZHJ0125-bushu-dev'

name = 'ZHJ0125'

class MyForm(FlaskForm):
    mobile = StringField('手机', validators=[DataRequired(), Regexp('^1[35789]\d{9}$', 0, '手机号码不合法')], render_kw={'placeholder': '输入手机号'})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        flash('抱歉兄弟，后端代码还没写呢，敬请期待😂')  # 显示错误提示
        # 获取表单数据
        username = request.form.get('username')  # 传入表单对应输入字段的 name 值
        password = request.form.get('password')
        steps = request.form.get('steps')
        print("[Debug] -> username="+username, "password="+password, "steps="+steps)
        if not username or not password or not steps:
            flash('输入的数据有误')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
    # 默认GET请求，返回主页面
    return render_template('index.html', name=name)

@app.route('/test', methods=['GET', 'POST'])
def test():
    form = MyForm()
    if form.validate_on_submit(): # 此方法会自动验证POST方式以及数据格式是否合法
        print("mobile = " + form.mobile.data)
    else:
        print("手机格式有误")
    return render_template('test.html', form=form)

@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html', user=name), 404  # 返回模板和状态码