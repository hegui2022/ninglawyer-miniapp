"""
数据库初始化脚本
创建所有数据表
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目路径到sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(backend_dir, 'src')
sys.path.insert(0, backend_dir)
sys.path.insert(0, src_dir)

from models.v1_models import Base


def init_database():
    """初始化数据库"""
    try:
        # 获取数据库URL
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            print("错误: DATABASE_URL环境变量未设置")
            return False
        
        print(f"连接数据库: {database_url}")
        
        # 创建引擎
        engine = create_engine(database_url, echo=True)
        
        # 创建所有表
        print("创建数据表...")
        Base.metadata.create_all(bind=engine)
        
        print("数据库初始化成功！")
        
        # 列出所有表
        with engine.connect() as conn:
            # SQLite查询所有表
            result = conn.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            ))
            tables = [row[0] for row in result]
            print(f"已创建的表: {', '.join(tables)}")
        
        return True
        
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        return False


if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
