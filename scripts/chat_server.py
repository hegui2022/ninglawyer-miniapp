"""
宁律师聊天测试服务器 - 支持文本+语音同时呈现
运行此脚本后，访问 http://localhost:8000 即可和宁律师对话
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

from flask import Flask, request, jsonify, render_template_string
from agents.agent import build_agent
import uuid
import json

app = Flask(__name__)

# 构建Agent
agent = build_agent()

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>宁律师 - 智能法律咨询</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .chat-container {
            width: 800px;
            height: 90vh;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }

        .chat-header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }

        .chat-header p {
            font-size: 14px;
            opacity: 0.9;
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f5f5f5;
        }

        .message {
            margin-bottom: 20px;
            display: flex;
            align-items: flex-start;
        }

        .message.user {
            justify-content: flex-end;
        }

        .message-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin: 0 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }

        .message.lawyer .message-avatar {
            background: #667eea;
            color: white;
        }

        .message.user .message-avatar {
            background: #4CAF50;
            color: white;
            margin-left: 10px;
            margin-right: 0;
        }

        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 12px;
            position: relative;
        }

        .message.lawyer .message-content {
            background: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .message.user .message-content {
            background: #4CAF50;
            color: white;
        }

        .message-audio {
            margin-top: 10px;
        }

        .message-audio audio {
            width: 100%;
        }

        .chat-input {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }

        .chat-input input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }

        .chat-input input:focus {
            border-color: #667eea;
        }

        .chat-input button {
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .chat-input button:hover {
            transform: scale(1.05);
        }

        .chat-input button:active {
            transform: scale(0.95);
        }

        .typing-indicator {
            padding: 10px 20px;
            color: #666;
            font-style: italic;
            display: none;
        }

        .typing-indicator.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>⚖️ 宁律师</h1>
            <p>智能法律咨询 - 文本+语音双模式</p>
        </div>

        <div class="chat-messages" id="chatMessages"></div>

        <div class="typing-indicator" id="typingIndicator">宁律师正在回复...</div>

        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="输入你的法律问题..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">发送</button>
        </div>
    </div>

    <script>
        // 添加消息到聊天界面
        function addMessage(role, content, audioUrl = null) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;

            const avatar = role === 'lawyer' ? '👨‍⚖️' : '👤';

            let audioHtml = '';
            if (audioUrl) {
                audioHtml = `
                    <div class="message-audio">
                        <audio controls autoplay>
                            <source src="${audioUrl}" type="audio/mpeg">
                            您的浏览器不支持音频播放。
                        </audio>
                    </div>
                `;
            }

            messageDiv.innerHTML = `
                <div class="message-avatar">${avatar}</div>
                <div class="message-content">
                    ${content}
                    ${audioHtml}
                </div>
            `;

            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        // 显示/隐藏输入指示器
        function showTypingIndicator(show) {
            const indicator = document.getElementById('typingIndicator');
            if (show) {
                indicator.classList.add('show');
            } else {
                indicator.classList.remove('show');
            }
        }

        // 发送消息
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();

            if (!message) return;

            // 显示用户消息
            addMessage('user', message);
            input.value = '';

            // 显示输入指示器
            showTypingIndicator(true);

            try {
                // 发送请求到后端
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        session_id: '{{ session_id }}'
                    })
                });

                const data = await response.json();

                // 隐藏输入指示器
                showTypingIndicator(false);

                // 显示律师回复
                if (data.success) {
                    // 如果有语音URL，语音会自动播放（audio标签有autoplay属性）
                    addMessage('lawyer', data.text, data.audio_url);
                } else {
                    addMessage('lawyer', data.error || '抱歉，回复出现问题，请重试。');
                }
            } catch (error) {
                showTypingIndicator(false);
                addMessage('lawyer', '网络错误，请检查连接后重试。');
                console.error('Error:', error);
            }
        }

        // 处理回车键
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // 页面加载完成后发送欢迎消息
        window.onload = function() {
            addMessage('lawyer', '你好！我是宁律师，有什么法律问题尽管问，我会用大白话给你讲清楚，还能语音回复你哦！🎤');
        };
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """聊天界面"""
    return render_template_string(HTML_TEMPLATE, session_id=str(uuid.uuid4()))


@app.route('/chat', methods=['POST'])
def chat():
    """处理聊天请求"""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', '')

        if not user_message:
            return jsonify({
                'success': False,
                'error': '消息不能为空'
            })

        print(f"[DEBUG] 收到消息: {user_message}, session_id: {session_id}")

        # 调用Agent
        from langchain_core.messages import HumanMessage

        # 使用新的session_id
        config = {
            "configurable": {"thread_id": session_id},
            "recursion_limit": 100  # 增加递归限制
        }

        print(f"[DEBUG] 开始调用 Agent...")
        # 调用Agent
        response = agent.invoke(
            {"messages": [HumanMessage(content=user_message)]},
            config=config
        )
        print(f"[DEBUG] Agent 调用完成")

        # 获取回复内容
        messages = response.get('messages', [])
        text_content = ""
        audio_url = None
        
        if messages:
            # 查找所有 AI 消息
            ai_messages = [msg for msg in messages if hasattr(msg, 'type') and msg.type == 'ai']
            
            if ai_messages:
                # 获取最后一个 AI 消息
                last_ai = ai_messages[-1]
                content = last_ai.content
                
                if isinstance(content, str):
                    # 提取语音URL
                    import re
                    
                    # 匹配各种格式的语音链接
                    url_patterns = [
                        r'https?://[^\s\)]+\.mp3[^\s\)]*',
                    ]
                    
                    for pattern in url_patterns:
                        match = re.search(pattern, content)
                        if match:
                            audio_url = match.group(0)
                            break
                    
                    # 清理文本内容，移除所有语音相关信息
                    clean_content = content
                    clean_content = re.sub(r'（语音链接：[^）]+）', '', clean_content)
                    clean_content = re.sub(r'语音已生成，访问地址：[^\n]*', '', clean_content)
                    clean_content = re.sub(r'（语音已生成[^）]+）', '', clean_content)
                    clean_content = re.sub(r'https?://[^\s\)]+\.mp3[^\s\)]*', '', clean_content)
                    
                    # 移除多余的换行和空格
                    clean_content = re.sub(r'\n\s*\n\s*\n', '\n\n', clean_content)
                    clean_content = clean_content.strip()
                    
                    # 如果清理后内容为空，使用默认消息
                    if not clean_content:
                        clean_content = "有什么具体问题随时说哈！"
                    
                    text_content = clean_content

        # 如果没有提取到文本，返回错误
        if not text_content:
            return jsonify({
                'success': False,
                'error': '无法获取回复'
            })

        # 自动调用 TTS 工具生成语音
        try:
            print(f"[DEBUG] 开始生成语音，文本长度: {len(text_content)}")
            
            # 直接调用 TTS API，而不是通过工具
            from coze_coding_dev_sdk import TTSClient
            from coze_coding_dev_sdk.s3 import S3SyncStorage
            from coze_coding_utils.runtime_ctx.context import new_context
            import requests
            import uuid
            
            # 步骤 1: 使用 TTS 合成语音
            ctx = new_context(method="tts.synthesize")
            tts_client = TTSClient(ctx=ctx)
            
            audio_url, audio_size = tts_client.synthesize(
                uid="legal_agent_user",
                text=text_content,
                speaker="saturn_zh_male_tiancaitongzhuo_tob",  # 天才同桌：聪明理性的男声
                audio_format="mp3",
                sample_rate=24000,
                speech_rate=-5,  # 稍慢语速，增加停顿感，更有阴阳顿挫
                loudness_rate=5   # 稍微提高音量，让重点更突出
            )
            
            # 步骤 2: 下载音频到临时目录
            response = requests.get(audio_url)
            audio_content = response.content
            
            # 生成临时文件名
            temp_filename = f"lawyer_reply_{uuid.uuid4().hex[:8]}.mp3"
            temp_filepath = os.path.join("/tmp", temp_filename)
            
            with open(temp_filepath, 'wb') as f:
                f.write(audio_content)
            
            # 步骤 3: 上传到对象存储
            storage = S3SyncStorage(
                endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
                access_key="",
                secret_key="",
                bucket_name=os.getenv("COZE_BUCKET_NAME"),
                region="cn-beijing",
            )
            
            # 生成对象存储的文件名
            file_key = f"legal_agent_audio/{temp_filename}"
            
            storage.upload_file(
                file_content=audio_content,
                file_name=file_key,
                content_type="audio/mpeg"
            )
            
            # 步骤 4: 生成签名 URL 并返回
            signed_url = storage.generate_presigned_url(
                key=file_key,
                expire_time=3600  # 1小时有效期
            )
            
            audio_url = signed_url
            print(f"[DEBUG] 语音生成成功: {audio_url[:50]}...")
        except Exception as e:
            print(f"[DEBUG] TTS 生成失败：{str(e)}")
            import traceback
            traceback.print_exc()
            # TTS 失败不影响文本回复

        return jsonify({
            'success': True,
            'text': text_content,
            'audio_url': audio_url
        })

    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': f'发生错误：{str(e)}'
        })


if __name__ == '__main__':
    print("=" * 60)
    print("🎙️  宁律师聊天服务器启动成功！")
    print("=" * 60)
    print("\n访问地址：http://localhost:8000")
    print("\n功能特点：")
    print("✓ 文本和语音同时显示")
    print("✓ 语音自动播放")
    print("✓ 知识库RAG支持")
    print("✓ 上下文记忆")
    print("✓ 幽默大白话风格")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 60 + "\n")

    app.run(host='0.0.0.0', port=8000, debug=True)
