"""
数据库模型（第一版）
根据项目决策重新设计
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


# ============================================
# 1. 用户表（users）
# ============================================
class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # 微信信息
    wechat_openid = Column(String(100), unique=True, index=True, nullable=True, comment="微信openid")
    wechat_unionid = Column(String(100), unique=True, index=True, nullable=True, comment="微信unionid")
    # 手机信息
    phone = Column(String(20), unique=True, index=True, nullable=True, comment="手机号")
    # 基本信息
    name = Column(String(50), nullable=True, comment="姓名")
    avatar = Column(String(500), nullable=True, comment="头像URL")
    # 用户角色
    role = Column(String(20), default='individual', index=True, comment="用户角色：individual | enterprise_member | admin")
    # 状态
    status = Column(String(20), default='active', comment="状态：active | inactive | banned")
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    enterprise_relations = relationship("UserEnterpriseRelation", back_populates="user")
    contracts = relationship("Contract", back_populates="user")
    feedbacks = relationship("UserFeedback", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")


# ============================================
# 2. 企业表（enterprises）
# ============================================
class Enterprise(Base):
    """企业表"""
    __tablename__ = "enterprises"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # 企业基本信息
    name = Column(String(200), nullable=False, comment="企业名称")
    unified_code = Column(String(50), unique=True, index=True, nullable=True, comment="统一社会信用代码")
    business_license = Column(String(500), nullable=True, comment="营业执照图片URL")
    # 认证信息
    verified = Column(Boolean, default=False, index=True, comment="是否已认证")
    verified_at = Column(DateTime, nullable=True, comment="认证时间")
    # 联系信息
    contact_name = Column(String(50), nullable=True, comment="联系人姓名")
    contact_phone = Column(String(20), nullable=True, comment="联系电话")
    contact_email = Column(String(100), nullable=True, comment="联系邮箱")
    # 地址信息
    address = Column(String(500), nullable=True, comment="地址")
    province = Column(String(50), nullable=True, comment="省份")
    city = Column(String(50), nullable=True, comment="城市")
    # 状态
    status = Column(String(20), default='active', comment="状态：active | inactive")
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    user_relations = relationship("UserEnterpriseRelation", back_populates="enterprise")


# ============================================
# 3. 用户-企业关系表（user_enterprise_relations）
# ============================================
class UserEnterpriseRelation(Base):
    """用户-企业关系表"""
    __tablename__ = "user_enterprise_relations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    enterprise_id = Column(Integer, ForeignKey("enterprises.id", ondelete="CASCADE"), nullable=False, comment="企业ID")
    # 在企业中的角色
    role_in_enterprise = Column(String(50), index=True, comment="在企业中的角色：法务 | 老总 | 负责人 | 员工 | 董事 | 股东")
    # 部门（可选）
    department = Column(String(100), nullable=True, comment="部门")
    # 职位（可选）
    position = Column(String(100), nullable=True, comment="职位")
    # 状态
    status = Column(String(20), default='active', comment="状态：active | inactive")
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="enterprise_relations")
    enterprise = relationship("Enterprise", back_populates="user_relations")


# ============================================
# 4. 合同记录表（contracts）
# ============================================
class Contract(Base):
    """合同记录表"""
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    # 合同基本信息
    contract_type = Column(String(50), index=True, comment="合同类型：采购合同 | 服务合同 | 租赁合同 | 劳动合同 | 合作协议 | 保密协议 | 借款合同")
    contract_title = Column(String(200), nullable=True, comment="合同标题")
    contract_text = Column(Text, nullable=True, comment="合同内容")
    # 合同状态
    status = Column(String(20), default='draft', index=True, comment="状态：draft | signed | archived")
    # 合同元数据
    party_a = Column(String(200), nullable=True, comment="甲方")
    party_b = Column(String(200), nullable=True, comment="乙方")
    contract_amount = Column(Numeric(18, 2), nullable=True, comment="合同金额")
    contract_start_date = Column(Date, nullable=True, comment="合同开始日期")
    contract_end_date = Column(Date, nullable=True, comment="合同结束日期")
    # 扣子智能体生成的信息
    bot_id = Column(String(100), nullable=True, comment="使用的智能体ID")
    bot_name = Column(String(100), nullable=True, comment="智能体名称")
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, index=True, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="contracts")


# ============================================
# 5. 用户反馈表（user_feedback）
# ============================================
class UserFeedback(Base):
    """用户反馈表"""
    __tablename__ = "user_feedback"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="用户ID")
    # 反馈信息
    feedback_text = Column(Text, nullable=False, comment="反馈内容")
    feedback_type = Column(String(50), index=True, comment="反馈类型：bug | feature | other | complaint")
    rating = Column(Integer, nullable=True, comment="评分（1-5星）")
    # 关联信息
    related_consultation_id = Column(String(100), nullable=True, comment="关联的咨询ID")
    # 处理状态
    status = Column(String(20), default='pending', index=True, comment="状态：pending | processing | resolved")
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, index=True, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="feedbacks")


# ============================================
# 6. 会话记录表（conversations）
# 可选：保存重要的对话记录（比如企业认证相关）
# ============================================
class Conversation(Base):
    """会话记录表"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="用户ID")
    # 会话信息
    session_id = Column(String(100), unique=True, index=True, comment="会话ID")
    conversation_type = Column(String(50), index=True, comment="会话类型：consultation | contract | compliance | certification")
    # 会话内容
    user_message = Column(Text, nullable=True, comment="用户消息")
    bot_response = Column(Text, nullable=True, comment="智能体回复")
    bot_id = Column(String(100), nullable=True, comment="智能体ID")
    bot_name = Column(String(100), nullable=True, comment="智能体名称")
    # 元数据
    app_type = Column(String(50), comment="小程序类型：ninglawyer | fangfengxian | contract")
    extra_data = Column(JSON, nullable=True, comment="额外数据（JSON格式）")
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, index=True, comment="创建时间")
    
    # 关系
    user = relationship("User", back_populates="conversations")


# ============================================
# 7. 验证码表（verification_codes）
# 用于存储短信验证码
# ============================================
class VerificationCode(Base):
    """验证码表"""
    __tablename__ = "verification_codes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(String(20), nullable=False, index=True, comment="手机号")
    code = Column(String(10), nullable=False, comment="验证码")
    code_type = Column(String(20), default='login', index=True, comment="验证码类型：login | register | bind_phone")
    # 过期时间（5分钟）
    expires_at = Column(DateTime, nullable=False, index=True, comment="过期时间")
    # 是否已使用
    used = Column(Boolean, default=False, comment="是否已使用")
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")


# ============================================
# 8. 管理员配置（可选）
# ============================================
class AdminConfig(Base):
    """管理员配置表"""
    __tablename__ = "admin_configs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False, comment="配置键")
    value = Column(Text, nullable=True, comment="配置值")
    description = Column(String(500), nullable=True, comment="描述")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
