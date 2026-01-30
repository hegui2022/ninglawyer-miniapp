"""
历史记录API接口
"""

from flask import Blueprint, request, jsonify
from loguru import logger
import traceback

from src.api.user import require_auth, get_current_user
from src.database import get_db_context
from src.crud.crud import consultation_crud, contract_crud, desensitize_crud, statistics_crud

# 创建蓝图
records_bp = Blueprint('records', __name__)


@records_bp.route('/consultations', methods=['GET'])
@require_auth
def get_consultation_records():
    """
    获取用户的咨询记录
    
    查询参数：
    - skip: 跳过数量（默认0）
    - limit: 限制数量（默认20）
    - domain: 法律领域（可选）
    """
    try:
        user_id = get_current_user()
        
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 20))
        domain = request.args.get('domain')
        
        with get_db_context() as db:
            if domain:
                records = consultation_crud.get_user_records_by_domain(db, user_id, domain)
            else:
                records = consultation_crud.get_user_records(db, user_id, skip, limit)
            
            result = [
                {
                    "record_id": r.id,
                    "domain": r.domain,
                    "question": r.question,
                    "analysis": r.analysis,
                    "legal_basis": r.legal_basis,
                    "suggestions": r.suggestions,
                    "risks": r.risks,
                    "created_at": r.created_at.isoformat()
                }
                for r in records
            ]
            
            return jsonify({
                'success': True,
                'data': {
                    'records': result,
                    'total': len(result)
                }
            })
            
    except Exception as e:
        logger.error(f"获取咨询记录异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'获取咨询记录失败：{str(e)}'
        }), 500


@records_bp.route('/consultations/<int:record_id>', methods=['GET'])
@require_auth
def get_consultation_detail(record_id: int):
    """
    获取咨询记录详情
    """
    try:
        with get_db_context() as db:
            record = consultation_crud.get_by_id(db, record_id)
            
            if not record:
                return jsonify({
                    'success': False,
                    'error': '记录不存在'
                }), 404
            
            return jsonify({
                'success': True,
                'data': {
                    'record_id': record.id,
                    'domain': record.domain,
                    'question': record.question,
                    'analysis': record.analysis,
                    'legal_basis': record.legal_basis,
                    'suggestions': record.suggestions,
                    'risks': record.risks,
                    'next_steps': record.next_steps,
                    'created_at': record.created_at.isoformat()
                }
            })
            
    except Exception as e:
        logger.error(f"获取咨询详情异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取咨询详情失败：{str(e)}'
        }), 500


@records_bp.route('/contracts', methods=['GET'])
@require_auth
def get_contract_records():
    """
    获取用户的合同记录
    
    查询参数：
    - skip: 跳过数量（默认0）
    - limit: 限制数量（默认20）
    """
    try:
        user_id = get_current_user()
        
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 20))
        
        with get_db_context() as db:
            records = contract_crud.get_user_records(db, user_id, skip, limit)
            
            result = [
                {
                    'record_id': r.id,
                    'contract_type': r.contract_type,
                    'action': r.action,
                    'key_points': r.key_points,
                    'tips': r.tips,
                    'risks': r.risks,
                    'score': r.score,
                    'created_at': r.created_at.isoformat()
                }
                for r in records
            ]
            
            return jsonify({
                'success': True,
                'data': {
                    'records': result,
                    'total': len(result)
                }
            })
            
    except Exception as e:
        logger.error(f"获取合同记录异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取合同记录失败：{str(e)}'
        }), 500


@records_bp.route('/contracts/<int:record_id>', methods=['GET'])
@require_auth
def get_contract_detail(record_id: int):
    """
    获取合同记录详情
    """
    try:
        with get_db_context() as db:
            record = contract_crud.get_by_id(db, record_id)
            
            if not record:
                return jsonify({
                    'success': False,
                    'error': '记录不存在'
                }), 404
            
            return jsonify({
                'success': True,
                'data': {
                    'record_id': record.id,
                    'contract_type': record.contract_type,
                    'contract_content': record.contract_content,
                    'action': record.action,
                    'key_points': record.key_points,
                    'tips': record.tips,
                    'risks': record.risks,
                    'score': record.score,
                    'missing_clauses': record.missing_clauses,
                    'created_at': record.created_at.isoformat()
                }
            })
            
    except Exception as e:
        logger.error(f"获取合同详情异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取合同详情失败：{str(e)}'
        }), 500


@records_bp.route('/desensitizes', methods=['GET'])
@require_auth
def get_desensitize_records():
    """
    获取用户的脱敏记录
    
    查询参数：
    - skip: 跳过数量（默认0）
    - limit: 限制数量（默认20）
    """
    try:
        user_id = get_current_user()
        
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 20))
        
        with get_db_context() as db:
            records = desensitize_crud.get_user_records(db, user_id, skip, limit)
            
            result = [
                {
                    'record_id': r.id,
                    'original_text': r.original_text[:100] + '...' if len(r.original_text) > 100 else r.original_text,
                    'desensitized_text': r.desensitized_text[:100] + '...' if len(r.desensitized_text) > 100 else r.desensitized_text,
                    'details': r.details,
                    'created_at': r.created_at.isoformat()
                }
                for r in records
            ]
            
            return jsonify({
                'success': True,
                'data': {
                    'records': result,
                    'total': len(result)
                }
            })
            
    except Exception as e:
        logger.error(f"获取脱敏记录异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取脱敏记录失败：{str(e)}'
        }), 500


@records_bp.route('/desensitizes/<int:record_id>', methods=['GET'])
@require_auth
def get_desensitize_detail(record_id: int):
    """
    获取脱敏记录详情
    """
    try:
        with get_db_context() as db:
            record = desensitize_crud.get_by_id(db, record_id)
            
            if not record:
                return jsonify({
                    'success': False,
                    'error': '记录不存在'
                }), 404
            
            return jsonify({
                'success': True,
                'data': {
                    'record_id': record.id,
                    'original_text': record.original_text,
                    'desensitized_text': record.desensitized_text,
                    'details': record.details,
                    'created_at': record.created_at.isoformat()
                }
            })
            
    except Exception as e:
        logger.error(f"获取脱敏详情异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取脱敏详情失败：{str(e)}'
        }), 500


@records_bp.route('/stats', methods=['GET'])
@require_auth
def get_records_stats():
    """
    获取用户记录统计
    
    返回格式：
    {
        "success": true,
        "data": {
            "consultation_count": 10,
            "contract_count": 5,
            "desensitize_count": 8
        }
    }
    """
    try:
        user_id = get_current_user()
        
        with get_db_context() as db:
            consultation_count = len(consultation_crud.get_user_records(db, user_id, 0, 1000))
            contract_count = len(contract_crud.get_user_records(db, user_id, 0, 1000))
            desensitize_count = len(desensitize_crud.get_user_records(db, user_id, 0, 1000))
            
            return jsonify({
                'success': True,
                'data': {
                    'consultation_count': consultation_count,
                    'contract_count': contract_count,
                    'desensitize_count': desensitize_count
                }
            })
            
    except Exception as e:
        logger.error(f"获取记录统计异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取记录统计失败：{str(e)}'
        }), 500
