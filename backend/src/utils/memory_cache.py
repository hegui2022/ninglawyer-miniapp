"""
本地内存缓存
实现简单的LRU缓存策略
"""

import time
from typing import Any, Optional, Dict
from collections import OrderedDict
from loguru import logger


class MemoryCache:
    """本地内存缓存（LRU策略）"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        """
        初始化内存缓存
        
        Args:
            max_size: 最大缓存数量
            default_ttl: 默认缓存时间（秒）
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: OrderedDict = OrderedDict()
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            key: 缓存键
        
        Returns:
            缓存值，不存在返回None
        """
        if key not in self.cache:
            return None
        
        # 检查是否过期
        value, expiry_time = self.cache[key]
        if time.time() > expiry_time:
            del self.cache[key]
            return None
        
        # 移到末尾（最近使用）
        self.cache.move_to_end(key)
        return value
    
    def set(self, key: str, value: Any, ttl: int = None) -> None:
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 缓存时间（秒），None表示使用默认值
        """
        # 检查是否超过最大容量
        if len(self.cache) >= self.max_size and key not in self.cache:
            # 删除最久未使用的项
            self.cache.popitem(last=False)
        
        # 计算过期时间
        cache_ttl = ttl if ttl is not None else self.default_ttl
        expiry_time = time.time() + cache_ttl
        
        # 设置缓存
        self.cache[key] = (value, expiry_time)
        self.cache.move_to_end(key)
    
    def delete(self, key: str) -> bool:
        """
        删除缓存
        
        Args:
            key: 缓存键
        
        Returns:
            是否成功
        """
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
        logger.info("✅ 内存缓存已清空")
    
    def size(self) -> int:
        """
        获取缓存大小
        
        Returns:
            缓存项数量
        """
        return len(self.cache)


# 全局实例
memory_cache = MemoryCache(max_size=1000, default_ttl=300)
