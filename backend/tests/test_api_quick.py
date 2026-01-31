#!/usr/bin/env python
"""
测试API网关 - 快速版本
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests

API_BASE_URL = 'http://localhost:5000'

# 测试用例
test_cases = [
    {
        "name": "健康检查",
        "url": f"{API_BASE_URL}/health",
        "method": "GET"
    },
    {
        "name": "获取技能列表",
        "url": f"{API_BASE_URL}/api/v1/skills",
        "method": "GET"
    },
    {
        "name": "民事咨询聊天",
        "url": f"{API_BASE_URL}/api/v1/chat",
        "method": "POST",
        "data": {"message": "一般民事纠纷怎么处理？", "user_id": 1001, "app_id": "miniprogram_civil"}
    },
    {
        "name": "婚姻家事聊天",
        "url": f"{API_BASE_URL}/api/v1/chat",
        "method": "POST",
        "data": {"message": "我想离婚，需要什么材料？", "user_id": 1002, "app_id": "miniprogram_family"}
    },
    {
        "name": "直接调用财产分割技能",
        "url": f"{API_BASE_URL}/api/v1/skills/property_division",
        "method": "POST",
        "data": {"message": "我们家房产和存款怎么分？", "user_id": 1004, "app_id": "miniprogram_family"}
    }
]

passed = 0
failed = 0

for i, test_case in enumerate(test_cases, 1):
    print(f"\n测试用例 {i}/{len(test_cases)}: {test_case['name']}")
    
    try:
        if test_case['method'] == 'GET':
            response = requests.get(test_case['url'], timeout=30)
        else:
            response = requests.post(test_case['url'], json=test_case['data'], timeout=30)
        
        result = response.json()
        
        if response.status_code == 200 and (result.get('success', True) or isinstance(result, str)):
            print(f"✅ 通过")
            passed += 1
        else:
            print(f"❌ 失败: {result.get('error', '未知错误')}")
            failed += 1
    
    except Exception as e:
        print(f"❌ 异常: {e}")
        failed += 1

print(f"\n测试总结: ✅ {passed}/{len(test_cases)} 通过, ❌ {failed}/{len(test_cases)} 失败")
