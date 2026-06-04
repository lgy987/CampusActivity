"""
用户 API 路由模块

提供用户资料管理相关的 API 接口：
- 获取当前用户信息
- 修改用户信息
- 修改头像
- 修改密码
- 注销账号

支持三种角色：普通用户、组织者、管理员
"""
from flask import Blueprint, request
from app.api.deps import get_json_data, require_auth, get_current_user
from app.common.response import success
from app.common.errors import BusinessError
from app.services.user_service import UserService

bp = Blueprint('User', __name__)


@bp.get('/profile')
@require_auth()
def get_profile():
    """
    获取当前用户信息
    
    根据当前登录用户的角色返回不同的信息：
    - 普通用户：返回用户基本信息 + 成就等级
    - 组织者：返回组织信息 + 审核状态
    - 管理员：返回管理员信息 + 角色权限
    
    Returns:
        dict: 用户资料信息
    """
    from flask import g
    result = UserService.get_profile(g.current_role, g.current_user_id)
    return success(result)


@bp.put('/profile')
@require_auth()
def update_profile():
    """
    修改用户信息
    
    支持修改的字段因角色而异：
    - 普通用户：username, gender, college, major, grade, phone, avatar
    - 组织者/管理员：仅支持 avatar
    
    Request Body:
        - username (str, optional): 用户名
        - gender (str, optional): 性别
        - college (str, optional): 学院
        - major (str, optional): 专业
        - grade (str, optional): 年级
        - phone (str, optional): 手机号（需校验格式）
        - avatar (str, optional): 头像URL
    
    Returns:
        message: 更新成功
    
    Raises:
        400: 手机号格式错误
        404: 用户不存在
    """
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
    """
    修改头像
    
    支持两种方式：
    1. 文件上传（multipart/form-data）：直接上传图片文件
    2. URL 方式（application/json）：提供图片URL
    
    图片上传限制：
    - 格式：jpg/png
    - 大小：不超过2MB
    
    Request (文件上传):
        - avatar (file): 头像图片文件
    
    Request (URL方式):
        {
            "avatar": "https://example.com/avatar.jpg"
        }
    
    Returns:
        - avatar_url: 头像URL
    
    Raises:
        400: 未上传文件、文件格式错误、文件大小超限
    """
    from flask import g
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
    """
    修改密码
    
    需要验证旧密码的正确性
    
    Request Body:
        - old_password (str): 旧密码
        - new_password (str): 新密码
        - confirm_password (str): 确认密码
    
    Returns:
        message: 密码重置成功
    
    Raises:
        400: 旧密码为空、新密码为空、两次密码不一致、旧密码错误
        404: 账号不存在
    """
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
    """
    注销账号
    
    软删除：仅将账号状态标记为 deleted，不物理删除数据
    
    限制：
    - 超级管理员账号不可注销
    - 注销后账号无法登录，但历史数据保留
    
    Request Body:
        - confirm (bool): 确认注销标志
    
    Returns:
        message: 账号已注销
    
    Raises:
        400: 未确认注销、超级管理员不可注销
        404: 账号不存在
    """
    from flask import g
    data = get_json_data()
    if not data.get('confirm'):
        raise BusinessError('请确认注销账号', code=400)
    try:
        UserService.delete_account(g.current_role, g.current_user_id)
        return success(None, message='账号已注销')
    except BusinessError as e:
        return e.to_response()