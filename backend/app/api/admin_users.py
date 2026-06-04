"""
管理员用户管理 API 路由模块

提供管理员对用户、组织者、管理员的管理功能：
- 用户管理（列表查询、详情查看）
- 组织者管理（列表查询、详情查看、审核）
- 管理员管理（创建、列表查询、删除）

权限说明：
- 普通管理员：可查看用户和组织者信息
- 超级管理员：可创建和删除管理员
"""

from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.user_service import UserService

bp = Blueprint('Admin_Users', __name__)

# ========== 用户管理 ==========
@bp.get('/users')
@require_auth()
@require_role('admin')
def list_users():
    """
    获取用户列表（管理员）
    
    支持分页和筛选
    
    Query Parameters:
        - page (int): 页码（默认1）
        - page_size (int): 每页数量（默认20，最大100）
        - student_id (str): 学号筛选（模糊匹配）
        - college (str): 学院筛选（模糊匹配）
    
    Returns:
        - total: 总记录数
        - page: 当前页码
        - page_size: 每页数量
        - list: 用户列表
            - user_id: 用户ID
            - student_id: 学号
            - email: 邮箱
            - college: 学院
            - major: 专业
            - grade: 年级
            - status: 状态
    """
    params = request.args.to_dict()
    result = UserService.list_users(params)
    return success(result)


@bp.get('/users/<int:user_id>')
@require_auth()
@require_role('admin')
def get_user_detail(user_id):
    """
    获取单个普通用户详细信息（管理员）
    
    Path Parameters:
        - user_id (int): 用户ID
    
    Returns:
        - user_id: 用户ID
        - student_id: 学号
        - email: 邮箱
        - gender: 性别
        - college: 学院
        - major: 专业
        - grade: 年级
        - status: 状态
    """
    result = UserService.get_user_detail(user_id)
    return success(result)

# ========== 组织者管理 ==========
@bp.get('/organizers')
@require_auth()
@require_role('admin')
def list_organizers():
    """
    获取组织者列表（管理员）
    
    支持分页和筛选
    
    Query Parameters:
        - page (int): 页码（默认1）
        - page_size (int): 每页数量（默认20，最大100）
        - org_name (str): 组织名称筛选（模糊匹配）
        - status (str): 状态筛选
            - pending: 待审核
            - approved: 已通过
            - rejected: 已拒绝
    
    Returns:
        - total: 总记录数
        - page: 当前页码
        - page_size: 每页数量
        - list: 组织者列表
            - organizer_id: 组织者ID
            - email: 邮箱
            - org_name: 组织名称
            - status: 状态
    """
    params = request.args.to_dict()
    result = UserService.list_organizers(params)
    return success(result)


@bp.get('/organizers/<int:organizer_id>')
@require_auth()
@require_role('admin')
def get_organizer_detail(organizer_id):
    """
    获取单个组织者详细信息（管理员）
    
    包含组织证明和审核状态
    
    Path Parameters:
        - organizer_id (int): 组织者ID
    
    Returns:
        - organizer_id: 组织者ID
        - email: 邮箱
        - org_name: 组织名称
        - org_proof_text: 组织证明文本
        - org_proof_image: 组织证明图片URL
        - status: 状态
        - avatar: 头像
        - reject_reason: 拒绝原因
    """
    result = UserService.get_organizer_detail(organizer_id)
    return success(result)


@bp.put('/organizers/<int:organizer_id>/review')
@require_auth()
@require_role('admin')
def review_organizer(organizer_id):
    """
    审核组织者（管理员）
    
    对新注册的组织者进行资质审核
    
    Path Parameters:
        - organizer_id (int): 组织者ID
    
    Request Body:
        - action (str): 审核动作
            - approve: 审核通过
            - reject: 审核拒绝
        - reject_reason (str): 拒绝原因（action为reject时必填）
    
    Returns:
        - organizer_id: 组织者ID
        - status: 新状态
    
    Raises:
        400: action无效、拒绝时未填写原因
    """
    data = get_json_data()
    action = data.get('action', '').strip()
    reject_reason = data.get('reject_reason', '').strip()
    if action not in ('approve', 'reject'):
        raise BusinessError('action无效', code=400)
    if action == 'reject' and not reject_reason:
        raise BusinessError('reject_reason必填', code=400)
    result = UserService.review_organizer(organizer_id, action, reject_reason)
    return success(result, message='审核完成')

# ========== 管理员管理（超级管理员专用）==========
@bp.post('/admins')
@require_auth()
@require_role('admin')
def create_admin():
    """
    创建管理员（需要超级管理员权限）
    
    自动生成6位管理员编号
    
    Request Body:
        - email (str): 邮箱
        - password (str): 密码
        - username (str): 管理员名称
        - role (str): 角色（admin/super_admin）
    
    Returns:
        - admin_id: 管理员ID
        - admin_no: 管理员编号（6位）
    
    Raises:
        403: 不是超级管理员
        400: 邮箱已存在、参数无效
    """
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
    """
    获取管理员列表
    
    返回所有管理员信息（排除已删除的）
    
    Returns:
        list: 管理员列表
            - admin_id: 管理员ID
            - admin_no: 管理员编号
            - email: 邮箱
            - username: 名称
            - role: 角色
            - status: 状态
    """
    result = UserService.list_admins()
    return success(result)


@bp.delete('/admins/<int:admin_id>')
@require_auth()
@require_role('admin')
def delete_admin(admin_id):
    """
    删除管理员（需要超级管理员权限）
    
    软删除，将管理员状态设为 deleted
    
    限制：
    - 超级管理员不可删除
    
    Path Parameters:
        - admin_id (int): 要删除的管理员ID
    
    Returns:
        message: 删除成功提示
    
    Raises:
        403: 不是超级管理员、不能删除超级管理员
        404: 管理员不存在
    """
    try:
        UserService.delete_admin(g.current_user_id, admin_id)
        return success(None, message='管理员已删除')
    except BusinessError as e:
        return e.to_response()