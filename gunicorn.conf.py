workers = 4              # 定义同时开启的处理请求的进程数量
worker_class = "gevent"  # 使用 gevent 库以支持异步处理请求
bind = "0.0.0.0:8103"    # 监听任意主机请求，端口可通过 docker 映射，不建议修改
timeout = 60             # 设置超时时间为 60 秒