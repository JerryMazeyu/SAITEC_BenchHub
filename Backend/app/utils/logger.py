import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(app):
    # 确保日志目录存在
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    log_dir = os.path.join(base_dir, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 配置日志记录器
    log_file = os.path.join(log_dir, "app.log")
    handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 10, backupCount=5)
    handler.setLevel(logging.INFO)  # 日志级别
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # 将处理器添加到 Flask 的日志器
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
