from flask import Blueprint, request, g
from app.api.deps import require_auth, require_role
from app.common.response import success
from app.services.stats_service import StatsService

bp = Blueprint('Statistics', __name__)


@bp.get('/admin/statistics')
@require_auth()
@require_role('admin')
def admin_statistics():
    """获取平台数据统计（管理员）"""
    result = StatsService.get_platform_stats()
    return success(result)


@bp.get('/leaderboard')
def leaderboard():
    """获取用户活跃度排行 """
    params = request.args.to_dict()
    result = StatsService.get_leaderboard(params)
    return success(result)