# bushu 开发手册

> 本文介绍 [微信刷步数(bushu)](https://github.com/ZHJ0125/bushu) 项目的开发过程。

此文档面向开发者，如果您是普通用户，请移步至[用户手册](./UserManual.md)。

## 项目概述

* 核心代码使用[方块君](https://github.com/577fkj) 大佬的 [mimotion](https://github.com/577fkj/mimotion) 项目
* Web 界面使用 [Flask](https://github.com/pallets/flask) 框架
* 网页代码部署在 [Heroku](https://www.heroku.com/) 平台
* 源代码托管在 [GitHub](https://github.com/ZHJ0125/bushu) 平台

## 如何构建本项目

### 在本地运行此项目

1. 克隆本项目

```powershell
# 克隆本项目
C:\Users\ZHJ\Desktop>git clone https://github.com/ZHJ0125/bushu.git
Cloning into 'bushu'...
remote: Enumerating objects: 58, done.
remote: Counting objects: 100% (58/58), done.
remote: Compressing objects: 100% (43/43), done.
remote: Total 58 (delta 23), reused 43 (delta 11), pack-reused 0
Receiving objects: 100% (58/58), 159.92 KiB | 839.00 KiB/s, done.
Resolving deltas: 100% (23/23), done.
# 进入项目文件夹
C:\Users\ZHJ\Desktop>cd bushu
# 查看文件夹下的内容
C:\Users\ZHJ\Desktop\bushu>dir
 Volume in drive C is WindowsOS
 Volume Serial Number is F468-2AC4

 Directory of C:\Users\ZHJ\Desktop\bushu

2022-03-11  21:57    <DIR>          .
2022-03-11  21:57    <DIR>          ..
2022-03-11  21:57                64 .flaskenv
2022-03-11  21:57                51 .gitignore
2022-03-11  21:57            19,870 main.py
2022-03-11  21:57                22 Procfile
2022-03-11  21:57                 7 README.md
2022-03-11  21:57               353 requirements.txt
2022-03-11  21:57    <DIR>          static
2022-03-11  21:57    <DIR>          templates
               6 File(s)         20,367 bytes
               4 Dir(s)  378,896,523,264 bytes free
```

2. 搭建开发环境（Windows10 + Python3.x + Venv）

```powershell
# 检查 Python 版本，需要是 Python3.x
C:\Users\ZHJ\Desktop\bushu>python -V
Python 3.7.2
# 确保安装了 pip 工具
C:\Users\ZHJ\Desktop\bushu>pip -V
pip 22.0.4 from D:\python\python3\install\lib\site-packages\pip (python 3.7)
# 安装 Venv 虚拟环境
C:\Users\ZHJ\Desktop\bushu>python -m venv venv
# 激活虚拟环境
C:\Users\ZHJ\Desktop\bushu>venv\Scripts\activate
# 激活之后会进入虚拟机环境，命令行显示如下（有venv提示）
(venv) C:\Users\ZHJ\Desktop\bushu>
# 将项目依赖添加到虚拟环境中，此过程需要联网下载依赖项
(venv) C:\Users\ZHJ\Desktop\bushu>pip install -r requirements.txt
# 列出已下载的依赖项，如下所示
(venv) C:\Users\ZHJ\Desktop\bushu>pip list
Package            Version
------------------ ---------
certifi            2021.10.8
charset-normalizer 2.0.12
click              8.0.4
colorama           0.4.4
Flask              2.0.3
Flask-WTF          1.0.0
gunicorn           20.1.0
idna               3.3
importlib-metadata 4.11.2
itsdangerous       2.1.1
Jinja2             3.0.3
MarkupSafe         2.1.0
pip                18.1
python-dotenv      0.19.2
requests           2.27.1
setuptools         40.6.2
typing-extensions  4.1.1
urllib3            1.26.8
Werkzeug           2.0.3
WTForms            3.0.1
zipp               3.7.0
```

3. 本地运行此项目

```powershell
# 本地运行此应用程序
(venv) C:\Users\ZHJ\Desktop\bushu>flask run
 * Serving Flask app 'main' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 672-602-107
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
# 此时打开http://127.0.0.1:5000 即可查看页面
```

### 将项目部署到 Heroku

Heroku 是一个 Web 部署平台，在本项目中，使用 Heroku 将本地应用程序部署到了公网，并获取到了应用程序链接：[https://zhj-bushu.herokuapp.com/](https://zhj-bushu.herokuapp.com/)

0. 将本地项目托管至 GitHub 平台

先去 GitHub 新建一个仓库，比如说命名为 `test-bushu`，然后将本地代码上传至你的 test-bushu 仓库，这一步我就不演示了

1. 注册 Heroku 账号

直接去 Heroku 官网 [heroku.com](heroku.com) 注册就可以了

2. 创建应用程序

在 Heroku 控制台 [https://dashboard.heroku.com/apps](https://dashboard.heroku.com/apps)，点击 `New` -> `Create new app` 新建一个应用程序。

起一个 `App name` -> 点击 `Create app`

`Deployment method` 选择 `Connect to GitHub`

在 `Connect to GitHub` 选项卡中，输入你的仓库地址，如 `test-bushu`，点击 `Search` 查找该仓库

3. 部署 web 应用

在 `Automatic deploys` 选项卡中，选择 `Enable Automatic Deploys` 自动更新部署

在 `Manual deploy` 选项卡中，选择 `Deploy Branch` 手动部署 main 分支。

等待部署完成后，他会显示 `Your app was successfully deployed.`，点击 `View` 或者访问平台给你的 Web 链接，就可以看到你部署的网页。

以本项目为例，链接为：[https://zhj-bushu.herokuapp.com/](https://zhj-bushu.herokuapp.com/)

## 项目代码梳理

本项目中包含的主要代码及代码作用如下：

```
./bushu
├── docs
│   ├── DevManual.md    // 开发手册
│   ├── UserManual.md   // 用户手册
│   └── show.jpg        // 展示图片
├── static
│   ├── images          // 图片资源
│   ├── favicon.ico     // 网站图标
│   └── style.css
├── templates
│   ├── 404.html
│   └── index.html
├── .flaskenv           // flask环境变量
├── .gitignore
├── LICENSE
├── main.py             // 主程序
├── Procfile            // Heroku的程序启动文件
├── README.md
└── requirements.txt    // Python依赖项
```

若您要开发其他功能，请阅读 [main.py](../main.py) 源代码

## 参考资料

* [mimotion Github](https://github.com/577fkj/mimotion)
* [HelloFlask Meta Github](https://github.com/greyli/helloflask)
* [Flask Project Document](https://flask.palletsprojects.com/en/2.0.x/)
* [Flask-WTF Document](https://flask-wtf.readthedocs.io/en/latest/quickstart/)
* [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python)
* [使用 HTML 和 CSS 构建一个注册表单](https://chinese.freecodecamp.org/news/how-to-build-sign-up-form-with-html-and-css/)
* [Heroku 部署 Flask 项目过程](https://wakingup.herokuapp.com/post/1/Heroku%E9%83%A8%E7%BD%B2Flask%E9%A1%B9%E7%9B%AE%E8%BF%87%E7%A8%8B)

---

## 依赖项目

* [mimotion](https://github.com/577fkj/mimotion) ( Apache License 2.0 ) - 小米运动刷步数
* [Flask](https://github.com/pallets/flask) ( BSD 3-Clause "New" or "Revised" License ) - 用于构建 Web 应用程序的 Python 微框架

## 开源协议

* 本项目使用 [GNU General Public License v3.0](https://github.com/ZHJ0125/bushu/blob/main/LICENSE)  开源许可协议
* Gitee地址：https://gitee.com/zhj0125/bushu
* GitHub地址：https://github.com/ZHJ0125/bushu
