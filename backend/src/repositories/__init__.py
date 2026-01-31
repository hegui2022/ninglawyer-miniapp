"""
Repository层
提供标准的数据访问接口
"""

from .base_repository import BaseRepository
from .user_repository import UserRepository
from .session_repository import SessionRepository
from .message_repository import MessageRepository

# 全局Repository实例（延迟初始化）
_user_repo = None
_session_repo = None
_message_repo = None


def get_user_repository(cache_manager=None) -> UserRepository:
    """获取用户Repository实例"""
    global _user_repo
    if _user_repo is None:
        _user_repo = UserRepository(cache_manager)
    return _user_repo


def get_session_repository(cache_manager=None) -> SessionRepository:
    """获取会话Repository实例"""
    global _session_repo
    if _session_repo is None:
        _session_repo = SessionRepository(cache_manager)
    return _session_repo


def get_message_repository(cache_manager=None) -> MessageRepository:
    """获取消息Repository实例"""
    global _message_repo
    if _message_repo is None:
        _message_repo = MessageRepository(cache_manager)
    return _message_repo


__all__ = [
    'BaseRepository',
    'UserRepository',
    'SessionRepository',
    'MessageRepository',
    'get_user_repository',
    'get_session_repository',
    'get_message_repository',
]
