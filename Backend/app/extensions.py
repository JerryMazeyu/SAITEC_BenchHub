from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache


# 初始化扩展实例
db = SQLAlchemy()                   # 数据库
migrate = Migrate()                 # 数据库迁移
login_manager = LoginManager()      # 用户认证管理器
cache = Cache()                     # 缓存扩展


def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cache.init_app(app)

    login_manager.login_view = 'admin.login'

