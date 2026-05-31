from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.activity_service import ActivityService

bp = Blueprint('admin_activities', __name__)


@bp.get('/activities')
@require_auth()
@require_role('admin')
def list_review_activities():
    """获取审核活动列表 """
    params = request.args.to_dict()
    result = ActivityService.list_review_activities(params)
    return success(result)

@bp.get('/activities/<int:activity_id>')
@require_auth()
@require_role('admin')
def get_admin_activity_detail(activity_id):
    """获取活动详情（管理员）"""
    from app.api.deps import get_current_user
    role, user_id = get_current_user()
    result = ActivityService.get_detail(activity_id, role, user_id)
    return success(result)

@bp.put('/activities/<int:activity_id>/review')
@require_auth()
@require_role('admin')
def review_activity(activity_id):
    """审核活动 """
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
    """下架活动 """
    data = get_json_data()
    reason = data.get('reason', '').strip()
    if not reason:
        raise BusinessError('请填写下架原因', code=400)
    try:
        ActivityService.remove_activity(activity_id, reason)
        return success(None, message='活动已下架，已通知发布者和所有报名用户')
    except BusinessError as e:
        return e.to_response()