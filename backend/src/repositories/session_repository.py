"""
会话Repository
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from loguru import logger

from database import get_db_context
from .base_repository import BaseRepository
from src.models.models import Session
from src.utils.cache_manager import CacheManager


class SessionRepository(BaseRepository[Session]):
    """会话Repository"""
    
    def __init__(self, cache_manager: CacheManager = None):
        """初始化会话Repository"""
        super().__init__(Session, cache_manager)
    
    def create_session(
        self,
        user_id: int,
        skill_type: str,
        title: str = None,
        **kwargs
    ) -> Optional[Session]:
        """
        创建会话
        
        Args:
            user_id: 用户ID
            skill_type: 技能类型
            title: 会话标题
            **kwargs: 其他字段
        
        Returns:
            创建的会话，失败返回None
        """
        try:
            # 创建会话
            session = self.create(
                user_id=user_id,
                skill_type=skill_type,
                title=title or f"{skill_type}会话",
                is_active=True,
                **kwargs
            )
            
            # 失效用户活跃会话缓存
            cache_key = f"session:user:{user_id}:{skill_type}:active"
            self._invalidate_cache(cache_key)
            
            return session
        
        except Exception as e:
            logger.error(f"❌ 创建会话失败: {e}")
            return None
    
    def get_active_session(
        self,
        user_id: int,
        skill_type: str
    ) -> Optional[Session]:
        """
        获取用户活跃会话
        
        Args:
            user_id: 用户ID
            skill_type: 技能类型
        
        Returns:
            活跃会话，不存在返回None
        """
        try:
            # 先查缓存
            cache_key = f"session:user:{user_id}:{skill_type}:active"
            cached_session = self._get_from_cache(cache_key)
            if cached_session:
                return cached_session
            
            # 查数据库
            with get_db_context() as db:
                session = db.query(Session).filter_by(
                    user_id=user_id,
                    skill_type=skill_type,
                    is_active=True
                ).order_by(Session.created_at.desc()).first()
                
                # 写入缓存
                if session:
                    session_dict = self.to_dict(session)
                    self._set_to_cache(cache_key, session_dict, ttl=3600)
                    
                    # 创建新的对象实例（无Session绑定）
                    return Session(**session_dict)
                
                return None
        
        except Exception as e:
            logger.error(f"❌ 获取活跃会话失败: {e}")
            return None
    
    def get_user_sessions(
        self,
        user_id: int,
        skill_type: str = None,
        limit: int = 50
    ) -> List[Session]:
        """
        获取用户会话列表
        
        Args:
            user_id: 用户ID
            skill_type: 技能类型（可选）
            limit: 返回数量限制
        
        Returns:
            会话列表
        """
        try:
            with get_db_context() as db:
                query = db.query(Session).filter_by(user_id=user_id)
                
                if skill_type:
                    query = query.filter_by(skill_type=skill_type)
                
                sessions = query.order_by(Session.created_at.desc()).limit(limit).all()
                
                # 创建新的对象实例列表（无Session绑定）
                return [Session(**self.to_dict(s)) for s in sessions]
        
        except Exception as e:
            logger.error(f"❌ 获取用户会话列表失败: {e}")
            return []
    
    def close_session(self, session_id: int) -> Optional[Session]:
        """
        关闭会话
        
        Args:
            session_id: 会话ID
        
        Returns:
            关闭后的会话，失败返回None
        """
        try:
            session = self.update(session_id, is_active=False)
            
            if session:
                # 失效活跃会话缓存
                cache_key = f"session:user:{session.user_id}:{session.skill_type}:active"
                self._invalidate_cache(cache_key)
            
            return session
        
        except Exception as e:
            logger.error(f"❌ 关闭会话失败: {e}")
            return None
    
    def update_session_title(self, session_id: int, title: str) -> Optional[Session]:
        """
        更新会话标题
        
        Args:
            session_id: 会话ID
            title: 新标题
        
        Returns:
            更新后的会话，失败返回None
        """
        try:
            return self.update(session_id, title=title)
        
        except Exception as e:
            logger.error(f"❌ 更新会话标题失败: {e}")
            return None
    
    def delete_session(self, session_id: int) -> bool:
        """
        删除会话
        
        Args:
            session_id: 会话ID
        
        Returns:
            是否成功
        """
        try:
            # 获取会话信息
            session = self.get_by_id(session_id)
            if not session:
                return False
            
            # 删除会话
            success = self.delete(session_id)
            
            if success:
                # 失效活跃会话缓存
                cache_key = f"session:user:{session.user_id}:{session.skill_type}:active"
                self._invalidate_cache(cache_key)
            
            return success
        
        except Exception as e:
            logger.error(f"❌ 删除会话失败: {e}")
            return False
    
    def get_or_create_session(
        self,
        user_id: int,
        skill_type: str
    ) -> Optional[Session]:
        """
        获取或创建会话
        
        Args:
            user_id: 用户ID
            skill_type: 技能类型
        
        Returns:
            会话对象
        """
        try:
            # 先尝试获取活跃会话
            session = self.get_active_session(user_id, skill_type)
            
            if session:
                return session
            
            # 创建新会话
            return self.create_session(user_id, skill_type)
        
        except Exception as e:
            logger.error(f"❌ 获取或创建会话失败: {e}")
            return None
    
    def get_session_scenario(self, session_id: int) -> str:
        """
        获取会话场景类型（预留）
        
        Args:
            session_id: 会话ID
        
        Returns:
            场景类型
        """
        # TODO: 从会话扩展表获取场景类型
        return "general"
