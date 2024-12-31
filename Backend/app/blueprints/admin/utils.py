from datetime import datetime
from app.extensions import db
from app.models import ActionLog


def log_admin_action(user_id, action):
    """
    记录管理员操作日志，同时更新用户的 last_login 字段（如果是登录操作）。
    """
    from app.models import AdminUser

    now = datetime.now()
    # 记录操作日志
    action_log = ActionLog(
        user_id=user_id,
        action=action,
        timestamp=now,
        description=f"User {user_id} {action} at {now}."
    )
    db.session.add(action_log)

    # 如果是登录操作，更新 last_login 字段
    if action == "login":
        user = AdminUser.query.get(user_id)
        if user:
            user.last_login = datetime.now()
            db.session.add(user)

    # 提交到数据库
    db.session.commit()