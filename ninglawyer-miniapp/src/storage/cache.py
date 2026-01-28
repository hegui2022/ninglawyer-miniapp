"""
缓存管理
"""
import redis
import json
import os
from typing import Any, Optional


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
            print("✓ Redis 连接成功")
        except Exception as e:
            print(f"✗ Redis 连接失败: {e}")
    
    def set(self, key: str, value: Any, expire: int = 3600):
        """设置缓存"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            self.client.setex(key, expire, value)
            return True
        except Exception as e:
            print(f"✗ 设置缓存失败: {e}")
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
            print(f"✗ 获取缓存失败: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"✗ 删除缓存失败: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            print(f"✗ 检查缓存失败: {e}")
            return False


# 全局缓存实例
_cache = None


def get_cache() -> Cache:
    """获取缓存实例"""
    global _cache
    if _cache is None:
        _cache = Cache()
    return _cache
