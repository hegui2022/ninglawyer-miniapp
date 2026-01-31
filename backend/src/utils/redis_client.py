"""
Redis缓存配置和连接管理
用于缓存对话记录等临时数据
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import redis

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis客户端封装"""
    
    _instance: Optional['RedisClient'] = None
    _client: Optional[redis.Redis] = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化Redis客户端"""
        if self._client is not None:
            return
        
        try:
            # 从环境变量获取配置
            redis_host = os.getenv('REDIS_HOST', 'localhost')
            redis_port = int(os.getenv('REDIS_PORT', 6379))
            redis_db = int(os.getenv('REDIS_DB', 0))
            redis_password = os.getenv('REDIS_PASSWORD', None)
            
            # 创建Redis连接
            self._client = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                password=redis_password,
                decode_responses=True,  # 自动解码为字符串
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
            
            # 测试连接
            self._client.ping()
            logger.info(f"Redis连接成功: {redis_host}:{redis_port}")
            
        except Exception as e:
            logger.error(f"Redis连接失败: {str(e)}")
            self._client = None
    
    @property
    def client(self) -> redis.Redis:
        """获取Redis客户端"""
        if self._client is None:
            raise RuntimeError("Redis客户端未初始化")
        return self._client
    
    def is_connected(self) -> bool:
        """检查连接状态"""
        try:
            if self._client:
                self._client.ping()
                return True
        except Exception as e:
            logger.error(f"Redis连接检查失败: {str(e)}")
        return False
    
    def close(self):
        """关闭连接"""
        if self._client:
            self._client.close()
            logger.info("Redis连接已关闭")
    
    def get_user_type(self, user_id: int) -> Optional[str]:
        """
        获取用户类型
        
        Args:
            user_id: 用户ID
        
        Returns:
            用户类型 (personal/corporate) 或 None
        """
        if not self.is_connected():
            return None
        
        try:
            key = f"user_type:{user_id}"
            user_type = self._client.get(key)
            return user_type
        except Exception as e:
            logger.error(f"获取用户类型失败: {str(e)}")
            return None
    
    def set_user_type(self, user_id: int, user_type: str, ttl: int = 3600) -> bool:
        """
        设置用户类型
        
        Args:
            user_id: 用户ID
            user_type: 用户类型 (personal/corporate)
            ttl: 过期时间（秒），默认1小时
        
        Returns:
            是否设置成功
        """
        if not self.is_connected():
            return False
        
        try:
            key = f"user_type:{user_id}"
            self._client.setex(key, ttl, user_type)
            logger.info(f"用户类型设置成功: user_id={user_id}, type={user_type}")
            return True
        except Exception as e:
            logger.error(f"设置用户类型失败: {str(e)}")
            return False


# ============================================
# 对话缓存管理
# ============================================

class ConversationCache:
    """对话缓存管理"""
    
    # 缓存前缀
    CONVERSATION_PREFIX = "conversation:"
    MESSAGE_PREFIX = "message:"
    
    # 过期时间（对话缓存30天）
    CONVERSATION_TTL = 30 * 24 * 60 * 60  # 30天
    MESSAGE_TTL = 7 * 24 * 60 * 60  # 7天
    
    def __init__(self):
        """初始化"""
        self.redis = RedisClient()
    
    def save_conversation(
        self,
        session_id: str,
        user_id: int,
        app_type: str,
        conversation_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        保存对话基本信息
        
        Args:
            session_id: 会话ID
            user_id: 用户ID
            app_type: 小程序类型
            conversation_type: 对话类型
            metadata: 额外元数据
        
        Returns:
            是否保存成功
        """
        try:
            key = f"{self.CONVERSATION_PREFIX}{session_id}"
            data = {
                "session_id": session_id,
                "user_id": str(user_id),
                "app_type": app_type,
                "conversation_type": conversation_type,
                "created_at": datetime.now().isoformat()
            }
            if metadata:
                data["metadata"] = metadata
            
            # 保存到Redis，设置过期时间
            self.redis.client.setex(
                key,
                self.CONVERSATION_TTL,
                json.dumps(data, ensure_ascii=False)
            )
            logger.info(f"对话缓存保存成功: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"对话缓存保存失败: {str(e)}")
            return False
    
    def get_conversation(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        获取对话基本信息
        
        Args:
            session_id: 会话ID
        
        Returns:
            对话信息
        """
        try:
            key = f"{self.CONVERSATION_PREFIX}{session_id}"
            data = self.redis.client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"对话缓存获取失败: {str(e)}")
            return None
    
    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        bot_id: Optional[str] = None,
        bot_name: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        保存单条消息
        
        Args:
            session_id: 会话ID
            role: 角色（user/assistant）
            content: 消息内容
            bot_id: 智能体ID
            bot_name: 智能体名称
            extra_data: 额外数据
        
        Returns:
            是否保存成功
        """
        try:
            key = f"{self.MESSAGE_PREFIX}{session_id}"
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            }
            if bot_id:
                message["bot_id"] = bot_id
            if bot_name:
                message["bot_name"] = bot_name
            if extra_data:
                message["extra_data"] = extra_data
            
            # 使用列表存储消息
            self.redis.client.lpush(key, json.dumps(message, ensure_ascii=False))
            # 设置过期时间
            self.redis.client.expire(key, self.MESSAGE_TTL)
            
            logger.debug(f"消息缓存保存成功: {session_id}, role={role}")
            return True
            
        except Exception as e:
            logger.error(f"消息缓存保存失败: {str(e)}")
            return False
    
    def get_messages(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> list:
        """
        获取对话消息历史
        
        Args:
            session_id: 会话ID
            limit: 消息数量限制（默认全部）
        
        Returns:
            消息列表（按时间正序）
        """
        try:
            key = f"{self.MESSAGE_PREFIX}{session_id}"
            # 获取所有消息（Redis列表是从右到左的，需要反转）
            messages = self.redis.client.lrange(key, 0, -1)
            
            # 反转为时间正序
            messages.reverse()
            
            # 解析JSON
            result = [json.loads(msg) for msg in messages]
            
            # 限制数量
            if limit and limit > 0:
                result = result[-limit:]
            
            logger.debug(f"获取消息历史: {session_id}, count={len(result)}")
            return result
            
        except Exception as e:
            logger.error(f"消息历史获取失败: {str(e)}")
            return []
    
    def clear_conversation(self, session_id: str) -> bool:
        """
        清除对话缓存
        
        Args:
            session_id: 会话ID
        
        Returns:
            是否清除成功
        """
        try:
            # 删除对话基本信息
            self.redis.client.delete(f"{self.CONVERSATION_PREFIX}{session_id}")
            # 删除消息列表
            self.redis.client.delete(f"{self.MESSAGE_PREFIX}{session_id}")
            
            logger.info(f"对话缓存清除成功: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"对话缓存清除失败: {str(e)}")
            return False
    
    def clear_user_conversations(self, user_id: int) -> int:
        """
        清除用户的所有对话（慎用）
        
        Args:
            user_id: 用户ID
        
        Returns:
            清除的数量
        """
        try:
            # 查找所有属于该用户的对话
            count = 0
            pattern = f"{self.CONVERSATION_PREFIX}*"
            keys = self.redis.client.keys(pattern)
            
            for key in keys:
                data = self.redis.client.get(key)
                if data:
                    info = json.loads(data)
                    if info.get("user_id") == str(user_id):
                        session_id = info["session_id"]
                        self.clear_conversation(session_id)
                        count += 1
            
            logger.info(f"用户对话缓存清除完成: user_id={user_id}, count={count}")
            return count
            
        except Exception as e:
            logger.error(f"用户对话清除失败: {str(e)}")
            return 0


# ============================================
# 临时数据缓存（用于验证码等）
# ============================================

class TempDataCache:
    """临时数据缓存"""
    
    # 验证码过期时间：5分钟
    VERIFICATION_CODE_TTL = 5 * 60
    
    def __init__(self):
        """初始化"""
        self.redis = RedisClient()
    
    def save_verification_code(
        self,
        phone: str,
        code: str,
        code_type: str = "login"
    ) -> bool:
        """
        保存验证码
        
        Args:
            phone: 手机号
            code: 验证码
            code_type: 验证码类型
        
        Returns:
            是否保存成功
        """
        try:
            key = f"verification:{phone}:{code_type}"
            data = {
                "phone": phone,
                "code": code,
                "code_type": code_type,
                "created_at": datetime.now().isoformat(),
                "used": False
            }
            
            self.redis.client.setex(
                key,
                self.VERIFICATION_CODE_TTL,
                json.dumps(data, ensure_ascii=False)
            )
            logger.info(f"验证码保存成功: {phone}, type={code_type}")
            return True
            
        except Exception as e:
            logger.error(f"验证码保存失败: {str(e)}")
            return False
    
    def get_verification_code(
        self,
        phone: str,
        code_type: str = "login"
    ) -> Optional[Dict[str, Any]]:
        """
        获取验证码
        
        Args:
            phone: 手机号
            code_type: 验证码类型
        
        Returns:
            验证码信息
        """
        try:
            key = f"verification:{phone}:{code_type}"
            data = self.redis.client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"验证码获取失败: {str(e)}")
            return None
    
    def verify_code(
        self,
        phone: str,
        code: str,
        code_type: str = "login"
    ) -> bool:
        """
        验证验证码
        
        Args:
            phone: 手机号
            code: 验证码
            code_type: 验证码类型
        
        Returns:
            是否验证成功
        """
        try:
            verification = self.get_verification_code(phone, code_type)
            if not verification:
                logger.warning(f"验证码不存在或已过期: {phone}")
                return False
            
            if verification.get("used"):
                logger.warning(f"验证码已使用: {phone}")
                return False
            
            if verification.get("code") != code:
                logger.warning(f"验证码错误: {phone}")
                return False
            
            # 标记为已使用
            key = f"verification:{phone}:{code_type}"
            data = json.loads(self.redis.client.get(key))
            data["used"] = True
            self.redis.client.setex(
                key,
                self.VERIFICATION_CODE_TTL,
                json.dumps(data, ensure_ascii=False)
            )
            
            logger.info(f"验证码验证成功: {phone}")
            return True
            
        except Exception as e:
            logger.error(f"验证码验证失败: {str(e)}")
            return False


# ============================================
# 全局实例
# ============================================

# 全局Redis客户端
redis_client = RedisClient()

# 对话缓存
conversation_cache = ConversationCache()

# 临时数据缓存
temp_data_cache = TempDataCache()
