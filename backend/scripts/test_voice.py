"""
语音咨询功能测试脚本
"""

import os
import sys
import json
import requests
import base64
import time
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ============================================
# 测试配置
# ============================================

BASE_URL = "http://localhost:5000"
TEST_AUDIO_FILE = "assets/test_audio.wav"  # 测试音频文件路径


def test_get_speakers():
    """测试获取可用语音列表"""
    print("\n" + "="*60)
    print("测试1: 获取可用语音列表")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/api/consultation/voice/speakers')
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功! 获取到语音列表:")
            
            for category, speakers in data['data'].items():
                print(f"\n{category}:")
                for speaker_id, speaker_info in speakers.items():
                    recommended = " [推荐]" if speaker_info.get('recommended') else ""
                    print(f"  - {speaker_info['name']}: {speaker_info['description']}{recommended}")
            
            return True
        else:
            print(f"失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"异常: {str(e)}")
        return False


def test_voice_recognize(token, audio_file_path):
    """测试语音识别"""
    print("\n" + "="*60)
    print("测试2: 语音识别")
    print("="*60)
    
    if not os.path.exists(audio_file_path):
        print(f"音频文件不存在: {audio_file_path}")
        print("提示: 您可以提供一个测试音频文件")
        return None
    
    try:
        with open(audio_file_path, 'rb') as f:
            files = {'audio': f}
            headers = {'Authorization': f'Bearer {token}'}
            
            response = requests.post(
                f'{BASE_URL}/api/consultation/voice/recognize',
                files=files,
                headers=headers
            )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功! 识别结果:")
            print(f"  识别文字: {data['data']['text']}")
            print(f"  音频时长: {data['data'].get('duration', 0) / 1000:.2f}秒")
            
            return data['data']['text']
        else:
            print(f"失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"异常: {str(e)}")
        return None


def test_voice_synthesize(token, text):
    """测试语音合成"""
    print("\n" + "="*60)
    print("测试3: 语音合成")
    print("="*60)
    
    try:
        payload = {
            'text': text,
            'speaker': 'zh_female_xiaohe_uranus_bigtts',
            'audio_format': 'mp3',
            'sample_rate': 24000
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f'{BASE_URL}/api/consultation/voice/synthesize',
            json=payload,
            headers=headers
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功! 合成结果:")
            print(f"  音频URL: {data['data']['audio_url']}")
            print(f"  文件大小: {data['data']['audio_size']} 字节")
            print(f"  音频格式: {data['data']['audio_format']}")
            
            return True
        else:
            print(f"失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"异常: {str(e)}")
        return False


def test_civil_voice_consultation(token, audio_file_path):
    """测试民事语音咨询（完整流程）"""
    print("\n" + "="*60)
    print("测试4: 民事语音咨询（完整流程）")
    print("="*60)
    
    if not os.path.exists(audio_file_path):
        print(f"音频文件不存在: {audio_file_path}")
        print("跳过完整流程测试")
        return False
    
    try:
        with open(audio_file_path, 'rb') as f:
            files = {'audio': f}
            data = {
                'speaker': 'zh_female_xiaohe_uranus_bigtts'
            }
            headers = {'Authorization': f'Bearer {token}'}
            
            print("发送语音文件...")
            response = requests.post(
                f'{BASE_URL}/api/consultation/civil/voice',
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print(f"成功! 获得语音回复")
            
            # 从响应头获取信息
            session_id = response.headers.get('X-Session-Id', '')
            recognized_text = response.headers.get('X-Recognized-Text', '')
            answer_text = response.headers.get('X-Answer-Text', '')
            bot_id = response.headers.get('X-Bot-Id', '')
            bot_name = response.headers.get('X-Bot-Name', '')
            
            print(f"\n会话信息:")
            print(f"  会话ID: {session_id}")
            print(f"  识别文字: {recognized_text}...")
            print(f"  回复文字: {answer_text}...")
            print(f"  智能体: {bot_name} ({bot_id})")
            
            # 保存语音文件
            output_dir = "assets"
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"voice_response_{int(time.time())}.mp3")
            
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            print(f"\n语音文件已保存: {output_file}")
            print(f"文件大小: {len(response.content)} 字节")
            
            return True
        else:
            print(f"失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"异常: {str(e)}")
        return False


def test_civil_text_consultation(token):
    """测试民事文字咨询（对比）"""
    print("\n" + "="*60)
    print("测试5: 民事文字咨询（对比）")
    print("="*60)
    
    try:
        payload = {
            'query': '请问如何追讨债务？',
            'stream': False
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f'{BASE_URL}/api/consultation/civil',
            json=payload,
            headers=headers
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功! 咨询结果:")
            print(f"  回复: {data['data']['answer'][:100]}...")
            print(f"  会话ID: {data['data']['session_id']}")
            print(f"  智能体: {data['data']['bot_name']}")
            
            return True
        else:
            print(f"失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"异常: {str(e)}")
        return False


def main():
    """主函数"""
    print("="*60)
    print("语音咨询功能测试")
    print("="*60)
    
    # 等待服务启动
    print("\n等待服务启动...")
    time.sleep(2)
    
    # 检查服务健康状态
    try:
        response = requests.get(f'{BASE_URL}/health')
        if response.status_code != 200:
            print("服务未启动，请先启动Flask服务")
            return
        print("服务运行正常")
    except:
        print("无法连接到服务，请检查服务是否启动")
        return
    
    # 测试结果
    results = {}
    
    # 测试1: 获取语音列表
    results['get_speakers'] = test_get_speakers()
    
    # 测试2: 语音识别（需要音频文件）
    token = None
    audio_file_path = TEST_AUDIO_FILE
    
    if os.path.exists(audio_file_path):
        print(f"\n发现测试音频文件: {audio_file_path}")
    else:
        print(f"\n未找到测试音频文件: {audio_file_path}")
        print("提示: 您可以将测试音频文件放到 assets/ 目录下")
        
        # 尝试查找assets目录下的音频文件
        assets_dir = "assets"
        if os.path.exists(assets_dir):
            for file in os.listdir(assets_dir):
                if file.endswith(('.mp3', '.wav', '.ogg', '.opus')):
                    audio_file_path = os.path.join(assets_dir, file)
                    print(f"使用替代音频文件: {audio_file_path}")
                    break
    
    # 测试3: 语音合成
    test_text = "您好，我是宁律师民事咨询助手，很高兴为您服务。请问有什么法律问题需要咨询吗？"
    results['voice_synthesize'] = test_voice_synthesize(token, test_text)
    
    # 测试4: 民事语音咨询（完整流程）
    if os.path.exists(audio_file_path):
        results['civil_voice_consultation'] = test_civil_voice_consultation(token, audio_file_path)
    else:
        results['civil_voice_consultation'] = None
        print("\n跳过语音咨询测试（没有音频文件）")
    
    # 测试5: 民事文字咨询（对比）
    results['civil_text_consultation'] = test_civil_text_consultation(token)
    
    # 打印测试结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    for test_name, result in results.items():
        if result is None:
            status = "⏭️ 跳过"
        elif result:
            status = "✅ 通过"
        else:
            status = "❌ 失败"
        print(f"{test_name}: {status}")
    
    # 统计
    passed = sum(1 for r in results.values() if r is True)
    skipped = sum(1 for r in results.values() if r is None)
    failed = sum(1 for r in results.values() if r is False)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 通过, {skipped} 跳过, {failed} 失败")
    print("="*60)
    
    # 使用说明
    print("\n使用说明:")
    print("1. 将测试音频文件（WAV/MP3/OGG）放到 assets/ 目录")
    print("2. 重新运行测试脚本")
    print("3. 测试语音咨询功能")
    print("\n语音咨询API:")
    print("  POST /api/consultation/civil/voice")
    print("  Content-Type: multipart/form-data")
    print("  参数:")
    print("    - audio: 语音文件（必需）")
    print("    - session_id: 会话ID（可选）")
    print("    - speaker: 语音ID（可选）")
    print("\n语音识别API:")
    print("  POST /api/consultation/voice/recognize")
    print("  Content-Type: multipart/form-data")
    print("  参数:")
    print("    - audio: 语音文件（必需）")
    print("\n语音合成API:")
    print("  POST /api/consultation/voice/synthesize")
    print("  Content-Type: application/json")
    print("  参数:")
    print("    - text: 要合成的文字（必需）")
    print("    - speaker: 语音ID（可选）")


if __name__ == '__main__':
    main()
