from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from flask import jsonify


# 初始化扩展实例
db = SQLAlchemy()                   # 数据库
migrate = Migrate()                 # 数据库迁移
login_manager = LoginManager()      # 用户认证管理器
cache = Cache()                     # 缓存扩展


@login_manager.user_loader
def load_user(user_id):
    """
    根据用户 ID 加载用户实例。
    Flask-Login 会调用此函数来获取当前用户。
    """
    from app.models import AdminUser
    return AdminUser.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    """
    未登录时的自定义响应
    """
    return jsonify({"error": "Unauthorized access. Please log in."}), 405

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cache.init_app(app)

    login_manager.unauthorized_handler = unauthorized
    login_manager.login_view = 'admin.login'

