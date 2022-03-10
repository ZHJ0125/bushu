from flask import Flask, render_template, request, flash, url_for, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZHJ0125-bushu-dev'

name = 'ZHJ0125'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        flash('抱歉兄弟，后端代码还没写呢，敬请期待😂')  # 显示错误提示
        # 获取表单数据
        username = request.form.get('username')  # 传入表单对应输入字段的 name 值
        password = request.form.get('password')
        steps = request.form.get('steps')
        if not username or not password or not steps:
            flash('抱歉兄弟，后端代码还没写呢，敬请期待😂')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
    return render_template('index.html', name=name, movies=movies)

@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html', user=name), 404  # 返回模板和状态码