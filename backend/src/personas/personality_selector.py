"""
人设选择器
根据用户类型和场景动态选择宁律师的人设，实现千人千面
"""

import os
from typing import Dict, Any
from loguru import logger

# 导入人设配置
from .warm_personal import WARM_PERSONALITY
from .professional_personal import PROFESSIONAL_PERSONALITY
from .business_corporate import BUSINESS_CORPORATE


class PersonalitySelector:
    """人设选择器"""
    
    def __init__(self):
        # 人设映射表
        self.personality_map = {
            "personal": {  # 个人用户
                "family_law": "warm_personal",  # 婚姻家事 → 温暖陪伴型
                "commercial": "professional_personal",  # 商事场景 → 专业严谨型
                "compliance": "professional_personal",  # 合规场景 → 专业严谨型
                "general": "warm_personal"  # 默认场景 → 温暖陪伴型
            },
            "corporate": {  # 企业用户
                "family_law": "professional_personal",  # 企业员工的婚姻问题 → 专业严谨型
                "commercial": "business_corporate",  # 企业商事 → 企业商务型
                "compliance": "business_corporate",  # 企业合规 → 企业商务型
                "general": "business_corporate"  # 默认场景 → 企业商务型
            }
        }
        
        logger.info("🎭 人设选择器初始化完成")
    
    def select(
        self,
        user_type: str = "personal",
        scenario: str = "general",
        force_personality: str = None,
        app_id: str = None
    ) -> str:
        """
        根据用户类型、场景和小程序选择人设
        
        Args:
            user_type: 用户类型 ("personal" | "corporate")
            scenario: 场景类型 ("family_law" | "commercial" | "compliance" | "general")
            force_personality: 强制指定人设（用于测试或特殊场景）
            app_id: 小程序标识（用于调整人设策略）
        
        Returns:
            人设ID
        """
        # 如果强制指定人设，直接返回
        if force_personality:
            logger.info(f"🎭 强制使用人设：{force_personality}")
            return force_personality
        
        # 根据小程序标识调整人设策略
        if app_id:
            # 文本脱敏小程序使用专业严谨型
            if app_id == 'miniprogram_desensitize':
                logger.info(f"🎭 小程序专用人设：{app_id} → 专业严谨型")
                return "professional_personal"
        
        # 获取人设
        try:
            personality_id = self.personality_map[user_type][scenario]
            logger.info(f"🎭 选择人设：用户类型={user_type}, 场景={scenario}, 小程序={app_id}, 人设={personality_id}")
            return personality_id
        except KeyError:
            # 如果找不到对应人设，返回默认人设
            default_personality = "warm_personal" if user_type == "personal" else "business_corporate"
            logger.warning(f"⚠️ 未找到人设映射：user_type={user_type}, scenario={scenario}，使用默认人设：{default_personality}")
            return default_personality
    
    def get_personality(self, personality_id: str) -> Dict[str, Any]:
        """
        获取人设配置
        
        Args:
            personality_id: 人设ID
        
        Returns:
            人设配置字典
        """
        personality_map = {
            "warm_personal": WARM_PERSONALITY,
            "professional_personal": PROFESSIONAL_PERSONALITY,
            "business_corporate": BUSINESS_CORPORATE,
        }
        
        personality = personality_map.get(personality_id)
        
        if personality:
            return personality
        else:
            logger.error(f"❌ 人设不存在：{personality_id}")
            return WARM_PERSONALITY  # 默认返回温暖陪伴型
    
    def list_personalities(self) -> Dict[str, Dict[str, Any]]:
        """
        列出所有可用的人设
        
        Returns:
            人设列表
        """
        personalities = {}
        
        try:
            personalities["warm_personal"] = self.get_personality("warm_personal")
        except Exception as e:
            logger.error(f"加载温暖陪伴型人设失败：{e}")
        
        # 阶段2补充其他 人设
        
        return personalities


# 全局实例
personality_selector = PersonalitySelector()
