"""
咨询相关API路由
包括刑事咨询、民事咨询等
"""

from flask import Blueprint, request, jsonify, Response, stream_with_context
import logging
from functools import wraps

from services.coze_agent import CozeAgentService
from services.auth import AuthService
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
