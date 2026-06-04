"""
统计 API 路由模块

提供数据统计相关的 API 接口：
- 平台数据统计（管理员）
- 用户活跃度排行榜（公开）
"""
from flask import Blueprint, request, g
from app.api.deps import require_auth, require_role
from app.common.response import success
from app.services.stats_service import StatsService

bp = Blueprint('Statistics', __name__)


@bp.get('/admin/statistics')
@require_auth()
@require_role('admin')
def admin_statistics():
    """
    获取平台数据统计（管理员）
    
    提供平台的宏观统计数据，用于管理后台的数据看板
    
    Returns:
        dict: 平台统计数据，包含以下模块：
        
        - activities: 活动统计
            - total: 活动总数
            - by_statuss: 按状态分布
                - pending: 待审核
                - open: 报名中
                - edit_pending: 修改审核中
                - ongoing: 进行中
                - ended: 已结束
            - by_categories: 按分类分布
                - 学术类: 数量
                - 文体类: 数量
                - 志愿服务: 数量
                - ...
        
        - user: 用户统计
            - total: 总用户数（学生+组织者+管理员）
            - student: 学生数量
            - organize: 组织者数量
            - admin: 管理员数量
        
        - total_participation_count: 总报名次数
        - average_checkin_rate: 平均签到率
    
    """
    result = StatsService.get_platform_stats()
    return success(result)


@bp.get('/leaderboard')
def leaderboard():
    """
    获取用户活跃度排行榜（公开）
    
    根据用户的报名次数和签到次数进行排名
    支持按周期、学院、年级筛选
    
    Query Parameters:
        - period (str): 统计周期
            - week: 最近一周
            - month: 最近一个月
            - all: 全部时间（默认）
        - college (str): 学院筛选（可选）
        - grade (str): 年级筛选（可选）
        - page (int): 页码（默认1）
        - page_size (int): 每页数量（默认20，最大100）
    
    Returns:
        - total: 总记录数
        - list: 排行榜列表
            - rank: 排名
            - user_id: 用户ID
            - student_id: 学号
            - college: 学院
            - grade: 年级
            - registration_count: 报名次数
            - effective_participation_count: 有效参与次数（签到次数）
    
    排名规则:
        1. 优先按签到次数降序
        2. 签到次数相同时按报名次数降序
        3. 报名次数相同时按用户ID升序
    """
    params = request.args.to_dict()
    result = StatsService.get_leaderboard(params)
    return success(result)