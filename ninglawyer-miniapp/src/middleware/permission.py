"""
权限检查装饰器
用于API接口的权限控制
"""

from functools import wraps
from flask import request, jsonify
from loguru import logger

from src.storage.db import get_db_session
from src.models.models import User
from src.config.subscription import check_permission
from src.utils.skill_registry import skill_registry


def check_subscription_permission(required_subscription: str = "basic"):
    """
    套餐权限检查装饰器
    
    Args:
        required_subscription: 需要的套餐类型
        
    Usage:
        @check_subscription_permission("premium")
        def my_api():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # 获取用户ID
                user_id = request.args.get('user_id') or request.json.get('user_id') if request.is_json else None
                
                if not user_id:
                    return jsonify({
                        "success": False,
                        "error": "缺少用户ID"
                    }), 401
                
                # 查询用户
                session = get_db_session()
                user = session.query(User).filter(User.id == user_id).first()
                
                if not user:
                    return jsonify({
                        "success": False,
                        "error": "用户不存在"
                    }), 404
                
                # 检查套餐
                if not check_permission(user.subscription_type, required_subscription):
                    logger.warning(f"用户 {user_id} (套餐: {user.subscription_type}) 尝试访问需要 {required_subscription} 套餐的功能")
                    return jsonify({
                        "success": False,
                        "error": f"您的套餐（{user.subscription_type}）不支持此功能，请升级到 {required_subscription} 或更高套餐",
                        "upgrade_required": True,
                        "required_subscription": required_subscription,
                        "current_subscription": user.subscription_type
                    }), 403
                
                # 检查套餐是否过期
                if user.subscription_end_at and user.subscription_end_at < datetime.utcnow():
                    return jsonify({
                        "success": False,
                        "error": "您的套餐已过期，请续费",
                        "subscription_expired": True
                    }), 403
                
                # 将用户信息传递给路由函数
                return f(user=user, *args, **kwargs)
                
            except Exception as e:
                logger.error(f"权限检查失败：{str(e)}")
                return jsonify({
                    "success": False,
                    "error": "权限检查失败"
                }), 500
        
        return decorated_function
    return decorator


def check_skill_permission(skill_name: str):
    """
    技能权限检查装饰器
    
    Args:
        skill_name: 技能名称
        
    Usage:
        @check_skill_permission("contract_draft")
        def contract_draft_api():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # 获取用户ID
                user_id = request.args.get('user_id') or request.json.get('user_id') if request.is_json else None
                
                if not user_id:
                    return jsonify({
                        "success": False,
                        "error": "缺少用户ID"
                    }), 401
                
                # 检查技能权限
                permission_check = skill_registry.check_user_permission(skill_name, user_id)
                
                if not permission_check["has_permission"]:
                    logger.warning(f"用户 {user_id} 无权限使用技能：{skill_name}")
                    return jsonify({
                        "success": False,
                        "error": permission_check["error"],
                        "upgrade_required": True,
                        "required_subscription": permission_check.get("required_subscription")
                    }), 403
                
                # 将用户信息传递给路由函数
                return f(user_id=user_id, *args, **kwargs)
                
            except Exception as e:
                logger.error(f"技能权限检查失败：{str(e)}")
                return jsonify({
                    "success": False,
                    "error": "技能权限检查失败"
                }), 500
        
        return decorated_function
    return decorator


def check_usage_limit(limit_type: str, max_usage: int):
    """
    使用量限制检查装饰器
    
    Args:
        limit_type: 限制类型（consultations_per_month, contracts_per_month等）
        max_usage: 最大使用量
        
    Usage:
        @check_usage_limit("consultations_per_month", 10)
        def consultation_api():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # 获取用户ID
                user_id = request.args.get('user_id') or request.json.get('user_id') if request.is_json else None
                
                if not user_id:
                    return jsonify({
                        "success": False,
                        "error": "缺少用户ID"
                    }), 401
                
                # 查询用户
                session = get_db_session()
                user = session.query(User).filter(User.id == user_id).first()
                
                if not user:
                    return jsonify({
                        "success": False,
                        "error": "用户不存在"
                    }), 404
                
                # 获取使用统计
                usage_stats = user.usage_stats or {}
                current_usage = usage_stats.get(limit_type, 0)
                
                # 检查使用量
                if max_usage > 0 and current_usage >= max_usage:
                    logger.warning(f"用户 {user_id} 的 {limit_type} 使用量已达上限：{current_usage}/{max_usage}")
                    return jsonify({
                        "success": False,
                        "error": f"您本月的{limit_type}使用量已达上限（{max_usage}次），请升级套餐或下个月再试",
                        "usage_limit_reached": True,
                        "current_usage": current_usage,
                        "max_usage": max_usage
                    }), 429
                
                # 更新使用量
                usage_stats[limit_type] = current_usage + 1
                user.usage_stats = usage_stats
                session.commit()
                
                # 将用户信息传递给路由函数
                return f(user=user, *args, **kwargs)
                
            except Exception as e:
                logger.error(f"使用量检查失败：{str(e)}")
                return jsonify({
                    "success": False,
                    "error": "使用量检查失败"
                }), 500
        
        return decorated_function
    return decorator
