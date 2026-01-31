"""
Sentry错误追踪测试
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock

from src.utils.sentry_config import (
    init_sentry,
    set_user_context,
    add_context,
    add_tag,
    capture_exception,
    capture_message
)


class TestSentryConfig:
    """Sentry配置测试"""
    
    @pytest.fixture
    def mock_sentry_init(self):
        """Mock Sentry初始化"""
        with patch('src.utils.sentry_config.sentry_sdk.init') as mock_init:
            yield mock_init
    
    def test_init_sentry_without_dsn(self):
        """测试未配置DSN时的初始化"""
        with patch.dict(os.environ, {'SENTRY_DSN': ''}):
            result = init_sentry()
            assert result is False
    
    def test_init_sentry_with_dsn(self, mock_sentry_init):
        """测试配置DSN时的初始化"""
        env_vars = {
            'SENTRY_DSN': 'https://test@sentry.io/123',
            'ENVIRONMENT': 'test',
            'APP_VERSION': '1.0.0',
            'SENTRY_TRACES_SAMPLE_RATE': '0.1',
            'SENTRY_ERROR_SAMPLE_RATE': '1.0'
        }
        
        with patch.dict(os.environ, env_vars):
            result = init_sentry()
            assert result is True
            mock_sentry_init.assert_called_once()
    
    def test_set_user_context(self):
        """测试设置用户上下文"""
        with patch('src.utils.sentry_config.sentry_sdk.set_user') as mock_set_user:
            set_user_context(user_id=123, openid='test_openid', subscription_type='premium')
            mock_set_user.assert_called_once()
            call_args = mock_set_user.call_args[0][0]
            assert call_args['id'] == '123'
            assert call_args['openid'] == 'test_openid'
            assert call_args['subscription'] == 'premium'
    
    def test_add_context(self):
        """测试添加上下文"""
        with patch('src.utils.sentry_config.sentry_sdk.set_context') as mock_set_context:
            add_context('test_key', {'data': 'test_value'})
            mock_set_context.assert_called_once_with('test_key', {'data': 'test_value'})
    
    def test_add_tag(self):
        """测试添加标签"""
        with patch('src.utils.sentry_config.sentry_sdk.set_tag') as mock_set_tag:
            add_tag('test_key', 'test_value')
            mock_set_tag.assert_called_once_with('test_key', 'test_value')
    
    def test_capture_exception(self):
        """测试捕获异常"""
        exception = ValueError('Test error')
        
        with patch('src.utils.sentry_config.sentry_sdk.push_scope') as mock_push_scope, \
             patch('src.utils.sentry_config.sentry_sdk.capture_exception') as mock_capture:
            
            mock_scope = MagicMock()
            mock_push_scope.return_value.__enter__.return_value = mock_scope
            
            capture_exception(exception, level='error', extra_info='test')
            
            mock_scope.set_level.assert_called_once_with('error')
            mock_scope.set_extra.assert_called_once_with('extra_info', 'test')
            mock_capture.assert_called_once_with(exception)
    
    def test_capture_message(self):
        """测试捕获消息"""
        with patch('src.utils.sentry_config.sentry_sdk.push_scope') as mock_push_scope, \
             patch('src.utils.sentry_config.sentry_sdk.capture_message') as mock_capture:
            
            mock_scope = MagicMock()
            mock_push_scope.return_value.__enter__.return_value = mock_scope
            
            capture_message('Test message', level='info', context='test')
            
            mock_scope.set_level.assert_called_once_with('info')
            mock_scope.set_extra.assert_called_once_with('context', 'test')
            mock_capture.assert_called_once_with('Test message')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
