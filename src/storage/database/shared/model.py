from sqlalchemy import BigInteger, Boolean, DateTime, Float, ForeignKey, Index, Integer, String, Text, JSON, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
from coze_coding_dev_sdk.database import Base

class Contract(Base):
    """合同表"""
    __tablename__ = "contracts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contract_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="合同名称")
    contract_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="合同类型")
    employer_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="用人单位名称")
    employee_name: Mapped[str] = mapped_column(String(128), nullable=False, comment="劳动者姓名")
    contract_content: Mapped[str] = mapped_column(Text, nullable=False, comment="合同内容")
    additional_clauses: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="附加条款内容")
    status: Mapped[str] = mapped_column(String(50), nullable=False, server_default="draft", comment="合同状态：draft/draft_signed/signed/terminated")
    version: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1", comment="版本号")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="创建时间")
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True, comment="更新时间")
    signed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="签署时间")
    terminated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="终止时间")
    
    # 外键：关联用户
    user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="创建用户ID")
    
    # 索引
    __table_args__ = (
        Index("ix_contracts_contract_type", "contract_type"),
        Index("ix_contracts_status", "status"),
        Index("ix_contracts_user_id", "user_id"),
    )


class ContractReview(Base):
    """合同审查记录表"""
    __tablename__ = "contract_reviews"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contract_id: Mapped[int] = mapped_column(Integer, ForeignKey("contracts.id"), nullable=False, comment="合同ID")
    review_result: Mapped[dict] = mapped_column(JSON, nullable=False, comment="审查结果（JSON）")
    overall_risk: Mapped[str] = mapped_column(String(50), nullable=False, comment="整体风险等级")
    high_risks: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0", comment="高风险数量")
    medium_risks: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0", comment="中风险数量")
    low_risks: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0", comment="低风险数量")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="审查时间")
    
    # 关系
    contract: Mapped["Contract"] = relationship("Contract", backref="reviews")


class ContractTemplate(Base):
    """合同模板表"""
    __tablename__ = "contract_templates"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    template_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="模板名称")
    template_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="模板类型")
    template_content: Mapped[str] = mapped_column(Text, nullable=False, comment="模板内容")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="模板描述")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true", comment="是否启用")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="创建时间")
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True, comment="更新时间")
    
    # 索引
    __table_args__ = (
        Index("ix_contract_templates_template_type", "template_type"),
        Index("ix_contract_templates_is_active", "is_active"),
    )


