"""
测试怎么判API
包括：裁判观点查询、判例检索、类案查询、胜诉率分析
"""

import os
import sys
import requests
import json

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BASE_URL = "http://localhost:5000"


def test_judge_opinion():
    """测试裁判观点查询"""
    print("=" * 80)
    print("🧪 测试1：裁判观点查询")
    print("=" * 80)
    
    endpoint = "/api/v1/how_to_judge/judge/opinion"
    
    data = {
        "query": "离婚财产分割中，房产如何分配？",
        "user_id": "test_user_judge",
        "filters": {
            "court_level": "中级",
            "year": "2023"
        }
    }
    
    try:
        response = requests.post(
            BASE_URL + endpoint,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 裁判观点查询成功!")
            print(f"置信度: {result['data']['confidence']}")
            print(f"裁判观点: {result['data']['opinion'][:200]}...")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n")


def test_search_judge_cases():
    """测试判例检索"""
    print("=" * 80)
    print("🧪 测试2：判例检索")
    print("=" * 80)
    
    endpoint = "/api/v1/how_to_judge/judge/cases"
    
    data = {
        "keywords": "房屋买卖合同纠纷",
        "user_id": "test_user_judge",
        "filters": {
            "court": "中级人民法院",
            "case_type": "民事",
            "year_from": "2020",
            "page": 1,
            "page_size": 10
        }
    }
    
    try:
        response = requests.post(
            BASE_URL + endpoint,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 判例检索成功!")
            print(f"找到案例数: {result['data']['total']}")
            print(f"当前页: {result['data']['page']}")
            print(f"每页数量: {result['data']['page_size']}")
            if result['data']['cases']:
                print(f"第一个案例: {result['data']['cases'][0]['case_title']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n")


def test_similar_cases():
    """测试类案查询"""
    print("=" * 80)
    print("🧪 测试3：类案查询")
    print("=" * 80)
    
    endpoint = "/api/v1/how_to_judge/judge/similar_cases"
    
    data = {
        "case_description": "我与开发商签订了购房合同，开发商逾期交房超过6个月，我要求解除合同并赔偿损失。",
        "user_id": "test_user_judge"
    }
    
    try:
        response = requests.post(
            BASE_URL + endpoint,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 类案查询成功!")
            print(f"找到类似案件数: {len(result['data']['similar_cases'])}")
            print(f"胜诉率: {result['data']['win_rate']}")
            if result['data']['similar_cases']:
                print(f"最相似案例: {result['data']['similar_cases'][0]['case_title']}")
                print(f"相似度: {result['data']['similar_cases'][0]['similarity']}")
            print(f"共同特征: {result['data']['common_features'][:100]}...")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n")


def test_win_rate():
    """测试胜诉率分析"""
    print("=" * 80)
    print("🧪 测试4：胜诉率分析")
    print("=" * 80)
    
    endpoint = "/api/v1/how_to_judge/judge/win_rate"
    
    data = {
        "case_type": "房屋买卖合同纠纷",
        "user_id": "test_user_judge",
        "filters": {
            "region": "北京市",
            "year": "2023"
        }
    }
    
    try:
        response = requests.post(
            BASE_URL + endpoint,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 胜诉率分析成功!")
            print(f"案件类型: {result['data']['case_type']}")
            print(f"总体胜诉率: {result['data']['overall_win_rate']}")
            print(f"各法院胜诉率:")
            for court, rate in result['data']['by_court'].items():
                print(f"  - {court}: {rate}")
            print(f"影响因素: {', '.join(result['data']['key_factors'])}")
            print(f"建议数量: {len(result['data']['recommendations'])}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🚀 怎么判API测试")
    print("=" * 80 + "\n")
    
    # 运行所有测试
    test_judge_opinion()
    test_search_judge_cases()
    test_similar_cases()
    test_win_rate()
    
    print("\n" + "=" * 80)
    print("✅ 所有测试完成")
    print("=" * 80)
