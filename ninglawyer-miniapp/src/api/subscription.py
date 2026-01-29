"""
用户套餐管理API
提供套餐查询、升级、降级等功能
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from loguru import logger

from src.storage.db import get_db_session
from src.models.models import User, Statistics
from src.config.subscription import SUBSCRIPTION_PLANS, MODULE_TO_MINIPROGRAM, get_upgrade_path
from src.utils.skill_registry import skill_registry

subscription_bp = Blueprint('subscription', __name__)


@subscription_bp.route('/api/subscription/plans', methods=['GET'])
def get_all_plans():
    """获取所有套餐信息"""
    try:
        return jsonify({
            "success": True,
            "data": list(SUBSCRIPTION_PLANS.values())
        })
    except Exception as e:
        logger.error(f"获取套餐列表失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": "获取套餐列表失败"
        }), 500


@subscription_bp.route('/api/user/subscription', methods=['GET'])
def get_user_subscription():
    """获取用户当前套餐信息"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({
                "success": False,
                "error": "缺少用户ID"
            }), 400
        
        session = get_db_session()
        user = session.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({
                "success": False,
                "error": "用户不存在"
            }), 404
        
        # 获取套餐配置
        plan = SUBSCRIPTION_PLANS.get(user.subscription_type, SUBSCRIPTION_PLANS["basic"])
        
        # 获取可用模块
        modules_info = []
        for module_id in plan["modules"]:
            module_info = MODULE_TO_MINIPROGRAM.get(module_id, {})
            if module_info:
                modules_info.append({
                    "id": module_id,
                    "name": module_info.get("name"),
                    "icon": module_info.get("icon"),
                    "path": module_info.get("path"),
                    "miniprogram": module_info.get("miniprogram"),
                    "description": module_info.get("description")
                })
        
        # 检查套餐是否过期
        is_expired = False
        if user.subscription_end_at and user.subscription_end_at < datetime.utcnow():
            is_expired = True
        
        return jsonify({
            "success": True,
            "data": {
                "user_id": user.id,
                "subscription_type": user.subscription_type,
                "subscription_name": plan["name"],
                "subscription_price": plan["price"],
                "subscription_duration": plan["duration"],
                "subscription_start_at": user.subscription_start_at,
                "subscription_end_at": user.subscription_end_at,
                "is_expired": is_expired,
                "features": plan["features"],
                "modules": modules_info,
                "limits": plan["limits"],
                "ui_config": plan["ui_config"],
                "usage_stats": user.usage_stats or {}
            }
        })
        
    except Exception as e:
        logger.error(f"获取用户套餐失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": "获取用户套餐失败"
        }), 500


@subscription_bp.route('/api/subscription/upgrade', methods=['POST'])
def upgrade_subscription():
    """升级套餐"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        target_plan = data.get('plan')
        
        if not user_id or not target_plan:
            return jsonify({
                "success": False,
                "error": "缺少用户ID或目标套餐"
            }), 400
        
        # 检查套餐是否存在
        if target_plan not in SUBSCRIPTION_PLANS:
            return jsonify({
                "success": False,
                "error": "目标套餐不存在"
            }), 400
        
        session = get_db_session()
        user = session.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({
                "success": False,
                "error": "用户不存在"
            }), 404
        
        # 检查是否可以升级
        upgrade_path = get_upgrade_path(user.subscription_type)
        if target_plan not in upgrade_path:
            return jsonify({
                "success": False,
                "error": "无效的升级路径"
            }), 400
        
        # 更新套餐
        plan = SUBSCRIPTION_PLANS[target_plan]
        user.subscription_type = target_plan
        user.subscription_start_at = datetime.utcnow()
        user.subscription_end_at = datetime.utcnow() + timedelta(days=plan["duration"])
        user.enabled_modules = plan["modules"]
        
        session.commit()
        
        logger.info(f"✅ 用户 {user_id} 升级到 {target_plan} 套餐")
        
        return jsonify({
            "success": True,
            "message": "升级成功",
            "data": {
                "subscription_type": target_plan,
                "subscription_end_at": user.subscription_end_at
            }
        })
        
    except Exception as e:
        logger.error(f"升级套餐失败：{str(e)}")
        session.rollback()
        return jsonify({
            "success": False,
            "error": "升级套餐失败"
        }), 500


@subscription_bp.route('/api/subscription/downgrade', methods=['POST'])
def downgrade_subscription():
    """降级套餐"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        target_plan = data.get('plan')
        
        if not user_id or not target_plan:
            return jsonify({
                "success": False,
                "error": "缺少用户ID或目标套餐"
            }), 400
        
        session = get_db_session()
        user = session.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({
                "success": False,
                "error": "用户不存在"
            }), 404
        
        # 检查是否可以降级
        if target_plan not in SUBSCRIPTION_PLANS:
            return jsonify({
                "success": False,
                "error": "目标套餐不存在"
            }), 400
        
        # 更新套餐
        plan = SUBSCRIPTION_PLANS[target_plan]
        user.subscription_type = target_plan
        user.subscription_start_at = datetime.utcnow()
        user.subscription_end_at = datetime.utcnow() + timedelta(days=plan["duration"])
        user.enabled_modules = plan["modules"]
        
        session.commit()
        
        logger.info(f"✅ 用户 {user_id} 降级到 {target_plan} 套餐")
        
        return jsonify({
            "success": True,
            "message": "降级成功",
            "data": {
                "subscription_type": target_plan,
                "subscription_end_at": user.subscription_end_at
            }
        })
        
    except Exception as e:
        logger.error(f"降级套餐失败：{str(e)}")
        session.rollback()
        return jsonify({
            "success": False,
            "error": "降级套餐失败"
        }), 500


@subscription_bp.route('/api/subscription/modules', methods=['GET'])
def get_available_modules():
    """获取用户可用的模块列表"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({
                "success": False,
                "error": "缺少用户ID"
            }), 400
        
        session = get_db_session()
        user = session.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({
                "success": False,
                "error": "用户不存在"
            }), 404
        
        # 获取套餐配置
        plan = SUBSCRIPTION_PLANS.get(user.subscription_type, SUBSCRIPTION_PLANS["basic"])
        
        # 获取可用模块
        modules_info = []
        for module_id in plan["modules"]:
            module_info = MODULE_TO_MINIPROGRAM.get(module_id, {})
            if module_info:
                modules_info.append({
                    "id": module_id,
                    "name": module_info.get("name"),
                    "icon": module_info.get("icon"),
                    "path": module_info.get("path"),
                    "miniprogram": module_info.get("miniprogram"),
                    "description": module_info.get("description")
                })
        
        return jsonify({
            "success": True,
            "data": {
                "subscription_type": user.subscription_type,
                "modules": modules_info
            }
        })
        
    except Exception as e:
        logger.error(f"获取可用模块失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": "获取可用模块失败"
        }), 500


@subscription_bp.route('/api/subscription/usage', methods=['GET'])
def get_usage_stats():
    """获取用户使用统计"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({
                "success": False,
                "error": "缺少用户ID"
            }), 400
        
        session = get_db_session()
        user = session.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({
                "success": False,
                "error": "用户不存在"
            }), 404
        
        # 获取套餐配置
        plan = SUBSCRIPTION_PLANS.get(user.subscription_type, SUBSCRIPTION_PLANS["basic"])
        
        # 获取使用统计
        usage_stats = user.usage_stats or {}
        
        return jsonify({
            "success": True,
            "data": {
                "usage_stats": usage_stats,
                "limits": plan["limits"],
                "remaining": {
                    "consultations": plan["limits"]["consultations_per_month"] - usage_stats.get("consultations_this_month", 0),
                    "contracts": plan["limits"]["contracts_per_month"] - usage_stats.get("contracts_this_month", 0),
                    "desensitize": plan["limits"]["desensitize_per_month"] - usage_stats.get("desensitize_this_month", 0),
                    "risk_scans": plan["limits"]["risk_scans_per_month"] - usage_stats.get("risk_scans_this_month", 0)
                }
            }
        })
        
    except Exception as e:
        logger.error(f"获取使用统计失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": "获取使用统计失败"
        }), 500
