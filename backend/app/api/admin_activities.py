"""
管理员活动审核 API 路由模块

提供管理员对活动的审核和管理功能：
- 获取待审核活动列表
- 获取活动详情（管理员视角）
- 审核活动（通过/拒绝）
- 下架活动
"""
from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.activity_service import ActivityService

bp = Blueprint('Admin_Activities', __name__)


@bp.get('/activities')
@require_auth()
@require_role('admin')
def list_review_activities():
    """
    获取待审核活动列表（管理员）
    
    默认显示 pending（待审核）和 edit_pending（修改待审核）状态的活动
    支持分页和多条件筛选
    
    Query Parameters:
        - page (int): 页码（默认1）
        - page_size (int): 每页数量（默认20，最大100）
        - status (str): 状态筛选（逗号分隔，如 pending,edit_pending）
        - keyword (str): 关键词搜索（活动名称）
        - organizer_id (int): 组织者ID筛选
        - category_id (int): 分类ID筛选
        - start_date (str): 开始日期（格式：YYYY-MM-DD）
    
    Returns:
        - total: 总记录数
        - page: 当前页码
        - page_size: 每页数量
        - list: 审核活动列表
            - activity_id: 活动ID
            - name: 活动名称
            - organizer_id: 组织者ID
            - organizer_name: 组织者名称
            - start_time: 开始时间
            - category_name: 分类名称
            - category_path: 分类路径
            - status: 活动状态
    """
    params = request.args.to_dict()
    result = ActivityService.list_review_activities(params)
    return success(result)

@bp.get('/activities/<int:activity_id>')
@require_auth()
@require_role('admin')
def get_admin_activity_detail(activity_id):
    """
    获取活动详情（管理员视角）
    
    管理员可以看到更多信息：
    - edit_pending 状态时可以看到待审核的修改内容
    - 可以看到组织者信息
    - 可以看到拒绝原因
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Returns:
        dict: 活动详细信息，包含组织者信息和审核状态
    """
    from app.api.deps import get_current_user
    role, user_id = get_current_user()
    result = ActivityService.get_detail(activity_id, role, user_id)
    return success(result)

@bp.put('/activities/<int:activity_id>/review')
@require_auth()
@require_role('admin')
def review_activity(activity_id):
    """
    审核活动（管理员）
    
    对 pending（待审核）或 edit_pending（修改待审核）状态的活动进行审核
    
    审核通过：
    - 新活动：状态变为 open（报名中）
    - 修改审核：应用修改内容，状态恢复为之前的状态
    
    审核拒绝：
    - 新活动：状态变为 rejected（已拒绝）
    - 修改审核：丢弃修改内容，活动恢复原状
    
    审核结果会通过通知系统发送给组织者
    修改审核通过时，还会通知已报名用户活动已变更
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Request Body:
        - action (str): 审核动作
            - approve: 审核通过
            - reject: 审核拒绝
        - reject_reason (str): 拒绝原因（action为reject时必填）
    
    Returns:
        - activity_id: 活动ID
        - new_status: 审核后的活动状态
    
    Raises:
        400: action无效、拒绝时未填写原因、活动状态不可审核
        404: 活动不存在
    """
    data = get_json_data()
    action = data.get('action', '').strip()
    reject_reason = data.get('reject_reason', '').strip()
    if action not in ('approve', 'reject'):
        raise BusinessError('action无效', code=400)
    if action == 'reject' and not reject_reason:
        raise BusinessError('reject_reason必填', code=400)
    try:
        result = ActivityService.review_activity(activity_id, action, reject_reason)
        return success(result, message='审核通过' if action == 'approve' else '已拒绝')
    except BusinessError as e:
        return e.to_response()


@bp.put('/activities/<int:activity_id>/remove')
@require_auth()
@require_role('admin')
def remove_activity(activity_id):
    """
    下架活动（管理员）
    
    将活动状态改为 removed（已下架），删除所有报名和签到数据
    下架后会通知组织者和所有已报名用户
    
    限制：
    - 活动开始后不可下架
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Request Body:
        - reason (str): 下架原因（必填）
    
    Returns:
        message: 下架成功提示
    
    Raises:
        400: 未填写下架原因、活动已开始
        404: 活动不存在
    """
    data = get_json_data()
    reason = data.get('reason', '').strip()
    if not reason:
        raise BusinessError('请填写下架原因', code=400)
    try:
        ActivityService.remove_activity(activity_id, reason)
        return success(None, message='活动已下架，已通知发布者和所有报名用户')
    except BusinessError as e:
        return e.to_response()