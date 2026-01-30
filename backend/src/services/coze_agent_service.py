"""
扣子智能体服务（Coze Agent Service）
提供调用扣子平台智能体/Bot的API接口
基于BaseThirdPartyAPIService基类实现
"""

from typing import Dict, Any, Optional, List
from loguru import logger

from .base_service import BaseThirdPartyAPIService


class CozeAuthService:
    """扣子认证服务（独立于智能体服务）"""
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        """
        初始化认证服务
        
        Args:
            client_id: 扣子Client ID
            client_secret: 扣子Client Secret
        """
        self.client_id = client_id or ""
        self.client_secret = client_secret or ""
        self.base_url = "https://api.coze.cn"
        self.access_token = None
        self.token_expires_at = 0
        
        logger.info("🔐 扣子认证服务初始化完成")
    
    def get_access_token(self) -> str:
        """
        获取 Access Token
        
        Returns:
            有效的 Access Token
        """
        import time
        import requests
        
        # 检查 token 是否有效
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        # 获取新 token
        url = f"{self.base_url}/v1/auth/token"
        headers = {"Content-Type": "application/json"}
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("error"):
                raise Exception(f"获取Token失败: {result.get('error_description')}")
            
            self.access_token = result.get("access_token")
            expires_in = result.get("expires_in", 7200)
            
            # 提前 5 分钟过期
            self.token_expires_at = time.time() + expires_in - 300
            
            logger.info(f"✅ 获取 Access Token 成功，有效期：{expires_in}秒")
            return self.access_token
            
        except Exception as e:
            logger.error(f"❌ 获取 Access Token 失败：{str(e)}")
            raise


class CozeAgentService(BaseThirdPartyAPIService):
    """扣子智能体服务（继承基础服务类）"""
    
    def __init__(self, access_token: str = None):
        """
        初始化智能体服务
        
        Args:
            access_token: 访问令牌（可选，如果不提供则使用认证服务获取）
        """
        # 使用固定值初始化（占位符）
        api_key = access_token or "ACCESS_TOKEN"
        base_url = "https://api.coze.cn"
        
        super().__init__(api_key=api_key, base_url=base_url, timeout=60)
        
        logger.info("🤖 扣子智能体服务初始化完成")
    
    def run_bot(
        self,
        bot_id: str,
        query: str,
        user_id: str,
        conversation_id: Optional[str] = None,
        stream: bool = False,
        additional_messages: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        运行智能体/Bot（非流式）
        
        Args:
            bot_id: Bot ID（智能体ID）
            query: 用户输入
            user_id: 用户ID
            conversation_id: 会话ID（可选，用于多轮对话）
            stream: 是否流式返回
            additional_messages: 额外的历史消息（可选）
            
        Returns:
            Bot 执行结果
        """
        # 构建请求数据
        data = {
            "bot_id": bot_id,
            "user": user_id,
            "query": query,
            "stream": stream
        }
        
        # 如果有会话ID，添加到请求中
        if conversation_id:
            data["conversation_id"] = conversation_id
        
        # 如果有额外消息，添加到请求中
        if additional_messages:
            data["additional_messages"] = additional_messages
        
        logger.info(f"🚀 调用智能体 Bot ID: {bot_id}, 用户: {user_id}")
        
        # 调用基础请求方法
        result = self._request(
            method="POST",
            path="/v1/bot/run",
            json=data
        )
        
        # 格式化返回结果
        if result.get("success"):
            data = result.get("data", {})
            result["data"] = self._format_bot_result(data)
        
        return result
    
    def run_bot_stream(
        self,
        bot_id: str,
        query: str,
        user_id: str,
        conversation_id: Optional[str] = None
    ):
        """
        流式运行智能体/Bot（流式请求不走通用请求方法）
        
        Args:
            bot_id: Bot ID
            query: 用户输入
            user_id: 用户ID
            conversation_id: 会话ID
            
        Yields:
            流式响应数据块
        """
        import requests
        
        url = f"{self.base_url}/v1/bot/run"
        headers = self.headers
        
        data = {
            "bot_id": bot_id,
            "user": user_id,
            "query": query,
            "stream": True
        }
        
        if conversation_id:
            data["conversation_id"] = conversation_id
        
        try:
            logger.info(f"🚀 流式调用智能体 Bot ID: {bot_id}")
            
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
            logger.error(f"❌ 流式智能体调用失败：{str(e)}")
            yield {
                "event": "error",
                "data": {
                    "error": str(e)
                }
            }
    
    def get_bot_list(self, page_size: int = 20) -> Dict[str, Any]:
        """
        获取 Bot 列表
        
        Args:
            page_size: 每页数量
            
        Returns:
            Bot 列表
        """
        params = {"page_size": page_size}
        
        result = self._request(
            method="GET",
            path="/v1/bot/list",
            params=params
        )
        
        return result
    
    def get_bot_info(self, bot_id: str) -> Dict[str, Any]:
        """
        获取 Bot 详细信息
        
        Args:
            bot_id: Bot ID
            
        Returns:
            Bot 详细信息
        """
        params = {"bot_id": bot_id}
        
        result = self._request(
            method="GET",
            path="/v1/bot/info",
            params=params
        )
        
        return result
    
    def _format_bot_result(self, data: Dict) -> Dict[str, Any]:
        """
        格式化Bot结果
        
        Args:
            data: 原始数据
            
        Returns:
            格式化后的结果
        """
        return {
            "bot_id": data.get("bot_id", ""),
            "conversation_id": data.get("conversation_id", ""),
            "answer": data.get("answer", ""),
            "messages": self._format_messages(data.get("messages", [])),
            "status": "completed"
        }
    
    def _format_messages(self, messages: List[Dict]) -> List[Dict[str, Any]]:
        """
        格式化消息列表
        
        Args:
            messages: 原始消息列表
            
        Returns:
            格式化后的消息列表
        """
        formatted = []
        for msg in messages:
            formatted.append({
                "role": msg.get("role", ""),
                "content": msg.get("content", ""),
                "content_type": msg.get("content_type", "text"),
                "timestamp": msg.get("timestamp", 0)
            })
        return formatted


# 全局实例（单例）
_coze_agent_service = None


def get_coze_agent_service(access_token: str = None) -> CozeAgentService:
    """
    获取扣子智能体服务实例（单例模式）
    
    Args:
        access_token: Access Token（可选）
        
    Returns:
        CozeAgentService 实例
    """
    global _coze_agent_service
    
    if _coze_agent_service is None:
        _coze_agent_service = CozeAgentService(access_token)
    elif access_token:
        _coze_agent_service.set_api_key(access_token)
    
    return _coze_agent_service


# 导出
__all__ = [
    "CozeAgentService",
    "CozeAuthService",
    "get_coze_agent_service"
]
