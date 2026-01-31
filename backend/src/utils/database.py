"""
数据库配置和连接管理
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from loguru import logger


# ============================================
# 数据库配置
# ============================================

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ninglawyer.db')

# 创建引擎（支持连接池配置）
engine = create_engine(
    DATABASE_URL,
    echo=False,  # 不打印SQL日志
    pool_pre_ping=True,  # 连接前检查
    pool_recycle=3600,  # 1小时回收连接
    pool_size=20,       # 连接池大小
    max_overflow=40,     # 最大溢出连接数
    pool_timeout=30,     # 连接超时时间（秒）
)

# 创建会话工厂
SessionLocal = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))


# ============================================
# 数据库会话管理
# ============================================

def get_db():
    """
    获取数据库会话
    
    Returns:
        数据库会话
    """
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e


@contextmanager
def get_db_context():
    """
    数据库会话上下文管理器
    
    使用方式:
        with get_db_context() as db:
            # 使用db
            pass
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


# ============================================
# 数据库初始化
# ============================================

def init_db():
    """初始化数据库"""
    try:
        # 导入所有模型
        from models.v1_models import Base
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("✅ 数据库表创建完成")
        
        # 创建索引
        try:
            from utils.db_indexes import create_indexes
            create_indexes(engine)
        except Exception as e:
            logger.warning(f"⚠️ 创建数据库索引失败（可忽略）: {e}")
        
        return True
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        return False


# ============================================
# 数据库关闭
# ============================================

def close_db():
    """关闭数据库连接"""
    try:
        SessionLocal.remove()
        engine.dispose()
        logger.info("数据库连接已关闭")
    except Exception as e:
        logger.error(f"关闭数据库连接失败: {str(e)}")
