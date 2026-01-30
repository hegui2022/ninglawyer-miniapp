"""
提示词管理器
统一管理和访问所有提示词模板
"""

from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

# 导入律师提示词
from src.prompts.lawyers.civil import CIVIL_LAWYER_TEMPLATE, CIVIL_LAWYER_TEMPLATE_SIMPLE
from src.prompts.lawyers.criminal import CRIMINAL_LAWYER_TEMPLATE, CRIMINAL_LAWYER_TEMPLATE_SIMPLE
from src.prompts.lawyers.contract import CONTRACT_LAWYER_TEMPLATE, CONTRACT_LAWYER_TEMPLATE_SIMPLE
from src.prompts.lawyers.labor import LABOR_LAWYER_TEMPLATE, LABOR_LAWYER_TEMPLATE_SIMPLE
from src.prompts.lawyers.company import COMPANY_LAWYER_TEMPLATE, COMPANY_LAWYER_TEMPLATE_SIMPLE
from src.prompts.lawyers.ip import IP_LAWYER_TEMPLATE, IP_LAWYER_TEMPLATE_SIMPLE
from src.prompts.lawyers.marriage import MARRIAGE_LAWYER_TEMPLATE, MARRIAGE_LAWYER_TEMPLATE_SIMPLE

# 导入技能提示词
from src.prompts.skills.civil_consult import CIVIL_CONSULT_TEMPLATE
from src.prompts.skills.contract import CONTRACT_DRAFT_TEMPLATE, CONTRACT_REVIEW_TEMPLATE
from src.prompts.skills.desensitize import DESENSITIZE_TEMPLATE
from src.prompts.skills.master_brain import MASTER_BRAIN_TEMPLATE


class PromptManager:
    """提示词管理器 - 统一管理和访问所有提示词模板"""
    
    # 律师提示词映射
    _LAWYER_PROMPTS = {
        'civil': {
            'full': CIVIL_LAWYER_TEMPLATE,
            'simple': CIVIL_LAWYER_TEMPLATE_SIMPLE,
        },
        'criminal': {
            'full': CRIMINAL_LAWYER_TEMPLATE,
            'simple': CRIMINAL_LAWYER_TEMPLATE_SIMPLE,
        },
        'contract': {
            'full': CONTRACT_LAWYER_TEMPLATE,
            'simple': CONTRACT_LAWYER_TEMPLATE_SIMPLE,
        },
        'labor': {
            'full': LABOR_LAWYER_TEMPLATE,
            'simple': LABOR_LAWYER_TEMPLATE_SIMPLE,
        },
        'company': {
            'full': COMPANY_LAWYER_TEMPLATE,
            'simple': COMPANY_LAWYER_TEMPLATE_SIMPLE,
        },
        'ip': {
            'full': IP_LAWYER_TEMPLATE,
            'simple': IP_LAWYER_TEMPLATE_SIMPLE,
        },
        'marriage': {
            'full': MARRIAGE_LAWYER_TEMPLATE,
            'simple': MARRIAGE_LAWYER_TEMPLATE_SIMPLE,
        },
    }
    
    # 技能提示词映射
    _SKILL_PROMPTS = {
        'civil_consult': CIVIL_CONSULT_TEMPLATE,
        'contract_draft': CONTRACT_DRAFT_TEMPLATE,
        'contract_review': CONTRACT_REVIEW_TEMPLATE,
        'desensitize': DESENSITIZE_TEMPLATE,
        'master_brain': MASTER_BRAIN_TEMPLATE,
    }
    
    @classmethod
    def get_lawyer_prompt(cls, lawyer_type: str, simple: bool = False) -> Optional[ChatPromptTemplate]:
        """
        获取律师提示词
        
        Args:
            lawyer_type: 律师类型 (civil, criminal, contract, labor, company, ip, marriage)
            simple: 是否使用简化版（无聊天历史）
        
        Returns:
            ChatPromptTemplate 或 None
        """
        if lawyer_type not in cls._LAWYER_PROMPTS:
            logger.error(f"未知的律师类型：{lawyer_type}")
            return None
        
        template_key = 'simple' if simple else 'full'
        return cls._LAWYER_PROMPTS[lawyer_type][template_key]
    
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
    def list_lawyers(cls) -> list:
        """
        列出所有可用的律师类型
        
        Returns:
            律师类型列表
        """
        return list(cls._LAWYER_PROMPTS.keys())
    
    @classmethod
    def list_skills(cls) -> list:
        """
        列出所有可用的技能
        
        Returns:
            技能名称列表
        """
        return list(cls._SKILL_PROMPTS.keys())
    
    @classmethod
    def get_lawyer_names(cls) -> dict:
        """
        获取律师类型对应的中文名称
        
        Returns:
            律师类型与名称的映射
        """
        return {
            'civil': '宁律师·民事',
            'criminal': '宁律师·刑事',
            'contract': '宁律师·合同',
            'labor': '宁律师·劳动',
            'company': '宁律师·公司',
            'ip': '宁律师·知识产权',
            'marriage': '宁律师·婚姻',
        }
    
    @classmethod
    def validate_lawyer_type(cls, lawyer_type: str) -> bool:
        """
        验证律师类型是否有效
        
        Args:
            lawyer_type: 律师类型
        
        Returns:
            是否有效
        """
        return lawyer_type in cls._LAWYER_PROMPTS
    
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
