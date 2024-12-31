import os
from flask import Flask
from flask_migrate import Migrate
from app import create_app
from app.extensions import db

# 动态加载配置
config_class = os.getenv('FLASK_CONFIG', 'app.config.DevelopmentConfig')

# 创建 Flask 应用
app = create_app(config_class)

# 初始化 Flask-Migrate
migrate = Migrate(app, db)


@app.cli.command("run")
def run():
    """启动 Flask 应用"""
    env = os.getenv('FLASK_ENV', 'development')
    print(f"Starting Flask app in {env} environment...")
    app.run()


@app.cli.command("db_reset")
def db_reset():
    """重置数据库：删除并重新创建表"""
    with app.app_context():
        db.drop_all()
        print("Dropped all tables.")
        db.create_all()
        print("Created all tables.")


@app.cli.command("db_init")
def db_init():
    """初始化数据库并运行脚本"""
    print("Initializing database...")
    with app.app_context():
        from flask_migrate import init, migrate, upgrade
        try:
            init()
        except Exception as e:
            print(f"Migration environment already exists: {e}")
        migrate()
        upgrade()

        print("Running scripts...")
        scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
        for script in os.listdir(scripts_dir):
            if script.endswith('.py') and script != '__init__.py':
                exec(open(os.path.join(scripts_dir, script)).read())
                print(f"Executed script: {script}")

        print("Database initialization complete.")
