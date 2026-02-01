"""
测试真实的LLM调用
"""

import os
import sys
import requests
import json

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_llm_chat():
    """测试LLM聊天功能"""
    
    base_url = "http://localhost:5000"
    endpoint = "/api/v1/ninglawyer/chat"
    
    # 测试用例1：温暖陪伴型人设
    print("🧪 测试用例1：温暖陪伴型人设")
    print("="*60)
    
    data = {
        "query": "我想离婚，财产怎么分？",
        "user_id": "test_user_001",
        "user_type": "individual",
        "session_id": "test_session_001"
    }
    
    try:
        response = requests.post(
            base_url + endpoint,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功!")
            print(f"人设: {result['data']['personality']['name']}")
            print(f"回复: {result['data']['answer'][:200]}...")
            print(f"意图: {result['data']['intent']}")
        else:
            print(f"❌ 失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n" + "="*60 + "\n")
    
    # 测试用例2：专业严谨型人设
    print("🧪 测试用例2：专业严谨型人设")
    print("="*60)
    
    data = {
        "query": "合同违约怎么赔偿？",
        "user_id": "test_user_002",
        "user_type": "individual",
        "session_id": "test_session_002"
    }
    
    try:
        response = requests.post(
            base_url + endpoint,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功!")
            print(f"人设: {result['data']['personality']['name']}")
            print(f"回复: {result['data']['answer'][:200]}...")
            print(f"意图: {result['data']['intent']}")
        else:
            print(f"❌ 失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n" + "="*60 + "\n")
    
    # 测试用例3：企业商务型人设
    print("🧪 测试用例3：企业商务型人设")
    print("="*60)
    
    data = {
        "query": "企业合规风险怎么管理？",
        "user_id": "test_user_003",
        "user_type": "corporate",
        "session_id": "test_session_003"
    }
    
    try:
        response = requests.post(
            base_url + endpoint,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功!")
            print(f"人设: {result['data']['personality']['name']}")
            print(f"回复: {result['data']['answer'][:200]}...")
            print(f"意图: {result['data']['intent']}")
        else:
            print(f"❌ 失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n" + "="*60 + "\n")
    
    # 测试用例4：多轮对话
    print("🧪 测试用例4：多轮对话")
    print("="*60)
    
    session_id = "test_session_004"
    
    # 第一轮对话
    data1 = {
        "query": "我想问一下劳动合同的问题",
        "user_id": "test_user_004",
        "user_type": "individual",
        "session_id": session_id
    }
    
    try:
        response1 = requests.post(
            base_url + endpoint,
            json=data1,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"第一轮对话状态码: {response1.status_code}")
        
        if response1.status_code == 200:
            result1 = response1.json()
            print(f"✅ 第一轮成功!")
            print(f"回复: {result1['data']['answer'][:150]}...")
            
            # 第二轮对话
            data2 = {
                "query": "如果公司不签合同怎么办？",
                "user_id": "test_user_004",
                "user_type": "individual",
                "session_id": session_id
            }
            
            response2 = requests.post(
                base_url + endpoint,
                json=data2,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"第二轮对话状态码: {response2.status_code}")
            
            if response2.status_code == 200:
                result2 = response2.json()
                print(f"✅ 第二轮成功!")
                print(f"回复: {result2['data']['answer'][:150]}...")
                print("✅ 多轮对话测试通过!")
            else:
                print(f"❌ 第二轮失败: {response2.text}")
        else:
            print(f"❌ 第一轮失败: {response1.text}")
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    test_llm_chat()
