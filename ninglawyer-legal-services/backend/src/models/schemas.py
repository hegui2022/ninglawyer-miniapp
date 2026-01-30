"""
数据库模型定义
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """用户基础模型"""
    openid: Optional[str] = None  # 微信openid
    unionid: Optional[str] = None  # 微信unionid
    nickname: Optional[str] = None  # 昵称
    avatar: Optional[str] = None  # 头像
    phone: Optional[str] = None  # 手机号
    email: Optional[str] = None  # 邮箱


class UserCreate(UserBase):
    """创建用户"""
    pass


class UserUpdate(BaseModel):
    """更新用户"""
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class User(UserBase):
    """用户模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True


class SessionBase(BaseModel):
    """会话基础模型"""
    user_id: int
    skill_type: str  # 技能类型：desensitize, civil_consult, contract
    title: str  # 会话标题


class SessionCreate(SessionBase):
    """创建会话"""
    pass


class Session(SessionBase):
    """会话模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    """消息基础模型"""
    session_id: int
    role: str  # user, assistant
    content: str


class Message(MessageBase):
    """消息模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConsultationRecordBase(BaseModel):
    """咨询记录基础模型"""
    user_id: int
    session_id: int
    domain: str  # 法律领域
    question: str
    analysis: str
    legal_basis: list = []
    suggestions: list = []
    risks: list = []


class ConsultationRecord(ConsultationRecordBase):
    """咨询记录模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ContractRecordBase(BaseModel):
    """合同记录基础模型"""
    user_id: int
    session_id: int
    contract_type: str  # 合同类型
    contract_content: str  # 合同内容
    action: str  # draft或review
    key_points: list = []
    tips: list = []
    risks: list = []


class ContractRecord(ContractRecordBase):
    """合同记录模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class DesensitizeRecordBase(BaseModel):
    """脱敏记录基础模型"""
    user_id: int
    session_id: int
    original_text: str
    desensitized_text: str
    details: list = []


class DesensitizeRecord(DesensitizeRecordBase):
    """脱敏记录模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class FileRecordBase(BaseModel):
    """文件记录基础模型"""
    user_id: int
    filename: str
    file_path: str
    file_size: int
    content_type: str
    category: str = 'evidence'
    session_id: Optional[int] = None


class FileCreate(FileRecordBase):
    """创建文件"""
    pass


class FileUpdate(BaseModel):
    """更新文件"""
    category: Optional[str] = None
    session_id: Optional[int] = None


class FileRecord(FileRecordBase):
    """文件记录模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfileBase(BaseModel):
    """用户档案基础模型"""
    user_id: int
    real_name: Optional[str] = None
    id_card: Optional[str] = None
    address: Optional[str] = None
    occupation: Optional[str] = None


class UserProfile(UserProfileBase):
    """用户档案模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
