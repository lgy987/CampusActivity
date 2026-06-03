from flask import Blueprint
from app.common.response import success

bp = Blueprint('Health', __name__)


@bp.get('/health')
def health_check():
    """健康检查"""
    return success({'service': 'campus-activity-api', 'status': 'ok'})