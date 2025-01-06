import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.extensions import db
from app.models import AdminUser
from app import create_app
from utils import printtify, Style
import warnings
warnings.filterwarnings('ignore')

# 创建 Flask 应用

# 向数据库插入初始数据
def insert_initial_admin_users(config_class):
    app = create_app(config_class)

    with app.app_context():  # 确保在应用上下文中运行
        # 检查是否已有数据，避免重复插入
        if AdminUser.query.first():
            printtify("初始管理员用户已经存在!", color='red')
            return
        
        # 创建两条管理员数据
        admin1 = AdminUser(username="sstl1")
        admin1.set_password("sstl")  # 设置加密密码
        
        admin2 = AdminUser(username="sstl2")
        admin2.set_password("sstl")  # 设置加密密码

        # 插入数据到数据库
        db.session.add(admin1)
        db.session.add(admin2)
        db.session.commit()

        printtify("管理员用户已成功添加!", color='green')
        printtify(f"用户为: {admin1.username}, {admin2.username}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a config for the Flask application.")
    parser.add_argument(
        "--env",
        choices=["development", "testing"],
        default="testing",
        help="Specify the environment.",
    )
    args = parser.parse_args()
    printtify("Step2. 管理员数据初始化", align="center", bright=True)
    config_class = f"app.config.{args.env.capitalize()}Config"
    printtify(f"使用配置文件为: {config_class}")
    insert_initial_admin_users(config_class)

