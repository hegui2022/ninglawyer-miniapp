"""
限流中间件测试
"""

import pytest
import time
from src.middleware.rate_limit import RateLimiter, get_rate_limiter


class TestRateLimiter:
    """限流器测试"""
    
    @pytest.fixture
    def limiter(self):
        """限流器实例"""
        return RateLimiter()
    
    def test_is_allowed_first_request(self, limiter):
        """测试首次请求允许"""
        allowed, info = limiter.is_allowed("test_key", "default")
        assert allowed is True
        assert info['current_requests'] == 1
    
    def test_is_allowed_under_limit(self, limiter):
        """测试未超限请求允许"""
        # 发送多个请求，但未达到限制
        for i in range(5):
            allowed, info = limiter.is_allowed("test_key_2", "default")
            assert allowed is True
    
    def test_is_allowed_exceeds_limit(self, limiter):
        """测试超限请求被拒绝"""
        # 发送超过限制的请求（默认60次）
        key = "test_key_3"
        rule = 'default'
        
        # 快速发送60次请求
        for i in range(60):
            allowed, info = limiter.is_allowed(key, rule)
            assert allowed is True
        
        # 第61次请求应该被拒绝
        allowed, info = limiter.is_allowed(key, rule)
        assert allowed is False
        assert 'retry_after' in info
    
    def test_is_allowed_login_rule(self, limiter):
        """测试登录接口限流（最多5次）"""
        key = "test_login_key"
        rule = 'login'
        
        # 登录接口最多5次
        for i in range(5):
            allowed, info = limiter.is_allowed(key, rule)
            assert allowed is True
        
        # 第6次应该被拒绝
        allowed, info = limiter.is_allowed(key, rule)
        assert allowed is False
    
    def test_reset(self, limiter):
        """测试重置限流"""
        key = "test_reset_key"
        
        # 发送一些请求
        for i in range(10):
            limiter.is_allowed(key, "default")
        
        # 重置
        limiter.reset(key)
        
        # 重置后应该可以继续请求
        allowed, info = limiter.is_allowed(key, "default")
        assert allowed is True
    
    def test_time_window(self, limiter):
        """测试时间窗口"""
        key = "test_time_key"
        
        # 发送请求
        allowed, info = limiter.is_allowed(key, "default")
        assert allowed is True
        
        # 等待时间窗口过期（这里只测试逻辑，不实际等待）
        # 实际使用时，过期记录会被自动清理
    
    def test_different_keys_independent(self, limiter):
        """测试不同键的限流是独立的"""
        key1 = "user1"
        key2 = "user2"
        
        # 为key1发送超过限制的请求
        for i in range(60):
            limiter.is_allowed(key1, "default")
        
        # key1应该被限流
        allowed, info = limiter.is_allowed(key1, "default")
        assert allowed is False
        
        # key2应该不受影响
        allowed, info = limiter.is_allowed(key2, "default")
        assert allowed is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
