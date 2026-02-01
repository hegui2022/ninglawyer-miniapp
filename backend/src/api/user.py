"""
用户API接口
"""

from flask import Blueprint, request, jsonify, g
from functools import wraps
from loguru import logger
import traceback

from services.user_service import user_service
from database import get_db_context
from crud.crud import statistics_crud
from models.models import User

# 创建蓝图
user_bp = Blueprint('user', __name__)


def require_auth(f):
    """
    认证装饰器
    验证JWT token
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # 获取token
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({
                    'success': False,
                    'error': '缺少认证token'
                }), 401
            
            token = auth_header.split(' ')[1]
            
            # 验证token
            payload = user_service.verify_jwt_token(token)
            if not payload:
                return jsonify({
                    'success': False,
                    'error': 'Token无效或已过期'
                }), 401
            
            # 设置当前用户ID
            g.user_id = payload['user_id']
            g.openid = payload['openid']
            
            return f(*args, **kwargs)
            
        except Exception as e:
            logger.error(f"认证失败：{str(e)}")
            return jsonify({
                'success': False,
                'error': '认证失败'
            }), 401
    
    return decorated_function


def get_current_user():
    """
    获取当前登录用户
    """
    return getattr(g, 'user_id', None)


@user_bp.route('/login', methods=['POST'])
def login():
    """
    微信小程序登录
    
    请求格式：
    {
        "code": "微信登录code"
    }
    
    返回格式：
    {
        "success": true,
        "data": {
            "user_id": 123,
            "token": "jwt_token",
            "is_new_user": false
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                'success': False,
                'error': '缺少code参数'
            }), 400
        
        code = data['code']
        
        logger.info(f"用户登录请求：code={code[:10]}...")
        
        # 微信登录
        result = user_service.wechat_login(code)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"登录接口异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'登录失败：{str(e)}'
        }), 500


@user_bp.route('/info', methods=['GET'])
@require_auth
def get_user_info():
    """
    获取用户信息
    
    返回格式：
    {
        "success": true,
        "data": {
            "user_id": 123,
            "nickname": "昵称",
            "avatar": "头像URL",
            ...
        }
    }
    """
    try:
        user_id = get_current_user()
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': '未登录'
            }), 401
        
        logger.info(f"获取用户信息：{user_id}")
        
        # 获取用户信息
        result = user_service.get_user_info(user_id)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"获取用户信息异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'获取用户信息失败：{str(e)}'
        }), 500


@user_bp.route('/update', methods=['POST'])
@require_auth
def update_user_info():
    """
    更新用户信息
    
    请求格式：
    {
        "nickname": "昵称",
        "avatar": "头像URL"
    }
    """
    try:
        user_id = get_current_user()
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': '未登录'
            }), 401
        
        data = request.get_json()
        
        logger.info(f"更新用户信息：{user_id}")
        
        # 更新用户信息
        result = user_service.update_user_info(
            user_id,
            nickname=data.get('nickname'),
            avatar=data.get('avatar')
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"更新用户信息异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'更新用户信息失败：{str(e)}'
        }), 500


@user_bp.route('/profile', methods=['GET'])
@require_auth
def get_user_profile():
    """
    获取用户档案
    """
    try:
        user_id = get_current_user()
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': '未登录'
            }), 401
        
        result = user_service.get_user_info(user_id)
        
        return jsonify({
            'success': True,
            'data': result.get('profile', {})
        })
        
    except Exception as e:
        logger.error(f"获取用户档案异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取用户档案失败：{str(e)}'
        }), 500


@user_bp.route('/profile', methods=['POST'])
@require_auth
def update_user_profile():
    """
    更新用户档案
    
    请求格式：
    {
        "real_name": "真实姓名",
        "address": "地址",
        "occupation": "职业"
    }
    """
    try:
        user_id = get_current_user()
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': '未登录'
            }), 401
        
        data = request.get_json()
        
        # 更新用户档案
        result = user_service.update_user_profile(user_id, data)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"更新用户档案异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'更新用户档案失败：{str(e)}'
        }), 500


@user_bp.route('/bind-phone', methods=['POST'])
@require_auth
def bind_phone():
    """
    绑定手机号
    
    请求格式：
    {
        "phone": "手机号"
    }
    """
    try:
        user_id = get_current_user()
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': '未登录'
            }), 401
        
        data = request.get_json()
        phone = data.get('phone')
        
        if not phone:
            return jsonify({
                'success': False,
                'error': '缺少手机号'
            }), 400
        
        # 绑定手机号
        result = user_service.bind_phone(user_id, phone)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"绑定手机号异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'绑定手机号失败：{str(e)}'
        }), 500


@user_bp.route('/delete', methods=['POST'])
@require_auth
def delete_user():
    """
    删除用户（软删除）
    """
    try:
        user_id = get_current_user()
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': '未登录'
            }), 401
        
        # 删除用户
        result = user_service.delete_user(user_id)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"删除用户异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'删除用户失败：{str(e)}'
        }), 500


@user_bp.route('/stats', methods=['GET'])
def get_app_stats():
    """
    获取应用统计数据（公开）
    
    返回格式：
    {
        "success": true,
        "data": {
            "total_users": 1000,
            "today_users": 10,
            "total_sessions": 5000,
            ...
        }
    }
    """
    try:
        with get_db_context() as db:
            # 统计数据
            total_users = user_crud.count_users(db)
            
            # 今日新用户
            from datetime import datetime
            today = datetime.utcnow().date()
            stats = statistics_crud.get_daily_stats(db, today)
            today_users = sum(s.metric_value for s in stats if s.metric_type == "new_users")
            
            return jsonify({
                'success': True,
                'data': {
                    'total_users': total_users,
                    'today_users': today_users or 0
                }
            })
            
    except Exception as e:
        logger.error(f"获取统计数据异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取统计数据失败：{str(e)}'
        }), 500
