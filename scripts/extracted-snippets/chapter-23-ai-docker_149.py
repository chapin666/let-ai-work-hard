# Source: chapter-23-ai-docker.md
# Lines: 149-183
# Language: python

"""Gunicorn配置"""
import os
import multiprocessing

# 服务器绑定
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# 工作进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"

# 连接设置
worker_connections = 1000
keepalive = 5

# 超时设置
timeout = 120
graceful_timeout = 30

# 日志配置
accesslog = "-"  # 输出到stdout
errorlog = "-"
loglevel = os.getenv('LOG_LEVEL', 'info')

# 进程名称
proc_name = "flask_app"

# 预加载应用（节省内存）
preload_app = True

# 优雅重启
max_requests = 1000
max_requests_jitter = 50
