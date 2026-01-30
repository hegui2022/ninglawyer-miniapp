"""
会话管理服务
支持多轮对话和上下文记忆
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from src.database import get_db_context
from src.crud.crud import session_crud
from src.models.schemas import SessionCreate


class SessionService:
    """会话服务"""
    
    def create_session(self, user_id: int, skill_type: str, title: str = None) -> Dict:
        """
        创建会话
        
        Args:
            user_id: 用户ID
            skill_type: 技能类型
            title: 会话标题
            
        Returns:
            会话信息
        """
        try:
            with get_db_context() as db:
                # 生成标题
                if not title:
                    title = self._generate_title(skill_type)
                
                # 创建会话
                session_data = SessionCreate(
                    skill_type=skill_type,
                    title=title
                )
                session = session_crud.create(db, session_data, user_id)
                
                logger.info(f"创建会话：{session.id} (user: {user_id}, skill: {skill_type})")
                
                return {
                    "session_id": session.id,
                    "skill_type": session.skill_type,
                    "title": session.title,
                    "created_at": session.created_at.isoformat()
                }
                
        except Exception as e:
            logger.error(f"创建会话失败：{str(e)}")
            raise
    
    def _generate_title(self, skill_type: str) -> str:
        """生成会话标题"""
        titles = {
            "desensitize": "证据脱敏",
            "civil_consult": "法律咨询",
            "contract": "合同起草"
        }
        return titles.get(skill_type, "新会话")
    
    def get_session(self, session_id: int) -> Optional[Dict]:
        """
        获取会话信息
        
        Args:
            session_id: 会话ID
            
        Returns:
            会话信息
        """
        try:
            with get_db_context() as db:
                session = session_crud.get_by_id(db, session_id)
                if not session:
                    return None
                
                return {
                    "session_id": session.id,
                    "user_id": session.user_id,
                    "skill_type": session.skill_type,
                    "title": session.title,
                    "created_at": session.created_at.isoformat(),
                    "updated_at": session.updated_at.isoformat()
                }
                
        except Exception as e:
            logger.error(f"获取会话失败：{str(e)}")
            return None
    
    def get_user_sessions(self, user_id: int, skill_type: str = None) -> List[Dict]:
        """
        获取用户的会话列表
        
        Args:
            user_id: 用户ID
            skill_type: 技能类型（可选）
            
        Returns:
            会话列表
        """
        try:
            with get_db_context() as db:
                sessions = session_crud.get_user_sessions(db, user_id, skill_type)
                
                return [
                    {
                        "session_id": s.id,
                        "skill_type": s.skill_type,
                        "title": s.title,
                        "created_at": s.created_at.isoformat(),
                        "updated_at": s.updated_at.isoformat()
                    }
                    for s in sessions
                ]
                
        except Exception as e:
            logger.error(f"获取会话列表失败：{str(e)}")
            return []
    
    def add_message(self, session_id: int, role: str, content: str) -> Dict:
        """
        添加消息到会话
        
        Args:
            session_id: 会话ID
            role: 角色（user/assistant）
            content: 消息内容
            
        Returns:
            消息信息
        """
        try:
            with get_db_context() as db:
                message = session_crud.add_message(db, session_id, role, content)
                
                logger.info(f"添加消息：{message.id} (session: {session_id}, role: {role})")
                
                return {
                    "message_id": message.id,
                    "role": message.role,
                    "content": message.content,
                    "created_at": message.created_at.isoformat()
                }
                
        except Exception as e:
            logger.error(f"添加消息失败：{str(e)}")
            raise
    
    def get_session_messages(self, session_id: int) -> List[Dict]:
        """
        获取会话消息列表
        
        Args:
            session_id: 会话ID
            
        Returns:
            消息列表
        """
        try:
            with get_db_context() as db:
                messages = session_crud.get_session_messages(db, session_id)
                
                return [
                    {
                        "message_id": m.id,
                        "role": m.role,
                        "content": m.content,
                        "created_at": m.created_at.isoformat()
                    }
                    for m in messages
                ]
                
        except Exception as e:
            logger.error(f"获取消息列表失败：{str(e)}")
            return []
    
    def get_langchain_messages(self, session_id: int, system_prompt: str = None) -> List:
        """
        获取LangChain格式的消息列表（用于LLM调用）
        
        Args:
            session_id: 会话ID
            system_prompt: 系统提示词（可选）
            
        Returns:
            LangChain消息列表
        """
        try:
            messages = self.get_session_messages(session_id)
            langchain_messages = []
            
            # 添加系统提示词
            if system_prompt:
                langchain_messages.append(SystemMessage(content=system_prompt))
            
            # 添加历史消息
            for msg in messages:
                if msg['role'] == 'user':
                    langchain_messages.append(HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    langchain_messages.append(AIMessage(content=msg['content']))
            
            return langchain_messages
            
        except Exception as e:
            logger.error(f"转换消息格式失败：{str(e)}")
            return []
    
    def delete_session(self, session_id: int) -> bool:
        """
        删除会话
        
        Args:
            session_id: 会话ID
            
        Returns:
            是否成功
        """
        try:
            with get_db_context() as db:
                session = session_crud.get_by_id(db, session_id)
                if not session:
                    return False
                
                db.delete(session)
                db.commit()
                
                logger.info(f"删除会话：{session_id}")
                return True
                
        except Exception as e:
            logger.error(f"删除会话失败：{str(e)}")
            return False
    
    def clear_old_sessions(self, user_id: int, days: int = 30) -> int:
        """
        清理旧会话
        
        Args:
            user_id: 用户ID
            days: 天数
            
        Returns:
            删除的会话数量
        """
        try:
            with get_db_context() as db:
                from src.models.models import Session
                from sqlalchemy import and_
                
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                old_sessions = db.query(Session).filter(
                    and_(
                        Session.user_id == user_id,
                        Session.created_at < cutoff_date
                    )
                ).all()
                
                count = len(old_sessions)
                
                for session in old_sessions:
                    db.delete(session)
                
                db.commit()
                
                logger.info(f"清理旧会话：{count} 个")
                
                return count
                
        except Exception as e:
            logger.error(f"清理旧会话失败：{str(e)}")
            return 0


# 全局会话服务实例
session_service = SessionService()
