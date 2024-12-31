import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.extensions import db
from app.models import AdminUser
from app import create_app

# 创建 Flask 应用
app = create_app('app.config.DevelopmentConfig')

# 向数据库插入初始数据
def insert_initial_admin_users():
    with app.app_context():  # 确保在应用上下文中运行
        # 检查是否已有数据，避免重复插入
        if AdminUser.query.first():
            print("Initial admin users already exist in the database.")
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

        print("Admin users created successfully!")
        print(f"Inserted users: {admin1.username}, {admin2.username}")

if __name__ == "__main__":
    insert_initial_admin_users()
