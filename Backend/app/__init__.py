from flask import Flask
from app.extensions import init_extensions

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)

    from app.blueprints.admin import admin_bp
    app.register_blueprint(admin_bp)

    return app