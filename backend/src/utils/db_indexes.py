"""
数据库索引配置
为高频查询字段添加索引
"""

from sqlalchemy import Index, DDL
from sqlalchemy.engine import Engine
from loguru import logger


def create_indexes(engine: Engine):
    """
    创建数据库索引
    
    Args:
        engine: 数据库引擎
    """
    logger.info("🔍 开始创建数据库索引...")
    
    try:
        with engine.connect() as conn:
            # 用户表索引 (users)
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_users_openid ON users(openid)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_users_unionid ON users(unionid)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_users_subscription ON users(subscription_type)"
            ))
            
            # 会话表索引 (sessions)
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_sessions_skill_type ON sessions(skill_type)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_sessions_user_skill ON sessions(user_id, skill_type)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at)"
            ))
            
            # 消息表索引 (messages)
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_messages_role ON messages(role)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at)"
            ))
            
            # 咨询记录表索引 (consultation_records)
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_consultation_records_user_id ON consultation_records(user_id)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_consultation_records_session_id ON consultation_records(session_id)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_consultation_records_domain ON consultation_records(domain)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_consultation_records_created_at ON consultation_records(created_at)"
            ))
            
            # 合同记录表索引 (contract_records)
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_contract_records_user_id ON contract_records(user_id)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_contract_records_session_id ON contract_records(session_id)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_contract_records_type ON contract_records(contract_type)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_contract_records_action ON contract_records(action)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_contract_records_created_at ON contract_records(created_at)"
            ))
            
            # 脱敏记录表索引 (desensitize_records)
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_desensitize_records_user_id ON desensitize_records(user_id)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_desensitize_records_session_id ON desensitize_records(session_id)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_desensitize_records_created_at ON desensitize_records(created_at)"
            ))
            
            # 文件记录表索引 (file_records)
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_file_records_user_id ON file_records(user_id)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_file_records_type ON file_records(file_type)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_file_records_related ON file_records(related_type, related_id)"
            ))
            conn.execute(DDL(
                "CREATE INDEX IF NOT EXISTS idx_file_records_created_at ON file_records(created_at)"
            ))
            
            logger.info("✅ 数据库索引创建完成")
    
    except Exception as e:
        logger.error(f"❌ 创建数据库索引失败: {e}")


# 索引配置说明
INDEX_DOCUMENTATION = """
# 数据库索引配置说明

## 用户表 (users)
- idx_users_openid: 微信openid索引（加速用户查询）
- idx_users_unionid: 微信unionid索引（加速用户查询）
- idx_users_phone: 手机号索引（加速用户查询）
- idx_users_subscription: 套餐类型索引（加速套餐筛选）

## 会话表 (sessions)
- idx_sessions_user_id: 用户ID索引（加速用户会话查询）
- idx_sessions_skill_type: 技能类型索引（加速技能统计）
- idx_sessions_user_skill: 组合索引（加速用户+技能查询）
- idx_sessions_created_at: 创建时间索引（加速时间范围查询）

## 消息表 (messages)
- idx_messages_session_id: 会话ID索引（加速消息查询）
- idx_messages_role: 角色索引（加速消息筛选）
- idx_messages_created_at: 创建时间索引（加速时间范围查询）

## 咨询记录表 (consultation_records)
- idx_consultation_records_user_id: 用户ID索引（加速用户记录查询）
- idx_consultation_records_session_id: 会话ID索引（加速会话记录查询）
- idx_consultation_records_domain: 法律领域索引（加速领域统计）
- idx_consultation_records_created_at: 创建时间索引（加速时间范围查询）

## 合同记录表 (contract_records)
- idx_contract_records_user_id: 用户ID索引（加速用户合同查询）
- idx_contract_records_session_id: 会话ID索引（加速会话合同查询）
- idx_contract_records_type: 合同类型索引（加速类型筛选）
- idx_contract_records_action: 操作类型索引（加速操作筛选）
- idx_contract_records_created_at: 创建时间索引（加速时间范围查询）

## 脱敏记录表 (desensitize_records)
- idx_desensitize_records_user_id: 用户ID索引（加速用户记录查询）
- idx_desensitize_records_session_id: 会话ID索引（加速会话记录查询）
- idx_desensitize_records_created_at: 创建时间索引（加速时间范围查询）

## 文件记录表 (file_records)
- idx_file_records_user_id: 用户ID索引（加速用户文件查询）
- idx_file_records_type: 文件类型索引（加速类型筛选）
- idx_file_records_related: 关联类型和ID索引（加速关联查询）
- idx_file_records_created_at: 创建时间索引（加速时间范围查询）
"""

