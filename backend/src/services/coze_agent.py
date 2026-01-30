"""
扣子智能体调用服务
第一版：全部智能体使用扣子官方API
"""

import os
import requests
import json
import logging
import uuid
from typing import Optional, Dict, Any, List, Iterator
from datetime import datetime
from sqlalchemy.orm import Session

from utils.redis_client import conversation_cache
from models.v1_models import Conversation

logger = logging.getLogger(__name__)


class CozeAgentService:
    """扣子智能体服务"""
    
    def __init__(self, db: Session):
        """初始化"""
        self.db = db
        self.api_key = os.getenv("COZE_API_KEY")
        self.api_base_url = os.getenv("COZE_API_BASE_URL", "https://api.coze.cn")
        self.api_endpoint = f"{self.api_base_url}/open_api/v2/chat"
        
        if not self.api_key:
            logger.error("扣子API Key未配置")
    
    def _load_agents_config(self) -> Dict[str, Any]:
        """加载智能体配置"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), "../../config/agents_config.json")
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载智能体配置失败: {str(e)}")
            return {}
    
    def _get_bot_id(self, app_type: str, agent_type: str) -> Optional[str]:
        """
        获取Bot ID
        
        Args:
            app_type: 小程序类型（ninglawyer/fangfengxian/contract）
            agent_type: 智能体类型（criminal_consultation/civil_consultation/contract_drafter等）
        
        Returns:
            Bot ID
        """
        try:
            config = self._load_agents_config()
            app_config = config.get("apps", {}).get(app_type)
            if not app_config:
                logger.error(f"应用配置不存在: {app_type}")
                return None
            
            agent_config = app_config.get("agents", {}).get(agent_type)
            if not agent_config:
                logger.error(f"智能体配置不存在: {app_type}/{agent_type}")
                return None
            
            bot_id = agent_config.get("bot_id")
            if not bot_id or bot_id == "请替换为实际的Bot ID":
                logger.error(f"Bot ID未配置: {app_type}/{agent_type}")
                return None
            
            return bot_id
            
        except Exception as e:
            logger.error(f"获取Bot ID失败: {str(e)}")
            return None
    
    def _get_bot_name(self, app_type: str, agent_type: str) -> str:
        """获取Bot名称"""
        try:
            config = self._load_agents_config()
            app_config = config.get("apps", {}).get(app_type)
            if not app_config:
                return f"{app_type}_{agent_type}"
            
            agent_config = app_config.get("agents", {}).get(agent_type)
            if not agent_config:
                return f"{app_type}_{agent_type}"
            
            return agent_config.get("name", f"{app_type}_{agent_type}")
            
        except Exception as e:
            logger.error(f"获取Bot名称失败: {str(e)}")
            return f"{app_type}_{agent_type}"
    
    def chat(
        self,
        user_id: int,
        app_type: str,
        agent_type: str,
        query: str,
        session_id: Optional[str] = None,
        stream: bool = False,
        save_to_db: bool = False,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any] | Iterator[Dict[str, Any]]:
        """
        调用扣子智能体
        
        Args:
            user_id: 用户ID
            app_type: 小程序类型
            agent_type: 智能体类型
            query: 用户消息
            session_id: 会话ID（可选，如果不提供则自动生成）
            stream: 是否流式输出
            save_to_db: 是否保存到数据库
            extra_data: 额外数据
        
        Returns:
            智能体响应
        """
        try:
            # 1. 获取Bot ID
            bot_id = self._get_bot_id(app_type, agent_type)
            if not bot_id:
                return {
                    "success": False,
                    "message": f"智能体未配置: {app_type}/{agent_type}"
                }
            bot_name = self._get_bot_name(app_type, agent_type)
            
            # 2. 生成或获取session_id
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # 3. 获取对话历史（从Redis）
            conversation_history = conversation_cache.get_messages(session_id)
            
            # 4. 构建请求消息
            messages = []
            
            # 添加历史消息（最近10条）
            if conversation_history:
                for msg in conversation_history[-10:]:
                    if msg.get("role") == "user":
                        messages.append({
                            "role": "user",
                            "content": msg.get("content", "")
                        })
                    elif msg.get("role") == "assistant":
                        messages.append({
                            "role": "assistant",
                            "content": msg.get("content", "")
                        })
            
            # 添加当前用户消息
            messages.append({
                "role": "user",
                "content": query
            })
            
            # 5. 构建请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            payload = {
                "bot_id": bot_id,
                "user_id": str(user_id),
                "stream": stream,
                "auto_save_history": True,
                "additional_messages": messages
            }
            
            # 6. 调用扣子API
            if stream:
                # 流式输出
                return self._chat_stream(
                    headers=headers,
                    payload=payload,
                    user_id=user_id,
                    session_id=session_id,
                    app_type=app_type,
                    agent_type=agent_type,
                    bot_id=bot_id,
                    bot_name=bot_name,
                    query=query,
                    save_to_db=save_to_db,
                    extra_data=extra_data
                )
            else:
                # 非流式输出
                return self._chat_sync(
                    headers=headers,
                    payload=payload,
                    user_id=user_id,
                    session_id=session_id,
                    app_type=app_type,
                    agent_type=agent_type,
                    bot_id=bot_id,
                    bot_name=bot_name,
                    query=query,
                    save_to_db=save_to_db,
                    extra_data=extra_data
                )
            
        except Exception as e:
            logger.error(f"调用智能体失败: {str(e)}")
            return {
                "success": False,
                "message": f"调用失败: {str(e)}"
            }
    
    def _chat_sync(
        self,
        headers: Dict[str, str],
        payload: Dict[str, Any],
        user_id: int,
        session_id: str,
        app_type: str,
        agent_type: str,
        bot_id: str,
        bot_name: str,
        query: str,
        save_to_db: bool,
        extra_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        同步调用智能体（非流式）
        """
        try:
            # 1. 发送请求
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=300
            )
            
            if response.status_code != 200:
                logger.error(f"扣子API调用失败: status={response.status_code}, body={response.text}")
                return {
                    "success": False,
                    "message": f"API调用失败: {response.status_code}"
                }
            
            result = response.json()
            
            # 2. 提取响应
            answer = ""
            if result.get("code") == 0:
                messages = result.get("messages", [])
                for msg in messages:
                    if msg.get("type") == "answer":
                        answer += msg.get("content", "")
            else:
                logger.error(f"扣子API返回错误: {result}")
                return {
                    "success": False,
                    "message": f"智能体返回错误: {result.get('msg', '未知错误')}"
                }
            
            if not answer:
                logger.warning("智能体返回空响应")
                answer = "抱歉，智能体暂时无法回答您的问题。"
            
            # 3. 保存到Redis
            conversation_cache.save_message(
                session_id=session_id,
                role="user",
                content=query,
                bot_id=bot_id,
                bot_name=bot_name
            )
            conversation_cache.save_message(
                session_id=session_id,
                role="assistant",
                content=answer,
                bot_id=bot_id,
                bot_name=bot_name
            )
            
            # 4. 保存对话基本信息
            conversation_cache.save_conversation(
                session_id=session_id,
                user_id=user_id,
                app_type=app_type,
                conversation_type=agent_type,
                metadata=extra_data
            )
            
            # 5. 保存到数据库（可选）
            if save_to_db:
                try:
                    conversation = Conversation(
                        user_id=user_id,
                        session_id=session_id,
                        conversation_type=agent_type,
                        user_message=query,
                        bot_response=answer,
                        bot_id=bot_id,
                        bot_name=bot_name,
                        app_type=app_type,
                        extra_data=extra_data
                    )
                    self.db.add(conversation)
                    self.db.commit()
                except Exception as e:
                    logger.error(f"保存对话到数据库失败: {str(e)}")
                    self.db.rollback()
            
            # 6. 返回结果
            return {
                "success": True,
                "data": {
                    "session_id": session_id,
                    "answer": answer,
                    "bot_id": bot_id,
                    "bot_name": bot_name,
                    "conversation_type": agent_type
                }
            }
            
        except Exception as e:
            logger.error(f"同步调用智能体失败: {str(e)}")
            return {
                "success": False,
                "message": f"调用失败: {str(e)}"
            }
    
    def _chat_stream(
        self,
        headers: Dict[str, str],
        payload: Dict[str, Any],
        user_id: int,
        session_id: str,
        app_type: str,
        agent_type: str,
        bot_id: str,
        bot_name: str,
        query: str,
        save_to_db: bool,
        extra_data: Optional[Dict[str, Any]]
    ) -> Iterator[Dict[str, Any]]:
        """
        流式调用智能体
        """
        try:
            # 1. 发送流式请求
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                stream=True,
                timeout=300
            )
            
            if response.status_code != 200:
                logger.error(f"扣子API调用失败: status={response.status_code}")
                yield {
                    "success": False,
                    "message": f"API调用失败: {response.status_code}"
                }
                return
            
            # 2. 处理流式响应
            full_answer = ""
            
            for line in response.iter_lines():
                if not line:
                    continue
                
                line = line.decode('utf-8')
                
                if line.startswith('data:'):
                    data_str = line[5:].strip()
                    
                    if not data_str or data_str == '[DONE]':
                        continue
                    
                    try:
                        data = json.loads(data_str)
                        
                        if data.get("event") == "message.delta":
                            content = data.get("content", "")
                            full_answer += content
                            
                            yield {
                                "success": True,
                                "data": {
                                    "type": "chunk",
                                    "content": content,
                                    "session_id": session_id,
                                    "bot_name": bot_name
                                }
                            }
                        elif data.get("event") == "message.end":
                            # 流式结束，保存消息
                            conversation_cache.save_message(
                                session_id=session_id,
                                role="user",
                                content=query,
                                bot_id=bot_id,
                                bot_name=bot_name
                            )
                            conversation_cache.save_message(
                                session_id=session_id,
                                role="assistant",
                                content=full_answer,
                                bot_id=bot_id,
                                bot_name=bot_name
                            )
                            
                            conversation_cache.save_conversation(
                                session_id=session_id,
                                user_id=user_id,
                                app_type=app_type,
                                conversation_type=agent_type,
                                metadata=extra_data
                            )
                            
                            # 保存到数据库（可选）
                            if save_to_db:
                                try:
                                    conversation = Conversation(
                                        user_id=user_id,
                                        session_id=session_id,
                                        conversation_type=agent_type,
                                        user_message=query,
                                        bot_response=full_answer,
                                        bot_id=bot_id,
                                        bot_name=bot_name,
                                        app_type=app_type,
                                        extra_data=extra_data
                                    )
                                    self.db.add(conversation)
                                    self.db.commit()
                                except Exception as e:
                                    logger.error(f"保存对话到数据库失败: {str(e)}")
                                    self.db.rollback()
                            
                            yield {
                                "success": True,
                                "data": {
                                    "type": "end",
                                    "session_id": session_id,
                                    "bot_id": bot_id,
                                    "bot_name": bot_name,
                                    "conversation_type": agent_type
                                }
                            }
                            break
                        
                    except json.JSONDecodeError as e:
                        logger.error(f"解析流式数据失败: {str(e)}, data={data_str}")
                        continue
                elif line.startswith('error:'):
                    error_str = line[6:].strip()
                    logger.error(f"扣子API返回错误: {error_str}")
                    yield {
                        "success": False,
                        "message": f"智能体错误: {error_str}"
                    }
                    return
            
        except Exception as e:
            logger.error(f"流式调用智能体失败: {str(e)}")
            yield {
                "success": False,
                "message": f"调用失败: {str(e)}"
            }
    
    def get_conversation_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        获取对话历史
        
        Args:
            session_id: 会话ID
            limit: 消息数量限制
        
        Returns:
            消息列表
        """
        try:
            return conversation_cache.get_messages(session_id, limit)
        except Exception as e:
            logger.error(f"获取对话历史失败: {str(e)}")
            return []
    
    def clear_conversation(self, session_id: str) -> Dict[str, Any]:
        """
        清除对话
        
        Args:
            session_id: 会话ID
        
        Returns:
            操作结果
        """
        try:
            success = conversation_cache.clear_conversation(session_id)
            
            if success:
                return {
                    "success": True,
                    "message": "对话已清除"
                }
            else:
                return {
                    "success": False,
                    "message": "清除失败"
                }
        except Exception as e:
            logger.error(f"清除对话失败: {str(e)}")
            return {
                "success": False,
                "message": f"清除失败: {str(e)}"
            }
