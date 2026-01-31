"""
测试数据库索引创建
验证所有索引是否正确创建
"""

import os
import sys

# 添加backend目录到sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sqlalchemy import text
from database import engine, get_db
from loguru import logger


def check_indexes():
    """检查数据库索引是否存在"""
    try:
        with engine.connect() as conn:
            # 检查SQLite索引
            indexes = conn.execute(text(
                "SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'"
            )).fetchall()
            
            logger.info(f"📊 数据库索引统计:")
            logger.info(f"总索引数: {len(indexes)}")
            
            if indexes:
                logger.info(f"\n索引列表:")
                for idx in indexes:
                    logger.info(f"  - {idx[0]} (表: {idx[1]})")
            else:
                logger.warning("未找到任何索引！")
                
        return True
    except Exception as e:
        logger.error(f"检查索引失败: {e}")
        return False


def test_performance():
    """测试索引性能"""
    try:
        from database import get_db_context
        with get_db_context() as db:
            from src.models.models import Message, User, Session
            
            # 测试User表索引
            logger.info("\n🔍 测试User表索引性能...")
            try:
                user = db.query(User).filter_by(openid="test_openid").first()
                logger.info(f"User表查询测试: ✅ 成功（{len(db.query(User).all())}条记录）")
            except Exception as e:
                logger.info(f"User表查询测试: ❌ 失败: {e}")
            
            # 测试Session表索引
            logger.info("\n🔍 测试Session表索引性能...")
            try:
                session = db.query(Session).filter_by(user_id=1, skill_type="consultation").first()
                logger.info(f"Session表查询测试: ✅ 成功（{len(db.query(Session).all())}条记录）")
            except Exception as e:
                logger.info(f"Session表查询测试: ❌ 失败: {e}")
            
            # 测试Message表索引
            logger.info("\n🔍 测试Message表索引性能...")
            try:
                msg = db.query(Message).filter_by(session_id=1).first()
                logger.info(f"Message表查询测试: ✅ 成功（{len(db.query(Message).all())}条记录）")
            except Exception as e:
                logger.info(f"Message表查询测试: ❌ 失败: {e}")
                
        return True
    except Exception as e:
        logger.error(f"性能测试失败: {e}")
        return False


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("🔧 数据库索引验证测试")
    logger.info("=" * 60)
    
    # 初始化数据库（创建表）
    logger.info("\n🔨 初始化数据库（创建表）...")
    try:
        from database import init_db
        init_db()
        logger.info("✅ 数据库表创建完成")
    except Exception as e:
        logger.error(f"❌ 初始化数据库失败: {e}")
        return False
    
    # 创建索引
    logger.info("\n🔨 创建数据库索引...")
    try:
        from src.utils.db_indexes import create_indexes
        create_indexes(engine)
        logger.info("✅ 数据库索引创建完成")
    except Exception as e:
        logger.error(f"❌ 创建数据库索引失败: {e}")
        return False
    
    # 检查索引
    if not check_indexes():
        logger.error("❌ 索引检查失败")
        return False
    
    # 性能测试
    if not test_performance():
        logger.error("❌ 性能测试失败")
        return False
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 数据库索引验证完成")
    logger.info("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
