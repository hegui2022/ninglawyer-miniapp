"""
日志工具
"""

from loguru import logger
from functools import wraps
import time
import json


def setup_logger(log_file: str = None, level: str = "INFO"):
    """
    设置日志
    
    Args:
        log_file: 日志文件路径
        level: 日志级别
    """
    if log_file:
        logger.add(
            log_file,
            rotation="500 MB",
            retention="10 days",
            level=level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
        )


def log_function_call(func):
    """
    函数调用日志装饰器
    
    Args:
        func: 被装饰的函数
    
    Returns:
        装饰后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.info(f"调用函数: {func_name}, 参数: args={args}, kwargs={kwargs}")
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"函数 {func_name} 执行成功, 耗时: {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"函数 {func_name} 执行失败, 耗时: {duration:.2f}s, 错误: {str(e)}")
            raise
    
    return wrapper


def log_api_request(func):
    """
    API 请求日志装饰器
    
    Args:
        func: 被装饰的函数
    
    Returns:
        装饰后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 获取请求数据
        request_data = {}
        if kwargs.get('request'):
            request = kwargs['request']
            request_data = {
                'method': request.method,
                'path': request.path,
                'remote_addr': request.remote_addr,
                'user_agent': request.headers.get('User-Agent', '')
            }
        
        logger.info(f"API 请求: {json.dumps(request_data)}")
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"API 请求成功, 耗时: {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"API 请求失败, 耗时: {duration:.2f}s, 错误: {str(e)}")
            raise
    
    return wrapper


def log_error(error: Exception, context: dict = None):
    """
    记录错误日志
    
    Args:
        error: 错误对象
        context: 上下文信息
    """
    error_info = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'context': context or {}
    }
    logger.error(f"错误发生: {json.dumps(error_info, ensure_ascii=False)}")


def log_performance(metric_name: str, value: float, unit: str = "ms"):
    """
    记录性能指标
    
    Args:
        metric_name: 指标名称
        value: 指标值
        unit: 单位
    """
    logger.info(f"性能指标: {metric_name} = {value}{unit}")


def log_business_event(event_name: str, data: dict = None):
    """
    记录业务事件
    
    Args:
        event_name: 事件名称
        data: 事件数据
    """
    event_info = {
        'event': event_name,
        'data': data or {}
    }
    logger.info(f"业务事件: {json.dumps(event_info, ensure_ascii=False)}")
