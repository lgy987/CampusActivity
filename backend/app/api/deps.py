"""
API 依赖模块

提供 API 层通用的依赖注入和工具函数：
- JSON 数据获取与验证
- JWT Token 解析获取当前用户
- 登录验证装饰器
- 角色权限验证装饰器
"""
from functools import wraps
from flask import request, g
from app.common.auth import decode_token
from app.common.errors import BusinessError


def get_json_data():
    """
    获取并验证请求 JSON 数据
    
    从 Flask request 对象中提取 JSON 数据
    如果请求体为空或不是 JSON 格式，抛出异常
    
    Returns:
        dict: 解析后的 JSON 数据
    
    Raises:
        BusinessError: 请求体为空或不是有效 JSON
    
    """
    data = request.get_json(silent=True) or {}
    if not data:
        raise BusinessError('请求体不能为空', code=400)
    return data


def get_current_user():
    """
    从 Authorization Header 解析 Token，获取当前用户信息
    
    从请求头中提取 Bearer Token，解密后获取用户角色和ID
    
    Returns:
        tuple: (role, user_id)
            - role: 用户角色（user/organizer/admin），解析失败时返回 None
            - user_id: 用户ID，解析失败时返回 None
    """
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None, None

    token = auth_header.replace('Bearer ', '', 1).strip()
    payload = decode_token(token)
    if not payload:
        return None, None

    return payload.get('role'), payload.get('user_id')


def require_auth():
    """
    要求登录的装饰器
    
    验证请求是否携带有效的 JWT Token
    验证通过后，将用户信息存入 Flask 的 g 对象中
    
    Raises:
        BusinessError: 未登录或 Token 无效/过期（401）
    
    g 对象注入:
        - g.current_role: 当前用户角色
        - g.current_user_id: 当前用户ID
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            role, user_id = get_current_user()
            if not role or not user_id:
                raise BusinessError('未登录或token失效', code=401, status_code=401)
            g.current_role = role
            g.current_user_id = user_id
            return f(*args, **kwargs)
        return wrapper
    return decorator


def require_role(*allowed_roles):
    """
    要求特定角色的装饰器
    
    验证当前登录用户是否拥有指定角色之一
    必须在 @require_auth() 之后使用
    
    Args:
        *allowed_roles: 允许的角色列表
            - 'user': 普通用户
            - 'organizer': 组织者
            - 'admin': 管理员
    
    Raises:
        BusinessError: 未登录（401）或权限不足（403）
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            role = getattr(g, 'current_role', None)
            if not role:
                raise BusinessError('未登录', code=401, status_code=401)
            if role not in allowed_roles:
                raise BusinessError('权限不足', code=403, status_code=403)
            return f(*args, **kwargs)
        return wrapper
    return decorator