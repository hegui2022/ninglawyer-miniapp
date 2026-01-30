"""
扣子技能服务（Coze Skill Service）
提供调用扣子平台技能的API接口
基于BaseThirdPartyAPIService基类实现
"""

from typing import Dict, Any, Optional
from loguru import logger

from .base_service import BaseThirdPartyAPIService


class CozeSkillService(BaseThirdPartyAPIService):
    """扣子技能服务（继承基础服务类）"""
    
    def __init__(self, access_token: str = None):
        """
        初始化技能服务
        
        Args:
            access_token: 访问令牌（可选）
        """
        # 使用占位符初始化
        api_key = access_token or "ACCESS_TOKEN"
        base_url = "https://api.coze.cn"
        
        super().__init__(api_key=api_key, base_url=base_url, timeout=60)
        
        logger.info("🎯 扣子技能服务初始化完成")
    
    def call_skill(
        self,
        skill_id: str,
        skill_params: Dict[str, Any],
        user_id: str = "default",
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        调用技能
        
        Args:
            skill_id: 技能ID
            skill_params: 技能参数
            user_id: 用户ID
            conversation_id: 会话ID（可选）
            
        Returns:
            技能执行结果
        """
        # 构建请求数据
        data = {
            "skill_id": skill_id,
            "parameters": skill_params,
            "user": user_id
        }
        
        if conversation_id:
            data["conversation_id"] = conversation_id
        
        logger.info(f"🎯 调用技能 ID: {skill_id}, 用户: {user_id}")
        
        # 调用基础请求方法
        result = self._request(
            method="POST",
            path="/v1/skill/call",
            json=data
        )
        
        # 格式化返回结果
        if result.get("success"):
            data = result.get("data", {})
            result["data"] = self._format_skill_result(data)
        
        return result
    
    def get_skill_info(self, skill_id: str) -> Dict[str, Any]:
        """
        获取技能信息
        
        Args:
            skill_id: 技能ID
            
        Returns:
            技能信息
        """
        params = {"skill_id": skill_id}
        
        result = self._request(
            method="GET",
            path="/v1/skill/info",
            params=params
        )
        
        return result
    
    def list_skills(self, page_size: int = 20) -> Dict[str, Any]:
        """
        获取技能列表
        
        Args:
            page_size: 每页数量
            
        Returns:
            技能列表
        """
        params = {"page_size": page_size}
        
        result = self._request(
            method="GET",
            path="/v1/skill/list",
            params=params
        )
        
        return result
    
    def _format_skill_result(self, data: Dict) -> Dict[str, Any]:
        """
        格式化技能结果
        
        Args:
            data: 原始数据
            
        Returns:
            格式化后的结果
        """
        return {
            "skill_id": data.get("skill_id", ""),
            "result": data.get("result", {}),
            "execution_time": data.get("execution_time", 0),
            "error": data.get("error", None)
        }


# 全局实例（单例）
_coze_skill_service = None


def get_coze_skill_service(access_token: str = None) -> CozeSkillService:
    """
    获取扣子技能服务实例（单例模式）
    
    Args:
        access_token: Access Token（可选）
        
    Returns:
        CozeSkillService 实例
    """
    global _coze_skill_service
    
    if _coze_skill_service is None:
        _coze_skill_service = CozeSkillService(access_token)
    elif access_token:
        _coze_skill_service.set_api_key(access_token)
    
    return _coze_skill_service


# 导出
__all__ = [
    "CozeSkillService",
    "get_coze_skill_service"
]
