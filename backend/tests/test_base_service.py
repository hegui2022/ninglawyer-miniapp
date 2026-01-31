"""
第三方API基础服务类测试
"""

import pytest
from unittest.mock import Mock, patch
from src.services.base_service import BaseThirdPartyAPIService


class TestBaseThirdPartyAPIService:
    """基础服务类测试"""
    
    @pytest.fixture
    def service(self):
        """初始化服务实例"""
        return BaseThirdPartyAPIService(
            api_key="test_key",
            base_url="https://test.api.com",
            timeout=30
        )
    
    def test_init(self, service):
        """测试初始化"""
        assert service.api_key == "test_key"
        assert service.base_url == "https://test.api.com"
        assert service.timeout == 30
        assert "Authorization" in service.headers
    
    def test_get_default_headers(self, service):
        """测试获取默认请求头"""
        headers = service._get_default_headers()
        assert headers["Content-Type"] == "application/json"
        assert headers["Authorization"] == "Bearer test_key"
    
    def test_create_success_response(self, service):
        """测试创建成功响应"""
        data = {"key": "value"}
        result = service._create_success_response(data)
        
        assert result["success"] is True
        assert result["data"] == data
    
    def test_create_error_response(self, service):
        """测试创建错误响应"""
        result = service._create_error_response(
            error_type="test_error",
            error_msg="Test error message"
        )
        
        assert result["success"] is False
        assert result["error_type"] == "test_error"
        assert result["error"] == "Test error message"
    
    def test_set_api_key(self, service):
        """测试设置API Key"""
        service.set_api_key("new_key")
        assert service.api_key == "new_key"
        assert service.headers["Authorization"] == "Bearer new_key"
    
    def test_set_timeout(self, service):
        """测试设置超时时间"""
        service.set_timeout(60)
        assert service.timeout == 60
    
    @patch('backend.src.services.base_service.requests.request')
    def test_request_success(self, mock_request, service):
        """测试成功请求"""
        # 模拟成功响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"code": 0, "data": {"result": "success"}}
        mock_request.return_value = mock_response
        
        result = service._request("POST", "/test", json={"param": "value"})
        
        assert result["success"] is True
        assert result["data"]["result"] == "success"
    
    @patch('backend.src.services.base_service.requests.request')
    def test_request_401(self, mock_request, service):
        """测试401错误"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_request.return_value = mock_response
        
        result = service._request("GET", "/test")
        
        assert result["success"] is False
        assert result["error_type"] == "token_expired"
    
    @patch('backend.src.services.base_service.requests.request')
    def test_request_404(self, mock_request, service):
        """测试404错误"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.url = "https://test.api.com/test"
        mock_request.return_value = mock_response
        
        result = service._request("GET", "/test")
        
        assert result["success"] is False
        assert result["error_type"] == "not_found"
    
    @patch('backend.src.services.base_service.requests.request')
    def test_request_400(self, mock_request, service):
        """测试400错误"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_request.return_value = mock_response
        
        result = service._request("GET", "/test")
        
        assert result["success"] is False
        assert result["error_type"] == "bad_request"
    
    @patch('backend.src.services.base_service.requests.request')
    def test_request_429(self, mock_request, service):
        """测试429错误"""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_request.return_value = mock_response
        
        result = service._request("GET", "/test")
        
        assert result["success"] is False
        assert result["error_type"] == "rate_limit"
    
    @patch('backend.src.services.base_service.requests.request')
    def test_request_timeout(self, mock_request, service):
        """测试超时错误"""
        import requests
        mock_request.side_effect = requests.exceptions.Timeout()
        
        result = service._request("GET", "/test")
        
        assert result["success"] is False
        assert result["error_type"] == "timeout"
    
    @patch('backend.src.services.base_service.requests.request')
    def test_request_connection_error(self, mock_request, service):
        """测试连接错误"""
        import requests
        mock_request.side_effect = requests.exceptions.ConnectionError()
        
        result = service._request("GET", "/test")
        
        assert result["success"] is False
        assert result["error_type"] == "connection_error"
    
    def test_is_business_success_code_zero(self, service):
        """测试业务成功判断（code=0）"""
        result = {"code": 0}
        assert service._is_business_success(result) is True
    
    def test_is_business_success_true(self, service):
        """测试业务成功判断（success=True）"""
        result = {"success": True}
        assert service._is_business_success(result) is True
    
    def test_is_business_success_false(self, service):
        """测试业务失败判断"""
        result = {"code": 1}
        assert service._is_business_success(result) is False
    
    def test_extract_business_data(self, service):
        """测试提取业务数据"""
        result = {"data": {"key": "value"}}
        data = service._extract_business_data(result)
        assert data == {"key": "value"}
    
    def test_extract_business_error(self, service):
        """测试提取业务错误"""
        result = {"msg": "Error message"}
        error = service._extract_business_error(result)
        assert error == "Error message"
    
    def test_extract_business_code(self, service):
        """测试提取业务错误码"""
        result = {"code": 1001}
        code = service._extract_business_code(result)
        assert code == 1001


class TestCustomService(BaseThirdPartyAPIService):
    """自定义服务类（用于测试）"""
    
    def custom_api_call(self, param1: str, param2: int):
        """自定义API调用"""
        return self._request(
            method="POST",
            path="/custom/api",
            json={"param1": param1, "param2": param2}
        )


class TestCustomServiceImplementation:
    """自定义服务实现测试"""
    
    @pytest.fixture
    def custom_service(self):
        """初始化自定义服务"""
        return TestCustomService(
            api_key="custom_key",
            base_url="https://custom.api.com"
        )
    
    @patch('backend.src.services.base_service.requests.request')
    def test_custom_api_call(self, mock_request, custom_service):
        """测试自定义API调用"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"code": 0, "data": {"result": "custom"}}
        mock_request.return_value = mock_response
        
        result = custom_service.custom_api_call("value", 123)
        
        assert result["success"] is True
        assert result["data"]["result"] == "custom"
        
        # 验证请求参数
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[0][0] == "POST"
        assert "custom/api" in call_args[0][1]


def run_tests():
    """运行测试"""
    print("🧪 开始测试第三方API基础服务类...\n")
    
    # 运行pytest
    import os
    os.system("python -m pytest backend/tests/test_base_service.py -v")


if __name__ == "__main__":
    run_tests()
