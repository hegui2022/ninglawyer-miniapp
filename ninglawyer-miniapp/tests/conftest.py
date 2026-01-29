"""
测试配置
"""

import os
import sys

# 设置测试环境变量（必须在导入之前设置）
os.environ['DATABASE_URL'] = 'sqlite:///test.db'
os.environ['REDIS_HOST'] = 'localhost'
os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-purposes'
os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret-key'
os.environ['DEBUG'] = 'True'
os.environ['WECHAT_APP_ID'] = 'test_app_id'
os.environ['WECHAT_APP_SECRET'] = 'test_app_secret'

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入 Flask 应用
from src.main import app

# 创建测试客户端
client = app.test_client()

# 设置测试认证头
def get_test_token():
    """获取测试 token"""
    response = client.post('/api/user/wechat-login', json={'code': 'test_code'})
    data = response.get_json()
    return data['data']['token']

test_token = get_test_token()
auth_header = {'Authorization': f'Bearer {test_token}'}
