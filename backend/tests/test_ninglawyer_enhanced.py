"""
测试宁律师增强版API
包括：流式聊天、语音识别、语音合成、历史记录查询
"""

import os
import sys
import requests
import json

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BASE_URL = "http://localhost:5000"


def test_chat_stream():
    """测试流式聊天"""
    print("=" * 80)
    print("🧪 测试1：流式聊天")
    print("=" * 80)
    
    endpoint = "/api/v1/ninglawyer/chat/stream"
    
    data = {
        "query": "什么是合同违约？",
        "user_id": "test_user_stream",
        "user_type": "individual"
    }
    
    try:
        response = requests.post(
            BASE_URL + endpoint,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30,
            stream=True
        )
        
        if response.status_code == 200:
            print("✅ 流式聊天成功！\n")
            
            full_content = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk_data = json.loads(line)
                        chunk_type = chunk_data.get("type")
                        
                        if chunk_type == "chunk":
                            content = chunk_data.get("content", "")
                            full_content += content
                            print(content, end="", flush=True)
                        elif chunk_type == "end":
                            print("\n\n📊 流式聊天结束")
                            end_data = chunk_data.get("data", {})
                            print(f"会话ID: {end_data.get('session_id')}")
                            print(f"意图: {end_data.get('intent_desc')}")
                            print(f"人设: {end_data.get('personality', {}).get('name')}")
                            print(f"是否案源: {end_data.get('is_lead')}")
                        elif chunk_type == "error":
                            print(f"\n❌ 错误: {chunk_data.get('message')}")
                    except json.JSONDecodeError:
                        continue
            
            print(f"\n\n完整回复长度: {len(full_content)} 字符")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n")


def test_voice_recognize():
    """测试语音识别（模拟）"""
    print("=" * 80)
    print("🧪 测试2：语音识别（ASR）")
    print("=" * 80)
    
    endpoint = "/api/v1/ninglawyer/voice/recognize"
    
    # 注意：这里使用模拟数据，实际使用时需要上传真实的音频文件
    data = {
        "audio_url": "https://example.com/audio.mp3",  # 替换为真实的音频URL
        "user_id": "test_user_voice"
    }
    
    print("⚠️ 注意：此测试需要真实的音频URL或Base64数据")
    print("当前使用模拟URL，实际使用时请替换为真实音频")
    print("\n请求体示例:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    # 暂不发送请求，避免错误
    # 实际使用时取消注释以下代码
    """
    try:
        response = requests.post(
            BASE_URL + endpoint,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 语音识别成功!")
            print(f"识别的文本: {result['data']['text']}")
            print(f"音频时长: {result['data']['duration']}ms")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    """
    
    print("\n")


def test_voice_synthesize():
    """测试语音合成（TTS）"""
    print("=" * 80)
    print("🧪 测试3：语音合成（TTS）")
    print("=" * 80)
    
    endpoint = "/api/v1/ninglawyer/voice/synthesize"
    
    data = {
        "text": "您好，我是宁律师，很高兴为您服务。",
        "user_id": "test_user_tts",
        "speaker": "zh_female_xiaohe_uranus_bigtts"
    }
    
    try:
        response = requests.post(
            BASE_URL + endpoint,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 语音合成成功!")
            print(f"音频URL: {result['data']['audio_url']}")
            print(f"音频大小: {result['data']['audio_size']} 字节")
            print(f"音色: {result['data']['speaker']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n")


def test_history_query():
    """测试历史记录查询"""
    print("=" * 80)
    print("🧪 测试4：历史记录查询")
    print("=" * 80)
    
    # 先发送一条消息
    chat_endpoint = "/api/v1/ninglawyer/chat"
    chat_data = {
        "query": "测试历史记录",
        "user_id": "test_user_history",
        "session_id": "test_session_123"
    }
    
    try:
        response = requests.post(
            BASE_URL + chat_endpoint,
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ 聊天消息发送成功")
        
        # 查询历史记录
        history_endpoint = "/api/v1/ninglawyer/history"
        params = {"session_id": "test_session_123"}
        
        response = requests.get(
            BASE_URL + history_endpoint,
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 查询历史记录成功!")
            print(f"会话ID: {result['data']['session_id']}")
            print(f"消息数量: {result['data']['count']}")
            print(f"历史记录: {json.dumps(result['data']['history'], indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 查询失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n")


def test_clear_session():
    """测试清除会话"""
    print("=" * 80)
    print("🧪 测试5：清除会话")
    print("=" * 80)
    
    endpoint = "/api/v1/ninglawyer/session"
    
    data = {
        "session_id": "test_session_123"
    }
    
    try:
        response = requests.delete(
            BASE_URL + endpoint,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 清除会话成功!")
            print(f"消息: {result['data']['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🚀 宁律师增强版API测试")
    print("=" * 80 + "\n")
    
    # 运行所有测试
    test_chat_stream()
    test_voice_recognize()
    test_voice_synthesize()
    test_history_query()
    test_clear_session()
    
    print("\n" + "=" * 80)
    print("✅ 所有测试完成")
    print("=" * 80)
