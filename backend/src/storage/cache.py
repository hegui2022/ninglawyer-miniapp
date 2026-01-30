"""
缓存管理
"""
import redis
import json
import os
from typing import Any, Optional, List
from functools import wraps
from loguru import logger


class Cache:
    """Redis 缓存类"""
    
    def __init__(self):
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.db = int(os.getenv('REDIS_DB', 0))
        
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True
        )
        
        # 测试连接
        try:
            self.client.ping()
            logger.info("Redis 连接成功")
        except Exception as e:
            logger.warning(f"Redis 连接失败: {e}")
    
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """设置缓存"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            self.client.setex(key, expire, value)
            return True
        except Exception as e:
            logger.error(f"设置缓存失败: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        try:
            value = self.client.get(key)
            if value is None:
                return None
            # 尝试解析 JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except Exception as e:
            logger.error(f"获取缓存失败: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"删除缓存失败: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"检查缓存失败: {e}")
            return False
    
    def mget(self, keys: List[str]) -> List[Any]:
        """批量获取缓存"""
        try:
            values = self.client.mget(keys)
            result = []
            for value in values:
                if value is None:
                    result.append(None)
                else:
                    try:
                        result.append(json.loads(value))
                    except json.JSONDecodeError:
                        result.append(value)
            return result
        except Exception as e:
            logger.error(f"批量获取缓存失败: {e}")
            return [None] * len(keys)
    
    def mset(self, mapping: dict, expire: int = 3600) -> bool:
        """批量设置缓存"""
        try:
            pipe = self.client.pipeline()
            for key, value in mapping.items():
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                pipe.setex(key, expire, value)
            pipe.execute()
            return True
        except Exception as e:
            logger.error(f"批量设置缓存失败: {e}")
            return False
    
    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """递增计数"""
        try:
            return self.client.incrby(key, amount)
        except Exception as e:
            logger.error(f"递增计数失败: {e}")
            return None
    
    def decr(self, key: str, amount: int = 1) -> Optional[int]:
        """递减计数"""
        try:
            return self.client.decrby(key, amount)
        except Exception as e:
            logger.error(f"递减计数失败: {e}")
            return None
    
    def expire(self, key: str, seconds: int) -> bool:
        """设置过期时间"""
        try:
            return self.client.expire(key, seconds)
        except Exception as e:
            logger.error(f"设置过期时间失败: {e}")
            return False
    
    def ttl(self, key: str) -> Optional[int]:
        """获取剩余时间"""
        try:
            return self.client.ttl(key)
        except Exception as e:
            logger.error(f"获取剩余时间失败: {e}")
            return None
    
    def flush_pattern(self, pattern: str) -> bool:
        """批量删除匹配模式的缓存"""
        try:
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"批量删除缓存失败: {e}")
            return False


# 全局缓存实例
_cache = None


def get_cache() -> Cache:
    """获取缓存实例"""
    global _cache
    if _cache is None:
        _cache = Cache()
    return _cache


def cache_result(key_prefix: str, expire: int = 3600):
    """
    缓存结果装饰器
    
    Args:
        key_prefix: 缓存键前缀
        expire: 过期时间（秒）
    
    Usage:
        @cache_result('user_info', 300)
        def get_user_info(user_id):
            return ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key_prefix}:{str(args)}:{str(kwargs)}"
            
            # 尝试从缓存获取
            cache = get_cache()
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.info(f"缓存命中: {cache_key}")
                return cached_value
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 设置缓存
            cache.set(cache_key, result, expire)
            
            return result
        return wrapper
    return decorator

