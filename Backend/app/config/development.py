class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev-secret-key'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'  # 开发环境数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_ROOT = r'C:\Users\H3C\WorkSpace\data'
    TRASH_ROOT = r'C:\Users\H3C\WorkSpace\backup'
