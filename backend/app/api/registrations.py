from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.registration_service import RegistrationService

bp = Blueprint('Registrations', __name__)


@bp.post('/activities/<int:activity_id>/register')
@require_auth()
@require_role('user')
def register_activity(activity_id):
    """报名活动 """
    try:
        result = RegistrationService.register(g.current_user_id, activity_id)
        return success(result, message='报名成功')
    except BusinessError as e:
        return e.to_response()


@bp.delete('/activities/<int:activity_id>/register')
@require_auth()
@require_role('user')
def cancel_registration(activity_id):
    """取消报名 """
    try:
        result = RegistrationService.cancel(g.current_user_id, activity_id)
        return success(result, message='取消报名成功，名额将在2分钟后释放')
    except BusinessError as e:
        return e.to_response()


@bp.get('/user/registrations')
@require_auth()
@require_role('user')
def get_my_registrations():
    """获取我的报名列表 """
    params = request.args.to_dict()
    result = RegistrationService.get_my_registrations(g.current_user_id, params)
    return success(result)


@bp.get('/organizer/activities/<int:activity_id>/registrations')
@require_auth()
@require_role('organizer')
def get_activity_registrations(activity_id):
    """获取活动报名人员列表（组织者）"""
    params = request.args.to_dict()
    result = RegistrationService.get_activity_registrations(g.current_user_id, activity_id, params)
    return success(result)


@bp.post('/organizer/registrations/<int:registration_id>/reject')
@require_auth()
@require_role('organizer')
def reject_registration(registration_id):
    """拒绝报名（组织者） """
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
    """获取活动数据统计（组织者） - 接口文档 5.6"""
    result = RegistrationService.get_registration_stats(g.current_user_id, activity_id)
    return success(result)