from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.checkin_service import CheckinService

bp = Blueprint('checkin', __name__)


@bp.get('/organizer/activities/<int:activity_id>/checkin-code')
@require_auth()
@require_role('organizer')
def get_checkin_code(activity_id):
    """获取签到码（组织者）"""
    result = CheckinService.get_checkin_code(g.current_user_id, activity_id)
    return success(result)


@bp.post('/activities/<int:activity_id>/checkin')
@require_auth()
@require_role('user')
def checkin(activity_id):
    """签到码（普通用户）"""
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
    """手动签到（组织者）"""
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
    """获取我的签到记录"""
    params = request.args.to_dict()
    result = CheckinService.get_my_checkins(g.current_user_id, params)
    return success(result)


@bp.get('/organizer/activities/<int:activity_id>/checkins')
@require_auth()
@require_role('organizer')
def get_checkin_stats(activity_id):
    """获取活动签到情况（组织者）"""
    result = CheckinService.get_checkin_stats(g.current_user_id, activity_id)
    return success(result)