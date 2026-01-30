"""
服务注册表（Skill Registry）
用于注册和管理所有技能模块
"""

from typing import Dict, Callable, Any, Optional
from loguru import logger
from src.config.subscription import check_permission


class SkillRegistry:
    """技能注册表"""
    
    def __init__(self):
        self._skills: Dict[str, Dict[str, Any]] = {}
        self._db_session = None  # 数据库会话，用于权限检查
        logger.info("📋 技能注册表初始化完成")
    
    def set_db_session(self, db_session):
        """设置数据库会话"""
        self._db_session = db_session
    
    def register(self, 
                 skill_name: str,
                 description: str,
                 execute_func: Callable,
                 category: str = "general",
                 required_subscription: str = "basic"):
        """
        注册技能
        
        Args:
            skill_name: 技能名称
            description: 技能描述
            execute_func: 技能执行函数
            category: 技能分类
            required_subscription: 需要的套餐类型
        """
        self._skills[skill_name] = {
            "name": skill_name,
            "description": description,
            "execute": execute_func,
            "category": category,
            "required_subscription": required_subscription
        }
        logger.info(f"✅ 注册技能：{skill_name} ({category}) - 需要{required_subscription}套餐")
    
    def get_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
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
    
    def check_user_permission(self, skill_name: str, user_id: Optional[int] = None, 
                             user_subscription: Optional[str] = None) -> Dict[str, Any]:
        """
        检查用户是否有权限使用某个技能
        
        Args:
            skill_name: 技能名称
            user_id: 用户ID
            user_subscription: 用户套餐类型（可选，如果不传则通过user_id查询）
        
        Returns:
            检查结果：{"has_permission": bool, "error": str}
        """
        skill = self.get_skill(skill_name)
        if not skill:
            return {
                "has_permission": False,
                "error": f"技能不存在：{skill_name}"
            }
        
        # 如果没有提供用户订阅信息，尝试从数据库查询
        if not user_subscription and user_id and self._db_session:
            try:
                from src.models.models import User
                user = self._db_session.query(User).filter(User.id == user_id).first()
                if user:
                    user_subscription = user.subscription_type
            except Exception as e:
                logger.error(f"查询用户套餐失败：{str(e)}")
                user_subscription = "basic"  # 默认基础版
        
        # 如果还是没有订阅信息，默认为基础版
        if not user_subscription:
            user_subscription = "basic"
        
        # 检查权限
        if check_permission(user_subscription, skill["required_subscription"]):
            return {
                "has_permission": True,
                "error": None
            }
        else:
            return {
                "has_permission": False,
                "error": f"您没有权限使用此功能，需要{skill['required_subscription']}套餐或更高",
                "required_subscription": skill["required_subscription"]
            }
    
    def execute_skill(self, skill_name: str, user_id: Optional[int] = None, 
                     user_subscription: Optional[str] = None, *args, **kwargs) -> Any:
        """
        执行技能（带权限检查）
        
        Args:
            skill_name: 技能名称
            user_id: 用户ID（用于权限检查）
            user_subscription: 用户套餐类型（用于权限检查）
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
        
        # 权限检查
        permission_check = self.check_user_permission(skill_name, user_id, user_subscription)
        if not permission_check["has_permission"]:
            logger.warning(f"⚠️ 用户无权限使用技能：{skill_name}")
            return {
                "success": False,
                "error": permission_check["error"],
                "upgrade_required": True,
                "required_subscription": skill.get("required_subscription", "premium")
            }
        
        # 执行技能
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
