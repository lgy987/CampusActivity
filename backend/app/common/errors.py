"""
错误处理模块

提供自定义业务异常类和全局错误处理器：
- BusinessError: 业务异常类
- 全局错误处理：404、500 等 HTTP 异常
"""
from flask import jsonify
class BusinessError(Exception):
    """
    业务异常类
    
    用于在业务逻辑层抛出可预期的业务错误
    与系统异常（如数据库连接失败）区分开
    
    Attributes:
        message (str): 错误消息，返回给前端
        code (int): 业务错误码
        status_code (int): HTTP 状态码
    
    错误码说明:
        - 200: 成功（不用于错误）
        - 400: 参数错误、业务逻辑错误
        - 401: 未登录、token 失效
        - 403: 权限不足
        - 404: 资源不存在
        - 500: 服务器内部错误
    """

    def __init__(self, message, code=400, status_code=None):
        """
        初始化业务异常
        
        Args:
            message (str): 错误消息
            code (int): 业务错误码，默认 400
            status_code (int): HTTP 状态码，默认与 code 相同
        """
        self.message = message
        self.code = code
        self.status_code = status_code or code

    def to_response(self):
        """
        将异常转换为 HTTP 响应
        
        返回统一格式的错误响应
        
        Returns:
            tuple: (response, status_code)
                - response: JSON 格式的错误响应
                - status_code: HTTP 状态码
        
        """
        return jsonify({
            'code': self.code,
            'message': self.message,
            'data': None
        }), self.status_code


def register_error_handlers(app):
    """
    注册全局错误处理
    
    为 Flask 应用注册统一的错误处理器，确保所有错误返回一致的格式
    
    Args:
        app: Flask 应用实例
    
    处理的错误类型:
        1. BusinessError - 自定义业务异常
        2. 404 - 路由未找到
        3. 500 - 服务器内部错误
    
    """
    @app.errorhandler(BusinessError)
    def handle_business_error(e):
        """
        处理业务异常
        
        将 BusinessError 转换为统一格式的响应
        """
        return e.to_response()

    @app.errorhandler(404)
    def handle_not_found(e):
        """
        处理 404 错误
        
        当请求的资源不存在时返回统一格式
        """
        return jsonify({'code': 404, 'message': '资源不存在', 'data': None}), 404

    @app.errorhandler(500)
    def handle_server_error(e):
        """
        处理 500 错误
        
        当服务器内部错误时返回统一格式
        """
        return jsonify({'code': 500, 'message': '服务器内部错误', 'data': None}), 500
