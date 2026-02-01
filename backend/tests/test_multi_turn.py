#!/usr/bin/env python
"""
测试多轮对话功能
"""

import requests
import json

BASE_URL = "http://localhost:5000"
CHAT_ENDPOINT = "/chat"

# 测试多轮对话
def test_multi_turn_conversation():
    session_id = None
    
    print("=" * 80)
    print("多轮对话测试")
    print("=" * 80)
    
    # 第1轮对话
    print("\n【第1轮对话】")
    print("用户: 我和别人签了合同，对方违约了，我该怎么办？")
    
    data1 = {
        "query": "我和别人签了合同，对方违约了，我该怎么办？",
        "user_id": "test_multi_turn",
        "user_type": "individual"
    }
    
    response1 = requests.post(f"{BASE_URL}{CHAT_ENDPOINT}", json=data1)
    result1 = response1.json()
    
    if result1.get('success'):
        session_id = result1['data']['session_id']
        print(f"宁律师: {result1['data']['answer'][:100]}...")
        print(f"Session ID: {session_id}")
    else:
        print(f"失败: {result1.get('message')}")
        return
    
    # 第2轮对话（使用相同的session_id）
    print("\n【第2轮对话】")
    print("用户: 那我需要准备什么证据？")
    
    data2 = {
        "query": "那我需要准备什么证据？",
        "user_id": "test_multi_turn",
        "session_id": session_id
    }
    
    response2 = requests.post(f"{BASE_URL}{CHAT_ENDPOINT}", json=data2)
    result2 = response2.json()
    
    if result2.get('success'):
        answer2 = result2['data']['answer']
        print(f"宁律师: {answer2}")
        
        # 检查是否引用了之前的对话
        if "基于我们之前的对话" in answer2 or "(基于我们之前的对话)" in answer2:
            print("\n✅ 多轮对话功能正常！宁律师成功引用了之前的对话。")
        else:
            print("\n⚠️ 多轮对话功能可能未正常工作，宁律师没有引用之前的对话。")
    else:
        print(f"失败: {result2.get('message')}")
    
    # 第3轮对话
    print("\n【第3轮对话】")
    print("用户: 如果协商不成，我可以起诉吗？")
    
    data3 = {
        "query": "如果协商不成，我可以起诉吗？",
        "user_id": "test_multi_turn",
        "session_id": session_id
    }
    
    response3 = requests.post(f"{BASE_URL}{CHAT_ENDPOINT}", json=data3)
    result3 = response3.json()
    
    if result3.get('success'):
        answer3 = result3['data']['answer']
        print(f"宁律师: {answer3}")
        
        # 检查是否引用了之前的对话
        if "基于我们之前的对话" in answer3 or "(基于我们之前的对话)" in answer3:
            print("\n✅ 多轮对话功能持续正常！")
        else:
            print("\n⚠️ 多轮对话功能可能未正常工作。")
    else:
        print(f"失败: {result3.get('message')}")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

if __name__ == "__main__":
    test_multi_turn_conversation()
