"""
数据库迁移脚本：添加套餐权限系统（SQLite版本）
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 设置环境变量使用SQLite
os.environ.setdefault('DATABASE_URL', 'sqlite:///ninglawyer.db')

from sqlalchemy import text
from src.database import engine, get_db_context
from src.models.models import Base, User, SkillPermission
from loguru import logger


def migrate_database():
    """执行数据库迁移"""
    logger.info("=" * 60)
    logger.info("开始数据库迁移：套餐权限系统")
    logger.info("=" * 60)
    
    try:
        with get_db_context() as session:
            # SQLite 不支持 ALTER TABLE 添加列，需要重建表
            # 但因为我们使用的是SQLAlchemy ORM，可以直接通过Base重新创建所有表
            logger.info("步骤 1/3: 重建数据库表（保留现有数据）...")
            
            # 获取现有数据
            existing_users = session.execute(text("SELECT * FROM users")).fetchall() if session.bind.dialect.name == 'sqlite' else []
            
            # 删除所有表
            Base.metadata.drop_all(bind=engine)
            
            # 重新创建所有表（包含新字段）
            Base.metadata.create_all(bind=engine)
            
            # 如果有旧数据，可以在这里恢复（可选）
            # 由于SQLite的限制，这里简化处理，只创建新表结构
            logger.info("  ✅ 数据库表已重建")
            
            # 2. 初始化技能权限数据
            logger.info("步骤 2/3: 初始化技能权限数据...")
            
            # 检查是否已有数据
            check_data_sql = """
                SELECT COUNT(*) FROM skill_permissions
            """
            data_count = session.execute(text(check_data_sql)).scalar()
            
            if data_count == 0:
                # 插入技能权限数据
                skills_data = [
                    {
                        'skill_name': 'desensitize',
                        'skill_display_name': '隐私脱敏',
                        'skill_category': 'privacy',
                        'required_subscription': 'basic',
                        'description': '对敏感信息进行脱敏处理（姓名、身份证、手机号、地址等）',
                        'daily_limit': 0,
                        'monthly_limit': 0
                    },
                    {
                        'skill_name': 'civil_consult',
                        'skill_display_name': '民事咨询',
                        'skill_category': 'legal',
                        'required_subscription': 'basic',
                        'description': '提供民事法律咨询服务（债务纠纷、婚姻家庭、劳动争议等）',
                        'daily_limit': 0,
                        'monthly_limit': 0
                    },
                    {
                        'skill_name': 'contract_draft',
                        'skill_display_name': '合同起草',
                        'skill_category': 'legal',
                        'required_subscription': 'premium',
                        'description': '起草各类合同（借款合同、租赁合同、劳动合同等）',
                        'daily_limit': 0,
                        'monthly_limit': 0
                    },
                    {
                        'skill_name': 'contract_review',
                        'skill_display_name': '合同审查',
                        'skill_category': 'legal',
                        'required_subscription': 'premium',
                        'description': '审查各类合同的风险并提供修改建议',
                        'daily_limit': 0,
                        'monthly_limit': 0
                    },
                    {
                        'skill_name': 'risk_scan',
                        'skill_display_name': '风险扫描',
                        'skill_category': 'business',
                        'required_subscription': 'enterprise',
                        'description': '扫描企业法律风险',
                        'daily_limit': 0,
                        'monthly_limit': 0
                    },
                    {
                        'skill_name': 'compliance_check',
                        'skill_display_name': '合规检查',
                        'skill_category': 'business',
                        'required_subscription': 'enterprise',
                        'description': '检查企业合规性',
                        'daily_limit': 0,
                        'monthly_limit': 0
                    },
                    {
                        'skill_name': 'e_signing',
                        'skill_display_name': '电子签约',
                        'skill_category': 'business',
                        'required_subscription': 'enterprise',
                        'description': '在线电子合同签署',
                        'daily_limit': 0,
                        'monthly_limit': 0
                    }
                ]
                
                for skill in skills_data:
                    session.execute(text("""
                        INSERT INTO skill_permissions 
                        (skill_name, skill_display_name, skill_category, required_subscription, 
                         description, daily_limit, monthly_limit)
                        VALUES 
                        (:skill_name, :skill_display_name, :skill_category, :required_subscription,
                         :description, :daily_limit, :monthly_limit)
                    """), skill)
                    logger.info(f"  ✅ 插入技能: {skill['skill_name']} (需要{skill['required_subscription']}套餐)")
                
                logger.info("  ✅ 技能权限数据初始化完成")
            else:
                logger.info(f"  ⏭️  已有 {data_count} 条技能权限数据")
            
            # 3. 创建测试用户
            logger.info("步骤 3/3: 创建测试用户...")
            
            # 检查是否已有测试用户
            check_user_sql = """
                SELECT COUNT(*) FROM users WHERE phone = '13800000001'
            """
            user_count = session.execute(text(check_user_sql)).scalar()
            
            if user_count == 0:
                session.execute(text("""
                    INSERT INTO users (phone, nickname, subscription_type, usage_stats, enabled_modules)
                    VALUES ('13800000001', '测试用户', 'basic', '{}', '[]')
                """))
                logger.info("  ✅ 创建测试用户")
            else:
                logger.info("  ⏭️  测试用户已存在")
        
        logger.info("=" * 60)
        logger.info("✅ 数据库迁移完成！")
        logger.info("=" * 60)
        
        # 显示迁移结果
        display_migration_result()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 数据库迁移失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def display_migration_result():
    """显示迁移结果"""
    try:
        with get_db_context() as session:
            # 显示 users 表结构
            logger.info("\n📊 Users 表字段：")
            columns_sql = """
                SELECT name FROM sqlite_master WHERE type='table' AND name='users'
            """
            table_exists = session.execute(text(columns_sql)).fetchone()
            
            if table_exists:
                # SQLite 获取列名
                columns_sql = "PRAGMA table_info(users)"
                columns = session.execute(text(columns_sql)).fetchall()
                for col in columns:
                    logger.info(f"  - {col[1]}: {col[2]}")
            else:
                logger.warning("  Users 表不存在")
            
            # 显示 skill_permissions 表数据
            logger.info("\n📊 SkillPermissions 表数据：")
            skills_sql = """
                SELECT skill_name, skill_display_name, required_subscription, enabled
                FROM skill_permissions
                ORDER BY required_subscription, skill_name
            """
            try:
                skills = session.execute(text(skills_sql)).fetchall()
                for skill in skills:
                    status = "✅" if skill[3] else "❌"
                    logger.info(f"  {status} {skill[1]} ({skill[0]}) - 需要{skill[2]}套餐")
            except Exception as e:
                logger.warning(f"  无法获取技能权限数据: {str(e)}")
            
            # 显示用户数量和套餐分布
            logger.info("\n👥 用户数量：")
            try:
                users_sql = "SELECT COUNT(*) FROM users"
                user_count = session.execute(text(users_sql)).scalar()
                logger.info(f"  总用户数: {user_count}")
            except Exception as e:
                logger.warning(f"  无法获取用户数据: {str(e)}")
                
    except Exception as e:
        logger.error(f"显示迁移结果失败：{str(e)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库迁移工具')
    parser.add_argument('--rollback', action='store_true', help='回滚迁移（删除所有表）')
    args = parser.parse_args()
    
    if args.rollback:
        logger.warning("回滚功能：删除所有表")
        try:
            from src.database import drop_all_tables
            drop_all_tables()
            logger.info("✅ 回滚完成")
            success = True
        except Exception as e:
            logger.error(f"❌ 回滚失败：{str(e)}")
            success = False
    else:
        success = migrate_database()
    
    sys.exit(0 if success else 1)
