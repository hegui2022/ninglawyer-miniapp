"""
管理后台API接口
"""

from flask import Blueprint, request, jsonify
from loguru import logger
import traceback
from datetime import datetime, timedelta
from sqlalchemy import func

from api.user import require_auth
from database import get_db_context
from crud.crud import (
    user_crud, session_crud, consultation_crud, 
    contract_crud, desensitize_crud, file_crud,
    statistics_crud
)
from models.models import User, Session, ConsultationRecord, ContractRecord, Message

# 创建蓝图
admin_bp = Blueprint('admin', __name__)


def require_admin(f):
    """
    管理员权限验证装饰器
    
    注意：这是一个简单实现，生产环境应该更严格
    """
    def decorated_function(*args, **kwargs):
        # 这里应该验证管理员权限
        # 暂时跳过，实际项目中应该实现
        return f(*args, **kwargs)
    
    # 保留原始函数名称以避免端点冲突
    decorated_function.__name__ = f.__name__
    return decorated_function


@admin_bp.route('/dashboard', methods=['GET'])
@require_admin
def get_dashboard_stats():
    """
    获取仪表板统计数据
    
    返回格式：
    {
        "success": true,
        "data": {
            "total_users": 100,
            "active_users": 50,
            "total_sessions": 500,
            "total_consultations": 300,
            "total_contracts": 100,
            "today_messages": 50,
            "user_growth": [
                {"date": "2024-01-01", "count": 10},
                ...
            ]
        }
    }
    """
    try:
        with get_db_context() as db:
            # 用户统计
            total_users = db.query(func.count(User.id)).scalar()
            active_users = db.query(func.count(User.id)).filter(
                User.last_login >= datetime.now() - timedelta(days=7)
            ).scalar()
            
            # 会话统计
            total_sessions = db.query(func.count(Session.id)).scalar()
            
            # 咨询记录统计
            total_consultations = db.query(func.count(ConsultationRecord.id)).scalar()
            
            # 合同记录统计
            total_contracts = db.query(func.count(ContractRecord.id)).scalar()
            
            # 今日消息数
            today_messages = db.query(func.count(Message.id)).filter(
                func.date(Message.created_at) == datetime.now().date()
            ).scalar()
            
            # 用户增长（最近7天）
            user_growth = []
            for i in range(7):
                date = datetime.now() - timedelta(days=6-i)
                count = db.query(func.count(User.id)).filter(
                    func.date(User.created_at) == date.date()
                ).scalar()
                user_growth.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'count': count
                })
            
            return jsonify({
                'success': True,
                'data': {
                    'total_users': total_users,
                    'active_users': active_users,
                    'total_sessions': total_sessions,
                    'total_consultations': total_consultations,
                    'total_contracts': total_contracts,
                    'today_messages': today_messages,
                    'user_growth': user_growth
                }
            })
            
    except Exception as e:
        logger.error(f"获取仪表板统计异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'获取统计数据失败：{str(e)}'
        }), 500


@admin_bp.route('/users', methods=['GET'])
@require_admin
def get_users():
    """
    获取用户列表
    
    查询参数：
    - skip: 跳过数量（默认0）
    - limit: 限制数量（默认20）
    - keyword: 搜索关键词（可选）
    - status: 用户状态（active/inactive，可选）
    """
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 20))
        keyword = request.args.get('keyword')
        status = request.args.get('status')
        
        with get_db_context() as db:
            query = db.query(User)
            
            # 关键词搜索
            if keyword:
                query = query.filter(
                    (User.nickname.contains(keyword)) |
                    (User.phone.contains(keyword))
                )
            
            # 状态筛选
            if status == 'active':
                query = query.filter(User.is_active == True)
            elif status == 'inactive':
                query = query.filter(User.is_active == False)
            
            total = query.count()
            users = query.offset(skip).limit(limit).all()
            
            result = [
                {
                    'user_id': u.id,
                    'nickname': u.nickname,
                    'avatar': u.avatar,
                    'phone': u.phone[:3] + '****' + u.phone[7:] if u.phone else '',
                    'is_active': u.is_active,
                    'created_at': u.created_at.isoformat(),
                    'last_login': u.last_login.isoformat() if u.last_login else None
                }
                for u in users
            ]
            
            return jsonify({
                'success': True,
                'data': {
                    'users': result,
                    'total': total,
                    'skip': skip,
                    'limit': limit
                }
            })
            
    except Exception as e:
        logger.error(f"获取用户列表异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取用户列表失败：{str(e)}'
        }), 500


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@require_admin
def get_user_detail(user_id: int):
    """
    获取用户详情
    """
    try:
        with get_db_context() as db:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return jsonify({
                    'success': False,
                    'error': '用户不存在'
                }), 404
            
            # 获取用户统计
            session_count = db.query(func.count(Session.id)).filter(
                Session.user_id == user_id
            ).scalar()
            
            consultation_count = db.query(func.count(ConsultationRecord.id)).filter(
                ConsultationRecord.user_id == user_id
            ).scalar()
            
            contract_count = db.query(func.count(ContractRecord.id)).filter(
                ContractRecord.user_id == user_id
            ).scalar()
            
            return jsonify({
                'success': True,
                'data': {
                    'user_id': user.id,
                    'nickname': user.nickname,
                    'avatar': user.avatar,
                    'phone': user.phone,
                    'email': user.email,
                    'is_active': user.is_active,
                    'profile': user.profile,
                    'created_at': user.created_at.isoformat(),
                    'last_login': user.last_login.isoformat() if user.last_login else None,
                    'statistics': {
                        'session_count': session_count,
                        'consultation_count': consultation_count,
                        'contract_count': contract_count
                    }
                }
            })
            
    except Exception as e:
        logger.error(f"获取用户详情异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取用户详情失败：{str(e)}'
        }), 500


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@require_admin
def update_user(user_id: int):
    """
    更新用户信息
    """
    try:
        data = request.get_json()
        
        with get_db_context() as db:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return jsonify({
                    'success': False,
                    'error': '用户不存在'
                }), 404
            
            # 更新字段
            if 'nickname' in data:
                user.nickname = data['nickname']
            if 'is_active' in data:
                user.is_active = data['is_active']
            if 'profile' in data:
                user.profile = data['profile']
            
            db.commit()
            
            return jsonify({
                'success': True,
                'message': '更新成功'
            })
            
    except Exception as e:
        logger.error(f"更新用户信息异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'更新用户信息失败：{str(e)}'
        }), 500


@admin_bp.route('/users/<int:user_id>/sessions', methods=['GET'])
@require_admin
def get_user_sessions(user_id: int):
    """
    获取用户的会话列表
    """
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 20))
        
        with get_db_context() as db:
            sessions = db.query(Session).filter(
                Session.user_id == user_id
            ).order_by(Session.updated_at.desc()).offset(skip).limit(limit).all()
            
            result = [
                {
                    'session_id': s.id,
                    'title': s.title,
                    'message_count': s.message_count,
                    'created_at': s.created_at.isoformat(),
                    'updated_at': s.updated_at.isoformat()
                }
                for s in sessions
            ]
            
            return jsonify({
                'success': True,
                'data': {
                    'sessions': result,
                    'total': len(result)
                }
            })
            
    except Exception as e:
        logger.error(f"获取用户会话列表异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取用户会话列表失败：{str(e)}'
        }), 500


@admin_bp.route('/reports', methods=['GET'])
@require_admin
def get_reports():
    """
    获取报告数据
    
    查询参数：
    - type: 报告类型（user/consultation/contract）
    - days: 统计天数（默认7）
    """
    try:
        report_type = request.args.get('type', 'user')
        days = int(request.args.get('days', 7))
        
        with get_db_context() as db:
            start_date = datetime.now() - timedelta(days=days)
            end_date = datetime.now()
            
            if report_type == 'user':
                # 用户增长报告
                data = []
                for i in range(days):
                    date = start_date + timedelta(days=i)
                    count = db.query(func.count(User.id)).filter(
                        func.date(User.created_at) == date.date()
                    ).scalar()
                    data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'count': count
                    })
            
            elif report_type == 'consultation':
                # 咨询报告
                data = []
                for i in range(days):
                    date = start_date + timedelta(days=i)
                    count = db.query(func.count(ConsultationRecord.id)).filter(
                        func.date(ConsultationRecord.created_at) == date.date()
                    ).scalar()
                    data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'count': count
                    })
            
            elif report_type == 'contract':
                # 合同报告
                data = []
                for i in range(days):
                    date = start_date + timedelta(days=i)
                    count = db.query(func.count(ContractRecord.id)).filter(
                        func.date(ContractRecord.created_at) == date.date()
                    ).scalar()
                    data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'count': count
                    })
            
            else:
                return jsonify({
                    'success': False,
                    'error': '不支持的报告类型'
                }), 400
            
            return jsonify({
                'success': True,
                'data': {
                    'type': report_type,
                    'period': f'{days}天',
                    'data': data
                }
            })
            
    except Exception as e:
        logger.error(f"获取报告数据异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取报告数据失败：{str(e)}'
        }), 500
