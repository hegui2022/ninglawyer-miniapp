"""
统一Repository层
提供标准的数据访问接口
"""

from typing import Type, TypeVar, Generic, Optional, List, Dict, Any
from abc import ABC, abstractmethod
from contextlib import contextmanager
from sqlalchemy.orm import Query
from loguru import logger

from database import get_db_context
from models.models import Base

# 泛型类型
T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T], ABC):
    """
    基础Repository接口
    
    提供通用的CRUD操作
    所有具体的Repository都应该继承这个类
    """
    
    def __init__(self, model: Type[T], cache_manager=None):
        """
        初始化Repository
        
        Args:
            model: SQLAlchemy模型类
            cache_manager: 缓存管理器（可选）
        """
        self.model = model
        self.cache_manager = cache_manager
        self.cache_prefix = self._get_cache_prefix()
        
        logger.info(f"📦 Repository初始化: {self.model.__name__}")
    
    def _get_cache_prefix(self) -> str:
        """
        获取缓存前缀
        
        Returns:
            缓存前缀
        """
        table_name = self.model.__tablename__
        return f"{table_name}"
    
    def _make_cache_key(self, identifier: str) -> str:
        """
        生成缓存键
        
        Args:
            identifier: 标识符
        
        Returns:
            缓存键
        """
        return f"{self.cache_prefix}:{identifier}"
    
    def _invalidate_cache(self, cache_key: str) -> bool:
        """
        失效缓存
        
        Args:
            cache_key: 缓存键
        
        Returns:
            是否成功
        """
        if self.cache_manager:
            return self.cache_manager.delete(cache_key)
        return False
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """
        从缓存获取数据
        
        Args:
            cache_key: 缓存键
        
        Returns:
            缓存值，不存在返回None
        """
        if self.cache_manager:
            return self.cache_manager.get(cache_key)
        return None
    
    def _set_to_cache(self, cache_key: str, value: Any, ttl: int = 3600) -> bool:
        """
        设置缓存
        
        Args:
            cache_key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒）
        
        Returns:
            是否成功
        """
        if self.cache_manager:
            return self.cache_manager.set(cache_key, value, ttl=ttl)
        return False
    
    def to_dict(self, obj: T) -> Dict[str, Any]:
        """
        将模型对象转换为字典
        
        Args:
            obj: 模型对象
        
        Returns:
            字典
        """
        if obj is None:
            return None
        
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    
    def to_dict_list(self, objs: List[T]) -> List[Dict[str, Any]]:
        """
        将模型对象列表转换为字典列表
        
        Args:
            objs: 模型对象列表
        
        Returns:
            字典列表
        """
        return [self.to_dict(obj) for obj in objs]
    
    def create(self, **kwargs) -> Optional[T]:
        """
        创建记录
        
        Args:
            **kwargs: 字段值
        
        Returns:
            创建的记录，失败返回None
        """
        try:
            with get_db_context() as db:
                obj = self.model(**kwargs)
                db.add(obj)
                db.flush()
                db.refresh(obj)
                
                # 将对象转换为字典，避免DetachedInstanceError
                obj_dict = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
                
                logger.debug(f"✅ 创建记录: {self.model.__name__}(id={obj.id})")
                
                # 创建新的对象实例（无Session绑定）
                return self.model(**obj_dict)
        
        except Exception as e:
            logger.error(f"❌ 创建记录失败: {e}")
            return None
    
    def get_by_id(self, id: int) -> Optional[T]:
        """
        根据ID获取记录
        
        Args:
            id: 记录ID
        
        Returns:
            记录，不存在返回None
        """
        try:
            # 先查缓存
            cache_key = self._make_cache_key(str(id))
            cached_obj = self._get_from_cache(cache_key)
            if cached_obj:
                return cached_obj
            
            # 查数据库
            with get_db_context() as db:
                obj = db.query(self.model).filter_by(id=id).first()
                
                # 写入缓存
                if obj:
                    obj_dict = self.to_dict(obj)
                    self._set_to_cache(cache_key, obj_dict, ttl=3600)
                    
                    # 创建新的对象实例（无Session绑定）
                    return self.model(**obj_dict)
                
                return None
        
        except Exception as e:
            logger.error(f"❌ 获取记录失败: {e}")
            return None
    
    def get_by(self, **kwargs) -> Optional[T]:
        """
        根据条件获取单条记录
        
        Args:
            **kwargs: 查询条件
        
        Returns:
            记录，不存在返回None
        """
        try:
            with get_db_context() as db:
                obj = db.query(self.model).filter_by(**kwargs).first()
                
                # 创建新的对象实例（无Session绑定）
                if obj:
                    obj_dict = self.to_dict(obj)
                    return self.model(**obj_dict)
                
                return None
        
        except Exception as e:
            logger.error(f"❌ 获取记录失败: {e}")
            return None
    
    def get_all(self, **kwargs) -> List[T]:
        """
        获取所有记录
        
        Args:
            **kwargs: 查询条件
        
        Returns:
            记录列表
        """
        try:
            with get_db_context() as db:
                query = db.query(self.model)
                
                # 添加过滤条件
                if kwargs:
                    query = query.filter_by(**kwargs)
                
                # 添加排序
                if hasattr(self.model, 'created_at'):
                    query = query.order_by(self.model.created_at.desc())
                
                objs = query.all()
                
                # 创建新的对象实例列表（无Session绑定）
                return [self.model(**self.to_dict(obj)) for obj in objs]
        
        except Exception as e:
            logger.error(f"❌ 获取记录列表失败: {e}")
            return []
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        """
        更新记录
        
        Args:
            id: 记录ID
            **kwargs: 更新字段
        
        Returns:
            更新后的记录，失败返回None
        """
        try:
            with get_db_context() as db:
                obj = db.query(self.model).filter_by(id=id).first()
                
                if not obj:
                    logger.warning(f"⚠️ 记录不存在: {self.model.__name__}(id={id})")
                    return None
                
                # 更新字段
                for key, value in kwargs.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                
                db.flush()
                db.refresh(obj)
                
                # 将对象转换为字典，避免DetachedInstanceError
                obj_dict = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
                
                # 失效缓存
                cache_key = self._make_cache_key(str(id))
                self._invalidate_cache(cache_key)
                
                logger.debug(f"✅ 更新记录: {self.model.__name__}(id={id})")
                
                # 创建新的对象实例（无Session绑定）
                return self.model(**obj_dict)
        
        except Exception as e:
            logger.error(f"❌ 更新记录失败: {e}")
            return None
    
    def delete(self, id: int) -> bool:
        """
        删除记录
        
        Args:
            id: 记录ID
        
        Returns:
            是否成功
        """
        try:
            with get_db_context() as db:
                obj = db.query(self.model).filter_by(id=id).first()
                
                if not obj:
                    logger.warning(f"⚠️ 记录不存在: {self.model.__name__}(id={id})")
                    return False
                
                db.delete(obj)
                
                # 失效缓存
                cache_key = self._make_cache_key(str(id))
                self._invalidate_cache(cache_key)
                
                logger.debug(f"✅ 删除记录: {self.model.__name__}(id={id})")
                
                return True
        
        except Exception as e:
            logger.error(f"❌ 删除记录失败: {e}")
            return False
    
    def count(self, **kwargs) -> int:
        """
        统计记录数量
        
        Args:
            **kwargs: 查询条件
        
        Returns:
            记录数量
        """
        try:
            with get_db_context() as db:
                query = db.query(self.model)
                
                if kwargs:
                    query = query.filter_by(**kwargs)
                
                count = query.count()
                return count
        
        except Exception as e:
            logger.error(f"❌ 统计记录数量失败: {e}")
            return 0
    
    def exists(self, **kwargs) -> bool:
        """
        检查记录是否存在
        
        Args:
            **kwargs: 查询条件
        
        Returns:
            是否存在
        """
        try:
            with get_db_context() as db:
                obj = db.query(self.model).filter_by(**kwargs).first()
                return obj is not None
        
        except Exception as e:
            logger.error(f"❌ 检查记录存在失败: {e}")
            return False
    
    def bulk_create(self, items: List[Dict[str, Any]]) -> List[T]:
        """
        批量创建记录
        
        Args:
            items: 记录列表
        
        Returns:
            创建的记录列表
        """
        try:
            with get_db_context() as db:
                objs = [self.model(**item) for item in items]
                db.add_all(objs)
                db.flush()
                
                logger.debug(f"✅ 批量创建记录: {self.model.__name__}(count={len(objs)})")
                
                # 创建新的对象实例列表（无Session绑定）
                return [self.model(**self.to_dict(obj)) for obj in objs]
        
        except Exception as e:
            logger.error(f"❌ 批量创建记录失败: {e}")
            return []
    
    def paginate(self, page: int = 1, page_size: int = 20, **kwargs) -> Dict[str, Any]:
        """
        分页查询
        
        Args:
            page: 页码
            page_size: 每页数量
            **kwargs: 查询条件
        
        Returns:
            分页结果
        """
        try:
            with get_db_context() as db:
                query = db.query(self.model)
                
                if kwargs:
                    query = query.filter_by(**kwargs)
                
                # 排序
                if hasattr(self.model, 'created_at'):
                    query = query.order_by(self.model.created_at.desc())
                
                # 分页
                total = query.count()
                offset = (page - 1) * page_size
                items = query.offset(offset).limit(page_size).all()
                
                # 创建新的对象实例列表（无Session绑定）
                items_dicts = [self.model(**self.to_dict(item)) for item in items]
                
                return {
                    'items': items_dicts,
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': (total + page_size - 1) // page_size
                }
        
        except Exception as e:
            logger.error(f"❌ 分页查询失败: {e}")
            return {
                'items': [],
                'total': 0,
                'page': page,
                'page_size': page_size,
                'total_pages': 0
            }
