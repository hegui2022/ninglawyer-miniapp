"""
提示词管理器
统一管理和访问所有提示词模板
新架构：仅管理技能提示词，不再管理独立的律师提示词
"""

from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

# 导入技能提示词
from prompts.skills.civil_consult import CIVIL_CONSULT_TEMPLATE
from prompts.skills.contract import CONTRACT_DRAFT_TEMPLATE, CONTRACT_REVIEW_TEMPLATE
from prompts.skills.desensitize import DESENSITIZE_TEMPLATE
from prompts.skills.master_brain import MASTER_BRAIN_TEMPLATE


class PromptManager:
    """提示词管理器 - 统一管理和访问所有提示词模板（新架构）"""
    
    # 技能提示词映射
    _SKILL_PROMPTS = {
        'civil_consult': CIVIL_CONSULT_TEMPLATE,
        'contract_draft': CONTRACT_DRAFT_TEMPLATE,
        'contract_review': CONTRACT_REVIEW_TEMPLATE,
        'desensitize': DESENSITIZE_TEMPLATE,
        'master_brain': MASTER_BRAIN_TEMPLATE,
    }
    
    @classmethod
    def get_skill_prompt(cls, skill_name: str) -> Optional[ChatPromptTemplate]:
        """
        获取技能提示词
        
        Args:
            skill_name: 技能名称 (civil_consult, contract_draft, contract_review, desensitize)
        
        Returns:
            ChatPromptTemplate 或 None
        """
        if skill_name not in cls._SKILL_PROMPTS:
            logger.error(f"未知的技能名称：{skill_name}")
            return None
        
        return cls._SKILL_PROMPTS[skill_name]
    
    @classmethod
    def list_skills(cls) -> list:
        """
        列出所有可用的技能
        
        Returns:
            技能名称列表
        """
        return list(cls._SKILL_PROMPTS.keys())
    
    @classmethod
    def validate_skill_name(cls, skill_name: str) -> bool:
        """
        验证技能名称是否有效
        
        Args:
            skill_name: 技能名称
        
        Returns:
            是否有效
        """
        return skill_name in cls._SKILL_PROMPTS


# 导出全局实例
prompt_manager = PromptManager()


__all__ = [
    'PromptManager',
    'prompt_manager',
]
