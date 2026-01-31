"""
消息Repository
"""

from typing import Optional, List, Dict, Any
from loguru import logger

from database import get_db_context
from .base_repository import BaseRepository
from src.models.models import Message
from src.utils.cache_manager import CacheManager


class MessageRepository(BaseRepository[Message]):
    """消息Repository"""
    
    def __init__(self, cache_manager: CacheManager = None):
        """初始化消息Repository"""
        super().__init__(Message, cache_manager)
    
    def create_message(
        self,
        session_id: int,
        role: str,
        content: str
    ) -> Optional[Message]:
        """
        创建消息
        
        Args:
            session_id: 会话ID
            role: 角色（user/assistant）
            content: 消息内容
        
        Returns:
            创建的消息，失败返回None
        """
        try:
            # 创建消息
            message = self.create(
                session_id=session_id,
                role=role,
                content=content
            )
            
            # 失效会话消息列表缓存
            cache_key = f"message:session:{session_id}"
            self._invalidate_cache(cache_key)
            
            return message
        
        except Exception as e:
            logger.error(f"❌ 创建消息失败: {e}")
            return None
    
    def get_session_messages(
        self,
        session_id: int,
        limit: int = 50
    ) -> List[Message]:
        """
        获取会话消息列表
        
        Args:
            session_id: 会话ID
            limit: 返回数量限制
        
        Returns:
            消息列表
        """
        try:
            # 先查缓存
            cache_key = f"message:session:{session_id}"
            cached_messages = self._get_from_cache(cache_key)
            if cached_messages:
                # 缓存返回字典列表，转换为Message对象（简化处理）
                # 实际使用时可以返回字典，这里返回对象列表
                return [Message(**msg) for msg in cached_messages[-limit:]]
            
            # 查数据库
            with get_db_context() as db:
                messages = db.query(Message).filter_by(
                    session_id=session_id
                ).order_by(Message.created_at.asc()).limit(limit).all()
                
                # 写入缓存
                if messages:
                    messages_dict = self.to_dict_list(messages)
                    self._set_to_cache(cache_key, messages_dict, ttl=600)
                
                # 创建新的对象实例列表（无Session绑定）
                return [Message(**self.to_dict(m)) for m in messages]
        
        except Exception as e:
            logger.error(f"❌ 获取会话消息列表失败: {e}")
            return []
    
    def get_session_messages_dict(
        self,
        session_id: int,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        获取会话消息列表（字典格式）
        
        Args:
            session_id: 会话ID
            limit: 返回数量限制
        
        Returns:
            消息字典列表
        """
        messages = self.get_session_messages(session_id, limit)
        return self.to_dict_list(messages)
    
    def get_last_message(
        self,
        session_id: int,
        role: str = None
    ) -> Optional[Message]:
        """
        获取会话最后一条消息
        
        Args:
            session_id: 会话ID
            role: 角色（可选）
        
        Returns:
            消息对象，不存在返回None
        """
        try:
            with get_db_context() as db:
                query = db.query(Message).filter_by(session_id=session_id)
                
                if role:
                    query = query.filter_by(role=role)
                
                message = query.order_by(Message.created_at.desc()).first()
                
                # 创建新的对象实例（无Session绑定）
                if message:
                    return Message(**self.to_dict(message))
                
                return None
        
        except Exception as e:
            logger.error(f"❌ 获取最后一条消息失败: {e}")
            return None
    
    def delete_session_messages(self, session_id: int) -> int:
        """
        删除会话所有消息
        
        Args:
            session_id: 会话ID
        
        Returns:
            删除的消息数量
        """
        try:
            with get_db_context() as db:
                count = db.query(Message).filter_by(
                    session_id=session_id
                ).delete()
                
                # 失效会话消息列表缓存
                cache_key = f"message:session:{session_id}"
                self._invalidate_cache(cache_key)
                
                logger.debug(f"✅ 删除会话消息: session_id={session_id}, count={count}")
                
                return count
        
        except Exception as e:
            logger.error(f"❌ 删除会话消息失败: {e}")
            return 0
    
    def get_message_count(self, session_id: int) -> int:
        """
        获取会话消息数量
        
        Args:
            session_id: 会话ID
        
        Returns:
            消息数量
        """
        return self.count(session_id=session_id)
    
    def bulk_create_messages(
        self,
        session_id: int,
        messages: List[Dict[str, Any]]
    ) -> List[Message]:
        """
        批量创建消息
        
        Args:
            session_id: 会话ID
            messages: 消息列表，每条消息包含role和content
        
        Returns:
            创建的消息列表
        """
        try:
            # 添加session_id
            for msg in messages:
                msg['session_id'] = session_id
            
            # 批量创建
            created_messages = self.bulk_create(messages)
            
            # 失效会话消息列表缓存
            cache_key = f"message:session:{session_id}"
            self._invalidate_cache(cache_key)
            
            # 创建新的对象实例列表（无Session绑定）
            return [Message(**self.to_dict(m)) for m in created_messages]
        
        except Exception as e:
            logger.error(f"❌ 批量创建消息失败: {e}")
            return []
    
    def get_conversation_history(
        self,
        session_id: int,
        limit: int = 20
    ) -> List[Dict[str, str]]:
        """
        获取对话历史（用于LLM上下文）
        
        Args:
            session_id: 会话ID
            limit: 返回数量限制
        
        Returns:
            对话历史列表，格式: [{"role": "user", "content": "..."}, ...]
        """
        try:
            messages = self.get_session_messages(session_id, limit)
            history = []
            
            for msg in messages:
                history.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            return history
        
        except Exception as e:
            logger.error(f"❌ 获取对话历史失败: {e}")
            return []
