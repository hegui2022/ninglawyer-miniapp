"""
统一异常处理中间件
"""

from flask import jsonify, request
from loguru import logger
import traceback
from typing import Any


class APIError(Exception):
    """API错误基类"""
    
    def __init__(self, message: str, status_code: int = 400, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or f"ERROR_{status_code}"


class ValidationError(APIError):
    """验证错误"""
    def __init__(self, message: str):
        super().__init__(message, 400, "VALIDATION_ERROR")


class AuthenticationError(APIError):
    """认证错误"""
    def __init__(self, message: str = "认证失败"):
        super().__init__(message, 401, "AUTHENTICATION_ERROR")


class AuthorizationError(APIError):
    """授权错误"""
    def __init__(self, message: str = "无权访问"):
        super().__init__(message, 403, "AUTHORIZATION_ERROR")


class NotFoundError(APIError):
    """资源不存在错误"""
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, 404, "NOT_FOUND_ERROR")


class ConflictError(APIError):
    """冲突错误"""
    def __init__(self, message: str = "资源冲突"):
        super().__init__(message, 409, "CONFLICT_ERROR")


class InternalServerError(APIError):
    """服务器内部错误"""
    def __init__(self, message: str = "服务器内部错误"):
        super().__init__(message, 500, "INTERNAL_SERVER_ERROR")


def init_error_handlers(app):
    """
    注册错误处理器
    
    Args:
        app: Flask应用实例
    """
    
    @app.errorhandler(APIError)
    def handle_api_error(error: APIError):
        """处理API错误"""
        return jsonify({
            'success': False,
            'error': error.message,
            'error_code': error.error_code
        }), error.status_code
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """处理400错误"""
        return jsonify({
            'success': False,
            'error': '请求参数错误',
            'error_code': 'BAD_REQUEST'
        }), 400
    
    @app.errorhandler(401)
    def handle_unauthorized(error):
        """处理401错误"""
        return jsonify({
            'success': False,
            'error': '未授权，请重新登录',
            'error_code': 'UNAUTHORIZED'
        }), 401
    
    @app.errorhandler(403)
    def handle_forbidden(error):
        """处理403错误"""
        return jsonify({
            'success': False,
            'error': '无权访问',
            'error_code': 'FORBIDDEN'
        }), 403
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """处理404错误"""
        return jsonify({
            'success': False,
            'error': '请求的资源不存在',
            'error_code': 'NOT_FOUND'
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """处理405错误"""
        return jsonify({
            'success': False,
            'error': '请求方法不允许',
            'error_code': 'METHOD_NOT_ALLOWED'
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_server_error(error):
        """处理500错误"""
        logger.error(f"500错误：{str(error)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': '服务器内部错误，请稍后重试',
            'error_code': 'INTERNAL_SERVER_ERROR'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """处理未预期的错误"""
        logger.error(f"未预期的错误：{str(error)}")
        logger.error(traceback.format_exc())
        
        # 记录请求信息
        logger.error(f"请求路径：{request.method} {request.path}")
        logger.error(f"请求参数：{dict(request.form)}")
        
        return jsonify({
            'success': False,
            'error': '服务器发生未知错误，请稍后重试',
            'error_code': 'UNKNOWN_ERROR'
        }), 500


def log_request(response):
    """记录请求日志"""
    try:
        logger.info(f"{request.method} {request.path} - {response.status_code}")
    except Exception as e:
        logger.error(f"记录请求日志失败：{str(e)}")
    return response


def setup_logging(app):
    """
    设置日志系统
    
    Args:
        app: Flask应用实例
    """
    # 配置Loguru
    logger.remove()  # 移除默认的handler
    
    # 控制台输出
    logger.add(
        sink=lambda msg: print(msg, end=''),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # 文件输出 - 一般日志
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO"
    )
    
    # 文件输出 - 错误日志
    logger.add(
        "logs/error.log",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR"
    )
    
    # 注册请求日志处理器
    app.after_request(log_request)
    
    logger.info("日志系统初始化完成")
