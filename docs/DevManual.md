# bushu 开发手册

> 本文介绍 [微信刷步数(bushu)](https://github.com/ZHJ0125/bushu) 项目的开发过程。

此文档面向开发者，如果您是普通用户，请移步至[用户手册](./UserManual.md)。

## 1. 项目概述

* 核心代码使用[方块君](https://github.com/577fkj) 大佬的 [mimotion](https://github.com/577fkj/mimotion) 项目
* Web 界面使用 [Flask](https://github.com/pallets/flask) 框架
* 网页由运行在腾讯云的 [Docker](https://hub.docker.com/repository/docker/zhj0125/bushu) 驱动
* 源代码托管在 [GitHub](https://github.com/ZHJ0125/bushu) 平台

## 2. 如何构建本项目

> ✔ 提示 1：快速上手可参考 `2.3.2 从 DockerHub 拉取镜像并运行`<br>
> ⚠ 提示 2：在服务器上运行时需要开放对应端口的防火墙

您可以尝试使用以下三种方式运行本项目，三种方式要求的环境如下：

1. 使用 Python Venv 虚拟环境
    * 建议使用 Linux 系统（Windows环境需要解决fcntl问题）
    * 安装 Python3.x 版本
2. 使用 Heroku 方式托管网页 - 属于 Heroku 分支（目前不再维护，此方式不需要服务器）
    * 需要拉取 Heroku 分支的代码
    * 建议使用 Windows 系统
    * 安装 Python3.x 版本
3. 使用 Docker 方式驱动网页 - main 主分支（推荐此方式，但需要服务器）
    * 建议使用 Linux 系统（Windows环境需要解决fcntl问题）
    * 需要已安装 Docker
    * Python3.x 版本

### 2.1 使用 Python Venv 虚拟环境

1. 克隆本项目（以 Linux 环境为例）

```bash
# 打开终端，克隆本项目
zhj@ubuntu:~$ git clone https://github.com/ZHJ0125/bushu.git
Cloning into 'bushu'...
remote: Enumerating objects: 137, done.
remote: Counting objects: 100% (137/137), done.
remote: Compressing objects: 100% (96/96), done.
remote: Total 137 (delta 60), reused 107 (delta 34), pack-reused 0
Receiving objects: 100% (137/137), 211.76 KiB | 377.00 KiB/s, done.
Resolving deltas: 100% (60/60), done.
# 进入项目文件夹
zhj@ubuntu:~$ cd bushu
# 查看文件夹下的内容
zhj@ubuntu:~/bushu$ ls -al
total 36
drwxrwxr-x  5 zhj zhj 4096 Oct 15 03:50 .
drwxr-xr-x 26 zhj zhj 4096 Oct 15 03:50 ..
drwxrwxr-x  4 zhj zhj 4096 Oct 15 03:50 app
-rw-rw-r--  1 zhj zhj  430 Oct 15 03:50 Dockerfile
drwxrwxr-x  2 zhj zhj 4096 Oct 15 03:50 docs
drwxrwxr-x  8 zhj zhj 4096 Oct 15 03:50 .git
-rw-rw-r--  1 zhj zhj   45 Oct 15 03:50 .gitignore
-rw-rw-r--  1 zhj zhj  305 Oct 15 03:50 gunicorn.conf.py
-rw-rw-r--  1 zhj zhj 1574 Oct 15 03:50 README.md
```

2. 搭建开发环境（Linux + Python3.x + Venv）

```bash
# 检查 Python 版本，需要是 Python3.x
zhj@ubuntu:~/bushu$ python -V
Python 3.7.5
# 安装 Venv 虚拟环境
zhj@ubuntu:~/bushu$ python -m venv env
# 激活虚拟环境
zhj@ubuntu:~/bushu$ source env/bin/activate
(env) zhj@ubuntu:~/bushu$ 
# 激活之后会进入虚拟机环境，命令行前面有(env)提示
(env) zhj@ubuntu:~/bushu$ 
# 在env环境中更新其pip版本
(env) zhj@ubuntu:~/bushu$ python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
Collecting pip
  Using cached https://pypi.tuna.tsinghua.edu.cn/packages/1f/2c/d9626f045e7b49a6225c6b09257861f24da78f4e5f23af2ddbdf852c99b8/pip-22.2.2-py3-none-any.whl
Installing collected packages: pip
  Found existing installation: pip 9.0.1
    Uninstalling pip-9.0.1:
      Successfully uninstalled pip-9.0.1
Successfully installed pip-22.2.2
# 将项目依赖添加到虚拟环境中
(env) zhj@ubuntu:~/bushu$ pip install -r app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 列出已下载的依赖项，如下所示
(env) zhj@ubuntu:~/bushu$ pip list
Package            Version
------------------ ---------
certifi            2021.10.8
charset-normalizer 2.0.12
click              8.0.4
colorama           0.4.4
Flask              2.0.3
Flask-WTF          1.0.0
gevent             21.12.0
greenlet           1.1.3
gunicorn           20.1.0
idna               3.3
importlib-metadata 4.11.2
itsdangerous       2.1.1
Jinja2             3.0.3
MarkupSafe         2.1.0
pip                22.2.2
pkg_resources      0.0.0
python-dotenv      0.19.2
requests           2.27.1
setuptools         39.0.1
typing_extensions  4.1.1
urllib3            1.26.8
Werkzeug           2.0.3
WTForms            3.0.1
zipp               3.7.0
zope.event         4.5.0
zope.interface     5.4.0
```

3. 本地运行此项目

```bash
# 本地运行此本项目（注意要在 env 环境下运行）
(env) zhj@ubuntu:~/bushu$ gunicorn -c gunicorn.conf.py --chdir ./app main:app
[2022-10-15 04:12:41 +0800] [59299] [INFO] Starting gunicorn 20.1.0
[2022-10-15 04:12:41 +0800] [59299] [INFO] Listening at: http://0.0.0.0:8103 (59299)
[2022-10-15 04:12:41 +0800] [59299] [INFO] Using worker: gevent
[2022-10-15 04:12:41 +0800] [59302] [INFO] Booting worker with pid: 59302
[2022-10-15 04:12:41 +0800] [59303] [INFO] Booting worker with pid: 59303
[2022-10-15 04:12:41 +0800] [59304] [INFO] Booting worker with pid: 59304
[2022-10-15 04:12:41 +0800] [59305] [INFO] Booting worker with pid: 59305
# 此时打开 http://0.0.0.0:8103 即可查看页面
```

### 2.2 使用 Heroku 方式托管网页

⚠ 注：Heroku方式已从主分支剥离，若要使用Heroku托管方式，请转至 [Heroku 分支](https://github.com/ZHJ0125/bushu/tree/heroku) 了解详情。

### 2.3 使用 Docker 方式驱动网页

* Dockerfile 是用来创建 Docker 镜像的文件，本项目提供 Dockerfile 文件进行镜像构建；
* DockerHub 是专门托管 Docker 镜像的平台，本项目中所使用的镜像也已经上传到了 DockerHub 中；

因此您可以选择自己构建 Docker 镜像或者直接从 DockerHub 拉取镜像两种方式。

#### 2.3.1 从 Dockerfile 构建镜像并运行

1. 克隆本项目（主分支+ Linux 服务器环境为例）

```bash
# 打开终端，克隆本项目
zhj@ubuntu:~$ git clone https://github.com/ZHJ0125/bushu.git
Cloning into 'bushu'...
remote: Enumerating objects: 137, done.
remote: Counting objects: 100% (137/137), done.
remote: Compressing objects: 100% (96/96), done.
remote: Total 137 (delta 60), reused 107 (delta 34), pack-reused 0
Receiving objects: 100% (137/137), 211.76 KiB | 377.00 KiB/s, done.
Resolving deltas: 100% (60/60), done.
# 进入项目文件夹
zhj@ubuntu:~$ cd bushu
# 查看文件夹下的内容
zhj@ubuntu:~/bushu$ ls -al
total 36
drwxrwxr-x  5 zhj zhj 4096 Oct 15 03:50 .
drwxr-xr-x 26 zhj zhj 4096 Oct 15 03:50 ..
drwxrwxr-x  4 zhj zhj 4096 Oct 15 03:50 app
-rw-rw-r--  1 zhj zhj  430 Oct 15 03:50 Dockerfile
drwxrwxr-x  2 zhj zhj 4096 Oct 15 03:50 docs
drwxrwxr-x  8 zhj zhj 4096 Oct 15 03:50 .git
-rw-rw-r--  1 zhj zhj   45 Oct 15 03:50 .gitignore
-rw-rw-r--  1 zhj zhj  305 Oct 15 03:50 gunicorn.conf.py
-rw-rw-r--  1 zhj zhj 1574 Oct 15 03:50 README.md
```

2. 使用 Dcoker 部署页面

```bash
# 检查 Docker 版本，若未安装请自行安装
# Docker 安装过程可参考清华大学开源软件镜像站帮助文档：
# https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/
zhj@ubuntu:~/bushu$ docker -v
Docker version 20.10.18, build b40c2f6
# 构建 Docker 镜像（确保在 bushu 根目录下，此路径下有 Dockerfile 文件）
zhj@ubuntu:~/bushu$ docker build -t "bushu:v0.1" .
Sending build context to Docker daemon  684.5kB
Step 1/9 : FROM python:3.7
 ---> d74a76afa4e0
Step 2/9 : MAINTAINER ZHJ0125 <zhanghoujin123 AT gmail DOT COM>
 ---> Using cache
 ---> d363e7e94f45
Step 3/9 : WORKDIR /Projects/bushu
 ---> Using cache
 ---> d8914bd4aa26
Step 4/9 : ENV PYTHONDONTWRITEBYTECODE=1     FLASK_ENV=production
 ---> Using cache
 ---> a89946577287
Step 5/9 : COPY ./app .
 ---> 99ed89c8f723
Step 6/9 : RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip &&     pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
 ---> Running in 53fcdeeb6a31
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Requirement already satisfied: pip in /usr/local/lib/python3.7/site-packages (22.0.4)
Collecting pip
    ...... # 此处省略多行下载过程 ......
Removing intermediate container 53fcdeeb6a31
 ---> 530df80e9089
Step 7/9 : EXPOSE 8103
 ---> Running in 00ef305d62a1
Removing intermediate container 00ef305d62a1
 ---> 4566f4617be1
Step 8/9 : COPY gunicorn.conf.py .
 ---> 76a4888a0ca5
Step 9/9 : CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:app"]
 ---> Running in 7aeac3683b6d
Removing intermediate container 7aeac3683b6d
 ---> bf6b68080e40
Successfully built bf6b68080e40
Successfully tagged bushu:v0.1
# 启动 Docker，运行容器
# 注1：以下命令为后台运行该容器
# 注2：8000端口为本机映射端口，可修改为其他端口；8103为 Docker 内部端口，不要修改
# 注3：更多关于 Docker 命令参数说明请查阅 Docker 文档：https://docs.docker.com/
zhj@ubuntu:~/bushu$ docker run -it -d -p 8000:8103 bushu:v0.1
d7c0be07ab572caceef5be60d85b6167a93435845cc1e54cc074e250ba260a53
# 运行后访问 http://服务器IP:8000 即可
```

#### 2.3.2 从 DockerHub 拉取镜像并运行

> 在已安装 Docker 的环境下，此方式最为简单，只需 2 条命令即可部署完成。

```bash
# 1. 拉取镜像
zhj@ubuntu:~$ docker pull zhj0125/bushu
Using default tag: latest
latest: Pulling from zhj0125/bushu
f606d8928ed3: Already exists 
47db815c6a45: Already exists 
bf4849400000: Already exists 
a572f7a256d3: Already exists 
8f7d05258955: Already exists 
7110f04115ae: Already exists 
a67c12cf4c39: Already exists 
4e5ce410e73f: Already exists 
d1c4120e1d6e: Already exists 
2744a6373f4c: Pull complete 
089934bb5017: Pull complete 
97cb7891e65a: Pull complete 
bb3d159899fa: Pull complete 
Digest: sha256:d0fcf92f9a6619e2c3c998d006ba0abbc389b657a425da41cef1f00f28bb8455
Status: Downloaded newer image for zhj0125/bushu:latest
docker.io/zhj0125/bushu:latest
# 2. 运行容器
# 注：8080端口为本机映射端口，可修改为其他端口；8103为 Docker 内部端口，不要修改
zhj@ubuntu:~$ docker run -it -d -p 8080:8103 zhj0125/bushu
c6557923aab001bcae0104875fd3cee22329e5ac01885161ff01a383d67c6a39
# 3. 访问 http://ip:8080 即可
```

## 项目代码梳理

本项目中包含的主要代码及代码作用如下：

```
./bushu
├── app                    // 应用程序文件夹
│   ├── main.py            // 主程序
│   ├── requirements.txt   // 依赖文件
│   ├── static             // 图片等静态文件
│   └── templates          // HTML 网页文件夹
├── Dockerfile             // 用于构建 Docker 镜像
├── docs
│   ├── DevLog.md          // 开发日志
│   ├── DevManual.md       // 开发手册
│   ├── show.jpg           // 展示图片
│   └── UserManual.md      // 使用手册
├── gunicorn.conf.py       // gunicorn 配置文件
└── README.md
```

若您要开发其他功能，请阅读 [main.py](../main.py) 源代码

## 参考资料

* [mimotion Github](https://github.com/577fkj/mimotion)
* [HelloFlask Meta Github](https://github.com/greyli/helloflask)
* [Flask Project Document](https://flask.palletsprojects.com/en/2.0.x/)
* [Flask-WTF Document](https://flask-wtf.readthedocs.io/en/latest/quickstart/)
* [Docker Docs - Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
* [Docker Community Edition 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/)
* [使用 HTML 和 CSS 构建一个注册表单](https://chinese.freecodecamp.org/news/how-to-build-sign-up-form-with-html-and-css/)

---

## 依赖项目

* [mimotion](https://github.com/577fkj/mimotion) ( Apache License 2.0 ) - 小米运动刷步数
* [Flask](https://github.com/pallets/flask) ( BSD 3-Clause "New" or "Revised" License ) - 用于构建 Web 应用程序的 Python 微框架
* [Docker](https://github.com/docker) - Develop faster. Run anywhere.

## 开源协议

* 本项目使用 [GNU General Public License v3.0](https://github.com/ZHJ0125/bushu/blob/main/LICENSE)  开源许可协议
* Gitee地址：https://gitee.com/zhj0125/bushu
* GitHub地址：https://github.com/ZHJ0125/bushu
