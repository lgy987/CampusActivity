from flask import Blueprint

# 导入所有蓝图
from app.api.auth import bp as Auth_bp
from app.api.user import bp as User_bp
from app.api.activities import bp as Activities_bp
from app.api.admin_activities import bp as Admin_Activities_bp
from app.api.admin_users import bp as Admin_Users_bp
from app.api.registrations import bp as Registrations_bp
from app.api.checkin import bp as Checkin_bp
from app.api.notifications import bp as Notifications_bp
from app.api.statistics import bp as Statistics_bp
from app.api.categories import bp as Categories_bp
from app.api.health import bp as Health_bp

# 统一导出
__all__ = [
    'Auth_bp',
    'User_bp',
    'Activities_bp',
    'Admin_Activities_bp',
    'Admin_Users_bp',
    'Registrations_bp',
    'Checkin_bp',
    'Notifications_bp',
    'Statistics_bp',
    'Categories_bp',
    'Health_bp',
]