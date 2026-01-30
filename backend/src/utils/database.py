"""
数据库配置和连接管理
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager


# ============================================
# 数据库配置
# ============================================

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ninglawyer.db')

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    echo=False,  # 不打印SQL日志
    pool_pre_ping=True,  # 连接前检查
    pool_recycle=3600  # 1小时回收连接
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
        
        return True
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        return False


# ============================================
# 数据库关闭
# ============================================

def close_db():
    """关闭数据库连接"""
    try:
        SessionLocal.remove()
        engine.dispose()
    except Exception as e:
        print(f"关闭数据库连接失败: {str(e)}")
