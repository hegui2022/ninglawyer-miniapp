"""
环境变量配置
验证和管理环境变量
"""

import os
from typing import List, Dict, Any
from loguru import logger

# 必需的环境变量
REQUIRED_ENV_VARS = [
    'JWT_SECRET_KEY',
    'DATABASE_URL',
]

# 可选的环境变量（有默认值）
OPTIONAL_ENV_VARS = {
    'FLASK_HOST': '0.0.0.0',
    'FLASK_PORT': '5000',
    'FLASK_DEBUG': 'False',
    'LOG_LEVEL': 'INFO',
    'LOG_FILE': 'logs/app.log',
    'ALLOWED_ORIGINS': '*',
}

# 敏感环境变量（不应该出现在日志中）
SENSITIVE_ENV_VARS = [
    'JWT_SECRET_KEY',
    'DATABASE_URL',
    'API_KEY',
    'SECRET_KEY',
    'PASSWORD',
    'TOKEN',
]


def check_required_env_vars() -> bool:
    """
    检查必需的环境变量是否存在
    
    Returns:
        是否所有必需的环境变量都已配置
    """
    missing_vars = []
    
    for var in REQUIRED_ENV_VARS:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ 缺少必需的环境变量: {', '.join(missing_vars)}")
        return False
    
    logger.info("✅ 所有必需的环境变量已配置")
    return True


def get_env_config() -> Dict[str, Any]:
    """
    获取环境配置
    
    Returns:
        配置字典
    """
    config = {}
    
    # 必需环境变量
    for var in REQUIRED_ENV_VARS:
        config[var] = os.getenv(var)
    
    # 可选环境变量
    for var, default_value in OPTIONAL_ENV_VARS.items():
        value = os.getenv(var, default_value)
        
        # 转换类型
        if var in ['FLASK_PORT']:
            value = int(value)
        elif var in ['FLASK_DEBUG']:
            value = value.lower() in ['true', '1', 'yes']
        
        config[var] = value
    
    return config


def log_config() -> None:
    """
    记录配置信息（脱敏敏感信息）
    """
    config = get_env_config()
    
    logger.info("=" * 60)
    logger.info("环境配置信息")
    logger.info("=" * 60)
    
    for key, value in config.items():
        if key in SENSITIVE_ENV_VARS:
            # 脱敏处理
            masked_value = '*' * min(len(str(value)), 10)
            logger.info(f"{key}: {masked_value}")
        else:
            logger.info(f"{key}: {value}")
    
    logger.info("=" * 60)
