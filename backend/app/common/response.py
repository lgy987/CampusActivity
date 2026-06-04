"""
统一响应模块

提供统一的 API 成功响应格式
确保所有成功响应返回一致的数据结构
"""
from flask import jsonify


def success(data=None, message='success', code=200):
    """
    统一成功响应
    
    生成标准格式的成功响应，包含状态码、消息和数据
    
    Args:
        data: 响应数据，可以是 dict、list、str 等任意类型，默认为 None
        message (str): 响应消息，默认为 'success'
        code (int): 业务状态码，默认为 200
    
    Returns:
        tuple: (response, status_code)
            - response: JSON 格式的响应体
            - status_code: HTTP 状态码
     
    Note:
        此函数用于成功响应，错误响应请使用 BusinessError
    """
    return jsonify({
        'code': code,
        'message': message,
        'data': data
    }), code