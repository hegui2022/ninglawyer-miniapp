"""
认证服务
处理用户认证相关逻辑：微信登录、电话验证码
"""

import os
import jwt
import requests
import logging
import random
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session

from models.v1_models import User
from utils.redis_client import temp_data_cache

logger = logging.getLogger(__name__)


class AuthService:
    """认证服务"""
    
    def __init__(self, db: Session):
        """初始化"""
        self.db = db
    
    # ============================================
    # 微信登录
    # ============================================
    
    def wechat_login(self, code: str) -> Dict[str, Any]:
        """
        微信小程序登录
        
        Args:
            code: 微信登录凭证
        
        Returns:
            登录结果，包含token和用户信息
        """
        try:
            # 1. 调用微信API获取openid和unionid
            openid, unionid = self._get_wechat_info(code)
            
            if not openid:
                return {
                    "success": False,
                    "message": "微信登录失败，无法获取用户信息"
                }
            
            # 2. 查找或创建用户
            user = self._get_or_create_user(openid, unionid)
            
            if not user:
                return {
                    "success": False,
                    "message": "用户创建失败"
                }
            
            # 3. 生成JWT token
            token = self._generate_token(user.id)
            
            logger.info(f"用户登录成功: user_id={user.id}, openid={openid}")
            
            return {
                "success": True,
                "data": {
                    "token": token,
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "avatar": user.avatar,
                        "role": user.role,
                        "has_phone": bool(user.phone)
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"微信登录失败: {str(e)}")
            return {
                "success": False,
                "message": f"登录失败: {str(e)}"
            }
    
    def _get_wechat_info(self, code: str) -> Tuple[Optional[str], Optional[str]]:
        """
        调用微信API获取openid和unionid
        
        Args:
            code: 微信登录凭证
        
        Returns:
            (openid, unionid)
        """
        try:
            app_id = os.getenv("WECHAT_APP_ID")
            app_secret = os.getenv("WECHAT_APP_SECRET")
            
            if not app_id or not app_secret:
                logger.error("微信小程序配置缺失")
                return None, None
            
            # 调用微信code2session接口
            url = "https://api.weixin.qq.com/sns/jscode2session"
            params = {
                "appid": app_id,
                "secret": app_secret,
                "js_code": code,
                "grant_type": "authorization_code"
            }
            
            response = requests.get(url, params=params, timeout=5)
            result = response.json()
            
            if "errcode" in result:
                logger.error(f"微信API调用失败: {result}")
                return None, None
            
            openid = result.get("openid")
            unionid = result.get("unionid")  # 需要微信开放平台账号绑定才能获取
            
            logger.info(f"获取微信用户信息成功: openid={openid}, unionid={unionid}")
            
            return openid, unionid
            
        except Exception as e:
            logger.error(f"调用微信API失败: {str(e)}")
            return None, None
    
    def _get_or_create_user(self, openid: str, unionid: Optional[str]) -> Optional[User]:
        """
        获取或创建用户
        
        Args:
            openid: 微信openid
            unionid: 微信unionid
        
        Returns:
            用户对象
        """
        try:
            # 1. 根据openid查找用户
            user = self.db.query(User).filter(
                User.wechat_openid == openid
            ).first()
            
            # 2. 如果用户不存在，创建新用户
            if not user:
                user = User(
                    wechat_openid=openid,
                    wechat_unionid=unionid,
                    role="individual",
                    status="active"
                )
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
                logger.info(f"创建新用户: user_id={user.id}")
            else:
                # 更新unionid（如果之前没有）
                if unionid and not user.wechat_unionid:
                    user.wechat_unionid = unionid
                    self.db.commit()
            
            return user
            
        except Exception as e:
            logger.error(f"获取或创建用户失败: {str(e)}")
            self.db.rollback()
            return None
    
    def _generate_token(self, user_id: int) -> str:
        """
        生成JWT token
        
        Args:
            user_id: 用户ID
        
        Returns:
            JWT token
        """
        try:
            secret_key = os.getenv("JWT_SECRET_KEY", "default_secret_key")
            expires_days = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 86400)) / 86400
            
            payload = {
                "user_id": user_id,
                "exp": datetime.utcnow() + timedelta(days=expires_days),
                "iat": datetime.utcnow()
            }
            
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            
            return token
            
        except Exception as e:
            logger.error(f"生成token失败: {str(e)}")
            raise
    
    def verify_token(self, token: str) -> Optional[int]:
        """
        验证JWT token
        
        Args:
            token: JWT token
        
        Returns:
            用户ID，验证失败返回None
        """
        try:
            secret_key = os.getenv("JWT_SECRET_KEY", "default_secret_key")
            
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            
            return user_id
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token已过期")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token无效: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"验证token失败: {str(e)}")
            return None
    
    # ============================================
    # 电话验证码
    # ============================================
    
    def send_verification_code(self, phone: str, code_type: str = "login") -> Dict[str, Any]:
        """
        发送验证码
        
        Args:
            phone: 手机号
            code_type: 验证码类型（login/register/bind_phone）
        
        Returns:
            发送结果
        """
        try:
            # 1. 生成6位数字验证码
            code = "".join([str(random.randint(0, 9)) for _ in range(6)])
            
            # 2. 保存到Redis（5分钟过期）
            saved = temp_data_cache.save_verification_code(phone, code, code_type)
            if not saved:
                return {
                    "success": False,
                    "message": "验证码保存失败"
                }
            
            # 3. 发送短信
            # 注意：这里需要对接实际的短信服务API
            # 第一版可以先跳过，或者使用mock
            sms_sent = self._send_sms(phone, code, code_type)
            
            if not sms_sent:
                return {
                    "success": False,
                    "message": "短信发送失败"
                }
            
            logger.info(f"验证码发送成功: phone={phone}, code_type={code_type}")
            
            return {
                "success": True,
                "data": {
                    "phone": phone,
                    "code_type": code_type,
                    "expires_in": 300  # 5分钟
                }
            }
            
        except Exception as e:
            logger.error(f"发送验证码失败: {str(e)}")
            return {
                "success": False,
                "message": f"发送失败: {str(e)}"
            }
    
    def _send_sms(self, phone: str, code: str, code_type: str) -> bool:
        """
        发送短信
        
        Args:
            phone: 手机号
            code: 验证码
            code_type: 验证码类型
        
        Returns:
            是否发送成功
        """
        try:
            # TODO: 对接实际的短信服务API
            # 这里可以使用腾讯云、阿里云、火山引擎等短信服务
            
            # 第一版可以先跳过，或者使用日志记录
            logger.info(f"[模拟发送短信] phone={phone}, code={code}, code_type={code_type}")
            
            # 模拟发送成功
            return True
            
        except Exception as e:
            logger.error(f"发送短信失败: {str(e)}")
            return False
    
    def verify_code(self, phone: str, code: str, code_type: str = "login") -> Dict[str, Any]:
        """
        验证验证码
        
        Args:
            phone: 手机号
            code: 验证码
            code_type: 验证码类型
        
        Returns:
            验证结果
        """
        try:
            # 1. 从Redis获取验证码
            verified = temp_data_cache.verify_code(phone, code, code_type)
            
            if not verified:
                return {
                    "success": False,
                    "message": "验证码错误或已过期"
                }
            
            logger.info(f"验证码验证成功: phone={phone}, code_type={code_type}")
            
            return {
                "success": True,
                "message": "验证成功"
            }
            
        except Exception as e:
            logger.error(f"验证验证码失败: {str(e)}")
            return {
                "success": False,
                "message": f"验证失败: {str(e)}"
            }
    
    def bind_phone(self, user_id: int, phone: str, code: str) -> Dict[str, Any]:
        """
        绑定手机号
        
        Args:
            user_id: 用户ID
            phone: 手机号
            code: 验证码
        
        Returns:
            绑定结果
        """
        try:
            # 1. 验证验证码
            verify_result = self.verify_code(phone, code, "bind_phone")
            if not verify_result.get("success"):
                return {
                    "success": False,
                    "message": verify_result.get("message")
                }
            
            # 2. 检查手机号是否已被绑定
            existing_user = self.db.query(User).filter(
                User.phone == phone,
                User.id != user_id
            ).first()
            
            if existing_user:
                return {
                    "success": False,
                    "message": "该手机号已被其他用户绑定"
                }
            
            # 3. 绑定手机号
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return {
                    "success": False,
                    "message": "用户不存在"
                }
            
            user.phone = phone
            self.db.commit()
            
            logger.info(f"手机号绑定成功: user_id={user_id}, phone={phone}")
            
            return {
                "success": True,
                "data": {
                    "phone": phone
                }
            }
            
        except Exception as e:
            logger.error(f"绑定手机号失败: {str(e)}")
            self.db.rollback()
            return {
                "success": False,
                "message": f"绑定失败: {str(e)}"
            }
    
    # ============================================
    # 获取用户信息
    # ============================================
    
    def get_user_info(self, user_id: int) -> Dict[str, Any]:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
        
        Returns:
            用户信息
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {
                    "success": False,
                    "message": "用户不存在"
                }
            
            return {
                "success": True,
                "data": {
                    "id": user.id,
                    "name": user.name,
                    "avatar": user.avatar,
                    "phone": user.phone,
                    "role": user.role,
                    "status": user.status,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
            }
            
        except Exception as e:
            logger.error(f"获取用户信息失败: {str(e)}")
            return {
                "success": False,
                "message": f"获取失败: {str(e)}"
            }
