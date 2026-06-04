"""
JWT 认证模块

提供 JSON Web Token (JWT) 的创建和解析功能
用于用户身份认证和授权
"""
import jwt
from flask import current_app
from datetime import datetime, timedelta

def create_token(role, user_id):
    """
    创建 JWT Token
    
    生成包含用户身份信息的加密 Token，用于后续请求的身份验证
    
    Token 载荷 (Payload) 包含：
    - role: 用户角色（user/organizer/admin）
    - user_id: 用户ID
    - exp: Token 过期时间（当前时间 + 2小时）
    
    Args:
        role (str): 用户角色
            - user: 普通用户
            - organizer: 组织者
            - admin: 管理员
        user_id (int): 用户ID
    
    Returns:
        str: JWT Token 字符串
    
    Example:
        >>> token = create_token('user', 123)
        >>> print(token)
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    """
    payload = {
        'role': role,
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def decode_token(token):
    """
    解析 JWT Token
    
    验证 Token 有效性并解析其中的用户信息
    
    流程：
    1. 使用密钥解密 Token
    2. 验证签名是否正确
    3. 检查是否过期
    
    Args:
        token (str): JWT Token 字符串
    
    Returns:
        dict or None: 解析成功返回 payload 字典，失败返回 None
            - role: 用户角色
            - user_id: 用户ID
            - exp: 过期时间戳
    
    Example:
        >>> payload = decode_token(token)
        >>> if payload:
        ...     print(f"用户 {payload['user_id']} 角色: {payload['role']}")
    
    Note:
        - ExpiredSignatureError: Token 已过期
        - InvalidTokenError: Token 无效（签名错误、格式错误等）
    """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None