from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class AdminUser(UserMixin, db.Model):
    """
    管理员用户模型。
    - 继承 UserMixin 提供 Flask-Login 的支持。
    """
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(50), unique=True, nullable=False)  # 用户名
    password_hash = db.Column(db.String(200), nullable=False)  # 哈希密码
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # 创建时间
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())  # 更新时间
    last_login = db.Column(db.DateTime, nullable=True)  # 新增字段

    def set_password(self, password):
        """
        设置用户密码，保存为哈希值。
        :param password: 明文密码
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        验证用户密码。
        :param password: 明文密码
        :return: 验证结果 (True/False)
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<AdminUser {self.username}>"
