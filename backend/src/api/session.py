"""
会话管理API接口
"""

from flask import Blueprint, request, jsonify
from loguru import logger
import traceback

from api.user import require_auth, get_current_user
from services.session_service import session_service

# 创建蓝图
session_bp = Blueprint('session', __name__)


@session_bp.route('/create', methods=['POST'])
@require_auth
def create_session():
    """
    创建会话
    
    请求格式：
    {
        "skill_type": "desensitize | civil_consult | contract",
        "title": "会话标题（可选）"
    }
    
    返回格式：
    {
        "success": true,
        "data": {
            "session_id": 123,
            "skill_type": "civil_consult",
            "title": "法律咨询"
        }
    }
    """
    try:
        user_id = get_current_user()
        data = request.get_json()
        
        skill_type = data.get('skill_type')
        title = data.get('title')
        
        if not skill_type:
            return jsonify({
                'success': False,
                'error': '缺少skill_type参数'
            }), 400
        
        # 创建会话
        result = session_service.create_session(user_id, skill_type, title)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"创建会话异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'创建会话失败：{str(e)}'
        }), 500


@session_bp.route('/<int:session_id>', methods=['GET'])
@require_auth
def get_session(session_id: int):
    """
    获取会话信息
    """
    try:
        session = session_service.get_session(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': '会话不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': session
        })
        
    except Exception as e:
        logger.error(f"获取会话异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取会话失败：{str(e)}'
        }), 500


@session_bp.route('/list', methods=['GET'])
@require_auth
def list_sessions():
    """
    获取用户的会话列表
    
    查询参数：
    - skill_type: 技能类型（可选）
    """
    try:
        user_id = get_current_user()
        skill_type = request.args.get('skill_type')
        
        sessions = session_service.get_user_sessions(user_id, skill_type)
        
        return jsonify({
            'success': True,
            'data': {
                'sessions': sessions,
                'total': len(sessions)
            }
        })
        
    except Exception as e:
        logger.error(f"获取会话列表异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取会话列表失败：{str(e)}'
        }), 500


@session_bp.route('/<int:session_id>/messages', methods=['GET'])
@require_auth
def get_session_messages(session_id: int):
    """
    获取会话消息列表
    """
    try:
        messages = session_service.get_session_messages(session_id)
        
        return jsonify({
            'success': True,
            'data': {
                'messages': messages,
                'total': len(messages)
            }
        })
        
    except Exception as e:
        logger.error(f"获取消息列表异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取消息列表失败：{str(e)}'
        }), 500


@session_bp.route('/<int:session_id>/delete', methods=['POST'])
@require_auth
def delete_session(session_id: int):
    """
    删除会话
    """
    try:
        success = session_service.delete_session(session_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': '会话不存在或删除失败'
            }), 404
        
        return jsonify({
            'success': True,
            'message': '会话已删除'
        })
        
    except Exception as e:
        logger.error(f"删除会话异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'删除会话失败：{str(e)}'
        }), 500


@session_bp.route('/clear-old', methods=['POST'])
@require_auth
def clear_old_sessions():
    """
    清理旧会话
    
    请求格式：
    {
        "days": 30  // 清理多少天前的会话
    }
    """
    try:
        user_id = get_current_user()
        data = request.get_json()
        days = data.get('days', 30)
        
        count = session_service.clear_old_sessions(user_id, days)
        
        return jsonify({
            'success': True,
            'message': f'已清理 {count} 个旧会话'
        })
        
    except Exception as e:
        logger.error(f"清理旧会话异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'清理旧会话失败：{str(e)}'
        }), 500
