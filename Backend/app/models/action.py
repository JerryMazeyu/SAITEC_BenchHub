from app.extensions import db
from datetime import datetime

class ActionLog(db.Model):
    __tablename__ = 'action_logs'

    id = db.Column(db.Integer, primary_key=True)  # 主键
    user_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=False)  # 关联到 AdminUser 表
    action = db.Column(db.String(50), nullable=False)  # 操作类型，例如 "login", "logout"
    timestamp = db.Column(db.DateTime, default=datetime.now(), nullable=False)  # 操作时间
    description = db.Column(db.Text, nullable=True)  # 描述字段，存储详细日志

    # 可选：提供便于调试的字符串表示
    def __repr__(self):
        return f"<AdminActionLog(user_id={self.user_id}, action='{self.action}', timestamp={self.timestamp})>"
