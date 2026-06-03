from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.user_service import UserService

bp = Blueprint('Admin_Users', __name__)


@bp.get('/users')
@require_auth()
@require_role('admin')
def list_users():
    """获取用户列表 """
    params = request.args.to_dict()
    result = UserService.list_users(params)
    return success(result)


@bp.get('/users/<int:user_id>')
@require_auth()
@require_role('admin')
def get_user_detail(user_id):
    """获取单个普通用户详细信息"""
    result = UserService.get_user_detail(user_id)
    return success(result)


@bp.get('/organizers')
@require_auth()
@require_role('admin')
def list_organizers():
    """获取组织者列表 """
    params = request.args.to_dict()
    result = UserService.list_organizers(params)
    return success(result)


@bp.get('/organizers/<int:organizer_id>')
@require_auth()
@require_role('admin')
def get_organizer_detail(organizer_id):
    """获取单个组织者详细信息 """
    result = UserService.get_organizer_detail(organizer_id)
    return success(result)


@bp.put('/organizers/<int:organizer_id>/review')
@require_auth()
@require_role('admin')
def review_organizer(organizer_id):
    """审核组织者 """
    data = get_json_data()
    action = data.get('action', '').strip()
    reject_reason = data.get('reject_reason', '').strip()
    if action not in ('approve', 'reject'):
        raise BusinessError('action无效', code=400)
    if action == 'reject' and not reject_reason:
        raise BusinessError('reject_reason必填', code=400)
    result = UserService.review_organizer(organizer_id, action, reject_reason)
    return success(result, message='审核完成')


@bp.post('/admins')
@require_auth()
@require_role('admin')
def create_admin():
    """创建管理员（超级管理员）"""
    data = get_json_data()
    try:
        result = UserService.create_admin(g.current_user_id, data)
        return success(result, message='管理员创建成功')
    except BusinessError as e:
        return e.to_response()


@bp.get('/admins')
@require_auth()
@require_role('admin')
def list_admins():
    """获取管理员列表 """
    result = UserService.list_admins()
    return success(result)


@bp.delete('/admins/<int:admin_id>')
@require_auth()
@require_role('admin')
def delete_admin(admin_id):
    """删除管理员（超级管理员）"""
    try:
        UserService.delete_admin(g.current_user_id, admin_id)
        return success(None, message='管理员已删除')
    except BusinessError as e:
        return e.to_response()