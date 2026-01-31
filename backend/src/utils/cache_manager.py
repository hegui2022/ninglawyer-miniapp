"""
缓存管理
使用Redis实现多级缓存策略
"""

import json
import time
from typing import Any, Optional, Callable
from loguru import logger

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("⚠️ Redis未安装，缓存功能将不可用")


class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        self.redis_client = None
        self.cache_prefix = "legal_assistant:"
        self.default_ttl = 3600  # 默认缓存时间1小时
        
        self._init_redis()
    
    def _init_redis(self):
        """初始化Redis客户端"""
        if not REDIS_AVAILABLE:
            return
        
        try:
            import os
            
            redis_host = os.getenv('REDIS_HOST', 'localhost')
            redis_port = int(os.getenv('REDIS_PORT', 6379))
            redis_password = os.getenv('REDIS_PASSWORD', None)
            redis_db = int(os.getenv('REDIS_DB', 0))
            
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                db=redis_db,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            
            # 测试连接
            self.redis_client.ping()
            logger.info(f"✅ Redis连接成功: {redis_host}:{redis_port}")
        
        except Exception as e:
            logger.error(f"❌ Redis连接失败: {e}")
            self.redis_client = None
    
    def is_available(self) -> bool:
        """
        检查缓存是否可用
        
        Returns:
            是否可用
        """
        return self.redis_client is not None
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            key: 缓存键
        
        Returns:
            缓存值，不存在返回None
        """
        if not self.is_available():
            return None
        
        try:
            full_key = self._get_full_key(key)
            value = self.redis_client.get(full_key)
            
            if value is not None:
                # 尝试解析JSON
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            
            return None
        
        except Exception as e:
            logger.error(f"❌ 获取缓存失败: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 缓存时间（秒），None表示使用默认值
        
        Returns:
            是否成功
        """
        if not self.is_available():
            return False
        
        try:
            full_key = self._get_full_key(key)
            
            # 序列化值
            if not isinstance(value, (str, int, float, bool)):
                value = json.dumps(value, ensure_ascii=False)
            
            # 设置缓存
            cache_ttl = ttl if ttl is not None else self.default_ttl
            self.redis_client.setex(full_key, cache_ttl, value)
            
            return True
        
        except Exception as e:
            logger.error(f"❌ 设置缓存失败: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        删除缓存
        
        Args:
            key: 缓存键
        
        Returns:
            是否成功
        """
        if not self.is_available():
            return False
        
        try:
            full_key = self._get_full_key(key)
            self.redis_client.delete(full_key)
            return True
        
        except Exception as e:
            logger.error(f"❌ 删除缓存失败: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> bool:
        """
        清除匹配模式的缓存
        
        Args:
            pattern: 匹配模式
        
        Returns:
            是否成功
        """
        if not self.is_available():
            return False
        
        try:
            full_pattern = self._get_full_key(pattern)
            keys = self.redis_client.keys(full_pattern)
            
            if keys:
                self.redis_client.delete(*keys)
                logger.info(f"✅ 清除缓存: {len(keys)}个")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ 清除缓存失败: {e}")
            return False
    
    def get_or_set(self, key: str, func: Callable, ttl: int = None) -> Any:
        """
        获取缓存，如果不存在则执行函数并缓存结果
        
        Args:
            key: 缓存键
            func: 函数
            ttl: 缓存时间（秒）
        
        Returns:
            缓存值或函数执行结果
        """
        # 尝试从缓存获取
        cached_value = self.get(key)
        if cached_value is not None:
            return cached_value
        
        # 执行函数
        start_time = time.time()
        value = func()
        exec_time = time.time() - start_time
        
        # 设置缓存
        self.set(key, value, ttl)
        logger.info(f"🔄 缓存未命中，执行函数: {key} (耗时: {exec_time:.2f}s)")
        
        return value
    
    def _get_full_key(self, key: str) -> str:
        """
        获取完整的缓存键
        
        Args:
            key: 原始键
        
        Returns:
            完整键
        """
        return f"{self.cache_prefix}{key}"


# 全局实例
cache_manager = CacheManager()
