from flask import Flask
from app.extensions import init_extensions
from app.utils.logger import setup_logger

def create_app(config_class='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    init_extensions(app)
    setup_logger(app)

    from app.blueprints.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.blueprints.benchmarks import benchmarks_bp
    app.register_blueprint(benchmarks_bp)

    return app