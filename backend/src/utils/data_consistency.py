"""
数据一致性保障
提供事务管理、缓存失效等数据一致性保障机制
"""

from contextlib import contextmanager
from typing import Callable, Optional, List, Dict, Any
from loguru import logger

from database import get_db_context
from utils.cache_manager import CacheManager


class TransactionManager:
    """事务管理器"""
    
    def __init__(self):
        """初始化事务管理器"""
        self.current_transaction = None
    
    @contextmanager
    def transaction(self):
        """
        事务上下文管理器
        
        使用方式:
            with transaction_manager.transaction() as db:
                # 执行数据库操作
                pass
        """
        with get_db_context() as db:
            try:
                yield db
            except Exception as e:
                logger.error(f"❌ 事务执行失败: {e}")
                raise


class CacheConsistencyManager:
    """缓存一致性管理器"""
    
    def __init__(self, cache_manager: CacheManager):
        """
        初始化缓存一致性管理器
        
        Args:
            cache_manager: 缓存管理器
        """
        self.cache_manager = cache_manager
    
    def write_through(
        self,
        db_operation: Callable,
        cache_key: str,
        cache_value: Any,
        cache_ttl: int = 3600
    ) -> Any:
        """
        写穿透策略：先写数据库，再更新缓存
        
        Args:
            db_operation: 数据库操作函数
            cache_key: 缓存键
            cache_value: 缓存值
            cache_ttl: 缓存过期时间
        
        Returns:
            数据库操作结果
        """
        try:
            # 1. 执行数据库操作
            result = db_operation()
            
            # 2. 更新缓存
            if result is not None and self.cache_manager:
                self.cache_manager.set(cache_key, cache_value, ttl=cache_ttl)
                logger.debug(f"✅ 写穿透: 更新缓存 {cache_key}")
            
            return result
        
        except Exception as e:
            logger.error(f"❌ 写穿透失败: {e}")
            raise
    
    def invalidate_cache(
        self,
        cache_keys: List[str]
    ) -> bool:
        """
        失效缓存
        
        Args:
            cache_keys: 缓存键列表
        
        Returns:
            是否成功
        """
        try:
            success_count = 0
            for cache_key in cache_keys:
                if self.cache_manager and self.cache_manager.delete(cache_key):
                    success_count += 1
                    logger.debug(f"✅ 失效缓存: {cache_key}")
            
            return success_count == len(cache_keys)
        
        except Exception as e:
            logger.error(f"❌ 失效缓存失败: {e}")
            return False
    
    def invalidate_cache_pattern(
        self,
        pattern: str
    ) -> int:
        """
        批量失效缓存（按模式）
        
        Args:
            pattern: 缓存键模式
        
        Returns:
            失效的缓存数量
        """
        try:
            if not self.cache_manager:
                return 0
            
            count = self.cache_manager.clear_pattern(pattern)
            logger.debug(f"✅ 批量失效缓存: {pattern}, count={count}")
            
            return count
        
        except Exception as e:
            logger.error(f"❌ 批量失效缓存失败: {e}")
            return 0
    
    def cache_aside(
        self,
        cache_key: str,
        db_operation: Callable,
        cache_ttl: int = 3600
    ) -> Any:
        """
        Cache-Aside策略：先查缓存，缓存没有则查数据库并写入缓存
        
        Args:
            cache_key: 缓存键
            db_operation: 数据库操作函数
            cache_ttl: 缓存过期时间
        
        Returns:
            数据
        """
        try:
            # 1. 先查缓存
            if self.cache_manager:
                cached_value = self.cache_manager.get(cache_key)
                if cached_value is not None:
                    logger.debug(f"✅ Cache-Aside: 缓存命中 {cache_key}")
                    return cached_value
            
            # 2. 查数据库
            result = db_operation()
            
            # 3. 写入缓存
            if result is not None and self.cache_manager:
                self.cache_manager.set(cache_key, result, ttl=cache_ttl)
                logger.debug(f"✅ Cache-Aside: 写入缓存 {cache_key}")
            
            return result
        
        except Exception as e:
            logger.error(f"❌ Cache-Aside失败: {e}")
            raise


class DataConsistencyGuard:
    """数据一致性保障"""
    
    def __init__(
        self,
        cache_manager: CacheManager = None
    ):
        """
        初始化数据一致性保障
        
        Args:
            cache_manager: 缓存管理器
        """
        self.transaction_manager = TransactionManager()
        self.cache_consistency = CacheConsistencyManager(cache_manager)
    
    def safe_create(
        self,
        db_operation: Callable,
        cache_key: str = None,
        cache_value: Any = None,
        cache_ttl: int = 3600,
        invalidate_keys: List[str] = None
    ) -> Any:
        """
        安全创建（写穿透 + 缓存失效）
        
        Args:
            db_operation: 数据库操作函数
            cache_key: 缓存键（用于更新）
            cache_value: 缓存值
            cache_ttl: 缓存过期时间
            invalidate_keys: 需要失效的缓存键列表
        
        Returns:
            创建的数据
        """
        try:
            with self.transaction_manager.transaction():
                # 1. 执行数据库操作
                result = db_operation()
                
                # 2. 更新缓存（写穿透）
                if cache_key and cache_value and self.cache_consistency.cache_manager:
                    self.cache_consistency.cache_manager.set(cache_key, cache_value, ttl=cache_ttl)
                
                # 3. 失效相关缓存
                if invalidate_keys and self.cache_consistency.cache_manager:
                    self.cache_consistency.invalidate_cache(invalidate_keys)
                
                return result
        
        except Exception as e:
            logger.error(f"❌ 安全创建失败: {e}")
            raise
    
    def safe_update(
        self,
        db_operation: Callable,
        cache_key: str = None,
        cache_value: Any = None,
        cache_ttl: int = 3600,
        invalidate_keys: List[str] = None
    ) -> Any:
        """
        安全更新（写穿透 + 缓存失效）
        
        Args:
            db_operation: 数据库操作函数
            cache_key: 缓存键（用于更新）
            cache_value: 缓存值
            cache_ttl: 缓存过期时间
            invalidate_keys: 需要失效的缓存键列表
        
        Returns:
            更新的数据
        """
        try:
            with self.transaction_manager.transaction():
                # 1. 执行数据库操作
                result = db_operation()
                
                # 2. 更新缓存（写穿透）
                if cache_key and cache_value and self.cache_consistency.cache_manager:
                    self.cache_consistency.cache_manager.set(cache_key, cache_value, ttl=cache_ttl)
                
                # 3. 失效相关缓存
                if invalidate_keys and self.cache_consistency.cache_manager:
                    self.cache_consistency.invalidate_cache(invalidate_keys)
                
                return result
        
        except Exception as e:
            logger.error(f"❌ 安全更新失败: {e}")
            raise
    
    def safe_delete(
        self,
        db_operation: Callable,
        cache_key: str = None,
        invalidate_keys: List[str] = None
    ) -> bool:
        """
        安全删除（缓存失效）
        
        Args:
            db_operation: 数据库操作函数
            cache_key: 缓存键
            invalidate_keys: 需要失效的缓存键列表
        
        Returns:
            是否成功
        """
        try:
            with self.transaction_manager.transaction():
                # 1. 执行数据库操作
                result = db_operation()
                
                # 2. 失效缓存
                keys_to_invalidate = []
                if cache_key:
                    keys_to_invalidate.append(cache_key)
                if invalidate_keys:
                    keys_to_invalidate.extend(invalidate_keys)
                
                if keys_to_invalidate and self.cache_consistency.cache_manager:
                    self.cache_consistency.invalidate_cache(keys_to_invalidate)
                
                return result
        
        except Exception as e:
            logger.error(f"❌ 安全删除失败: {e}")
            raise
    
    def safe_read(
        self,
        cache_key: str,
        db_operation: Callable,
        cache_ttl: int = 3600
    ) -> Any:
        """
        安全读取（Cache-Aside）
        
        Args:
            cache_key: 缓存键
            db_operation: 数据库操作函数
            cache_ttl: 缓存过期时间
        
        Returns:
            数据
        """
        return self.cache_consistency.cache_aside(
            cache_key=cache_key,
            db_operation=db_operation,
            cache_ttl=cache_ttl
        )
