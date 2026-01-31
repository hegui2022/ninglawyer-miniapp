"""
扣子知识库API测试
"""

import pytest
from src.services.coze_knowledge_service import CozeKnowledgeService, get_coze_knowledge_service


class TestCozeKnowledgeService:
    """扣子知识库服务测试"""
    
    @pytest.fixture
    def service(self):
        """初始化服务实例"""
        return CozeKnowledgeService(
            access_token="ACCESS_TOKEN",
            dataset_id="DATASET_ID"
        )
    
    def test_init(self, service):
        """测试初始化"""
        assert service.access_token == "ACCESS_TOKEN"
        assert service.dataset_id == "DATASET_ID"
    
    def test_set_access_token(self, service):
        """测试设置Access Token"""
        service.set_access_token("NEW_TOKEN")
        assert service.access_token == "NEW_TOKEN"
    
    def test_set_dataset_id(self, service):
        """测试设置Dataset ID"""
        service.set_dataset_id("NEW_DATASET")
        assert service.dataset_id == "NEW_DATASET"
    
    def test_format_results(self, service):
        """测试结果格式化"""
        raw_data = [
            {
                "content": "这是法律条文内容",
                "score": 0.95,
                "doc_id": "doc_123",
                "metadata": {"title": "刑法"}
            },
            {
                "content": "这是案例内容",
                "score": 0.87,
                "document_id": "doc_456",
                "title": "案例"
            }
        ]
        
        formatted = service._format_results(raw_data)
        
        assert len(formatted) == 2
        assert formatted[0]["content"] == "这是法律条文内容"
        assert formatted[0]["score"] == 0.95
        assert formatted[0]["document_id"] == "doc_123"
        assert formatted[1]["document_id"] == "doc_456"
    
    def test_handle_response_401(self, service):
        """测试401响应（Token过期）"""
        from unittest.mock import Mock
        
        mock_response = Mock()
        mock_response.status_code = 401
        
        result = service._handle_response(mock_response)
        
        assert result["success"] is False
        assert result["error_type"] == "token_expired"
        assert "Access Token" in result["error"]
    
    def test_handle_response_404(self, service):
        """测试404响应（Dataset不存在）"""
        from unittest.mock import Mock
        
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.request = Mock()
        mock_response.request.get = Mock(return_value="test_dataset")
        
        result = service._handle_response(mock_response)
        
        assert result["success"] is False
        assert result["error_type"] == "dataset_not_found"
        assert "Dataset ID不存在" in result["error"]
    
    def test_handle_response_200_success(self, service):
        """测试200响应（成功）"""
        from unittest.mock import Mock
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 0,
            "data": [
                {
                    "content": "测试内容",
                    "score": 0.9,
                    "doc_id": "doc_001"
                }
            ]
        }
        
        result = service._handle_response(mock_response)
        
        assert result["success"] is True
        assert len(result["data"]) == 1
        assert result["data"][0]["content"] == "测试内容"
    
    def test_handle_response_200_business_error(self, service):
        """测试200响应但业务失败"""
        from unittest.mock import Mock
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 1001,
            "msg": "业务错误"
        }
        
        result = service._handle_response(mock_response)
        
        assert result["success"] is False
        assert result["error_type"] == "business_error"
        assert result["error"] == "业务错误"
    
    def test_singleton(self):
        """测试单例模式"""
        service1 = get_coze_knowledge_service("TOKEN1", "DATASET1")
        service2 = get_coze_knowledge_service("TOKEN2", "DATASET2")
        
        assert service1 is service2
        # 单例的值会被更新
        assert service2.access_token == "TOKEN2"
        assert service2.dataset_id == "DATASET2"
    
    def test_search_with_different_dataset_id(self, service):
        """测试使用不同的Dataset ID"""
        from unittest.mock import Mock, patch
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 0,
            "data": []
        }
        
        with patch.object(service, 'search', return_value=mock_response):
            # 使用默认Dataset ID
            result1 = service.search("query1")
            
            # 使用指定的Dataset ID
            result2 = service.search("query2", dataset_id="ANOTHER_DATASET")
            
            # 两次调用应该有不同的Dataset ID
            # 注意：这里只是测试接口，实际调用会因为mock而返回相同结果


def run_tests():
    """运行测试"""
    print("🧪 开始测试扣子知识库API...\n")
    
    # 运行pytest
    import os
    os.system("python -m pytest backend/tests/test_coze_knowledge_api.py -v")


if __name__ == "__main__":
    run_tests()
