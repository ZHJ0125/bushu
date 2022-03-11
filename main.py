# -*- coding: utf8 -*-
from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp
import time, json, random, re, requests
from urllib.parse import quote

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
            
            #################################
            
            session['_flashes'].clear()  # 清除所有闪现内容
            result = SendMiRequest(form.username.data, form.password.data, form.steps.data)
            if result[:7] == "[Error]":
                type_of_message = "error"
            else:
                type_of_message = "message"
                flash("🚩刷新步数成功！稍后可查看您的支付宝或微信步数", type_of_message)
            # print(result)
            flash(result, type_of_message)
            
            #################################

            form.submit.render_kw = {'type':"submit", 'class':"submitBtn"}  # 启用submit
        else:
            flash('输入的数据格式有误，请重新输入账号和密码', 'error')  # 显示错误提示
            return render_template('index.html', form=form)
    # 默认GET请求，返回主页面
    return render_template('index.html', form=form)

@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html', user=name), 404  # 返回模板和状态码

now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 当前时间
headers = {  # API请求头
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; MI 6 MIUI/20.6.18)'
}

def get_code(location):
    """
    获取登录code
    """
    code_pattern = re.compile("(?<=access=).*?(?=&)")
    code = code_pattern.findall(location)[0]
    return code


def login(_user, password):
    """
    登录
    """
    url1 = "https://api-user.huami.com/registrations/+86" + _user + "/tokens"
    _headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "MiFit/4.6.0 (iPhone; iOS 14.0.1; Scale/2.00)"
    }
    data1 = {
        "client_id": "HuaMi",
        "password": f"{password}",
        "redirect_uri": "https://s3-us-west-2.amazonaws.com/hm-registration/successsignin.html",
        "token": "access"
    }
    r1 = requests.post(url1, data=data1, headers=_headers, allow_redirects=False)
    try:
        location = r1.headers["Location"]
        code = get_code(location)
    except:
        return 0, 0
    # print("access_code获取成功！")
    # print(code)

    url2 = "https://account.huami.com/v2/client/login"
    data2 = {
        "app_name": "com.xiaomi.hm.health",
        "app_version": "4.6.0",
        "code": f"{code}",
        "country_code": "CN",
        "device_id": "2C8B4939-0CCD-4E94-8CBA-CB8EA6E613A1",
        "device_model": "phone",
        "grant_type": "access_token",
        "third_name": "huami_phone",
    }
    r2 = requests.post(url2, data=data2, headers=_headers).json()
    login_token = r2["token_info"]["login_token"]
    # print("login_token获取成功！")
    # print(login_token)
    userid = r2["token_info"]["user_id"]
    # print("userid获取成功！")
    # print(userid)

    return login_token, userid


def SendMiRequest(_user, _passwd, _step):
    """
    主函数
    """
    _user = str(_user)
    password = str(_passwd)
    _step = str(_step)
    if _user == '' or password == '':
        print("用户名或密码不能为空！")
        return "[Error]:用户名或密码不能为空！"

    if _step == '':
        print("已设置为随机步数（10000-19999）")
        _step = str(random.randint(10000, 19999))
    login_token, userid = login(_user, password)
    if login_token == 0:
        print("登陆失败！")
        return "[Error]:登陆失败，请检查用户名和密码"

    t = get_time()

    app_token = get_app_token(login_token)

    today = time.strftime("%F")

    summary = {
        "v": 6,
        "slp": {
            "st": int(time.time()),
            "ed": int(time.time()),
            "dp": 0,
            "lt": 0,
            "wk": 0,
            "usrSt": -1440,
            "usrEd": -1440,
            "wc": 0,
            "is": 0,
            "lb": 0,
            "to": 0,
            "dt": 0,
            "rhr": 0,
            "ss": 0
        },
        "stp": {
            "ttl": _step,
            "dis": 10627,
            "cal": 510,
            "wk": 41,
            "rn": 50,
            "runDist": 7654,
            "runCal": 397,
            "stage": [
                {
                    "start": 327,
                    "stop": 341,
                    "mode": 1,
                    "dis": 481,
                    "cal": 13,
                    "step": 680
                },
                {
                    "start": 342,
                    "stop": 367,
                    "mode": 3,
                    "dis": 2295,
                    "cal": 95,
                    "step": 2874
                },
                {
                    "start": 368,
                    "stop": 377,
                    "mode": 4,
                    "dis": 1592,
                    "cal": 88,
                    "step": 1664
                },
                {
                    "start": 378,
                    "stop": 386,
                    "mode": 3,
                    "dis": 1072,
                    "cal": 51,
                    "step": 1245
                },
                {
                    "start": 387,
                    "stop": 393,
                    "mode": 4,
                    "dis": 1036,
                    "cal": 57,
                    "step": 1124
                },
                {
                    "start": 394,
                    "stop": 398,
                    "mode": 3,
                    "dis": 488,
                    "cal": 19,
                    "step": 607
                },
                {
                    "start": 399,
                    "stop": 414,
                    "mode": 4,
                    "dis": 2220,
                    "cal": 120,
                    "step": 2371
                },
                {
                    "start": 415,
                    "stop": 427,
                    "mode": 3,
                    "dis": 1268,
                    "cal": 59,
                    "step": 1489
                },
                {
                    "start": 428,
                    "stop": 433,
                    "mode": 1,
                    "dis": 152,
                    "cal": 4,
                    "step": 238
                },
                {
                    "start": 434,
                    "stop": 444,
                    "mode": 3,
                    "dis": 2295,
                    "cal": 95,
                    "step": 2874
                },
                {
                    "start": 445,
                    "stop": 455,
                    "mode": 4,
                    "dis": 1592,
                    "cal": 88,
                    "step": 1664
                },
                {
                    "start": 456,
                    "stop": 466,
                    "mode": 3,
                    "dis": 1072,
                    "cal": 51,
                    "step": 1245
                },
                {
                    "start": 467,
                    "stop": 477,
                    "mode": 4,
                    "dis": 1036,
                    "cal": 57,
                    "step": 1124
                },
                {
                    "start": 478,
                    "stop": 488,
                    "mode": 3,
                    "dis": 488,
                    "cal": 19,
                    "step": 607
                },
                {
                    "start": 489,
                    "stop": 499,
                    "mode": 4,
                    "dis": 2220,
                    "cal": 120,
                    "step": 2371
                },
                {
                    "start": 500,
                    "stop": 511,
                    "mode": 3,
                    "dis": 1268,
                    "cal": 59,
                    "step": 1489
                },
                {
                    "start": 512,
                    "stop": 522,
                    "mode": 1,
                    "dis": 152,
                    "cal": 4,
                    "step": 238
                }
            ]
        },
        "goal": 8000,
        "tz": "28800"
    }

    data_json = [
        {
            "data_hr": "//////9L////////////Vv///////////0v///////////9e/////0n/a///S////////////0b//////////1FK////////////R/////////////////9PTFFpaf9L////////////R////////////0j///////////9K////////////Ov///////////zf///86/zr/Ov88/zf/Pf///0v/S/8/////////////Sf///////////z3//////0r/Ov//////S/9L/zb/Sf9K/0v/Rf9H/zj/Sf9K/0//N////0D/Sf83/zr/Pf9M/0v/Ov9e////////////S////////////zv//z7/O/83/zv/N/83/zr/N/86/z//Nv83/zn/Xv84/zr/PP84/zj/N/9e/zr/N/89/03/P/89/z3/Q/9N/0v/Tv9C/0H/Of9D/zz/Of88/z//PP9A/zr/N/86/zz/Nv87/0D/Ov84/0v/O/84/zf/MP83/zH/Nv83/zf/N/84/zf/Of82/zf/OP83/zb/Mv81/zX/R/9L/0v/O/9I/0T/S/9A/zn/Pf89/zn/Nf9K/07/N/83/zn/Nv83/zv/O/9A/0H/Of8//zj/PP83/zj/S/87/zj/Nv84/zf/Of83/zf/Of83/zb/Nv9L/zj/Nv82/zb/N/85/zf/N/9J/zf/Nv83/zj/Nv84/0r/Sv83/zf/MP///zb/Mv82/zb/Of85/z7/Nv8//0r/S/85/0H/QP9B/0D/Nf89/zj/Ov83/zv/Nv8//0f/Sv9O/0ZeXv///////////1X///////////9B////////////TP///1b//////0////////////9N/////////v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+",
            "date": today,
            "data": [
                {
                    "start": 0,
                    "stop": 1439,
                    "value": "UA8AUBQAUAwAUBoAUAEAYCcAUBkAUB4AUBgAUCAAUAEAUBkAUAwAYAsAYB8AYB0AYBgAYCoAYBgAYB4AUCcAUBsAUB8AUBwAUBIAYBkAYB8AUBoAUBMAUCEAUCIAYBYAUBwAUCAAUBgAUCAAUBcAYBsAYCUAATIPYD0KECQAYDMAYB0AYAsAYCAAYDwAYCIAYB0AYBcAYCQAYB0AYBAAYCMAYAoAYCIAYCEAYCYAYBsAYBUAYAYAYCIAYCMAUB0AUCAAUBYAUCoAUBEAUC8AUB0AUBYAUDMAUDoAUBkAUC0AUBQAUBwAUA0AUBsAUAoAUCEAUBYAUAwAUB4AUAwAUCcAUCYAUCwKYDUAAUUlEC8IYEMAYEgAYDoAYBAAUAMAUBkAWgAAWgAAWgAAWgAAWgAAUAgAWgAAUBAAUAQAUA4AUA8AUAkAUAIAUAYAUAcAUAIAWgAAUAQAUAkAUAEAUBkAUCUAWgAAUAYAUBEAWgAAUBYAWgAAUAYAWgAAWgAAWgAAWgAAUBcAUAcAWgAAUBUAUAoAUAIAWgAAUAQAUAYAUCgAWgAAUAgAWgAAWgAAUAwAWwAAXCMAUBQAWwAAUAIAWgAAWgAAWgAAWgAAWgAAWgAAWgAAWgAAWREAWQIAUAMAWSEAUDoAUDIAUB8AUCEAUC4AXB4AUA4AWgAAUBIAUA8AUBAAUCUAUCIAUAMAUAEAUAsAUAMAUCwAUBYAWgAAWgAAWgAAWgAAWgAAWgAAUAYAWgAAWgAAWgAAUAYAWwAAWgAAUAYAXAQAUAMAUBsAUBcAUCAAWwAAWgAAWgAAWgAAWgAAUBgAUB4AWgAAUAcAUAwAWQIAWQkAUAEAUAIAWgAAUAoAWgAAUAYAUB0AWgAAWgAAUAkAWgAAWSwAUBIAWgAAUC4AWSYAWgAAUAYAUAoAUAkAUAIAUAcAWgAAUAEAUBEAUBgAUBcAWRYAUA0AWSgAUB4AUDQAUBoAXA4AUA8AUBwAUA8AUA4AUA4AWgAAUAIAUCMAWgAAUCwAUBgAUAYAUAAAUAAAUAAAUAAAUAAAUAAAUAAAUAAAUAAAWwAAUAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAeSEAeQ8AcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcBcAcAAAcAAAcCYOcBUAUAAAUAAAUAAAUAAAUAUAUAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcCgAeQAAcAAAcAAAcAAAcAAAcAAAcAYAcAAAcBgAeQAAcAAAcAAAegAAegAAcAAAcAcAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcCkAeQAAcAcAcAAAcAAAcAwAcAAAcAAAcAIAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcCIAeQAAcAAAcAAAcAAAcAAAcAAAeRwAeQAAWgAAUAAAUAAAUAAAUAAAUAAAcAAAcAAAcBoAeScAeQAAegAAcBkAeQAAUAAAUAAAUAAAUAAAUAAAUAAAcAAAcAAAcAAAcAAAcAAAcAAAegAAegAAcAAAcAAAcBgAeQAAcAAAcAAAcAAAcAAAcAAAcAkAegAAegAAcAcAcAAAcAcAcAAAcAAAcAAAcAAAcA8AeQAAcAAAcAAAeRQAcAwAUAAAUAAAUAAAUAAAUAAAUAAAcAAAcBEAcA0AcAAAWQsAUAAAUAAAUAAAUAAAUAAAcAAAcAoAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAYAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcBYAegAAcAAAcAAAegAAcAcAcAAAcAAAcAAAcAAAcAAAeRkAegAAegAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAEAcAAAcAAAcAAAcAUAcAQAcAAAcBIAeQAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcBsAcAAAcAAAcBcAeQAAUAAAUAAAUAAAUAAAUAAAUBQAcBYAUAAAUAAAUAoAWRYAWTQAWQAAUAAAUAAAUAAAcAAAcAAAcAAAcAAAcAAAcAMAcAAAcAQAcAAAcAAAcAAAcDMAeSIAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcAAAcBQAeQwAcAAAcAAAcAAAcAMAcAAAeSoAcA8AcDMAcAYAeQoAcAwAcFQAcEMAeVIAaTYAbBcNYAsAYBIAYAIAYAIAYBUAYCwAYBMAYDYAYCkAYDcAUCoAUCcAUAUAUBAAWgAAYBoAYBcAYCgAUAMAUAYAUBYAUA4AUBgAUAgAUAgAUAsAUAsAUA4AUAMAUAYAUAQAUBIAASsSUDAAUDAAUBAAYAYAUBAAUAUAUCAAUBoAUCAAUBAAUAoAYAIAUAQAUAgAUCcAUAsAUCIAUCUAUAoAUA4AUB8AUBkAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAAfgAA",
                    "tz": 32,
                    "did": "DA932FFFFE8816E7",
                    "src": 24
                }
            ],
            "summary": json.dumps(summary),
            "source": 24,
            "type": 0
        }
    ]

    url = f'https://api-mifit-cn.huami.com/v1/data/band_data.json?&t={t}'
    head = {
        "apptoken": app_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = f'userid={userid}&last_sync_data_time=1597306380&device_type=0&last_deviceid=DA932FFFFE8816E7&data_json={quote(json.dumps(data_json))}'

    response = requests.post(url, data=data, headers=head).json()
    # print(response)
    result = f"用户: {_user[:4]}****{_user[-4:]} \n时间: [{now}] \n修改步数: {_step}\n状态码: " + response['message']
    print(result)
    return result


def get_time():
    """
    获取时间戳
    """
    url = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'
    response = requests.get(url, headers=headers).json()
    t = response['data']['t']
    return t


def get_app_token(login_token):
    """
    获取app_token
    """
    url = f"https://account-cn.huami.com/v1/client/app_tokens" \
          f"?app_name=com.xiaomi.hm.health&dn=api-user.huami.com%2Capi-mifit.huami.com%2Capp-analytics.huami.com" \
          f"&login_token={login_token}"
    response = requests.get(url, headers=headers).json()
    app_token = response['token_info']['app_token']
    # print("app_token获取成功！")
    # print(app_token)
    return app_token