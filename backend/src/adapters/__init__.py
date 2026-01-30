"""
数据适配器模块（Data Adapters）
负责将第三方API返回的数据转换为前端需要的格式
"""

from .base_adapter import DataAdapterBase
from .legal_knowledge_adapter import LegalKnowledgeAdapter, get_legal_knowledge_adapter

__all__ = [
    "DataAdapterBase",
    "LegalKnowledgeAdapter",
    "get_legal_knowledge_adapter"
]
