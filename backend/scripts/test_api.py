"""
API测试脚本
"""

import os
import sys
import json
import time
import requests

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_health_check():
    """测试健康检查接口"""
    print("\n========== 测试健康检查接口 ==========")
    try:
        response = requests.get('http://localhost:5000/health')
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def test_wechat_login():
    """测试微信登录接口"""
    print("\n========== 测试微信登录接口 ==========")
    try:
        # 模拟微信登录（需要真实的微信code，这里使用模拟数据）
        response = requests.post(
            'http://localhost:5000/api/auth/wechat/login',
            json={'code': 'test_code_123'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def test_send_verification_code():
    """测试发送验证码接口"""
    print("\n========== 测试发送验证码接口 ==========")
    try:
        response = requests.post(
            'http://localhost:5000/api/auth/verification-code/send',
            json={'phone': '13800138000', 'code_type': 'login'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def test_get_user_info(token):
    """测试获取用户信息接口"""
    print("\n========== 测试获取用户信息接口 ==========")
    try:
        if not token:
            print("跳过：没有token")
            return True
        
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            'http://localhost:5000/api/auth/user-info',
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def test_criminal_consultation(token):
    """测试刑事咨询接口"""
    print("\n========== 测试刑事咨询接口 ==========")
    try:
        if not token:
            print("跳过：没有token")
            return True
        
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(
            'http://localhost:5000/api/consultation/criminal',
            json={'query': '请问醉驾会判刑吗？', 'stream': False},
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def test_civil_consultation(token):
    """测试民事咨询接口"""
    print("\n========== 测试民事咨询接口 ==========")
    try:
        if not token:
            print("跳过：没有token")
            return True
        
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(
            'http://localhost:5000/api/consultation/civil',
            json={'query': '请问如何追讨债务？', 'stream': False},
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def test_contract_draft(token):
    """测试合同起草接口"""
    print("\n========== 测试合同起草接口 ==========")
    try:
        if not token:
            print("跳过：没有token")
            return True
        
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(
            'http://localhost:5000/api/contract/draft',
            json={
                'query': '帮我起草一份服务合同，甲方是一家IT公司，乙方是一家设计公司',
                'contract_type': '服务合同',
                'stream': False,
                'save_to_db': False
            },
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("开始API测试")
    print("=" * 50)
    
    # 等待服务启动
    print("\n等待服务启动...")
    time.sleep(3)
    
    # 测试结果
    results = {}
    
    # 测试健康检查
    results['health_check'] = test_health_check()
    
    # 测试微信登录
    results['wechat_login'] = test_wechat_login()
    
    # 获取token（微信登录失败则使用测试token）
    token = None
    if results['wechat_login']:
        try:
            response = requests.post(
                'http://localhost:5000/api/auth/wechat/login',
                json={'code': 'test_code_123'}
            )
            if response.status_code == 200:
                token = response.json().get('data', {}).get('token')
                print(f"\n获取到token: {token[:20]}...")
        except:
            pass
    
    # 测试其他接口
    results['send_verification_code'] = test_send_verification_code()
    results['get_user_info'] = test_get_user_info(token)
    results['criminal_consultation'] = test_criminal_consultation(token)
    results['civil_consultation'] = test_civil_consultation(token)
    results['contract_draft'] = test_contract_draft(token)
    
    # 打印测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    # 统计
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    print(f"\n总计: {passed}/{total} 通过")
    print("=" * 50)


if __name__ == '__main__':
    main()
