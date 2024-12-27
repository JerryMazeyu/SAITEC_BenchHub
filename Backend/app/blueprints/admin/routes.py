from flask import request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models import AdminUser  # 用户模型
from . import admin_bp  # 引入 Blueprint
from .utils import log_admin_action  # 日志工具

# 登录视图
@admin_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录视图。
    - 请求方式: POST
    - 接收 JSON 格式的用户名和密码。
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # 验证用户
    user = AdminUser.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):  # 假设 verify_password 方法验证哈希密码
        return jsonify({"error": "Invalid username or password"}), 401

    # 登录用户并记录操作
    login_user(user)
    log_admin_action(user.id, "login")

    # 重定向到 next 参数指向的页面（如有），否则返回成功信息
    next_url = request.args.get('next')
    return redirect(next_url or url_for('admin.dashboard'))

# 登出视图
@admin_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    用户登出视图。
    - 请求方式: POST
    """
    user_id = current_user.id
    username = current_user.username

    # 登出用户并记录操作
    logout_user()
    log_admin_action(user_id, "logout")

    return jsonify({"message": f"Goodbye, {username}!"}), 200

# 查看仪表盘（受保护路由）
@admin_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    查看仪表盘视图。
    - 请求方式: GET
    - 需要用户登录。
    """
    return jsonify({"message": f"Welcome to the dashboard, {current_user.username}!"}), 200

# 查看使用记录
@admin_bp.route('/logs', methods=['GET'])
@login_required
def get_logs():
    """
    查看管理员操作日志。
    - 请求方式: GET
    - 返回操作日志的 JSON 数据。
    """
    from flask import current_app as app
    logs = app.config.get('ADMIN_LOGS', [])
    return jsonify({"logs": logs}), 200
