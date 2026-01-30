"""
用户认证和授权系统
"""

import os
import json
import time
import hashlib
import requests
from typing import Optional, Dict
from datetime import datetime, timedelta
from loguru import logger
from jose import JWTError, jwt

from src.database import get_db_context
from src.crud.crud import user_crud, user_profile_crud, statistics_crud
from src.models.schemas import UserCreate, UserProfileBase


class UserService:
    """用户服务"""
    
    def __init__(self):
        self.appid = os.getenv("WECHAT_APP_ID", "")
        self.secret = os.getenv("WECHAT_APP_SECRET", "")
        self.jwt_secret = os.getenv("JWT_SECRET", "ninglawyer-secret-key-2025")
        self.jwt_algorithm = "HS256"
        self.jwt_expiration = 30 * 24 * 60 * 60  # 30天
    
    def wechat_login(self, code: str) -> Dict:
        """
        微信小程序登录
        
        Args:
            code: 微信登录code
            
        Returns:
            用户信息和token
        """
        try:
            # 1. 获取session_key和openid
            session_data = self._get_wechat_session(code)
            openid = session_data.get("openid")
            session_key = session_data.get("session_key")
            
            if not openid:
                raise ValueError("获取openid失败")
            
            # 2. 查询或创建用户
            with get_db_context() as db:
                user = user_crud.get_by_openid(db, openid)
                
                if not user:
                    # 创建新用户
                    user_data = UserCreate(openid=openid)
                    user = user_crud.create(db, user_data)
                    
                    # 记录新用户统计
                    statistics_crud.record_metric(db, "new_users", 1)
                    logger.info(f"新用户注册：{user.id}")
                else:
                    logger.info(f"用户登录：{user.id}")
                
                # 生成JWT token
                token = self._create_jwt_token(user.id, openid)
                
                return {
                    "user_id": user.id,
                    "token": token,
                    "is_new_user": not user.nickname  # 如果没有昵称，说明是新用户
                }
                
        except Exception as e:
            logger.error(f"微信登录失败：{str(e)}")
            raise
    
    def _get_wechat_session(self, code: str) -> Dict:
        """
        获取微信session
        
        Args:
            code: 微信登录code
            
        Returns:
            openid, session_key等
        """
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": self.appid,
            "secret": self.secret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "errcode" in data:
            raise ValueError(f"微信登录失败：{data.get('errmsg')}")
        
        return data
    
    def _create_jwt_token(self, user_id: int, openid: str) -> str:
        """
        创建JWT token
        
        Args:
            user_id: 用户ID
            openid: 微信openid
            
        Returns:
            JWT token
        """
        payload = {
            "user_id": user_id,
            "openid": openid,
            "exp": datetime.utcnow() + timedelta(seconds=self.jwt_expiration),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return token
    
    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        """
        验证JWT token
        
        Args:
            token: JWT token
            
        Returns:
            用户信息或None
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except JWTError as e:
            logger.warning(f"Token验证失败：{str(e)}")
            return None
    
    def update_user_info(self, user_id: int, nickname: str = None, avatar: str = None) -> Dict:
        """
        更新用户信息
        
        Args:
            user_id: 用户ID
            nickname: 昵称
            avatar: 头像
            
        Returns:
            更新后的用户信息
        """
        try:
            with get_db_context() as db:
                user = user_crud.get_by_id(db, user_id)
                if not user:
                    raise ValueError("用户不存在")
                
                # 更新用户信息
                from src.models.schemas import UserUpdate
                update_data = UserUpdate(nickname=nickname, avatar=avatar)
                user = user_crud.update(db, user, update_data)
                
                return {
                    "user_id": user.id,
                    "nickname": user.nickname,
                    "avatar": user.avatar
                }
                
        except Exception as e:
            logger.error(f"更新用户信息失败：{str(e)}")
            raise
    
    def get_user_info(self, user_id: int) -> Dict:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户信息
        """
        try:
            with get_db_context() as db:
                user = user_crud.get_by_id(db, user_id)
                if not user:
                    raise ValueError("用户不存在")
                
                profile = user_profile_crud.get_by_user_id(db, user_id)
                
                return {
                    "user_id": user.id,
                    "nickname": user.nickname,
                    "avatar": user.avatar,
                    "phone": user.phone,
                    "email": user.email,
                    "profile": {
                        "real_name": profile.real_name if profile else None,
                        "address": profile.address if profile else None,
                        "occupation": profile.occupation if profile else None
                    } if profile else None,
                    "created_at": user.created_at.isoformat()
                }
                
        except Exception as e:
            logger.error(f"获取用户信息失败：{str(e)}")
            raise
    
    def update_user_profile(self, user_id: int, profile_data: Dict) -> Dict:
        """
        更新用户档案
        
        Args:
            user_id: 用户ID
            profile_data: 档案数据
            
        Returns:
            更新结果
        """
        try:
            with get_db_context() as db:
                user = user_crud.get_by_id(db, user_id)
                if not user:
                    raise ValueError("用户不存在")
                
                # 更新或创建用户档案
                profile = UserProfileBase(**profile_data)
                user_profile_crud.create_or_update(db, profile, user_id)
                
                return {
                    "success": True,
                    "message": "档案更新成功"
                }
                
        except Exception as e:
            logger.error(f"更新用户档案失败：{str(e)}")
            raise
    
    def bind_phone(self, user_id: int, phone: str) -> Dict:
        """
        绑定手机号
        
        Args:
            user_id: 用户ID
            phone: 手机号
            
        Returns:
            绑定结果
        """
        try:
            with get_db_context() as db:
                user = user_crud.get_by_id(db, user_id)
                if not user:
                    raise ValueError("用户不存在")
                
                # 检查手机号是否已被绑定
                existing_user = user_crud.get_by_phone(db, phone)
                if existing_user and existing_user.id != user_id:
                    raise ValueError("该手机号已被其他用户绑定")
                
                # 更新手机号
                from src.models.schemas import UserUpdate
                update_data = UserUpdate(phone=phone)
                user = user_crud.update(db, user, update_data)
                
                return {
                    "success": True,
                    "message": "手机号绑定成功",
                    "phone": phone
                }
                
        except Exception as e:
            logger.error(f"绑定手机号失败：{str(e)}")
            raise
    
    def delete_user(self, user_id: int) -> Dict:
        """
        删除用户（软删除）
        
        Args:
            user_id: 用户ID
            
        Returns:
            删除结果
        """
        try:
            with get_db_context() as db:
                # 标记为非活跃
                user = user_crud.get_by_id(db, user_id)
                if not user:
                    raise ValueError("用户不存在")
                
                user.is_active = False
                db.commit()
                
                logger.info(f"用户已删除：{user_id}")
                
                return {
                    "success": True,
                    "message": "用户已删除"
                }
                
        except Exception as e:
            logger.error(f"删除用户失败：{str(e)}")
            raise


# 全局用户服务实例
user_service = UserService()
