"""
API 限流中间件
"""
from flask import request, jsonify
from functools import wraps
from loguru import logger
from collections import defaultdict
import time

from config.rate_limit_config import rate_limit_config


class RateLimiter:
    """API 限流器"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.rules = rate_limit_config.DEFAULT_RULES
    
    def is_allowed(self, key: str, rule_name: str = 'default') -> tuple[bool, dict]:
        """
        检查是否允许请求
        
        Args:
            key: 限流键（通常是用户ID或IP地址）
            rule_name: 规则名称
        
        Returns:
            (是否允许, 限制信息)
        """
        rule = self.rules.get(rule_name, self.rules['default'])
        max_requests = rule['max_requests']
        window = rule['window']
        
        now = time.time()
        cutoff = now - window
        
        # 清理过期记录
        self.requests[key] = [t for t in self.requests[key] if t > cutoff]
        
        # 检查是否超过限制
        request_count = len(self.requests[key])
        
        if request_count >= max_requests:
            return False, {
                'max_requests': max_requests,
                'window': window,
                'current_requests': request_count,
                'retry_after': int(self.requests[key][0] - cutoff) + 1
            }
        
        # 记录请求
        self.requests[key].append(now)
        
        return True, {
            'max_requests': max_requests,
            'window': window,
            'current_requests': request_count + 1,
            'remaining': max_requests - request_count - 1
        }
    
    def reset(self, key: str):
        """重置限流"""
        if key in self.requests:
            del self.requests[key]


# 全局限流器实例
_rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """获取限流器实例"""
    return _rate_limiter


def rate_limit(rule_name: str = 'default'):
    """
    限流装饰器
    
    Args:
        rule_name: 限流规则名称
    
    Usage:
        @rate_limit('login')
        def login():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 检查是否启用限流
            if not rate_limit_config.ENABLED:
                return f(*args, **kwargs)
            
            # 获取限流键（优先使用用户ID，否则使用IP地址）
            from src.api.user import get_current_user
            
            try:
                user_id = get_current_user()
                key = f"user:{user_id}"
            except:
                key = f"ip:{request.remote_addr}"
            
            # 检查是否允许请求
            limiter = get_rate_limiter()
            allowed, info = limiter.is_allowed(key, rule_name)
            
            if not allowed:
                logger.warning(f"限流触发: key={key}, rule={rule_name}")
                
                response = jsonify({
                    'success': False,
                    'error': '请求过于频繁，请稍后再试',
                    'error_code': 'RATE_LIMIT_EXCEEDED',
                    'retry_after': info.get('retry_after', 60)
                })
                
                response.headers['X-RateLimit-Limit'] = str(info['max_requests'])
                response.headers['X-RateLimit-Remaining'] = '0'
                response.headers['X-RateLimit-Reset'] = str(info['retry_after'])
                
                return response, 429
            
            # 添加限流信息到响应头
            response = f(*args, **kwargs)
            
            if hasattr(response, 'headers'):
                response.headers['X-RateLimit-Limit'] = str(info['max_requests'])
                response.headers['X-RateLimit-Remaining'] = str(info['remaining'])
            
            return response
        
        return decorated_function
    return decorator
