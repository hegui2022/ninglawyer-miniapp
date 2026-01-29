"""
数据库表定义（PostgreSQL）
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    openid = Column(String(100), unique=True, index=True, nullable=True, comment="微信openid")
    unionid = Column(String(100), unique=True, index=True, nullable=True, comment="微信unionid")
    nickname = Column(String(100), nullable=True, comment="昵称")
    avatar = Column(String(500), nullable=True, comment="头像URL")
    phone = Column(String(20), nullable=True, index=True, comment="手机号")
    email = Column(String(100), nullable=True, comment="邮箱")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    sessions = relationship("Session", back_populates="user")
    consultation_records = relationship("ConsultationRecord", back_populates="user")
    contract_records = relationship("ContractRecord", back_populates="user")
    desensitize_records = relationship("DesensitizeRecord", back_populates="user")
    file_records = relationship("FileRecord", back_populates="user")
    profile = relationship("UserProfile", back_populates="user", uselist=False)


class Session(Base):
    """会话表"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    skill_type = Column(String(50), nullable=False, comment="技能类型")
    title = Column(String(200), nullable=True, comment="会话标题")
    is_active = Column(Boolean, default=True, comment="是否活跃")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    consultation_records = relationship("ConsultationRecord", back_populates="session")
    contract_records = relationship("ContractRecord", back_populates="session")
    desensitize_records = relationship("DesensitizeRecord", back_populates="session")


class Message(Base):
    """消息表"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, comment="会话ID")
    role = Column(String(20), nullable=False, comment="角色：user/assistant")
    content = Column(Text, nullable=False, comment="消息内容")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关系
    session = relationship("Session", back_populates="messages")


class ConsultationRecord(Base):
    """咨询记录表"""
    __tablename__ = "consultation_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, comment="会话ID")
    domain = Column(String(50), nullable=False, comment="法律领域")
    question = Column(Text, nullable=False, comment="问题")
    analysis = Column(Text, nullable=True, comment="法律分析")
    legal_basis = Column(JSON, default=list, comment="法律依据")
    suggestions = Column(JSON, default=list, comment="建议")
    risks = Column(JSON, default=list, comment="风险")
    next_steps = Column(JSON, default=list, comment="下一步行动")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关系
    user = relationship("User", back_populates="consultation_records")
    session = relationship("Session", back_populates="consultation_records")


class ContractRecord(Base):
    """合同记录表"""
    __tablename__ = "contract_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, comment="会话ID")
    contract_type = Column(String(50), nullable=False, comment="合同类型")
    contract_content = Column(Text, nullable=False, comment="合同内容")
    action = Column(String(20), nullable=False, comment="操作类型：draft/review")
    key_points = Column(JSON, default=list, comment="要点")
    tips = Column(JSON, default=list, comment="提示")
    risks = Column(JSON, default=list, comment="风险")
    score = Column(Integer, nullable=True, comment="风险评分")
    missing_clauses = Column(JSON, default=list, comment="缺失条款")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关系
    user = relationship("User", back_populates="contract_records")
    session = relationship("Session", back_populates="contract_records")


class DesensitizeRecord(Base):
    """脱敏记录表"""
    __tablename__ = "desensitize_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, comment="会话ID")
    original_text = Column(Text, nullable=False, comment="原始文本")
    desensitized_text = Column(Text, nullable=False, comment="脱敏后文本")
    details = Column(JSON, default=list, comment="脱敏详情")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关系
    user = relationship("User", back_populates="desensitize_records")
    session = relationship("Session", back_populates="desensitize_records")


class FileRecord(Base):
    """文件记录表"""
    __tablename__ = "file_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    filename = Column(String(255), nullable=False, comment="文件名")
    file_path = Column(String(500), nullable=False, comment="文件路径")
    file_size = Column(Integer, nullable=False, comment="文件大小（字节）")
    file_type = Column(String(50), nullable=False, comment="文件类型：image/document/other")
    mime_type = Column(String(100), nullable=True, comment="MIME类型")
    related_type = Column(String(50), nullable=True, comment="关联类型")
    related_id = Column(Integer, nullable=True, comment="关联ID")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关系
    user = relationship("User", back_populates="file_records")


class UserProfile(Base):
    """用户档案表"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, comment="用户ID")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    id_card = Column(String(50), nullable=True, comment="身份证号")
    address = Column(String(500), nullable=True, comment="地址")
    occupation = Column(String(100), nullable=True, comment="职业")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="profile")


class Statistics(Base):
    """统计表"""
    __tablename__ = "statistics"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DateTime, nullable=False, comment="日期")
    metric_type = Column(String(50), nullable=False, comment="指标类型")
    metric_value = Column(Integer, default=0, comment="指标值")
    extra_data = Column(JSON, default=dict, comment="额外数据")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")


class SystemConfig(Base):
    """系统配置表"""
    __tablename__ = "system_configs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False, comment="配置键")
    value = Column(Text, nullable=True, comment="配置值")
    description = Column(String(500), nullable=True, comment="描述")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
