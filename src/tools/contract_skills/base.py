"""
基础技能类
Base Skill Class
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseSkill(ABC):
    """技能基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def generate(self, info: Dict[str, Any]) -> str:
        """
        生成合同条款
        
        Args:
            info: 用户信息字典
            
        Returns:
            生成的合同条款文本
        """
        pass
    
    @abstractmethod
    def get_required_fields(self) -> list:
        """
        获取该技能所需的必填字段
        
        Returns:
            必填字段列表
        """
        pass
    
    @abstractmethod
    def get_prompt_template(self) -> str:
        """
        获取收集信息的提示模板
        
        Returns:
            提示模板
        """
        pass
