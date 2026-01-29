"""
MCP (Model Context Protocol) API
提供模型上下文管理服务
"""

from flask import Blueprint, request, jsonify
from loguru import logger

from src.utils.response import success_response, error_response
from src.utils.logger import log_api_request

# 创建蓝图
mcp_bp = Blueprint('mcp', __name__)

# 模拟会话存储（生产环境应该使用 Redis）
_mcp_sessions = {}


def _get_session(session_id):
    """获取会话"""
    return _mcp_sessions.get(session_id)


def _save_session(session_id, session_data):
    """保存会话"""
    _mcp_sessions[session_id] = session_data


@mcp_bp.route('/init', methods=['POST'])
@log_api_request
def init_session():
    """
    初始化 MCP 会话
    """
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        context = data.get('context', {})
        tools = data.get('tools', [])
        
        if not session_id:
            return error_response("缺少会话 ID", 400)
        
        # 初始化会话
        session_data = {
            'session_id': session_id,
            'context': context,
            'tools': tools,
            'history': [],
            'created_at': datetime.now()
        }
        
        _save_session(session_id, session_data)
        
        logger.info(f"MCP 会话初始化: {session_id}")
        
        return success_response({
            'session_id': session_id,
            'status': 'initialized'
        })
        
    except Exception as e:
        logger.error(f"MCP 会话初始化失败：{str(e)}")
        return error_response(f"MCP 会话初始化失败：{str(e)}", 500)


@mcp_bp.route('/message', methods=['POST'])
@log_api_request
def send_message():
    """
    发送消息到 MCP
    """
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        message = data.get('message')
        history = data.get('history', [])
        context = data.get('context', {})
        metadata = data.get('metadata', {})
        
        if not session_id or not message:
            return error_response("缺少必要参数", 400)
        
        # 获取会话
        session = _get_session(session_id)
        if not session:
            return error_response("会话不存在", 404)
        
        # 更新上下文
        session['context'].update(context)
        session['history'] = history
        
        # TODO: 调用大模型生成响应
        # 这里应该集成真正的大模型调用
        response = f"收到您的消息: {message}"
        
        # 检查是否需要调用工具
        tool_calls = []
        if "合同" in message and "起草" in message:
            tool_calls.append({
                'id': f"tool_{len(tool_calls)}",
                'name': 'draft_contract',
                'parameters': {
                    'contract_type': '通用合同',
                    'partyA': '甲方',
                    'partyB': '乙方'
                }
            })
        
        # 更新历史
        session['history'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        session['history'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        _save_session(session_id, session)
        
        return success_response({
            'response': response,
            'toolCalls': tool_calls,
            'metadata': metadata
        })
        
    except Exception as e:
        logger.error(f"MCP 发送消息失败：{str(e)}")
        return error_response(f"MCP 发送消息失败：{str(e)}", 500)


@mcp_bp.route('/tool-result', methods=['POST'])
@log_api_request
def send_tool_result():
    """
    发送工具结果
    """
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        toolCallId = data.get('toolCallId')
        result = data.get('result')
        
        if not session_id or not toolCallId:
            return error_response("缺少必要参数", 400)
        
        # 获取会话
        session = _get_session(session_id)
        if not session:
            return error_response("会话不存在", 404)
        
        # TODO: 将工具结果发送给大模型继续处理
        response = f"工具调用完成，结果: {result}"
        
        # 更新历史
        session['history'].append({
            'role': 'tool',
            'content': str(result),
            'toolCallId': toolCallId,
            'timestamp': datetime.now().isoformat()
        })
        
        session['history'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        _save_session(session_id, session)
        
        return success_response({
            'response': response
        })
        
    except Exception as e:
        logger.error(f"MCP 发送工具结果失败：{str(e)}")
        return error_response(f"MCP 发送工具结果失败：{str(e)}", 500)


@mcp_bp.route('/context', methods=['PUT'])
@log_api_request
def update_context():
    """
    更新上下文
    """
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        context = data.get('context', {})
        
        if not session_id:
            return error_response("缺少会话 ID", 400)
        
        # 获取会话
        session = _get_session(session_id)
        if not session:
            return error_response("会话不存在", 404)
        
        # 更新上下文
        session['context'].update(context)
        _save_session(session_id, session)
        
        return success_response({
            'context': session['context']
        })
        
    except Exception as e:
        logger.error(f"MCP 更新上下文失败：{str(e)}")
        return error_response(f"MCP 更新上下文失败：{str(e)}", 500)


@mcp_bp.route('/end', methods=['POST'])
@log_api_request
def end_session():
    """
    结束会话
    """
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        
        if not session_id:
            return error_response("缺少会话 ID", 400)
        
        # 删除会话
        if session_id in _mcp_sessions:
            del _mcp_sessions[session_id]
        
        logger.info(f"MCP 会话结束: {session_id}")
        
        return success_response({
            'message': '会话已结束'
        })
        
    except Exception as e:
        logger.error(f"MCP 结束会话失败：{str(e)}")
        return error_response(f"MCP 结束会话失败：{str(e)}", 500)
