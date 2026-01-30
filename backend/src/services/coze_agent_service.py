"""
扣子智能体服务（Coze Agent Service）
提供调用扣子平台智能体/Bot的API接口
"""

import os
import requests
import json
import time
from typing import Dict, Any, Optional, List
from loguru import logger


class CozeAuthService:
    """扣子认证服务"""
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        """
        初始化认证服务
        
        Args:
            client_id: 扣子Client ID
            client_secret: 扣子Client Secret
        """
        self.client_id = client_id or os.getenv("COZE_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("COZE_CLIENT_SECRET", "")
        self.base_url = os.getenv("COZE_API_BASE_URL", "https://api.coze.cn")
        self.access_token = None
        self.token_expires_at = 0
        
        logger.info("🔐 扣子认证服务初始化完成")
    
    def get_access_token(self) -> str:
        """
        获取 Access Token
        
        Returns:
            有效的 Access Token
        """
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
            expires_in = result.get("expires_in", 7200)  # 默认 2 小时
            
            # 提前 5 分钟过期
            self.token_expires_at = time.time() + expires_in - 300
            
            logger.info(f"✅ 获取 Access Token 成功，有效期：{expires_in}秒")
            return self.access_token
            
        except Exception as e:
            logger.error(f"❌ 获取 Access Token 失败：{str(e)}")
            raise
    
    def get_headers(self) -> Dict[str, str]:
        """
        获取带认证的请求头
        
        Returns:
            包含 Authorization 的请求头
        """
        token = self.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }


class CozeAgentService:
    """扣子智能体服务"""
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        """
        初始化智能体服务
        
        Args:
            client_id: 扣子Client ID
            client_secret: 扣子Client Secret
        """
        self.auth = CozeAuthService(client_id, client_secret)
        self.base_url = self.auth.base_url
        
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
        url = f"{self.base_url}/v1/bot/run"
        headers = self.auth.get_headers()
        
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
        
        try:
            logger.info(f"🚀 调用智能体 Bot ID: {bot_id}, 用户: {user_id}")
            
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            # 检查是否有错误
            if result.get("code") != 0:
                raise Exception(f"Bot 调用失败: {result.get('msg', '未知错误')}")
            
            logger.info(f"✅ 智能体调用成功，会话ID: {result.get('conversation_id')}")
            
            # 格式化返回结果
            return {
                "success": True,
                "bot_id": bot_id,
                "conversation_id": result.get("conversation_id", ""),
                "answer": result.get("answer", ""),
                "messages": self._format_messages(result.get("messages", [])),
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"❌ 智能体调用失败：{str(e)}")
            return {
                "success": False,
                "bot_id": bot_id,
                "error": str(e),
                "status": "failed"
            }
    
    def run_bot_stream(
        self,
        bot_id: str,
        query: str,
        user_id: str,
        conversation_id: Optional[str] = None
    ):
        """
        流式运行智能体/Bot
        
        Args:
            bot_id: Bot ID
            query: 用户输入
            user_id: 用户ID
            conversation_id: 会话ID
            
        Yields:
            流式响应数据块
        """
        url = f"{self.base_url}/v1/bot/run"
        headers = self.auth.get_headers()
        
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
                    # SSE 格式: "data: {...}"
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
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
        url = f"{self.base_url}/v1/bot/list"
        headers = self.auth.get_headers()
        
        params = {
            "page_size": page_size
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("code") != 0:
                raise Exception(f"获取 Bot 列表失败: {result.get('msg', '未知错误')}")
            
            return {
                "success": True,
                "bots": result.get("data", {}).get("bots", []),
                "total": result.get("data", {}).get("total", 0)
            }
            
        except Exception as e:
            logger.error(f"❌ 获取 Bot 列表失败：{str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_bot_info(self, bot_id: str) -> Dict[str, Any]:
        """
        获取 Bot 详细信息
        
        Args:
            bot_id: Bot ID
            
        Returns:
            Bot 详细信息
        """
        url = f"{self.base_url}/v1/bot/info"
        headers = self.auth.get_headers()
        
        params = {
            "bot_id": bot_id
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("code") != 0:
                raise Exception(f"获取 Bot 信息失败: {result.get('msg', '未知错误')}")
            
            return {
                "success": True,
                "bot_info": result.get("data", {})
            }
            
        except Exception as e:
            logger.error(f"❌ 获取 Bot 信息失败：{str(e)}")
            return {
                "success": False,
                "error": str(e)
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


def get_coze_agent_service() -> CozeAgentService:
    """
    获取扣子智能体服务实例（单例模式）
    
    Returns:
        CozeAgentService 实例
    """
    global _coze_agent_service
    
    if _coze_agent_service is None:
        _coze_agent_service = CozeAgentService()
    
    return _coze_agent_service


# 导出
__all__ = [
    "CozeAgentService",
    "CozeAuthService",
    "get_coze_agent_service"
]
