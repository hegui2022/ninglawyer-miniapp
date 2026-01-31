"""
限流配置
"""

import os


class RateLimitConfig:
    """限流配置类"""
    
    # 是否启用限流
    ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    
    # 限流存储方式：memory（内存）或 redis（分布式）
    STORAGE = os.getenv('RATE_LIMIT_STORAGE', 'memory')
    
    # 默认限流规则
    DEFAULT_RULES = {
        'default': {
            'max_requests': int(os.getenv('RATE_LIMIT_DEFAULT_MAX', '60')),
            'window': int(os.getenv('RATE_LIMIT_DEFAULT_WINDOW', '60'))
        },
        'login': {
            'max_requests': int(os.getenv('RATE_LIMIT_LOGIN_MAX', '5')),
            'window': int(os.getenv('RATE_LIMIT_LOGIN_WINDOW', '60'))
        },
        'register': {
            'max_requests': int(os.getenv('RATE_LIMIT_REGISTER_MAX', '3')),
            'window': int(os.getenv('RATE_LIMIT_REGISTER_WINDOW', '60'))
        },
        'send_code': {
            'max_requests': int(os.getenv('RATE_LIMIT_SEND_CODE_MAX', '1')),
            'window': int(os.getenv('RATE_LIMIT_SEND_CODE_WINDOW', '60'))
        },
        'upload': {
            'max_requests': int(os.getenv('RATE_LIMIT_UPLOAD_MAX', '10')),
            'window': int(os.getenv('RATE_LIMIT_UPLOAD_WINDOW', '60'))
        },
        'query': {
            'max_requests': int(os.getenv('RATE_LIMIT_QUERY_MAX', '120')),
            'window': int(os.getenv('RATE_LIMIT_QUERY_WINDOW', '60'))
        },
        'chat': {
            'max_requests': int(os.getenv('RATE_LIMIT_CHAT_MAX', '30')),
            'window': int(os.getenv('RATE_LIMIT_CHAT_WINDOW', '60'))
        },
    }
    
    # Redis配置（用于分布式限流）
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    
    @classmethod
    def get_rule(cls, rule_name: str) -> dict:
        """获取限流规则"""
        return cls.DEFAULT_RULES.get(rule_name, cls.DEFAULT_RULES['default'])
    
    @classmethod
    def get_redis_url(cls) -> str:
        """获取Redis连接URL"""
        if cls.REDIS_PASSWORD:
            return f"redis://:{cls.REDIS_PASSWORD}@{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
        return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"


rate_limit_config = RateLimitConfig()
