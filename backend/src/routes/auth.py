"""
认证相关API路由
"""

from flask import Blueprint, request, jsonify
from functools import wraps
import logging

from services.auth import AuthService
from utils.database import get_db

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ============================================
# 装饰器：验证token
# ============================================

def require_auth(f):
    """装饰器：验证JWT token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # 从header获取token
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                return jsonify({
                    "success": False,
                    "message": "缺少认证token"
                }), 401
            
            # 提取token（格式：Bearer <token>）
            token = auth_header.replace('Bearer ', '')
            
            # 验证token
            db = get_db()
            auth_service = AuthService(db)
            user_id = auth_service.verify_token(token)
            
            if not user_id:
                return jsonify({
                    "success": False,
                    "message": "token无效或已过期"
                }), 401
            
            # 将user_id传递给视图函数
            return f(user_id=user_id, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"认证失败: {str(e)}")
            return jsonify({
                "success": False,
                "message": "认证失败"
            }), 401
    
    return decorated_function


# ============================================
# 微信登录
# ============================================

@auth_bp.route('/wechat/login', methods=['POST'])
def wechat_login():
    """
    微信小程序登录
    
    Request Body:
        {
            "code": "微信登录凭证"
        }
    
    Response:
        {
            "success": true,
            "data": {
                "token": "JWT token",
                "user": {
                    "id": 1,
                    "name": "用户昵称",
                    "avatar": "头像URL",
                    "role": "individual",
                    "has_phone": false
                }
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                "success": False,
                "message": "缺少code参数"
            }), 400
        
        code = data.get('code')
        
        db = get_db()
        auth_service = AuthService(db)
        result = auth_service.wechat_login(code)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"微信登录失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"登录失败: {str(e)}"
        }), 500


# ============================================
# 发送验证码
# ============================================

@auth_bp.route('/verification-code/send', methods=['POST'])
def send_verification_code():
    """
    发送验证码
    
    Request Body:
        {
            "phone": "手机号",
            "code_type": "验证码类型（login/register/bind_phone）"
        }
    
    Response:
        {
            "success": true,
            "data": {
                "phone": "手机号",
                "code_type": "login",
                "expires_in": 300
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'phone' not in data:
            return jsonify({
                "success": False,
                "message": "缺少phone参数"
            }), 400
        
        phone = data.get('phone')
        code_type = data.get('code_type', 'login')
        
        # 验证手机号格式
        if len(phone) != 11 or not phone.isdigit():
            return jsonify({
                "success": False,
                "message": "手机号格式不正确"
            }), 400
        
        db = get_db()
        auth_service = AuthService(db)
        result = auth_service.send_verification_code(phone, code_type)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"发送验证码失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"发送失败: {str(e)}"
        }), 500


# ============================================
# 验证验证码
# ============================================

@auth_bp.route('/verification-code/verify', methods=['POST'])
def verify_verification_code():
    """
    验证验证码
    
    Request Body:
        {
            "phone": "手机号",
            "code": "验证码",
            "code_type": "验证码类型"
        }
    
    Response:
        {
            "success": true,
            "message": "验证成功"
        }
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['phone', 'code']):
            return jsonify({
                "success": False,
                "message": "缺少必要参数"
            }), 400
        
        phone = data.get('phone')
        code = data.get('code')
        code_type = data.get('code_type', 'login')
        
        db = get_db()
        auth_service = AuthService(db)
        result = auth_service.verify_code(phone, code, code_type)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"验证验证码失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"验证失败: {str(e)}"
        }), 500


# ============================================
# 绑定手机号
# ============================================

@auth_bp.route('/bind-phone', methods=['POST'])
@require_auth
def bind_phone(user_id):
    """
    绑定手机号
    
    Request Body:
        {
            "phone": "手机号",
            "code": "验证码"
        }
    
    Response:
        {
            "success": true,
            "data": {
                "phone": "手机号"
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['phone', 'code']):
            return jsonify({
                "success": False,
                "message": "缺少必要参数"
            }), 400
        
        phone = data.get('phone')
        code = data.get('code')
        
        db = get_db()
        auth_service = AuthService(db)
        result = auth_service.bind_phone(user_id, phone, code)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"绑定手机号失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"绑定失败: {str(e)}"
        }), 500


# ============================================
# 获取用户信息
# ============================================

@auth_bp.route('/user-info', methods=['GET'])
@require_auth
def get_user_info(user_id):
    """
    获取用户信息
    
    Response:
        {
            "success": true,
            "data": {
                "id": 1,
                "name": "用户昵称",
                "avatar": "头像URL",
                "phone": "手机号",
                "role": "individual",
                "status": "active",
                "created_at": "2025-01-10T00:00:00"
            }
        }
    """
    try:
        db = get_db()
        auth_service = AuthService(db)
        result = auth_service.get_user_info(user_id)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取失败: {str(e)}"
        }), 500
