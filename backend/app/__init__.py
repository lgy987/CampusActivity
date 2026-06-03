from flask import Flask
from config import get_config
from app.common.errors import register_error_handlers
from app.task.scheduler import start_scheduler

def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or get_config())
    start_scheduler()

    from app.api import (
        Auth_bp,
        User_bp,
        Activities_bp,
        Admin_Activities_bp,
        Admin_Users_bp,
        Registrations_bp,
        Checkin_bp,
        Notifications_bp,
        Statistics_bp,
        Categories_bp,
        Health_bp,
    )

    # 认证接口
    app.register_blueprint(Auth_bp, url_prefix='/auth')
    # 用户接口
    app.register_blueprint(User_bp, url_prefix='/user')
    # 活动接口（公开 + 组织者）
    app.register_blueprint(Activities_bp, url_prefix='')
    # 管理员接口
    app.register_blueprint(Admin_Activities_bp, url_prefix='/admin')
    app.register_blueprint(Admin_Users_bp, url_prefix='/admin')
    # 报名接口
    app.register_blueprint(Registrations_bp, url_prefix='')
    # 签到接口
    app.register_blueprint(Checkin_bp, url_prefix='')
    # 通知接口
    app.register_blueprint(Notifications_bp, url_prefix='')
    # 统计接口
    app.register_blueprint(Statistics_bp, url_prefix='')
    # 分类接口
    app.register_blueprint(Categories_bp, url_prefix='/categories')
    # 健康检查
    app.register_blueprint(Health_bp, url_prefix='')
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
