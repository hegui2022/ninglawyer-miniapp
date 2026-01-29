"""
服务注册表（Skill Registry）
用于注册和管理所有技能模块
"""

from typing import Dict, Callable, Any
from loguru import logger


class SkillRegistry:
    """技能注册表"""
    
    def __init__(self):
        self._skills: Dict[str, Dict[str, Any]] = {}
        logger.info("📋 技能注册表初始化完成")
    
    def register(self, 
                 skill_name: str,
                 description: str,
                 execute_func: Callable,
                 category: str = "general"):
        """
        注册技能
        
        Args:
            skill_name: 技能名称
            description: 技能描述
            execute_func: 技能执行函数
            category: 技能分类
        """
        self._skills[skill_name] = {
            "name": skill_name,
            "description": description,
            "execute": execute_func,
            "category": category
        }
        logger.info(f"✅ 注册技能：{skill_name} ({category})")
    
    def get_skill(self, skill_name: str) -> Dict[str, Any]:
        """获取技能"""
        skill = self._skills.get(skill_name)
        if skill:
            return skill
        else:
            logger.warning(f"⚠️ 未找到技能：{skill_name}")
            return None
    
    def list_skills(self, category: str = None) -> Dict[str, Dict[str, Any]]:
        """
        列出所有技能
        
        Args:
            category: 筛选分类，None表示全部
        """
        if category:
            return {
                name: skill 
                for name, skill in self._skills.items() 
                if skill["category"] == category
            }
        return self._skills.copy()
    
    def execute_skill(self, skill_name: str, *args, **kwargs) -> Any:
        """
        执行技能
        
        Args:
            skill_name: 技能名称
            *args, **kwargs: 技能参数
            
        Returns:
            技能执行结果
        """
        skill = self.get_skill(skill_name)
        if not skill:
            return {
                "success": False,
                "error": f"未找到技能：{skill_name}"
            }
        
        try:
            logger.info(f"🔧 执行技能：{skill_name}")
            result = skill["execute"](*args, **kwargs)
            logger.info(f"✅ 技能执行完成：{skill_name}")
            return result
        except Exception as e:
            logger.error(f"❌ 技能执行失败：{skill_name} - {str(e)}")
            return {
                "success": False,
                "error": f"技能执行错误：{str(e)}"
            }


# 全局技能注册表实例
skill_registry = SkillRegistry()
