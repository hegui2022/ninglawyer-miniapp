"""
安全加密工具
"""
import os
import hashlib
import hmac
import secrets
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
from loguru import logger


class Security:
    """安全加密工具类"""
    
    def __init__(self):
        # 从环境变量获取加密密钥
        secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
        
        # 生成 Fernet 密钥
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=secret_key.encode(),
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret_key.encode()))
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """
        加密数据
        
        Args:
            data: 明文字符串
        
        Returns:
            加密后的字符串（Base64编码）
        """
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"加密失败: {str(e)}")
            raise
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        解密数据
        
        Args:
            encrypted_data: 加密的数据字符串
        
        Returns:
            解密后的明文
        """
        try:
            encrypted = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"解密失败: {str(e)}")
            raise
    
    def hash_password(self, password: str) -> str:
        """
        哈希密码
        
        Args:
            password: 明文密码
        
        Returns:
            哈希后的密码
        """
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000
        )
        return f"{salt}${hashed.hex()}"
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        验证密码
        
        Args:
            password: 明文密码
            hashed_password: 哈希密码
        
        Returns:
            是否匹配
        """
        try:
            salt, hashed = hashed_password.split('$')
            computed_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt.encode(),
                100000
            )
            return hmac.compare_digest(computed_hash.hex(), hashed)
        except Exception as e:
            logger.error(f"密码验证失败: {str(e)}")
            return False
    
    def generate_token(self, length: int = 32) -> str:
        """
        生成随机令牌
        
        Args:
            length: 令牌长度
        
        Returns:
            随机令牌字符串
        """
        return secrets.token_urlsafe(length)
    
    def mask_sensitive_data(self, data: str, mask_char: str = '*', visible_chars: int = 4) -> str:
        """
        脱敏敏感数据
        
        Args:
            data: 原始数据
            mask_char: 遮罩字符
            visible_chars: 可见字符数
        
        Returns:
            脱敏后的数据
        """
        if not data or len(data) <= visible_chars:
            return mask_char * len(data)
        
        start = visible_chars // 2
        end = len(data) - (visible_chars - start)
        
        return data[:start] + mask_char * (end - start) + data[end:]


class PhoneSecurity(Security):
    """手机号安全处理"""
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        验证手机号格式
        
        Args:
            phone: 手机号
        
        Returns:
            是否有效
        """
        import re
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """
        脱敏手机号
        
        Args:
            phone: 手机号
        
        Returns:
            脱敏后的手机号
        """
        if not phone or len(phone) != 11:
            return phone
        return phone[:3] + '****' + phone[7:]


class IDCardSecurity(Security):
    """身份证安全处理"""
    
    @staticmethod
    def validate_idcard(idcard: str) -> bool:
        """
        验证身份证格式
        
        Args:
            idcard: 身份证号
        
        Returns:
            是否有效
        """
        import re
        # 简单验证，实际应该更严格
        pattern = r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$'
        return bool(re.match(pattern, idcard))
    
    @staticmethod
    def mask_idcard(idcard: str) -> str:
        """
        脱敏身份证号
        
        Args:
            idcard: 身份证号
        
        Returns:
            脱敏后的身份证号
        """
        if not idcard or len(idcard) < 10:
            return idcard
        return idcard[:6] + '********' + idcard[-4:]


class EmailSecurity(Security):
    """邮箱安全处理"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        验证邮箱格式
        
        Args:
            email: 邮箱地址
        
        Returns:
            是否有效
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def mask_email(email: str) -> str:
        """
        脱敏邮箱
        
        Args:
            email: 邮箱地址
        
        Returns:
            脱敏后的邮箱
        """
        if not email or '@' not in email:
            return email
        username, domain = email.split('@', 1)
        if len(username) > 2:
            username = username[0] + '*' * (len(username) - 2) + username[-1]
        return f"{username}@{domain}"


# 全局安全实例
_security = None


def get_security() -> Security:
    """获取安全实例"""
    global _security
    if _security is None:
        _security = Security()
    return _security
