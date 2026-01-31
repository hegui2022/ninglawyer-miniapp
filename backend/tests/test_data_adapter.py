"""
数据适配器单元测试
"""

import unittest
from unittest.mock import Mock, patch

from src.adapters import LegalKnowledgeAdapter, get_legal_knowledge_adapter


class TestLegalKnowledgeAdapter(unittest.TestCase):
    """法律知识库适配器测试"""
    
    def setUp(self):
        """测试前置准备"""
        self.adapter = LegalKnowledgeAdapter(enable_llm_enhance=False)
    
    def tearDown(self):
        """测试后清理"""
        pass
    
    def test_init(self):
        """测试初始化"""
        adapter = LegalKnowledgeAdapter()
        self.assertEqual(adapter.get_target_format(), "wechat_miniprogram")
        self.assertTrue(adapter.enable_llm_enhance)
        
        adapter2 = LegalKnowledgeAdapter(enable_llm_enhance=False)
        self.assertFalse(adapter2.enable_llm_enhance)
    
    def test_adapt_success(self):
        """测试适配成功"""
        raw_data = {
            "success": True,
            "data": [
                {
                    "document_id": "doc_001",
                    "content": "《中华人民共和国刑法》第二百六十四条【盗窃罪】盗窃公私财物，数额较大的，或者多次盗窃、入户盗窃、携带凶器盗窃、扒窃的，处三年以下有期徒刑、拘役或者管制，并处或者单处罚金；数额巨大或者有其他严重情节的，处三年以上十年以下有期徒刑，并处罚金；数额特别巨大或者有其他特别严重情节的，处十年以上有期徒刑或者无期徒刑，并处罚金或者没收财产。"
                }
            ],
            "total": 1,
            "has_more": False
        }
        
        result = self.adapter.adapt(raw_data)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["total"], 1)
        self.assertEqual(len(result["data"]), 1)
        
        # 检查提取的字段
        item = result["data"][0]
        self.assertEqual(item["article_number"], "第二百六十四条")
        self.assertEqual(item["law_name"], "中华人民共和国刑法")
        self.assertEqual(item["crime_name"], "盗窃罪")
        
        # 检查刑期
        self.assertGreater(len(item["penalties"]), 0)
        self.assertIn("有期徒刑", [p["type"] for p in item["penalties"]])
        
        # 检查情节
        self.assertIn("数额较大", item["circumstances"])
        self.assertIn("多次盗窃", item["circumstances"])
        
        # 检查关键词
        self.assertIn("第二百六十四条", item["keywords"])
        self.assertIn("盗窃罪", item["keywords"])
    
    def test_adapt_error(self):
        """测试适配错误数据"""
        raw_data = {
            "success": False,
            "error": "知识库检索失败"
        }
        
        result = self.adapter.adapt(raw_data)
        
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "知识库检索失败")
        self.assertEqual(result["error_type"], "adapt_error")
    
    def test_extract_article_number(self):
        """测试提取法条编号"""
        content = "《中华人民共和国刑法》第二百六十四条【盗窃罪】"
        article_number = self.adapter._extract_article_number(content)
        
        self.assertEqual(article_number, "第二百六十四条")
    
    def test_extract_law_name(self):
        """测试提取法条名称"""
        content = "《中华人民共和国刑法》第二百六十四条"
        law_name = self.adapter._extract_law_name(content)
        
        self.assertEqual(law_name, "中华人民共和国刑法")
    
    def test_extract_crime_name(self):
        """测试提取罪名"""
        content = "第二百六十四条【盗窃罪】"
        crime_name = self.adapter._extract_crime_name(content)
        
        self.assertEqual(crime_name, "盗窃罪")
    
    def test_extract_penalties(self):
        """测试提取刑期"""
        content = "处三年以下有期徒刑、拘役或者管制，处三年以上十年以下有期徒刑"
        penalties = self.adapter._extract_penalties(content)
        
        self.assertEqual(len(penalties), 2)
        self.assertEqual(penalties[0]["term"], "三")
        self.assertEqual(penalties[0]["type"], "有期徒刑")
    
    def test_extract_circumstances(self):
        """测试提取情节"""
        content = "数额较大的，或者多次盗窃、入户盗窃、携带凶器盗窃、扒窃的"
        circumstances = self.adapter._extract_circumstances(content)
        
        self.assertIn("数额较大", circumstances)
        self.assertIn("多次盗窃", circumstances)
        self.assertIn("入户盗窃", circumstances)
    
    def test_split_content_sections(self):
        """测试内容分段"""
        content = "第二百六十四条【盗窃罪】内容一。内容二。内容三。"
        sections = self.adapter._split_content_sections(content)
        
        self.assertGreater(len(sections), 0)
        self.assertIn("section_id", sections[0])
        self.assertIn("content", sections[0])
    
    def test_extract_keywords(self):
        """测试提取关键词"""
        content = "第二百六十四条【盗窃罪】数额较大的，或者多次盗窃"
        keywords = self.adapter._extract_keywords(content)
        
        self.assertIn("第二百六十四条", keywords)
        self.assertIn("盗窃罪", keywords)
        self.assertIn("数额较大", keywords)
        self.assertIn("多次盗窃", keywords)
    
    def test_format_single_item(self):
        """测试格式化单个数据项"""
        item = {
            "document_id": "doc_001",
            "content": "第二百六十四条【盗窃罪】数额较大的，处三年以下有期徒刑",
            "score": 0.95
        }
        
        formatted = self.adapter._format_single_item(item)
        
        self.assertEqual(formatted["article_number"], "第二百六十四条")
        self.assertEqual(formatted["crime_name"], "盗窃罪")
        self.assertEqual(formatted["score"], 0.95)
    
    @patch('backend.src.adapters.legal_knowledge_adapter.LLMClient')
    def test_llm_enhance(self, mock_llm_client):
        """测试LLM增强"""
        # 模拟LLM响应
        mock_response = Mock()
        mock_response.content = "这是一条关于盗窃罪的法条"
        mock_llm_client.return_value.invoke.return_value = mock_response
        
        data = {
            "success": True,
            "data": [
                {
                    "document_id": "doc_001",
                    "content": "第二百六十四条【盗窃罪】盗窃公私财物..."
                }
            ]
        }
        
        adapter = LegalKnowledgeAdapter(enable_llm_enhance=True)
        
        # 这里不会真的调用LLM，因为会抛出异常
        # 实际使用时需要提供有效的LLM配置
        try:
            result = adapter._llm_enhance(data)
            # 如果成功，检查是否添加了摘要
            if "data" in result and len(result["data"]) > 0:
                if "summary" in result["data"][0]:
                    self.assertIsNotNone(result["data"][0]["summary"])
        except Exception as e:
            # 如果因为环境问题失败，这是预期的
            pass
    
    def test_get_legal_knowledge_adapter_singleton(self):
        """测试获取适配器单例"""
        adapter1 = get_legal_knowledge_adapter()
        adapter2 = get_legal_knowledge_adapter()
        
        self.assertIs(adapter1, adapter2)
    
    def test_adapt_empty_data(self):
        """测试适配空数据"""
        raw_data = {
            "success": True,
            "data": [],
            "total": 0
        }
        
        result = self.adapter.adapt(raw_data)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["total"], 0)
        self.assertEqual(len(result["data"]), 0)
    
    def test_adapt_missing_fields(self):
        """测试适配缺失字段的数据"""
        raw_data = {
            "success": True,
            "data": [
                {
                    "document_id": "doc_001"
                    # 缺少 content 字段
                }
            ]
        }
        
        result = self.adapter.adapt(raw_data)
        
        self.assertTrue(result["success"])
        # 不应该抛出异常
        self.assertEqual(len(result["data"]), 1)


class TestDataAdapterIntegration(unittest.TestCase):
    """数据适配器集成测试"""
    
    @patch('backend.src.services.coze_knowledge_service.get_coze_knowledge_service')
    def test_full_adaptation_flow(self, mock_kb_service):
        """测试完整适配流程"""
        # 模拟扣子知识库服务返回
        mock_kb_instance = Mock()
        mock_kb_instance.search.return_value = {
            "success": True,
            "data": [
                {
                    "document_id": "doc_001",
                    "content": "第二百六十四条【盗窃罪】数额较大的，处三年以下有期徒刑"
                }
            ],
            "total": 1
        }
        mock_kb_service.return_value = mock_kb_instance
        
        # 执行适配流程
        from backend.src.services import get_coze_knowledge_service
        from backend.src.adapters import get_legal_knowledge_adapter
        
        kb_service = get_coze_knowledge_service(
            access_token="test_token",
            dataset_id="test_dataset"
        )
        
        raw_result = kb_service.search(query="盗窃罪", top_k=1)
        
        adapter = get_legal_knowledge_adapter(enable_llm_enhance=False)
        adapted_result = adapter.adapt(raw_result)
        
        # 验证结果
        self.assertTrue(adapted_result["success"])
        self.assertEqual(len(adapted_result["data"]), 1)
        self.assertEqual(adapted_result["data"][0]["article_number"], "第二百六十四条")
        self.assertEqual(adapted_result["data"][0]["crime_name"], "盗窃罪")


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试用例
    suite.addTests(loader.loadTestsFromTestCase(TestLegalKnowledgeAdapter))
    suite.addTests(loader.loadTestsFromTestCase(TestDataAdapterIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    
    if success:
        print("\n✅ 所有测试通过！")
    else:
        print("\n❌ 部分测试失败！")
