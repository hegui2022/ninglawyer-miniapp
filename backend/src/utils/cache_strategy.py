"""
统一缓存策略配置
"""

from typing import Dict, Any
from enum import Enum


class CacheKeyPrefix(Enum):
    """缓存键前缀"""
    USER = "user"
    SESSION = "session"
    MESSAGE = "message"
    USER_TYPE = "user_type"
    SCENARIO = "scenario"
    SYSTEM_CONFIG = "system_config"
    SKILL_PERMISSION = "skill_permission"


class CacheTTL(Enum):
    """缓存过期时间（秒）"""
    USER_INFO = 3600  # 用户信息：1小时
    USER_TYPE = 3600  # 用户类型：1小时
    SESSION_INFO = 3600  # 会话信息：1小时
    MESSAGE_LIST = 600  # 消息列表：10分钟
    SCENARIO_TYPE = 3600  # 场景类型：1小时
    SYSTEM_CONFIG = 3600  # 系统配置：1小时
    SHORT = 60  # 短期缓存：1分钟
    MEDIUM = 600  # 中期缓存：10分钟
    LONG = 3600  # 长期缓存：1小时


class CacheKeyBuilder:
    """缓存键构建器"""
    
    @staticmethod
    def build_user_key(user_id: int) -> str:
        """构建用户缓存键"""
        return f"{CacheKeyPrefix.USER.value}:{user_id}"
    
    @staticmethod
    def build_user_openid_key(openid: str) -> str:
        """构建用户openid缓存键"""
        return f"{CacheKeyPrefix.USER.value}:openid:{openid}"
    
    @staticmethod
    def build_user_phone_key(phone: str) -> str:
        """构建用户手机号缓存键"""
        return f"{CacheKeyPrefix.USER.value}:phone:{phone}"
    
    @staticmethod
    def build_user_type_key(user_id: int) -> str:
        """构建用户类型缓存键"""
        return f"{CacheKeyPrefix.USER_TYPE.value}:{user_id}"
    
    @staticmethod
    def build_session_key(session_id: int) -> str:
        """构建会话缓存键"""
        return f"{CacheKeyPrefix.SESSION.value}:{session_id}"
    
    @staticmethod
    def build_active_session_key(user_id: int, skill_type: str) -> str:
        """构建活跃会话缓存键"""
        return f"{CacheKeyPrefix.SESSION.value}:user:{user_id}:{skill_type}:active"
    
    @staticmethod
    def build_message_session_key(session_id: int) -> str:
        """构建会话消息列表缓存键"""
        return f"{CacheKeyPrefix.MESSAGE.value}:session:{session_id}"
    
    @staticmethod
    def build_scenario_session_key(session_id: int) -> str:
        """构建会话场景类型缓存键"""
        return f"{CacheKeyPrefix.SCENARIO.value}:session:{session_id}"
    
    @staticmethod
    def build_system_config_key(config_key: str) -> str:
        """构建系统配置缓存键"""
        return f"{CacheKeyPrefix.SYSTEM_CONFIG.value}:{config_key}"


class CacheStrategy:
    """缓存策略"""
    
    # 缓存键前缀
    PREFIXES = {
        "user": "user",
        "session": "session",
        "message": "message",
        "user_type": "user_type",
        "scenario": "scenario",
        "system_config": "system_config",
    }
    
    # 缓存过期时间
    TTL = {
        "user_info": 3600,
        "user_type": 3600,
        "session_info": 3600,
        "message_list": 600,
        "scenario_type": 3600,
        "system_config": 3600,
        "short": 60,
        "medium": 600,
        "long": 3600,
    }
    
    # 缓存失效模式
    INVALIDATION_MODES = {
        "write_through": "写穿透",  # 先写数据库，再更新缓存
        "write_back": "写回",  # 先写缓存，异步更新数据库
        "write_around": "绕过缓存",  # 只写数据库，不更新缓存
        "cache_aside": "Cache-Aside",  # 读时加载缓存
    }
    
    @staticmethod
    def get_ttl(resource_type: str) -> int:
        """
        获取资源类型的缓存过期时间
        
        Args:
            resource_type: 资源类型
        
        Returns:
            过期时间（秒）
        """
        return CacheStrategy.TTL.get(resource_type, 600)
    
    @staticmethod
    def build_cache_key(prefix: str, identifier: str) -> str:
        """
        构建缓存键
        
        Args:
            prefix: 前缀
            identifier: 标识符
        
        Returns:
            缓存键
        """
        return f"{prefix}:{identifier}"
    
    @staticmethod
    def should_cache(resource_type: str) -> bool:
        """
        判断资源类型是否应该缓存
        
        Args:
            resource_type: 资源类型
        
        Returns:
            是否应该缓存
        """
        # 默认都缓存
        return True
    
    @staticmethod
    def get_cache_key_pattern(prefix: str) -> str:
        """
        获取缓存键匹配模式（用于批量失效）
        
        Args:
            prefix: 前缀
        
        Returns:
            缓存键模式
        """
        return f"{prefix}:*"


# 缓存策略配置示例
CACHE_STRATEGY_CONFIG = {
    "user": {
        "prefix": "user",
        "ttl": 3600,
        "keys": {
            "by_id": "{prefix}:{id}",
            "by_openid": "{prefix}:openid:{openid}",
            "by_phone": "{prefix}:phone:{phone}",
        }
    },
    "session": {
        "prefix": "session",
        "ttl": 3600,
        "keys": {
            "by_id": "{prefix}:{id}",
            "active": "{prefix}:user:{user_id}:{skill_type}:active",
        }
    },
    "message": {
        "prefix": "message",
        "ttl": 600,
        "keys": {
            "session_messages": "{prefix}:session:{session_id}",
        }
    },
    "user_type": {
        "prefix": "user_type",
        "ttl": 3600,
        "keys": {
            "by_user_id": "{prefix}:{user_id}",
        }
    },
    "scenario": {
        "prefix": "scenario",
        "ttl": 3600,
        "keys": {
            "by_session_id": "{prefix}:session:{session_id}",
        }
    },
}
