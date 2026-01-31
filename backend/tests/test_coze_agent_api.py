"""
扣子智能体API测试
"""

import os
import pytest
from src.services.coze_agent_service import CozeAgentService, get_coze_agent_service


class TestCozeAgentService:
    """扣子智能体服务测试"""
    
    @pytest.fixture
    def service(self):
        """初始化服务实例"""
        # 确保环境变量已配置
        if not os.getenv("COZE_CLIENT_ID") or not os.getenv("COZE_CLIENT_SECRET"):
            pytest.skip("未配置扣子API凭证，跳过测试")
        
        return get_coze_agent_service()
    
    def test_singleton(self, service):
        """测试单例模式"""
        service2 = get_coze_agent_service()
        assert service is service2
    
    def test_get_access_token(self, service):
        """测试获取Access Token"""
        token = service.auth.get_access_token()
        assert token is not None
        assert len(token) > 0
        print(f"✅ Access Token: {token[:20]}...")
    
    def test_get_bot_list(self, service):
        """测试获取Bot列表"""
        result = service.get_bot_list(page_size=10)
        assert result.get("success") is True
        assert "bots" in result
        print(f"✅ 获取到 {result.get('total')} 个Bot")
    
    def test_run_bot(self, service):
        """测试运行Bot"""
        # 注意：这里需要替换为实际的Bot ID
        bot_id = os.getenv("TEST_BOT_ID", "")
        if not bot_id:
            pytest.skip("未配置测试用的Bot ID")
        
        result = service.run_bot(
            bot_id=bot_id,
            query="你好",
            user_id="test_user_123"
        )
        
        assert result.get("success") is True
        assert "answer" in result
        assert "conversation_id" in result
        print(f"✅ Bot回答: {result.get('answer')[:50]}...")
    
    def test_run_bot_with_conversation_id(self, service):
        """测试带会话ID的Bot调用"""
        bot_id = os.getenv("TEST_BOT_ID", "")
        if not bot_id:
            pytest.skip("未配置测试用的Bot ID")
        
        # 第一轮对话
        result1 = service.run_bot(
            bot_id=bot_id,
            query="刑法第二百六十四条是什么？",
            user_id="test_user_456"
        )
        
        assert result1.get("success") is True
        conversation_id = result1.get("conversation_id")
        
        # 第二轮对话（使用会话ID）
        result2 = service.run_bot(
            bot_id=bot_id,
            query="量刑标准是多少？",
            user_id="test_user_456",
            conversation_id=conversation_id
        )
        
        assert result2.get("success") is True
        print(f"✅ 多轮对话测试通过")
    
    def test_get_bot_info(self, service):
        """测试获取Bot信息"""
        bot_id = os.getenv("TEST_BOT_ID", "")
        if not bot_id:
            pytest.skip("未配置测试用的Bot ID")
        
        result = service.get_bot_info(bot_id=bot_id)
        
        assert result.get("success") is True
        bot_info = result.get("bot_info")
        assert "bot_id" in bot_info
        print(f"✅ Bot名称: {bot_info.get('bot_name')}")
    
    def test_run_bot_error_handling(self, service):
        """测试错误处理"""
        # 使用不存在的Bot ID
        result = service.run_bot(
            bot_id="invalid_bot_id",
            query="测试",
            user_id="test_user_789"
        )
        
        # 应该返回失败
        assert result.get("success") is False
        assert "error" in result
        print(f"✅ 错误处理测试通过: {result.get('error')}")


def run_tests():
    """运行测试"""
    print("🧪 开始测试扣子智能体API...\n")
    
    # 运行pytest
    os.system("python -m pytest backend/tests/test_coze_agent_api.py -v")


if __name__ == "__main__":
    run_tests()
