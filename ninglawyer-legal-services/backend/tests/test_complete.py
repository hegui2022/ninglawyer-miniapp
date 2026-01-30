"""
宁律师法律咨询小程序 - 完整测试用例
"""

import unittest
import json
import time
from datetime import datetime
from src.database import SessionLocal
from src.models.models import User, Session, Message


class TestUserAPI(unittest.TestCase):
    """用户 API 测试"""
    
    def test_01_wechat_login(self):
        """测试微信登录"""
        print("\n[测试] 微信登录...")
        # 模拟微信登录
        response = self.client.post('/api/user/wechat-login', 
                                   json={'code': 'test_code'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('token', data['data'])
        self.assertIn('user_info', data['data'])
        print("✓ 微信登录测试通过")
    
    def test_02_get_profile(self):
        """测试获取用户信息"""
        print("\n[测试] 获取用户信息...")
        response = self.client.get('/api/user/profile',
                                  headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('nickname', data['data'])
        print("✓ 获取用户信息测试通过")
    
    def test_03_update_profile(self):
        """测试更新用户信息"""
        print("\n[测试] 更新用户信息...")
        response = self.client.put('/api/user/profile',
                                  headers=self.auth_header,
                                  json={'nickname': '测试用户123'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        print("✓ 更新用户信息测试通过")


class TestSessionAPI(unittest.TestCase):
    """会话 API 测试"""
    
    def test_01_create_session(self):
        """测试创建会话"""
        print("\n[测试] 创建会话...")
        response = self.client.post('/api/session/create',
                                   headers=self.auth_header,
                                   json={'title': '测试会话'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('session_id', data['data'])
        self.session_id = data['data']['session_id']
        print(f"✓ 创建会话测试通过，会话ID: {self.session_id}")
    
    def test_02_get_sessions(self):
        """测试获取会话列表"""
        print("\n[测试] 获取会话列表...")
        response = self.client.get('/api/session/list',
                                  headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('sessions', data['data'])
        print(f"✓ 获取会话列表测试通过，共 {len(data['data']['sessions'])} 个会话")
    
    def test_03_add_message(self):
        """测试添加消息"""
        print("\n[测试] 添加消息...")
        response = self.client.post(f'/api/session/{self.session_id}/message',
                                   headers=self.auth_header,
                                   json={'content': '测试消息', 'role': 'user'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        print("✓ 添加消息测试通过")


class TestConsultationAPI(unittest.TestCase):
    """咨询 API 测试"""
    
    def test_01_get_domains(self):
        """测试获取法律领域"""
        print("\n[测试] 获取法律领域...")
        response = self.client.get('/api/consultation/domains')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['data']), 0)
        print(f"✓ 获取法律领域测试通过，共 {len(data['data'])} 个领域")
    
    def test_02_text_consult(self):
        """测试文字咨询"""
        print("\n[测试] 文字咨询...")
        response = self.client.post('/api/consultation/consult',
                                   headers=self.auth_header,
                                   json={
                                       'domain': 'civil',
                                       'question': '劳动仲裁的流程是什么？',
                                       'chat_history': []
                                   })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('answer', data['data'])
        print("✓ 文字咨询测试通过")


class TestRecordsAPI(unittest.TestCase):
    """历史记录 API 测试"""
    
    def test_01_get_consultation_records(self):
        """测试获取咨询记录"""
        print("\n[测试] 获取咨询记录...")
        response = self.client.get('/api/records/consultations',
                                  headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('records', data['data'])
        print("✓ 获取咨询记录测试通过")
    
    def test_02_get_stats(self):
        """测试获取统计数据"""
        print("\n[测试] 获取统计数据...")
        response = self.client.get('/api/records/stats',
                                  headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('consultation_count', data['data'])
        print("✓ 获取统计数据测试通过")


class TestFilesAPI(unittest.TestCase):
    """文件 API 测试"""
    
    def test_01_upload_file(self):
        """测试文件上传"""
        print("\n[测试] 文件上传...")
        import io
        
        # 创建测试文件
        file_content = b"Test file content"
        file_data = io.BytesIO(file_content)
        
        response = self.client.post('/api/files/upload',
                                   headers=self.auth_header,
                                   data={'file': (file_data, 'test.txt')},
                                   content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.file_id = data['data']['file_id']
        print(f"✓ 文件上传测试通过，文件ID: {self.file_id}")
    
    def test_02_get_file_info(self):
        """测试获取文件信息"""
        print("\n[测试] 获取文件信息...")
        response = self.client.get(f'/api/files/{self.file_id}',
                                  headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        print("✓ 获取文件信息测试通过")


class TestDatabase(unittest.TestCase):
    """数据库测试"""
    
    def test_01_create_user(self):
        """测试创建用户"""
        print("\n[测试] 数据库 - 创建用户...")
        db = SessionLocal()
        try:
            user = User(
                openid='test_openid_123',
                nickname='测试用户',
                phone='13800138000'
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            self.assertIsNotNone(user.id)
            print(f"✓ 创建用户测试通过，用户ID: {user.id}")
        finally:
            db.close()
    
    def test_02_create_session(self):
        """测试创建会话"""
        print("\n[测试] 数据库 - 创建会话...")
        db = SessionLocal()
        try:
            session = Session(
                user_id=1,
                title='测试会话'
            )
            db.add(session)
            db.commit()
            db.refresh(session)
            self.assertIsNotNone(session.id)
            print(f"✓ 创建会话测试通过，会话ID: {session.id}")
        finally:
            db.close()
    
    def test_03_create_message(self):
        """测试创建消息"""
        print("\n[测试] 数据库 - 创建消息...")
        db = SessionLocal()
        try:
            message = Message(
                session_id=1,
                role='user',
                content='测试消息'
            )
            db.add(message)
            db.commit()
            db.refresh(message)
            self.assertIsNotNone(message.id)
            print(f"✓ 创建消息测试通过，消息ID: {message.id}")
        finally:
            db.close()


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_01_complete_consultation_flow(self):
        """测试完整的咨询流程"""
        print("\n[集成测试] 完整咨询流程...")
        
        # 1. 创建会话
        response = self.client.post('/api/session/create',
                                   headers=self.auth_header,
                                   json={'title': '完整流程测试'})
        self.assertEqual(response.status_code, 200)
        session_id = json.loads(response.data)['data']['session_id']
        print(f"  ✓ 步骤1: 创建会话 (ID: {session_id})")
        
        # 2. 添加用户消息
        response = self.client.post(f'/api/session/{session_id}/message',
                                   headers=self.auth_header,
                                   json={'content': '劳动仲裁流程是什么？', 'role': 'user'})
        self.assertEqual(response.status_code, 200)
        print("  ✓ 步骤2: 添加用户消息")
        
        # 3. 发起咨询
        response = self.client.post('/api/consultation/consult',
                                   headers=self.auth_header,
                                   json={'domain': 'labor', 'question': '劳动仲裁流程是什么？'})
        self.assertEqual(response.status_code, 200)
        print("  ✓ 步骤3: 发起咨询")
        
        # 4. 获取会话消息
        response = self.client.get(f'/api/session/{session_id}/messages',
                                  headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        print("  ✓ 步骤4: 获取会话消息")
        
        # 5. 查询历史记录
        response = self.client.get('/api/records/consultations',
                                  headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        print("  ✓ 步骤5: 查询历史记录")
        
        print("✓ 完整咨询流程测试通过")


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_01_multiple_requests(self):
        """测试多次请求"""
        print("\n[性能测试] 多次请求...")
        
        start_time = time.time()
        
        for i in range(10):
            response = self.client.get('/api/consultation/domains')
            self.assertEqual(response.status_code, 200)
        
        elapsed_time = time.time() - start_time
        avg_time = elapsed_time / 10
        
        print(f"✓ 10次请求完成，平均响应时间: {avg_time:.3f}s")
        self.assertLess(avg_time, 1.0, "平均响应时间应小于1秒")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("开始运行宁律师法律咨询小程序完整测试")
    print("="*60)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestUserAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestConsultationAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestRecordsAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestFilesAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
