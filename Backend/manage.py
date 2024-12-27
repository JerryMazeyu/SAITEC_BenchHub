from flask_script import Manager
from flask_migrate import MigrateCommand
from app import create_app
from app.extensions import db

# 根据环境加载配置
app = create_app('app.config.DevelopmentConfig')  # 或 TestingConfig
manager = Manager(app)

# 添加数据库迁移命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
