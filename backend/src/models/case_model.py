"""
法律案例模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.v1_models import Base
import json


class LegalCase(Base):
    """案例主表"""
    __tablename__ = 'legal_cases'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False, comment='标题')
    subtitle = Column(String(500), nullable=False, comment='副标题')
    basic_facts = Column(Text, comment='基本案情（HTML格式）')
    judgment_essence = Column(Text, comment='裁判要旨（HTML格式）')
    judgment_result = Column(Text, comment='裁判结果（HTML格式）')
    dispute_foci = Column(Text, comment='争议焦点（JSON字符串）')
    related_index = Column(Text, comment='关联索引（JSON字符串）')
    keywords = Column(Text, comment='关键词（JSON字符串）')
    
    status = Column(String(20), default='draft', comment='状态：draft-草稿, published-已发布')
    created_by = Column(String(100), comment='创建人')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关联关系
    proceedings = relationship("CaseProceeding", back_populates="case", cascade="all, delete-orphan")
    laws = relationship("CaseLaw", back_populates="case", cascade="all, delete-orphan")


class CaseProceeding(Base):
    """历审程序表"""
    __tablename__ = 'case_proceedings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey('legal_cases.id', ondelete='CASCADE'), nullable=False)
    
    procedure_type = Column(String(50), comment='审理程序')
    court = Column(String(200), comment='审理法院')
    case_number = Column(String(200), comment='案号')
    judgment_type = Column(String(50), comment='裁判类型')
    judgment_date = Column(DateTime, comment='裁判日期')
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联关系
    case = relationship("LegalCase", back_populates="proceedings")


class CaseLaw(Base):
    """主要法条表"""
    __tablename__ = 'case_laws'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey('legal_cases.id', ondelete='CASCADE'), nullable=False)
    
    law_name = Column(String(200), nullable=False, comment='法律名称')
    article_numbers = Column(String(500), nullable=False, comment='法条序号')
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联关系
    case = relationship("LegalCase", back_populates="laws")


def case_to_dict(case: LegalCase):
    """将案例对象转换为字典"""
    # 解析 JSON 字符串
    try:
        dispute_foci = json.loads(case.dispute_foci) if case.dispute_foci else []
    except:
        dispute_foci = []
    
    try:
        related_index = json.loads(case.related_index) if case.related_index else {}
    except:
        related_index = {}
    
    try:
        keywords = json.loads(case.keywords) if case.keywords else []
    except:
        keywords = []
    
    return {
        'id': case.id,
        'title': case.title,
        'subtitle': case.subtitle,
        'basic_facts': case.basic_facts,
        'judgment_essence': case.judgment_essence,
        'judgment_result': case.judgment_result,
        'dispute_foci': dispute_foci,
        'related_index': related_index,
        'keywords': keywords,
        'status': case.status,
        'created_by': case.created_by,
        'created_at': case.created_at.isoformat() if case.created_at else None,
        'updated_at': case.updated_at.isoformat() if case.updated_at else None,
        'proceedings': [
            {
                'id': p.id,
                'procedure_type': p.procedure_type,
                'court': p.court,
                'case_number': p.case_number,
                'judgment_type': p.judgment_type,
                'judgment_date': p.judgment_date.isoformat() if p.judgment_date else None
            }
            for p in case.proceedings
        ],
        'laws': [
            {
                'id': l.id,
                'law_name': l.law_name,
                'article_numbers': l.article_numbers
            }
            for l in case.laws
        ]
    }
