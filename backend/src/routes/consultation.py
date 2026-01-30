"""
咨询相关API路由
包括刑事咨询、民事咨询等
"""

from flask import Blueprint, request, jsonify, Response, stream_with_context, send_file
import logging
import os
import tempfile
from functools import wraps

from services.coze_agent import CozeAgentService
from services.auth import AuthService
from services.voice import VoiceService
from utils.database import get_db
from routes.auth import require_auth

logger = logging.getLogger(__name__)

consultation_bp = Blueprint('consultation', __name__, url_prefix='/api/consultation')


# ============================================
# 刑事咨询
# ============================================

@consultation_bp.route('/criminal', methods=['POST'])
@require_auth
def criminal_consultation(user_id):
    """
    刑事法律咨询
    
    Request Body:
        {
            "query": "用户咨询问题",
            "session_id": "会话ID（可选，用于多轮对话）",
            "stream": false  // 是否流式输出（可选，默认false）
        }
    
    Response (非流式):
        {
            "success": true,
            "data": {
                "session_id": "会话ID",
                "answer": "智能体回复",
                "bot_id": "Bot ID",
                "bot_name": "Bot名称",
                "conversation_type": "criminal_consultation"
            }
        }
    
    Response (流式):
        事件流格式（SSE）
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "success": False,
                "message": "缺少query参数"
            }), 400
        
        query = data.get('query')
        session_id = data.get('session_id')
        stream = data.get('stream', False)
        
        db = get_db()
        agent_service = CozeAgentService(db)
        
        if stream:
            # 流式输出
            def generate():
                result = agent_service.chat(
                    user_id=user_id,
                    app_type="ninglawyer",
                    agent_type="criminal_consultation",
                    query=query,
                    session_id=session_id,
                    stream=True,
                    save_to_db=False
                )
                
                for chunk in result:
                    if isinstance(chunk, dict):
                        if chunk.get("success"):
                            data_chunk = chunk.get("data", {})
                            chunk_type = data_chunk.get("type")
                            
                            if chunk_type == "chunk":
                                # 消息片段
                                yield f"data: {json.dumps(data_chunk, ensure_ascii=False)}\n\n"
                            elif chunk_type == "end":
                                # 对话结束
                                yield f"data: {json.dumps(data_chunk, ensure_ascii=False)}\n\n"
                                yield "data: [DONE]\n\n"
                        else:
                            # 错误
                            error_chunk = {
                                "type": "error",
                                "message": chunk.get("message", "未知错误")
                            }
                            yield f"data: {json.dumps(error_chunk, ensure_ascii=False)}\n\n"
                            yield "data: [DONE]\n\n"
            
            return Response(
                stream_with_context(generate()),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'X-Accel-Buffering': 'no'
                }
            )
        else:
            # 非流式输出
            result = agent_service.chat(
                user_id=user_id,
                app_type="ninglawyer",
                agent_type="criminal_consultation",
                query=query,
                session_id=session_id,
                stream=False,
                save_to_db=False
            )
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"刑事咨询失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"咨询失败: {str(e)}"
        }), 500


# ============================================
# 民事咨询
# ============================================

@consultation_bp.route('/civil', methods=['POST'])
@require_auth
def civil_consultation(user_id):
    """
    民事法律咨询
    
    Request Body:
        {
            "query": "用户咨询问题",
            "session_id": "会话ID（可选）",
            "stream": false
        }
    
    Response: 同刑事咨询
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "success": False,
                "message": "缺少query参数"
            }), 400
        
        query = data.get('query')
        session_id = data.get('session_id')
        stream = data.get('stream', False)
        
        db = get_db()
        agent_service = CozeAgentService(db)
        
        if stream:
            # 流式输出
            def generate():
                result = agent_service.chat(
                    user_id=user_id,
                    app_type="fangfengxian",
                    agent_type="civil_consultation",
                    query=query,
                    session_id=session_id,
                    stream=True,
                    save_to_db=False
                )
                
                for chunk in result:
                    if isinstance(chunk, dict):
                        if chunk.get("success"):
                            data_chunk = chunk.get("data", {})
                            chunk_type = data_chunk.get("type")
                            
                            if chunk_type == "chunk":
                                yield f"data: {json.dumps(data_chunk, ensure_ascii=False)}\n\n"
                            elif chunk_type == "end":
                                yield f"data: {json.dumps(data_chunk, ensure_ascii=False)}\n\n"
                                yield "data: [DONE]\n\n"
                        else:
                            error_chunk = {
                                "type": "error",
                                "message": chunk.get("message", "未知错误")
                            }
                            yield f"data: {json.dumps(error_chunk, ensure_ascii=False)}\n\n"
                            yield "data: [DONE]\n\n"
            
            return Response(
                stream_with_context(generate()),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'X-Accel-Buffering': 'no'
                }
            )
        else:
            # 非流式输出
            result = agent_service.chat(
                user_id=user_id,
                app_type="fangfengxian",
                agent_type="civil_consultation",
                query=query,
                session_id=session_id,
                stream=False,
                save_to_db=False
            )
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"民事咨询失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"咨询失败: {str(e)}"
        }), 500


# ============================================
# 获取对话历史
# ============================================

@consultation_bp.route('/history/<session_id>', methods=['GET'])
@require_auth
def get_consultation_history(user_id, session_id):
    """
    获取对话历史
    
    Response:
        {
            "success": true,
            "data": [
                {
                    "role": "user",
                    "content": "用户消息",
                    "timestamp": "2025-01-10T00:00:00"
                },
                {
                    "role": "assistant",
                    "content": "智能体回复",
                    "timestamp": "2025-01-10T00:00:00",
                    "bot_id": "Bot ID",
                    "bot_name": "Bot名称"
                }
            ]
        }
    """
    try:
        db = get_db()
        agent_service = CozeAgentService(db)
        
        limit = request.args.get('limit', type=int)
        
        messages = agent_service.get_conversation_history(session_id, limit)
        
        return jsonify({
            "success": True,
            "data": messages
        }), 200
        
    except Exception as e:
        logger.error(f"获取对话历史失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取失败: {str(e)}"
        }), 500


# ============================================
# 清除对话
# ============================================

@consultation_bp.route('/clear', methods=['POST'])
@require_auth
def clear_consultation(user_id):
    """
    清除对话
    
    Request Body:
        {
            "session_id": "会话ID"
        }
    
    Response:
        {
            "success": true,
            "message": "对话已清除"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'session_id' not in data:
            return jsonify({
                "success": False,
                "message": "缺少session_id参数"
            }), 400
        
        session_id = data.get('session_id')
        
        db = get_db()
        agent_service = CozeAgentService(db)
        
        result = agent_service.clear_conversation(session_id)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"清除对话失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"清除失败: {str(e)}"
        }), 500


# ============================================
# 民事语音咨询
# ============================================

@consultation_bp.route('/civil/voice', methods=['POST'])
@require_auth
def civil_voice_consultation(user_id):
    """
    民事法律语音咨询
    
    接收语音文件，进行语音识别、咨询、语音合成，返回语音回复
    
    Request Body (multipart/form-data):
        - audio: 语音文件（WAV/MP3/OGG OPUS，最大100MB，最大2小时）
        - session_id: 会话ID（可选，用于多轮对话）
        - speaker: 语音ID（可选，默认使用女声）
    
    Response:
        {
            "success": true,
            "data": {
                "session_id": "会话ID",
                "recognized_text": "识别出的文字",
                "answer_text": "智能体回复的文字",
                "audio_file": "语音文件（MP3格式）",
                "bot_id": "Bot ID",
                "bot_name": "Bot名称",
                "conversation_type": "civil_consultation"
            }
        }
    """
    try:
        # 1. 检查是否上传了音频文件
        if 'audio' not in request.files:
            return jsonify({
                "success": False,
                "message": "缺少audio文件"
            }), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({
                "success": False,
                "message": "未选择文件"
            }), 400
        
        # 2. 保存临时音频文件
        temp_dir = tempfile.gettempdir()
        temp_audio_path = os.path.join(temp_dir, f"upload_{user_id}_{os.urandom(8).hex()}.wav")
        audio_file.save(temp_audio_path)
        
        logger.info(f"收到语音文件: user_id={user_id}, file={audio_file.filename}, size={os.path.getsize(temp_audio_path)}")
        
        # 3. 语音识别（ASR）
        db = get_db()
        voice_service = VoiceService(db)
        
        asr_result = voice_service.recognize_audio(
            user_id=user_id,
            audio_file_path=temp_audio_path
        )
        
        if not asr_result.get('success'):
            # 删除临时文件
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            
            return jsonify({
                "success": False,
                "message": f"语音识别失败: {asr_result.get('message')}"
            }), 400
        
        recognized_text = asr_result['data']['text']
        logger.info(f"语音识别成功: user_id={user_id}, text={recognized_text[:50]}...")
        
        # 4. 调用民事咨询智能体
        agent_service = CozeAgentService(db)
        session_id = request.form.get('session_id')
        
        consult_result = agent_service.chat(
            user_id=user_id,
            app_type="fangfengxian",
            agent_type="civil_consultation",
            query=recognized_text,
            session_id=session_id,
            stream=False,
            save_to_db=False
        )
        
        if not consult_result.get('success'):
            # 删除临时文件
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            
            return jsonify({
                "success": False,
                "message": f"咨询失败: {consult_result.get('message')}"
            }), 400
        
        answer_text = consult_result['data']['answer']
        bot_id = consult_result['data'].get('bot_id')
        bot_name = consult_result['data'].get('bot_name')
        actual_session_id = consult_result['data'].get('session_id')
        
        logger.info(f"民事咨询成功: user_id={user_id}, answer={answer_text[:50]}...")
        
        # 5. 语音合成（TTS）
        speaker = request.form.get('speaker')
        
        tts_result = voice_service.synthesize_and_download(
            user_id=user_id,
            text=answer_text,
            output_dir=temp_dir,
            speaker=speaker
        )
        
        if not tts_result.get('success'):
            # 删除临时文件
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            
            return jsonify({
                "success": False,
                "message": f"语音合成失败: {tts_result.get('message')}"
            }), 400
        
        voice_file_path = tts_result['data']['file_path']
        logger.info(f"语音合成成功: user_id={user_id}, file={voice_file_path}")
        
        # 6. 返回语音文件
        def remove_files():
            try:
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)
                if os.path.exists(voice_file_path):
                    os.remove(voice_file_path)
            except:
                pass
        
        response = send_file(
            voice_file_path,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name=f"consultation_{user_id}.mp3"
        )
        
        # 添加自定义响应头
        response.headers['X-Session-Id'] = actual_session_id
        response.headers['X-Recognized-Text'] = recognized_text[:100]  # 只返回前100个字符
        response.headers['X-Answer-Text'] = answer_text[:100]  # 只返回前100个字符
        response.headers['X-Bot-Id'] = bot_id or ''
        response.headers['X-Bot-Name'] = bot_name or ''
        
        # 设置文件删除回调
        response.call_on_close(remove_files)
        
        return response
        
    except Exception as e:
        logger.error(f"民事语音咨询失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"咨询失败: {str(e)}"
        }), 500


# ============================================
# 获取可用语音列表
# ============================================

@consultation_bp.route('/voice/speakers', methods=['GET'])
def get_voice_speakers():
    """
    获取可用的语音列表
    
    Response:
        {
            "success": true,
            "data": {
                "通用语音": {
                    "zh_female_xiaohe_uranus_bigtts": {
                        "name": "小禾（女声）",
                        "description": "通用女声，适合日常对话",
                        "gender": "female",
                        "recommended": True
                    },
                    ...
                },
                ...
            }
        }
    """
    try:
        speakers = VoiceService.get_available_speakers()
        
        return jsonify({
            "success": True,
            "data": speakers
        }), 200
        
    except Exception as e:
        logger.error(f"获取语音列表失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取失败: {str(e)}"
        }), 500


# ============================================
# 语音识别接口（单独使用）
# ============================================

@consultation_bp.route('/voice/recognize', methods=['POST'])
@require_auth
def voice_recognize(user_id):
    """
    语音识别（语音转文字）
    
    Request Body (multipart/form-data):
        - audio: 语音文件（WAV/MP3/OGG OPUS）
    
    Response:
        {
            "success": true,
            "data": {
                "text": "识别出的文字",
                "duration": 音频时长（毫秒）,
                "utterances": [...]
            }
        }
    """
    try:
        if 'audio' not in request.files:
            return jsonify({
                "success": False,
                "message": "缺少audio文件"
            }), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({
                "success": False,
                "message": "未选择文件"
            }), 400
        
        # 保存临时音频文件
        temp_dir = tempfile.gettempdir()
        temp_audio_path = os.path.join(temp_dir, f"recognize_{user_id}_{os.urandom(8).hex()}.wav")
        audio_file.save(temp_audio_path)
        
        try:
            # 语音识别
            db = get_db()
            voice_service = VoiceService(db)
            
            result = voice_service.recognize_audio(
                user_id=user_id,
                audio_file_path=temp_audio_path
            )
            
            return jsonify(result), 200 if result.get('success') else 400
            
        finally:
            # 删除临时文件
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
        
    except Exception as e:
        logger.error(f"语音识别失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"识别失败: {str(e)}"
        }), 500


# ============================================
# 语音合成接口（单独使用）
# ============================================

@consultation_bp.route('/voice/synthesize', methods=['POST'])
@require_auth
def voice_synthesize(user_id):
    """
    语音合成（文字转语音）
    
    Request Body:
        {
            "text": "要合成的文字",
            "speaker": "语音ID（可选）",
            "audio_format": "音频格式（可选，默认mp3）",
            "sample_rate": "采样率（可选，默认24000）"
        }
    
    Response:
        {
            "success": true,
            "data": {
                "audio_url": "音频文件URL",
                "audio_size": 文件大小（字节）,
                "audio_format": "音频格式"
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "success": False,
                "message": "缺少text参数"
            }), 400
        
        text = data.get('text')
        speaker = data.get('speaker')
        audio_format = data.get('audio_format', 'mp3')
        sample_rate = data.get('sample_rate', 24000)
        
        db = get_db()
        voice_service = VoiceService(db)
        
        result = voice_service.synthesize_speech(
            user_id=user_id,
            text=text,
            speaker=speaker,
            audio_format=audio_format,
            sample_rate=sample_rate
        )
        
        return jsonify(result), 200 if result.get('success') else 400
        
    except Exception as e:
        logger.error(f"语音合成失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"合成失败: {str(e)}"
        }), 500
