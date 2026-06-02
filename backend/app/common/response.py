from flask import jsonify


def success(data=None, message='成功', code=200):
    """统一成功响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': data
    }), code