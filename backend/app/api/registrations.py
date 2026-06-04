"""
报名 API 路由模块

提供报名管理相关的 API 接口：
- 报名活动（普通用户）
- 取消报名（普通用户）
- 我的报名列表（普通用户）
- 活动报名人员列表（组织者）
- 拒绝报名（组织者）
- 活动数据统计（组织者）
"""
from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.registration_service import RegistrationService

bp = Blueprint('Registrations', __name__)

# ========== 普通用户接口 ==========
@bp.post('/activities/<int:activity_id>/register')
@require_auth()
@require_role('user')
def register_activity(activity_id):
    """
    报名活动（普通用户）
    
    用户报名参加指定活动
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Returns:
        - registration_id: 报名记录ID
        - status: 报名状态
        - remaining_slots: 剩余名额
    
    Raises:
        400: 活动不可报名、报名已截止、名额已满、重复报名、被拒绝冷却中等
        404: 活动不存在
    """
    try:
        result = RegistrationService.register(g.current_user_id, activity_id)
        return success(result, message='报名成功')
    except BusinessError as e:
        return e.to_response()


@bp.delete('/activities/<int:activity_id>/register')
@require_auth()
@require_role('user')
def cancel_registration(activity_id):
    """
    取消报名（普通用户）
    
    取消对指定活动的报名
    取消后名额不会立即释放，有2分钟延迟释放（给用户反悔机会）
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Returns:
        - release_time: 名额释放时间
    
    Raises:
        400: 取消报名已截止、尚未报名
        404: 活动不存在
    """
    try:
        result = RegistrationService.cancel(g.current_user_id, activity_id)
        return success(result, message='取消报名成功，名额将在2分钟后释放')
    except BusinessError as e:
        return e.to_response()


@bp.get('/user/registrations')
@require_auth()
@require_role('user')
def get_my_registrations():
    """
    获取我的报名列表（普通用户）
    
    返回当前用户的有效报名记录（registered/re_registered）
    支持分页和多条件筛选
    
    Query Parameters:
        - page (int): 页码（默认1）
        - page_size (int): 每页数量（默认20，最大100）
        - name (str): 活动名称筛选（模糊匹配）
        - activity_id (int): 活动ID筛选
        - category_id (int): 分类ID筛选
        - start_date (str): 开始日期筛选（格式：YYYY-MM-DD）
        - campus (str): 校区筛选
    
    Returns:
        - total: 总记录数
        - page: 当前页码
        - page_size: 每页数量
        - list: 报名列表
            - registration_id: 报名记录ID
            - activity_id: 活动ID
            - activity_name: 活动名称
            - start_time: 开始时间
            - end_time: 结束时间
            - location: 地点
            - registration_time: 报名时间
            - status: 报名状态
            - checkin_status: 签到状态（checked/not_checked）
            - checkin_time: 签到时间（如已签到）
    """
    params = request.args.to_dict()
    result = RegistrationService.get_my_registrations(g.current_user_id, params)
    return success(result)

# ========== 组织者接口 ==========
@bp.get('/organizer/activities/<int:activity_id>/registrations')
@require_auth()
@require_role('organizer')
def get_activity_registrations(activity_id):
    """
    获取活动报名人员列表（组织者）
    
    返回指定活动的报名人员信息，包含签到情况和统计数据
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Query Parameters:
        - page (int): 页码（默认1）
        - page_size (int): 每页数量（默认20，最大100）
        - gender (str): 性别筛选
        - college (str): 学院筛选
        - grade (str): 年级筛选
        - major (str): 专业筛选
    
    Returns:
        - total: 总记录数
        - statistics: 统计数据
            - total_registered: 总报名人数
            - total_checked: 已签到人数
            - remaining_slots: 剩余名额
            - by_gender: 性别分布
            - by_college: 学院分布
            - by_grade: 年级分布
            - by_major: 专业分布
        - list: 报名人员列表
            - registration_id: 报名记录ID
            - user_id: 用户ID
            - student_id: 学号
            - gender: 性别
            - college: 学院
            - major: 专业
            - grade: 年级
            - registration_time: 报名时间
            - status: 状态
            - reject_reason: 拒绝原因
            - checkin_status: 签到状态
    """
    params = request.args.to_dict()
    result = RegistrationService.get_activity_registrations(g.current_user_id, activity_id, params)
    return success(result)


@bp.post('/organizer/registrations/<int:registration_id>/reject')
@require_auth()
@require_role('organizer')
def reject_registration(registration_id):
    """
    拒绝报名（组织者）
    
    拒绝某用户的报名申请
    
    拒绝规则：
    - 第1次拒绝：状态变为 rejected（可再次报名，但有10分钟冷却）
    - 第2次拒绝：状态变为 blocked（永久禁止报名该活动）
    
    Path Parameters:
        - registration_id (int): 报名记录ID
    
    Request Body:
        - reason (str): 拒绝原因
    
    Returns:
        - new_status: 新状态（rejected/blocked）
        - reject_count: 拒绝次数
    
    Raises:
        400: 未填写拒绝原因、该用户没有有效报名
        403: 无权操作（不是自己的活动）
        404: 报名记录不存在
    """
    data = get_json_data()
    reason = data.get('reason', '').strip()
    if not reason:
        raise BusinessError('请填写拒绝原因', code=400)
    try:
        result = RegistrationService.reject_registration(g.current_user_id, registration_id, reason)
        return success(result, message='已拒绝该用户报名')
    except BusinessError as e:
        return e.to_response()


@bp.get('/activities/<int:activity_id>/registration-stats')
@require_auth()
@require_role('organizer')
def get_registration_stats(activity_id):
    """
    获取活动数据统计（组织者）
    
    返回报名人数统计、签到人数、剩余名额、人员分布等
    与上面的 get_activity_registrations 接口共用统计逻辑
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Returns:
        - total_registered: 总报名人数
        - remaining_slots: 剩余名额
        - total_checked: 已签到人数
        - by_gender: 性别分布
        - by_college: 学院分布
        - by_grade: 年级分布
        - by_major: 专业分布
    """
    result = RegistrationService.get_registration_stats(g.current_user_id, activity_id)
    return success(result)