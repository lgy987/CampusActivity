from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.activity_service import ActivityService

bp = Blueprint('Activities', __name__)


@bp.post('/organizer/activities')
@require_auth()
@require_role('organizer')
def create_activity():
    """创建活动（草稿）"""
    data = get_json_data()
    try:
        result = ActivityService.create_activity(g.current_user_id, data)
        return success(result, message='活动创建成功')
    except BusinessError as e:
        return e.to_response()


@bp.post('/organizer/activities/<int:activity_id>/submit')
@require_auth()
@require_role('organizer')
def submit_activity(activity_id):
    """提交审核 """
    try:
        result = ActivityService.submit_activity(g.current_user_id, activity_id)
        return success(result, message='已提交审核')
    except BusinessError as e:
        return e.to_response()


@bp.get('/activities')
def list_activities():
    """获取活动列表"""
    params = request.args.to_dict()
    result = ActivityService.list_activities(params)
    return success(result)


@bp.get('/activities/<int:activity_id>')
def get_activity_detail(activity_id):
    """获取活动详情 """
    # 尝试获取当前用户信息（可选）
    from app.api.deps import get_current_user
    role, user_id = get_current_user()
    result = ActivityService.get_detail(activity_id, role, user_id)
    return success(result)


@bp.put('/organizer/activities/<int:activity_id>')
@require_auth()
@require_role('organizer')
def update_activity(activity_id):
    """更新活动 """
    data = get_json_data()
    try:
        result = ActivityService.update_activity(g.current_user_id, activity_id, data)
        return success(result, message='活动更新成功')
    except BusinessError as e:
        return e.to_response()


@bp.delete('/organizer/activities/<int:activity_id>')
@require_auth()
@require_role('organizer')
def delete_activity(activity_id):
    """删除活动 """
    try:
        ActivityService.delete_activity(g.current_user_id, activity_id)
        return success(None, message='活动已删除，已通知所有报名用户')
    except BusinessError as e:
        return e.to_response()


@bp.get('/organizer/activities')
@require_auth()
@require_role('organizer')
def get_my_activities():
    """获取我发布的活动"""
    params = request.args.to_dict()
    result = ActivityService.get_my_activities(g.current_user_id, params)
    return success(result)