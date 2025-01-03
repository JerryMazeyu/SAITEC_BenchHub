import os
from app import create_app


config_class = os.getenv('FLASK_CONFIG', 'app.config.DevelopmentConfig')

# 根据需要选择开发或测试环境
app = create_app('app.config.DevelopmentConfig')
app = create_app(config_class)


if __name__ == '__main__':
    app.run()
