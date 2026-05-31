from flask import Flask
from config import get_config
from app.common.errors import register_error_handlers
from app.task.scheduler import start_scheduler

def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or get_config())
    start_scheduler()

    from app.api import (
        auth_bp,
        user_bp,
        activities_bp,
        admin_activities_bp,
        admin_users_bp,
        registrations_bp,
        checkin_bp,
        notifications_bp,
        statistics_bp,
        categories_bp,
        health_bp,
    )

    # 认证接口
    app.register_blueprint(auth_bp, url_prefix='/auth')
    # 用户接口
    app.register_blueprint(user_bp, url_prefix='/user')
    # 活动接口（公开 + 组织者）
    app.register_blueprint(activities_bp, url_prefix='')
    # 管理员接口
    app.register_blueprint(admin_activities_bp, url_prefix='/admin')
    app.register_blueprint(admin_users_bp, url_prefix='/admin')
    # 报名接口
    app.register_blueprint(registrations_bp, url_prefix='')
    # 签到接口
    app.register_blueprint(checkin_bp, url_prefix='')
    # 通知接口
    app.register_blueprint(notifications_bp, url_prefix='')
    # 统计接口
    app.register_blueprint(statistics_bp, url_prefix='')
    # 分类接口
    app.register_blueprint(categories_bp, url_prefix='/categories')
    # 健康检查
    app.register_blueprint(health_bp, url_prefix='')
    register_error_handlers(app)
    register_cors_headers(app)

    return app


def register_cors_headers(app):
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response
