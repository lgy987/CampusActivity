"""
签到 API 路由模块

提供签到管理相关的 API 接口：
- 获取签到码（组织者）
- 扫码签到（普通用户）
- 手动签到（组织者）
- 我的签到记录（普通用户）
- 签到统计（组织者）
"""
from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.checkin_service import CheckinService

bp = Blueprint('Checkin', __name__)


@bp.get('/organizer/activities/<int:activity_id>/checkin-code')
@require_auth()
@require_role('organizer')
def get_checkin_code(activity_id):
    """
    获取签到码（组织者）
    
    组织者可以在签到时间窗口内向用户展示签到码
    如果活动还没有签到码，会自动生成一个6位随机码
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Returns:
        - checkin_code: 6位签到码（大写字母+数字）
    
    Raises:
        403: 无权操作（不是自己的活动）
        404: 活动不存在
    """
    result = CheckinService.get_checkin_code(g.current_user_id, activity_id)
    return success(result)


@bp.post('/activities/<int:activity_id>/checkin')
@require_auth()
@require_role('user')
def checkin(activity_id):
    """
    扫码签到（普通用户）
    
    用户通过输入组织者提供的签到码完成签到
    
    签到时间窗口：
    - 开始时间：活动开始前30分钟
    - 结束时间：活动结束时间
    
    前置条件：
    - 用户必须已报名该活动
    - 用户未签到过
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Request Body:
        - checkin_code (str): 签到码（6位）
    
    Returns:
        - checkin_id: 签到记录ID
        - checkin_time: 签到时间
    
    Raises:
        400: 缺少签到码、签到码错误、签到未开始、签到已结束
        403: 未报名
    """
    data = get_json_data()
    checkin_code = data.get('checkin_code', '').strip()
    if not checkin_code:
        raise BusinessError('缺少签到码', code=400)
    try:
        result = CheckinService.checkin(g.current_user_id, activity_id, checkin_code)
        return success(result, message='签到成功')
    except BusinessError as e:
        return e.to_response()


@bp.post('/organizer/activities/<int:activity_id>/manual-checkin')
@require_auth()
@require_role('organizer')
def manual_checkin(activity_id):
    """
    手动签到（组织者）
    
    组织者通过输入用户学号帮助用户完成签到
    适用于扫码失败的场景
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Request Body:
        - student_id (str): 用户学号（10位）
    
    Returns:
        - user_id: 用户ID
        - checkin_time: 签到时间
    
    Raises:
        400: 缺少学号、用户未报名、已签到
        403: 无权操作（不是自己的活动）
        404: 活动不存在、用户不存在
    """
    data = get_json_data()
    student_id = data.get('student_id', '').strip()
    if not student_id:
        raise BusinessError('缺少学号', code=400)
    try:
        result = CheckinService.manual_checkin(g.current_user_id, activity_id, student_id)
        return success(result, message='签到成功')
    except BusinessError as e:
        return e.to_response()


@bp.get('/user/checkins')
@require_auth()
@require_role('user')
def get_my_checkins():
    """
    获取我的签到记录（普通用户）
    
    返回用户历史签到记录，按签到时间倒序
    
    Query Parameters:
        - page (int): 页码（默认1）
        - page_size (int): 每页数量（默认20，最大100）
    
    Returns:
        - total: 总记录数
        - list: 签到记录列表
            - activity_id: 活动ID
            - activity_name: 活动名称
            - activity_start_time: 活动开始时间
            - checkin_time: 签到时间
            - checkin_method: 签到方式（code/manual）
    """
    params = request.args.to_dict()
    result = CheckinService.get_my_checkins(g.current_user_id, params)
    return success(result)


@bp.get('/organizer/activities/<int:activity_id>/checkins')
@require_auth()
@require_role('organizer')
def get_checkin_stats(activity_id):
    """
    获取活动签到情况（组织者）
    
    返回活动的签到统计数据和详细列表
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Returns:
        - total_registered: 总报名人数
        - checked_in: 已签到人数
        - not_checked_in: 未签到人数
        - checkin_rate: 签到率（百分比）
        - checkin_list: 已签到用户列表
            - user_id: 用户ID
            - student_id: 学号
            - username: 用户名
            - college: 学院
            - major: 专业
            - grade: 年级
            - checkin_time: 签到时间
            - checkin_method: 签到方式
        - notCheckedIn: 未签到用户列表
            - user_id: 用户ID
            - student_id: 学号
            - username: 用户名
            - registration_time: 报名时间
    
    Raises:
        403: 无权操作（不是自己的活动）
        404: 活动不存在
    """
    result = CheckinService.get_checkin_stats(g.current_user_id, activity_id)
    return success(result)