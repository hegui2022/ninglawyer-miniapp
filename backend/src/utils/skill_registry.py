"""
技能注册表
支持自动发现和手动注册，统一管理所有技能
"""

import os
import importlib
from typing import Dict, Callable, Any, Optional
from datetime import datetime
from loguru import logger
from .exception_handler import exception_handler, RouteError, SkillExecutionError, ExceptionLevel


class SkillRegistry:
    """
    技能注册表
    
    功能：
    - 自动扫描 skills/ 目录并注册技能（开发阶段）
    - 手动注册核心技能（生产阶段）
    - 执行技能（带异常处理）
    - 列出所有技能
    """
    
    def __init__(self):
        self.skills: Dict[str, Dict[str, Any]] = {}
        
        # 默认使用手动注册模式（避免循环导入）
        logger.info("📋 技能注册表初始化完成（手动注册模式）")
        logger.info("💡 提示：请通过 skills.register_all_skills() 注册技能")
    
    def auto_register(self):
        """自动扫描 skills/ 目录并注册技能"""
        import os.path
        
        skills_dir = os.path.join(os.path.dirname(__file__), "../skills")
        
        if not os.path.exists(skills_dir):
            logger.warning(f"⚠️ skills 目录不存在：{skills_dir}")
            return
        
        logger.info(f"🔍 正在扫描目录：{skills_dir}")
        
        for file in os.listdir(skills_dir):
            if file.endswith("_skill.py") and not file.startswith("__"):
                module_name = f"src.skills.{file[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    
                    # 查找以 execute_ 开头的函数
                    for name in dir(module):
                        if name.startswith("execute_") and callable(getattr(module, name)):
                            skill_name = name.replace("execute_", "")
                            skill_func = getattr(module, name)
                            
                            self.register_skill(
                                skill_name=skill_name,
                                skill_func=skill_func,
                                description=getattr(skill_func, "__doc__", skill_name),
                                category=self._infer_category(skill_name),
                                module=module_name
                            )
                
                except Exception as e:
                    logger.error(f"❌ 加载技能模块 {module_name} 失败：{e}")
        
        logger.info(f"✅ 自动注册完成，共注册 {len(self.skills)} 个技能")
    
    def _manual_register_core_skills(self):
        """手动注册核心技能（生产环境）"""
        # 婚姻家事技能
        core_skills = [
            ("divorce_procedure", "离婚流程说明", "family_law"),
            ("property_division", "财产分割计算", "family_law"),
            ("child_custody", "子女抚养权", "family_law"),
            ("domestic_violence", "家暴维权", "family_law"),
            ("alimony_calculation", "抚养费计算", "family_law"),
        ]
        
        for skill_name, description, category in core_skills:
            try:
                module_name = f"src.skills.{skill_name}_skill"
                module = importlib.import_module(module_name)
                skill_func = getattr(module, f"execute_{skill_name}")
                
                self.register_skill(
                    skill_name=skill_name,
                    skill_func=skill_func,
                    description=description,
                    category=category,
                    module=module_name
                )
            
            except Exception as e:
                logger.error(f"❌ 注册技能 {skill_name} 失败：{e}")
        
        logger.info(f"✅ 手动注册完成，共注册 {len(self.skills)} 个核心技能")
    
    def register_skill(
        self,
        skill_name: str,
        skill_func: Callable,
        description: str = "",
        category: str = "general",
        module: str = "",
        tags: list = None
    ):
        """
        注册技能
        
        Args:
            skill_name: 技能名称
            skill_func: 技能函数
            description: 技能描述
            category: 技能分类
            module: 所属模块
            tags: 技能标签
        """
        self.skills[skill_name] = {
            "func": skill_func,
            "description": description,
            "category": category,
            "module": module,
            "tags": tags or [],
            "registered_at": datetime.now().isoformat()
        }
        logger.info(f"✅ 注册技能：{skill_name} ({description}) [{category}]")
    
    @exception_handler(
        default_return={"success": False, "reply": "抱歉，我暂时还不了解这个问题～"},
        log_level=ExceptionLevel.ERROR
    )
    def execute(self, skill_name: str, user_input: str, context: dict) -> dict:
        """
        执行技能
        
        Args:
            skill_name: 技能名称
            user_input: 用户输入
            context: 上下文信息
        
        Returns:
            执行结果
        """
        if skill_name not in self.skills:
            logger.warning(f"⚠️ 技能不存在：{skill_name}")
            raise RouteError(f"技能不存在：{skill_name}")
        
        skill_info = self.skills[skill_name]
        logger.info(f"🚀 执行技能：{skill_name}")
        
        try:
            result = skill_info["func"](user_input, context)
            logger.info(f"✅ 技能执行完成：{skill_name}")
            return result
        
        except Exception as e:
            logger.error(f"❌ 技能执行异常：{skill_name} - {e}")
            raise SkillExecutionError(f"技能 {skill_name} 执行失败：{e}")
    
    def list_skills(self, category: str = None) -> Dict[str, Dict[str, Any]]:
        """
        列出所有技能
        
        Args:
            category: 筛选分类，None表示全部
        
        Returns:
            技能列表
        """
        if category:
            return {
                name: skill
                for name, skill in self.skills.items()
                if skill.get("category") == category
            }
        return self.skills.copy()
    
    def get_skill_info(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        获取技能信息
        
        Args:
            skill_name: 技能名称
        
        Returns:
            技能信息
        """
        return self.skills.get(skill_name)
    
    def skill_exists(self, skill_name: str) -> bool:
        """
        检查技能是否存在
        
        Args:
            skill_name: 技能名称
        
        Returns:
            是否存在
        """
        return skill_name in self.skills
    
    def _infer_category(self, skill_name: str) -> str:
        """
        推断技能分类
        
        Args:
            skill_name: 技能名称
        
        Returns:
            分类名称
        """
        category_map = {
            "divorce": "family_law",
            "property": "family_law",
            "child": "family_law",
            "custody": "family_law",
            "domestic": "family_law",
            "violence": "family_law",
            "alimony": "family_law",
            "contract": "commercial",
            "company": "commercial",
            "compliance": "compliance",
        }
        
        for keyword, category in category_map.items():
            if keyword in skill_name:
                return category
        
        return "general"


# 全局实例
skill_registry = SkillRegistry()


# 导出
__all__ = [
    'SkillRegistry',
    'skill_registry',
]
