class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev-secret-key'

class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # 开发环境数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_ROOT = r'C:\Users\H3C\WorkSpace\test_data'
    TRASH_ROOT = r'C:\Users\H3C\WorkSpace\test_backup'
