"""
Lawyer Agent Factory - 宁律师工厂
负责创建和管理所有宁律师 AGENT
"""

from typing import Dict, Any, Optional
from loguru import logger

from utils.logger import log_function_call
from config.lawyer_domains import (
    CIVIL_LAWYER_CONFIG,
    CRIMINAL_LAWYER_CONFIG,
    CONTRACT_LAWYER_CONFIG,
    LABOR_LAWYER_CONFIG,
    COMPANY_LAWYER_CONFIG,
    IP_LAWYER_CONFIG,
    MARRIAGE_LAWYER_CONFIG
)


class LawyerAgentFactory:
    """宁律师工厂 - 负责创建不同领域的宁律师"""
    
    def __init__(self):
        """初始化宁律师工厂"""
        self._lawyer_cache = {}
        self.domain_configs = {
            'civil': CIVIL_LAWYER_CONFIG,
            'criminal': CRIMINAL_LAWYER_CONFIG,
            'contract': CONTRACT_LAWYER_CONFIG,
            'labor': LABOR_LAWYER_CONFIG,
            'company': COMPANY_LAWYER_CONFIG,
            'ip': IP_LAWYER_CONFIG,
            'marriage': MARRIAGE_LAWYER_CONFIG
        }
        
        logger.info("宁律师工厂初始化完成")
    
    @log_function_call
    def create_lawyer(self, domain: str):
        """
        创建宁律师
        
        Args:
            domain: 法律领域
        
        Returns:
            宁律师实例
        """
        if domain not in self.domain_configs:
            logger.error(f"未知的法律领域：{domain}")
            raise ValueError(f"Unknown domain: {domain}")
        
        config = self.domain_configs[domain]
        
        # 动态导入宁律师模板
        from src.agents.ning_lawyer_template import NingLawyerTemplate
        lawyer = NingLawyerTemplate(config)
        
        logger.info(f"创建宁律师：{domain}")
        return lawyer
    
    @log_function_call
    def get_lawyer(self, domain: str):
        """
        获取宁律师（带缓存）
        
        Args:
            domain: 法律领域
        
        Returns:
            宁律师实例
        """
        if domain not in self._lawyer_cache:
            self._lawyer_cache[domain] = self.create_lawyer(domain)
        
        return self._lawyer_cache[domain]
    
    @log_function_call
    def list_lawyers(self) -> list:
        """
        列出所有宁律师
        
        Returns:
            宁律师列表
        """
        lawyers = []
        for domain, config in self.domain_configs.items():
            lawyers.append({
                'domain': domain,
                'id': config.get('persona', {}).get('name', ''),
                'name': config.get('persona', {}).get('name', ''),
                'icon': config.get('persona', {}).get('avatar', ''),
                'description': config.get('description', config.get('persona', {}).get('system_prompt', '')[:100]),
                'helpCount': config.get('helpCount', 0),
                'rating': config.get('rating', 0),
                'consultCount': config.get('consultCount', 0)
            })
        
        return lawyers
    
    @log_function_call
    def get_lawyer_info(self, domain: str) -> Optional[Dict[str, Any]]:
        """
        获取宁律师信息
        
        Args:
            domain: 法律领域
        
        Returns:
            宁律师信息
        """
        if domain not in self.domain_configs:
            return None
        
        config = self.domain_configs[domain]
        
        return {
            'domain': domain,
            'id': config['persona']['name'],
            'name': config['persona']['name'],
            'icon': config['persona']['avatar'],
            'fullName': config['persona']['name'],
            'description': config.get('description', config['persona']['system_prompt'][:100]),
            'domainType': config['domain'],
            'helpCount': config.get('helpCount', 0),
            'rating': config.get('rating', 0),
            'consultCount': config.get('consultCount', 0),
            'skills': [
                {
                    'id': skill,
                    'name': skill.replace('_', ' ').title(),
                    'description': f"{skill} 服务"
                }
                for skill in config.get('skills', [])
            ],
            'expertise': config.get('expertise', []),
            'reviews': config.get('reviews', [])
        }
    
    @log_function_call
    def clear_cache(self):
        """清除缓存"""
        self._lawyer_cache.clear()
        logger.info("宁律师缓存已清除")
