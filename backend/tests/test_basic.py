"""
基础架构测试
"""

import pytest


class TestBasicArchitecture:
    """测试基础架构"""
    
    def test_import_config(self):
        """测试配置导入"""
        from src.utils.config import load_config, get_config
        config = load_config()
        assert config is not None
        assert 'API_PORT' in config
        
        config2 = get_config()
        assert config2 is not None
    
    def test_import_logger(self):
        """测试日志工具导入"""
        from src.utils.logger import (
            setup_logger,
            log_function_call,
            log_api_request,
            log_error,
            log_performance,
            log_business_event
        )
        assert setup_logger is not None
        assert log_function_call is not None
        assert log_api_request is not None
    
    def test_import_response(self):
        """测试响应工具导入"""
        from src.utils.response import (
            success_response,
            error_response,
            paginate_response,
            validation_error_response,
            ResponseCode
        )
        assert success_response is not None
        assert error_response is not None
        assert paginate_response is not None
        assert validation_error_response is not None
        assert ResponseCode is not None
    
    def test_response_success(self):
        """测试成功响应"""
        from src.utils.response import success_response, ResponseCode
        
        response = success_response({"test": "data"}, "测试成功")
        assert response['success'] is True
        assert response['message'] == "测试成功"
        assert response['code'] == ResponseCode.SUCCESS.value
        assert response['data'] == {"test": "data"}
    
    def test_response_error(self):
        """测试错误响应"""
        from src.utils.response import error_response, ResponseCode
        
        response = error_response("测试失败", ResponseCode.BAD_REQUEST.value)
        assert response['success'] is False
        assert response['message'] == "测试失败"
        assert response['code'] == ResponseCode.BAD_REQUEST.value
    
    def test_response_paginate(self):
        """测试分页响应"""
        from src.utils.response import paginate_response
        
        data = [{"id": 1}, {"id": 2}]
        response = paginate_response(data, 10, 1, 2)
        assert response['success'] is True
        assert response['data']['list'] == data
        assert response['data']['pagination']['total'] == 10
        assert response['data']['pagination']['page'] == 1
        assert response['data']['pagination']['page_size'] == 2
        assert response['data']['pagination']['total_pages'] == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
