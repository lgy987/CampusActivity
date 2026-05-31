from flask import Blueprint, request
from app.api.deps import get_json_data, require_auth, get_current_user
from app.common.response import success
from app.common.errors import BusinessError
from app.services.user_service import UserService

bp = Blueprint('user', __name__)


@bp.get('/profile')
@require_auth()
def get_profile():
    """获取当前用户信息"""
    from flask import g
    result = UserService.get_profile(g.current_role, g.current_user_id)
    return success(result)


@bp.put('/profile')
@require_auth()
def update_profile():
    """修改用户信息"""
    from flask import g
    data = get_json_data()
    try:
        UserService.update_profile(g.current_role, g.current_user_id, data)
        return success(None, message='更新成功')
    except BusinessError as e:
        return e.to_response()


@bp.post('/avatar')
@require_auth()
def update_avatar():
    """修改头像"""
    from flask import g
    # 支持 multipart/form-data 和 JSON 两种方式
    if request.files.get('avatar'):
        file = request.files['avatar']
        avatar_url = UserService.upload_avatar(g.current_role, g.current_user_id, file)
    else:
        data = request.get_json(silent=True) or {}
        avatar_url = data.get('avatar', '').strip()
        if not avatar_url:
            raise BusinessError('请上传头像文件', code=400)
        UserService.update_avatar_url(g.current_role, g.current_user_id, avatar_url)
        avatar_url = avatar_url
    return success({'avatar_url': avatar_url}, message='头像更新成功')


@bp.post('/reset-password')
@require_auth()
def reset_password():
    """修改密码"""
    from flask import g
    data = get_json_data()
    old_password = data.get('old_password', '')  
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')
    if not old_password:
        raise BusinessError('请输入旧密码', code=400)
    if not new_password:
        raise BusinessError('new_password is required', code=400)
    if new_password != confirm_password:
        raise BusinessError('两次密码不一致', code=400)
    try:
        UserService.reset_password(g.current_role, g.current_user_id, old_password, new_password)
        return success(None, message='密码重置成功')
    except BusinessError as e:
        return e.to_response()


@bp.delete('/account')
@require_auth()
def delete_account():
    """注销账号"""
    from flask import g
    data = get_json_data()
    if not data.get('confirm'):
        raise BusinessError('请确认注销账号', code=400)
    try:
        UserService.delete_account(g.current_role, g.current_user_id)
        return success(None, message='账号已注销')
    except BusinessError as e:
        return e.to_response()