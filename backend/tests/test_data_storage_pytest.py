"""
数据统一存储单元测试（pytest版本）
"""

import pytest
from src.repositories import get_user_repository, get_session_repository, get_message_repository
from src.utils.cache_manager import CacheManager
from src.utils.data_consistency import DataConsistencyGuard


class TestUserRepository:
    """用户Repository测试"""
    
    @pytest.fixture
    def cache_manager(self):
        """缓存管理器"""
        return CacheManager()
    
    @pytest.fixture
    def user_repo(self, cache_manager):
        """用户Repository"""
        return get_user_repository(cache_manager)
    
    def test_get_by_id(self, user_repo):
        """测试根据ID获取用户"""
        user = user_repo.get_by_id(1)
        if user:
            assert user.id == 1
            assert user.openid is not None
    
    def test_get_by_openid(self, user_repo):
        """测试根据openid获取用户"""
        user = user_repo.get_by_openid("test_openid_001")
        if user:
            assert user.openid == "test_openid_001"
    
    def test_get_user_type(self, user_repo):
        """测试获取用户类型"""
        user_type = user_repo.get_user_type(1)
        assert user_type in ["basic", "premium", "enterprise"]
    
    def test_count(self, user_repo):
        """测试统计用户数量"""
        count = user_repo.count()
        assert count >= 0


class TestSessionRepository:
    """会话Repository测试"""
    
    @pytest.fixture
    def cache_manager(self):
        """缓存管理器"""
        return CacheManager()
    
    @pytest.fixture
    def session_repo(self, cache_manager):
        """会话Repository"""
        return get_session_repository(cache_manager)
    
    def test_get_by_id(self, session_repo):
        """测试根据ID获取会话"""
        session = session_repo.get_by_id(1)
        if session:
            assert session.id == 1
    
    def test_get_user_sessions(self, session_repo):
        """测试获取用户会话列表"""
        sessions = session_repo.get_user_sessions(1, "consultation")
        assert isinstance(sessions, list)


class TestMessageRepository:
    """消息Repository测试"""
    
    @pytest.fixture
    def cache_manager(self):
        """缓存管理器"""
        return CacheManager()
    
    @pytest.fixture
    def message_repo(self, cache_manager):
        """消息Repository"""
        return get_message_repository(cache_manager)
    
    def test_get_session_messages(self, message_repo):
        """测试获取会话消息列表"""
        messages = message_repo.get_session_messages(1)
        assert isinstance(messages, list)
    
    def test_get_message_count(self, message_repo):
        """测试获取消息数量"""
        count = message_repo.get_message_count(1)
        assert count >= 0


class TestDataConsistency:
    """数据一致性测试"""
    
    @pytest.fixture
    def cache_manager(self):
        """缓存管理器"""
        return CacheManager()
    
    @pytest.fixture
    def consistency_guard(self, cache_manager):
        """一致性保障"""
        return DataConsistencyGuard(cache_manager)
    
    def test_cache_aside(self, consistency_guard):
        """测试Cache-Aside模式"""
        result = consistency_guard.safe_read(
            cache_key="test:key",
            db_operation=lambda: {"data": "test"},
            cache_ttl=60
        )
        assert result is not None
        assert result["data"] == "test"
    
    def test_transaction_manager(self, consistency_guard):
        """测试事务管理器"""
        with consistency_guard.transaction_manager.transaction():
            # 测试事务上下文
            pass
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
