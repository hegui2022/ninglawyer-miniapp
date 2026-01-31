"""
用户Repository
"""

from typing import Optional, List, Dict, Any
from loguru import logger

from database import get_db_context
from .base_repository import BaseRepository
from src.models.models import User
from src.utils.cache_manager import CacheManager


class UserRepository(BaseRepository[User]):
    """用户Repository"""
    
    def __init__(self, cache_manager: CacheManager = None):
        """初始化用户Repository"""
        super().__init__(User, cache_manager)
    
    def get_by_openid(self, openid: str) -> Optional[User]:
        """
        根据微信openid获取用户
        
        Args:
            openid: 微信openid
        
        Returns:
            用户对象，不存在返回None
        """
        try:
            # 先查缓存
            cache_key = self._make_cache_key(f"openid:{openid}")
            cached_user = self._get_from_cache(cache_key)
            if cached_user:
                return cached_user
            
            # 查数据库
            user = super().get_by(openid=openid)
            
            # 写入缓存
            if user:
                user_dict = self.to_dict(user)
                self._set_to_cache(cache_key, user_dict, ttl=3600)
            
            return user
        
        except Exception as e:
            logger.error(f"❌ 根据openid获取用户失败: {e}")
            return None
    
    def get_by_phone(self, phone: str) -> Optional[User]:
        """
        根据手机号获取用户
        
        Args:
            phone: 手机号
        
        Returns:
            用户对象，不存在返回None
        """
        try:
            # 先查缓存
            cache_key = self._make_cache_key(f"phone:{phone}")
            cached_user = self._get_from_cache(cache_key)
            if cached_user:
                return cached_user
            
            # 查数据库
            user = super().get_by(phone=phone)
            
            # 写入缓存
            if user:
                user_dict = self.to_dict(user)
                self._set_to_cache(cache_key, user_dict, ttl=3600)
            
            return user
        
        except Exception as e:
            logger.error(f"❌ 根据手机号获取用户失败: {e}")
            return None
    
    def get_user_type(self, user_id: int) -> str:
        """
        获取用户类型（带缓存）
        
        Args:
            user_id: 用户ID
        
        Returns:
            用户类型
        """
        try:
            # 先查缓存
            cache_key = f"user_type:{user_id}"
            user_type = self._get_from_cache(cache_key)
            if user_type:
                return user_type
            
            # 查数据库
            user = self.get_by_id(user_id)
            if user:
                user_type = user.subscription_type
            else:
                user_type = "basic"
            
            # 写入缓存
            self._set_to_cache(cache_key, user_type, ttl=3600)
            
            return user_type
        
        except Exception as e:
            logger.error(f"❌ 获取用户类型失败: {e}")
            return "basic"
    
    def create_user(self, openid: str = None, phone: str = None, **kwargs) -> Optional[User]:
        """
        创建用户
        
        Args:
            openid: 微信openid
            phone: 手机号
            **kwargs: 其他字段
        
        Returns:
            创建的用户，失败返回None
        """
        try:
            # 创建用户
            user = self.create(
                openid=openid,
                phone=phone,
                subscription_type="basic",
                **kwargs
            )
            
            # 失效相关缓存
            if openid:
                cache_key = self._make_cache_key(f"openid:{openid}")
                self._invalidate_cache(cache_key)
            
            if phone:
                cache_key = self._make_cache_key(f"phone:{phone}")
                self._invalidate_cache(cache_key)
            
            return user
        
        except Exception as e:
            logger.error(f"❌ 创建用户失败: {e}")
            return None
    
    def update_user_type(self, user_id: int, user_type: str) -> Optional[User]:
        """
        更新用户类型
        
        Args:
            user_id: 用户ID
            user_type: 用户类型
        
        Returns:
            更新后的用户，失败返回None
        """
        try:
            # 更新用户
            user = self.update(user_id, subscription_type=user_type)
            
            if user:
                # 失效用户类型缓存
                cache_key = f"user_type:{user_id}"
                self._invalidate_cache(cache_key)
            
            return user
        
        except Exception as e:
            logger.error(f"❌ 更新用户类型失败: {e}")
            return None
    
    def get_user_usage_stats(self, user_id: int) -> Dict[str, Any]:
        """
        获取用户使用统计
        
        Args:
            user_id: 用户ID
        
        Returns:
            使用统计
        """
        try:
            user = self.get_by_id(user_id)
            if user:
                return user.usage_stats or {}
            return {}
        
        except Exception as e:
            logger.error(f"❌ 获取用户使用统计失败: {e}")
            return {}
    
    def increment_usage_count(self, user_id: int, module: str) -> bool:
        """
        增加使用次数
        
        Args:
            user_id: 用户ID
            module: 模块名称
        
        Returns:
            是否成功
        """
        try:
            with get_db_context() as db:
                user = db.query(User).filter_by(id=user_id).first()
                
                if not user:
                    return False
                
                # 更新使用统计
                if not user.usage_stats:
                    user.usage_stats = {}
                
                if module not in user.usage_stats:
                    user.usage_stats[module] = 0
                
                user.usage_stats[module] += 1
                
                db.flush()
                
                # 失效缓存
                cache_key = self._make_cache_key(str(user_id))
                self._invalidate_cache(cache_key)
                
                return True
        
        except Exception as e:
            logger.error(f"❌ 增加使用次数失败: {e}")
            return False
    
    def get_enabled_modules(self, user_id: int) -> List[str]:
        """
        获取用户启用的模块
        
        Args:
            user_id: 用户ID
        
        Returns:
            启用的模块列表
        """
        try:
            user = self.get_by_id(user_id)
            if user:
                return user.enabled_modules or []
            return []
        
        except Exception as e:
            logger.error(f"❌ 获取启用的模块失败: {e}")
            return []
