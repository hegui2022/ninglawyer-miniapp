"""
数据库迁移脚本：添加套餐权限系统
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from src.storage.db import engine, get_db_session
from loguru import logger


def migrate_database():
    """执行数据库迁移"""
    logger.info("=" * 60)
    logger.info("开始数据库迁移：套餐权限系统")
    logger.info("=" * 60)
    
    session = get_db_session()
    
    try:
        # 1. 添加新字段到 users 表
        logger.info("步骤 1/3: 添加套餐相关字段到 users 表...")
        
        # 检查字段是否已存在
        check_sql = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            AND column_name IN ('subscription_type', 'subscription_start_at', 'subscription_end_at', 'enabled_modules', 'usage_stats')
        """
        existing_columns = session.execute(text(check_sql)).fetchall()
        existing_column_names = [col[0] for col in existing_columns]
        
        # 添加 subscription_type 字段
        if 'subscription_type' not in existing_column_names:
            session.execute(text("""
                ALTER TABLE users 
                ADD COLUMN subscription_type VARCHAR(20) DEFAULT 'basic'
            """))
            logger.info("  ✅ 添加字段: subscription_type")
        else:
            logger.info("  ⏭️  字段已存在: subscription_type")
        
        # 添加 subscription_start_at 字段
        if 'subscription_start_at' not in existing_column_names:
            session.execute(text("""
                ALTER TABLE users 
                ADD COLUMN subscription_start_at TIMESTAMP
            """))
            logger.info("  ✅ 添加字段: subscription_start_at")
        else:
            logger.info("  ⏭️  字段已存在: subscription_start_at")
        
        # 添加 subscription_end_at 字段
        if 'subscription_end_at' not in existing_column_names:
            session.execute(text("""
                ALTER TABLE users 
                ADD COLUMN subscription_end_at TIMESTAMP
            """))
            logger.info("  ✅ 添加字段: subscription_end_at")
        else:
            logger.info("  ⏭️  字段已存在: subscription_end_at")
        
        # 添加 enabled_modules 字段
        if 'enabled_modules' not in existing_column_names:
            session.execute(text("""
                ALTER TABLE users 
                ADD COLUMN enabled_modules JSON DEFAULT '[]'
            """))
            logger.info("  ✅ 添加字段: enabled_modules")
        else:
            logger.info("  ⏭️  字段已存在: enabled_modules")
        
        # 添加 usage_stats 字段
        if 'usage_stats' not in existing_column_names:
            session.execute(text("""
                ALTER TABLE users 
                ADD COLUMN usage_stats JSON DEFAULT '{}'
            """))
            logger.info("  ✅ 添加字段: usage_stats")
        else:
            logger.info("  ⏭️  字段已存在: usage_stats")
        
        session.commit()
        
        # 2. 创建 skill_permissions 表
        logger.info("步骤 2/3: 创建 skill_permissions 表...")
        
        check_table_sql = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'skill_permissions'
            )
        """
        table_exists = session.execute(text(check_table_sql)).scalar()
        
        if not table_exists:
            session.execute(text("""
                CREATE TABLE skill_permissions (
                    id SERIAL PRIMARY KEY,
                    skill_name VARCHAR(50) UNIQUE NOT NULL,
                    skill_display_name VARCHAR(100) NOT NULL,
                    skill_category VARCHAR(50) NOT NULL,
                    required_subscription VARCHAR(20) NOT NULL,
                    enabled BOOLEAN DEFAULT TRUE,
                    description TEXT,
                    daily_limit INTEGER DEFAULT 0,
                    monthly_limit INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            logger.info("  ✅ 创建表: skill_permissions")
            
            # 添加索引
            session.execute(text("""
                CREATE INDEX idx_skill_permissions_skill_name ON skill_permissions(skill_name)
            """))
            session.execute(text("""
                CREATE INDEX idx_skill_permissions_required_subscription ON skill_permissions(required_subscription)
            """))
            logger.info("  ✅ 创建索引")
        else:
            logger.info("  ⏭️  表已存在: skill_permissions")
        
        session.commit()
        
        # 3. 初始化技能权限数据
        logger.info("步骤 3/3: 初始化技能权限数据...")
        
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
            
            session.commit()
        else:
            logger.info(f"  ⏭️  已有 {data_count} 条技能权限数据")
        
        logger.info("=" * 60)
        logger.info("✅ 数据库迁移完成！")
        logger.info("=" * 60)
        
        # 显示迁移结果
        display_migration_result()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 数据库迁移失败：{str(e)}")
        session.rollback()
        return False


def display_migration_result():
    """显示迁移结果"""
    session = get_db_session()
    
    # 显示 users 表结构
    logger.info("\n📊 Users 表结构：")
    columns_sql = """
        SELECT column_name, data_type, column_default 
        FROM information_schema.columns 
        WHERE table_name = 'users'
        AND column_name LIKE 'subscription%'
        ORDER BY ordinal_position
    """
    columns = session.execute(text(columns_sql)).fetchall()
    for col in columns:
        logger.info(f"  - {col[0]}: {col[1]} (默认: {col[2]})")
    
    # 显示 skill_permissions 表数据
    logger.info("\n📊 SkillPermissions 表数据：")
    skills_sql = """
        SELECT skill_name, skill_display_name, required_subscription, enabled
        FROM skill_permissions
        ORDER BY required_subscription, skill_name
    """
    skills = session.execute(text(skills_sql)).fetchall()
    for skill in skills:
        status = "✅" if skill[3] else "❌"
        logger.info(f"  {status} {skill[1]} ({skill[0]}) - 需要{skill[2]}套餐")
    
    # 显示用户数量和套餐分布
    logger.info("\n👥 用户套餐分布：")
    users_sql = """
        SELECT subscription_type, COUNT(*) as count
        FROM users
        GROUP BY subscription_type
        ORDER BY subscription_type
    """
    users = session.execute(text(users_sql)).fetchall()
    for user in users:
        plan_name = user[0] or "未设置"
        logger.info(f"  - {plan_name}: {user[1]} 个用户")


def rollback_migration():
    """回滚迁移（仅用于开发环境）"""
    logger.warning("=" * 60)
    logger.warning("⚠️  开始回滚数据库迁移...")
    logger.warning("=" * 60)
    
    session = get_db_session()
    
    try:
        # 删除 skill_permissions 表
        logger.info("删除 skill_permissions 表...")
        session.execute(text("DROP TABLE IF EXISTS skill_permissions"))
        
        # 删除 users 表的新字段
        logger.info("删除 users 表的新字段...")
        columns_to_drop = [
            'subscription_type',
            'subscription_start_at',
            'subscription_end_at',
            'enabled_modules',
            'usage_stats'
        ]
        
        for col in columns_to_drop:
            session.execute(text(f"""
                ALTER TABLE users 
                DROP COLUMN IF EXISTS {col}
            """))
            logger.info(f"  ✅ 删除字段: {col}")
        
        session.commit()
        
        logger.warning("=" * 60)
        logger.warning("✅ 数据库迁移已回滚！")
        logger.warning("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 回滚失败：{str(e)}")
        session.rollback()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库迁移工具')
    parser.add_argument('--rollback', action='store_true', help='回滚迁移')
    args = parser.parse_args()
    
    if args.rollback:
        success = rollback_migration()
    else:
        success = migrate_database()
    
    sys.exit(0 if success else 1)
