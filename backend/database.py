"""
数据库连接和初始化
"""

import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from loguru import logger

from src.models.models import Base


# 数据库文件路径（项目根目录）
DB_DIR = Path(__file__).parent.parent
DB_FILE = DB_DIR / "ninglawyer.db"

# 数据库URL - 优先使用环境变量，测试环境使用 SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DB_FILE}"
)

# 如果 DATABASE_URL 以 sqlite:// 开头，使用 SQLite 特定配置
if DATABASE_URL.startswith('sqlite://'):
    # SQLite 配置
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        echo=False,
        connect_args={"check_same_thread": False}  # SQLite 线程安全
    )
else:
    # PostgreSQL 配置
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=False
    )

# 创建Session工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    获取数据库会话
    用于依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    获取数据库会话上下文管理器
    用于with语句
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"数据库操作失败：{str(e)}")
        raise
    finally:
        db.close()


def init_db():
    """
    初始化数据库（创建所有表）
    """
    try:
        logger.info("开始初始化数据库...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ 数据库初始化完成")
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败：{str(e)}")
        raise


def drop_all_tables():
    """
    删除所有表（危险操作，仅用于开发）
    """
    try:
        logger.warning("开始删除所有表...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("✅ 所有表已删除")
    except Exception as e:
        logger.error(f"❌ 删除表失败：{str(e)}")
        raise


def check_db_connection():
    """
    检查数据库连接
    """
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("✅ 数据库连接正常")
        return True
    except Exception as e:
        logger.error(f"❌ 数据库连接失败：{str(e)}")
        return False


def reset_db():
    """
    重置数据库（删除并重建）
    """
    drop_all_tables()
    init_db()
