"""
配置加载工具
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any

# 加载 .env 文件
load_dotenv()


def load_config() -> Dict[str, Any]:
    """
    加载配置
    
    Returns:
        配置字典
    """
    return {
        # API 配置
        'API_HOST': os.getenv('API_HOST', 'localhost'),
        'API_PORT': int(os.getenv('API_PORT', '8080')),
        'API_DEBUG': os.getenv('API_DEBUG', 'True').lower() == 'true',
        
        # 数据库配置
        'DB_HOST': os.getenv('DB_HOST', 'localhost'),
        'DB_PORT': int(os.getenv('DB_PORT', '5432')),
        'DB_NAME': os.getenv('DB_NAME', 'ninglawyer'),
        'DB_USER': os.getenv('DB_USER', 'postgres'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD', ''),
        
        # 向量数据库配置
        'VECTOR_DB_HOST': os.getenv('VECTOR_DB_HOST', 'localhost'),
        'VECTOR_DB_PORT': int(os.getenv('VECTOR_DB_PORT', '19530')),
        'VECTOR_DB_NAME': os.getenv('VECTOR_DB_NAME', 'ninglawyer_kb'),
        
        # 图数据库配置
        'GRAPH_DB_HOST': os.getenv('GRAPH_DB_HOST', 'localhost'),
        'GRAPH_DB_PORT': int(os.getenv('GRAPH_DB_PORT', '7687')),
        'GRAPH_DB_USER': os.getenv('GRAPH_DB_USER', 'neo4j'),
        'GRAPH_DB_PASSWORD': os.getenv('GRAPH_DB_PASSWORD', ''),
        
        # Redis 配置
        'REDIS_HOST': os.getenv('REDIS_HOST', 'localhost'),
        'REDIS_PORT': int(os.getenv('REDIS_PORT', '6379')),
        'REDIS_DB': int(os.getenv('REDIS_DB', '0')),
        'REDIS_PASSWORD': os.getenv('REDIS_PASSWORD', ''),
        
        # 对象存储配置
        'S3_ENDPOINT': os.getenv('S3_ENDPOINT', ''),
        'S3_ACCESS_KEY': os.getenv('S3_ACCESS_KEY', ''),
        'S3_SECRET_KEY': os.getenv('S3_SECRET_KEY', ''),
        'S3_BUCKET': os.getenv('S3_BUCKET', 'ninglawyer'),
        
        # 模型配置
        'MODEL_API_KEY': os.getenv('MODEL_API_KEY', ''),
        'MODEL_BASE_URL': os.getenv('MODEL_BASE_URL', ''),
        'MODEL_NAME': os.getenv('MODEL_NAME', 'doubao-seed-1-6-251015'),
        'MODEL_TEMPERATURE': float(os.getenv('MODEL_TEMPERATURE', '0.7')),
        
        # 语音服务配置
        'VOICE_API_KEY': os.getenv('VOICE_API_KEY', ''),
        'VOICE_BASE_URL': os.getenv('VOICE_BASE_URL', ''),
        
        # 小程序配置
        'MINIPROGRAM_APPID': os.getenv('MINIPROGRAM_APPID', ''),
        'MINIPROGRAM_SECRET': os.getenv('MINIPROGRAM_SECRET', ''),
        
        # 日志配置
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
        'LOG_FILE': os.getenv('LOG_FILE', '/app/work/logs/bypass/app.log'),
    }


# 全局配置实例
config = load_config()


def get_config() -> Dict[str, Any]:
    """
    获取配置实例
    
    Returns:
        配置字典
    """
    return config
