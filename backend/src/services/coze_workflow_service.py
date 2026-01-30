"""
扣子工作流服务（Coze Workflow Service）
提供调用扣子平台工作流的API接口
基于BaseThirdPartyAPIService基类实现
"""

from typing import Dict, Any, Optional
from loguru import logger

from .base_service import BaseThirdPartyAPIService


class CozeWorkflowService(BaseThirdPartyAPIService):
    """扣子工作流服务（继承基础服务类）"""
    
    def __init__(self, access_token: str = None):
        """
        初始化工作流服务
        
        Args:
            access_token: 访问令牌（可选）
        """
        # 使用占位符初始化
        api_key = access_token or "ACCESS_TOKEN"
        base_url = "https://api.coze.cn"
        
        super().__init__(api_key=api_key, base_url=base_url, timeout=60)
        
        logger.info("⚙️ 扣子工作流服务初始化完成")
    
    def run_workflow(
        self,
        workflow_id: str,
        params: Dict[str, Any],
        stream: bool = False,
        user_id: str = "default"
    ) -> Dict[str, Any]:
        """
        运行工作流
        
        Args:
            workflow_id: 工作流ID
            params: 工作流参数
            stream: 是否流式返回
            user_id: 用户ID
            
        Returns:
            工作流执行结果
        """
        # 构建请求数据
        data = {
            "workflow_id": workflow_id,
            "parameters": params,
            "user": user_id,
            "stream": stream
        }
        
        logger.info(f"⚙️ 运行工作流 ID: {workflow_id}, 用户: {user_id}")
        
        # 调用基础请求方法
        result = self._request(
            method="POST",
            path="/v1/workflow/run",
            json=data
        )
        
        # 格式化返回结果
        if result.get("success"):
            data = result.get("data", {})
            result["data"] = self._format_workflow_result(data)
        
        return result
    
    def run_workflow_stream(
        self,
        workflow_id: str,
        params: Dict[str, Any],
        user_id: str = "default"
    ):
        """
        流式运行工作流
        
        Args:
            workflow_id: 工作流ID
            params: 工作流参数
            user_id: 用户ID
            
        Yields:
            流式响应数据块
        """
        import requests
        
        url = f"{self.base_url}/v1/workflow/run"
        headers = self.headers
        
        data = {
            "workflow_id": workflow_id,
            "parameters": params,
            "user": user_id,
            "stream": True
        }
        
        try:
            logger.info(f"⚙️ 流式运行工作流 ID: {workflow_id}")
            
            response = requests.post(url, headers=headers, json=data, stream=True, timeout=60)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        import json
                        json_data = line_str[6:]
                        try:
                            yield json.loads(json_data)
                        except json.JSONDecodeError:
                            continue
                    
        except Exception as e:
            logger.error(f"❌ 流式工作流调用失败：{str(e)}")
            yield {
                "event": "error",
                "data": {
                    "error": str(e)
                }
            }
    
    def get_workflow_info(self, workflow_id: str) -> Dict[str, Any]:
        """
        获取工作流信息
        
        Args:
            workflow_id: 工作流ID
            
        Returns:
            工作流信息
        """
        params = {"workflow_id": workflow_id}
        
        result = self._request(
            method="GET",
            path="/v1/workflow/info",
            params=params
        )
        
        return result
    
    def list_workflows(self, page_size: int = 20) -> Dict[str, Any]:
        """
        获取工作流列表
        
        Args:
            page_size: 每页数量
            
        Returns:
            工作流列表
        """
        params = {"page_size": page_size}
        
        result = self._request(
            method="GET",
            path="/v1/workflow/list",
            params=params
        )
        
        return result
    
    def _format_workflow_result(self, data: Dict) -> Dict[str, Any]:
        """
        格式化工作流结果
        
        Args:
            data: 原始数据
            
        Returns:
            格式化后的结果
        """
        return {
            "workflow_id": data.get("workflow_id", ""),
            "status": data.get("status", ""),
            "result": data.get("data", {}),
            "execution_time": data.get("execution_time", 0),
            "error": data.get("error", None)
        }


# 全局实例（单例）
_coze_workflow_service = None


def get_coze_workflow_service(access_token: str = None) -> CozeWorkflowService:
    """
    获取扣子工作流服务实例（单例模式）
    
    Args:
        access_token: Access Token（可选）
        
    Returns:
        CozeWorkflowService 实例
    """
    global _coze_workflow_service
    
    if _coze_workflow_service is None:
        _coze_workflow_service = CozeWorkflowService(access_token)
    elif access_token:
        _coze_workflow_service.set_api_key(access_token)
    
    return _coze_workflow_service


# 导出
__all__ = [
    "CozeWorkflowService",
    "get_coze_workflow_service"
]
