"""
Sentry错误追踪配置
"""

import os
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from loguru import logger


def init_sentry():
    """
    初始化Sentry错误追踪
    """
    # 从环境变量获取Sentry DSN
    sentry_dsn = os.getenv('SENTRY_DSN')
    
    if not sentry_dsn:
        logger.info("未配置SENTRY_DSN，跳过Sentry初始化")
        return False
    
    # 获取环境配置
    environment = os.getenv('ENVIRONMENT', 'production')
    release = os.getenv('APP_VERSION', '1.0.0')
    
    # 配置Sentry
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=environment,
        release=release,
        
        # 集成
        integrations=[
            FlaskIntegration(),
            LoggingIntegration(
                level=logging.INFO,  # 捕获info及以上级别的日志
                event_level=logging.ERROR,  # 只发送error及以上级别的事件
            ),
            SqlalchemyIntegration(),
        ],
        
        # 采样率
        traces_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
        
        # 错误采样率
        error_sample_rate=float(os.getenv('SENTRY_ERROR_SAMPLE_RATE', '1.0')),
        
        # 过滤敏感信息
        before_send=before_send_filter,
        before_breadcrumb=before_breadcrumb_filter,
        
        # 自定义标签
        attach_stacktrace=True,
    )
    
    logger.info(f"Sentry初始化成功: environment={environment}, release={release}")
    return True


def before_send_filter(event, hint):
    """
    发送前过滤器 - 过滤敏感信息
    """
    # 移除敏感的请求头
    if 'request' in event and 'headers' in event['request']:
        headers = event['request']['headers']
        sensitive_headers = ['authorization', 'cookie', 'x-api-key', 'x-auth-token']
        for header in sensitive_headers:
            if header in headers:
                headers[header] = '[Filtered]'
    
    # 移除敏感的环境变量
    if 'extra' in event and 'env' in event['extra']:
        env = event['extra']['env']
        sensitive_keys = ['password', 'secret', 'key', 'token', 'database_url']
        for key in list(env.keys()):
            if any(s in key.lower() for s in sensitive_keys):
                env[key] = '[Filtered]'
    
    # 添加自定义标签
    event['tags'] = event.get('tags', {})
    event['tags']['app'] = 'ninglawyer'
    
    return event


def before_breadcrumb_filter(breadcrumb, hint):
    """
    面包屑过滤器 - 过滤敏感信息
    """
    # 过滤掉敏感的URL和查询参数
    if breadcrumb.get('type') == 'http':
        url = breadcrumb.get('data', {}).get('url', '')
        # 移除查询参数中的敏感信息
        if '?' in url:
            url = url.split('?')[0]
            breadcrumb['data']['url'] = url
    
    return breadcrumb


def set_user_context(user_id: int, openid: str = None, subscription_type: str = None):
    """
    设置用户上下文
    
    Args:
        user_id: 用户ID
        openid: 微信openid
        subscription_type: 订阅类型
    """
    user_data = {
        'id': str(user_id),
    }
    
    if openid:
        user_data['openid'] = openid
    
    if subscription_type:
        user_data['subscription'] = subscription_type
    
    sentry_sdk.set_user(user_data)


def add_context(key: str, value: dict):
    """
    添加自定义上下文
    
    Args:
        key: 上下文键
        value: 上下文值
    """
    sentry_sdk.set_context(key, value)


def add_tag(key: str, value: str):
    """
    添加自定义标签
    
    Args:
        key: 标签键
        value: 标签值
    """
    sentry_sdk.set_tag(key, value)


def capture_exception(exception: Exception, level: str = 'error', **kwargs):
    """
    捕获异常
    
    Args:
        exception: 异常对象
        level: 日志级别
        **kwargs: 额外的上下文信息
    """
    with sentry_sdk.push_scope() as scope:
        # 设置日志级别
        scope.set_level(level)
        
        # 添加额外的上下文
        for key, value in kwargs.items():
            scope.set_extra(key, value)
        
        # 捕获异常
        sentry_sdk.capture_exception(exception)


def capture_message(message: str, level: str = 'info', **kwargs):
    """
    捕获消息
    
    Args:
        message: 消息内容
        level: 日志级别
        **kwargs: 额外的上下文信息
    """
    with sentry_sdk.push_scope() as scope:
        # 设置日志级别
        scope.set_level(level)
        
        # 添加额外的上下文
        for key, value in kwargs.items():
            scope.set_extra(key, value)
        
        # 捕获消息
        sentry_sdk.capture_message(message)
