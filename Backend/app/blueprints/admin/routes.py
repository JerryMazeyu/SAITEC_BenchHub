from flask import request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import AdminUser  # 用户模型
from . import admin_bp  # 引入 Blueprint
from .utils import log_admin_action  # 日志工具

@admin_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录视图。
    - 请求方式: POST
    - 接收 JSON 格式的用户名和密码。
    """
    try:
        # 确保请求内容是 JSON
        if not request.is_json:
            return jsonify({"success": False, "message": "Request must be JSON"}), 415

        # 获取请求数据
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # 检查参数是否为空
        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required"}), 400

        # 验证用户
        user = AdminUser.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):  # 假设 verify_password 方法验证哈希密码
            return jsonify({"success": False, "message": "Invalid username or password"}), 401

        # 登录用户
        login_user(user)  # 将用户的登录状态存储到会话（session）中，并允许您在整个应用中通过 current_user 访问已登录的用户
        log_admin_action(user.id, "login")  # 记录上次登陆时间

        # 返回登录成功信息和用户数据
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "last_login": user.last_login
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"[admin] Login error: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# 登出视图
@admin_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    用户登出视图。
    - 请求方式: POST
    """
    try:
        user_id = current_user.id
        username = current_user.username

        # 登出用户并记录操作
        logout_user()
        log_admin_action(user_id, "logout")

        return jsonify({"success": True, "message": "Goodbye, {username}!"}), 200
    except Exception as e:
        current_app.logger.error(f"[admin] Logout error: {e}")
        return jsonify({"success": False, "message": f"Internal server error: {e}"}), 500

