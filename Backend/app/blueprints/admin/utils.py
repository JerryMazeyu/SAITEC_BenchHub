from flask import current_app as app


def log_admin_action(admin_id, action):
    """
    将管理员操作记录到日志中。
    :param admin_id: 管理员 ID
    :param action: 操作类型（如登录、登出）
    """
    log_entry = {"admin_id": admin_id, "action": action}
    if 'ADMIN_LOGS' not in app.config:
        app.config['ADMIN_LOGS'] = []
    app.config['ADMIN_LOGS'].append(log_entry)