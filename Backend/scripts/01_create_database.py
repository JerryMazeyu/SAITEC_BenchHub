import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app import create_app
from app.extensions import db
from flask import current_app
from utils import printtify, Style
import warnings
warnings.filterwarnings('ignore')

def create_database(config_class):
    """
    根据指定的配置创建数据库。
    """
    app = create_app(config_class)

    with app.app_context():
        printtify(f"数据库URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        if os.path.exists(os.path.join(current_app.root_path, "..", "instance", app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])):
            printtify("数据库已存在, 无需重复创建!", color='red')
        else:
            db.create_all()  # 创建所有表
            printtify("数据库已成功创建!",color='green')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a database for the Flask application.")
    parser.add_argument(
        "--env",
        choices=["development", "testing"],
        default="testing",
        help="Specify the environment for which to create the database.",
    )
    args = parser.parse_args()
    printtify("Step1. 数据库初始化（测试）", align="center", bright=True)
    config_class = f"app.config.{args.env.capitalize()}Config"
    printtify(f"使用配置文件为: {config_class}")
    create_database(config_class)
