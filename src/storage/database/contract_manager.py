"""
合同管理 Manager
Contract Management Manager - 处理合同的 CRUD 操作
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from storage.database.shared.model import Contract, ContractReview, ContractTemplate
from coze_coding_dev_sdk.database import get_session
from datetime import datetime


# --- Pydantic Models for Contract ---
class ContractCreate(BaseModel):
    """创建合同的数据模型"""
    contract_name: str = Field(..., description="合同名称")
    contract_type: str = Field(..., description="合同类型")
    employer_name: str = Field(..., description="用人单位名称")
    employee_name: str = Field(..., description="劳动者姓名")
    contract_content: str = Field(..., description="合同内容")
    additional_clauses: Optional[str] = Field(None, description="附加条款内容")
    status: str = Field(default="draft", description="合同状态")
    user_id: Optional[int] = Field(None, description="创建用户ID")


class ContractUpdate(BaseModel):
    """更新合同的数据模型"""
    contract_name: Optional[str] = None
    contract_type: Optional[str] = None
    employer_name: Optional[str] = None
    employee_name: Optional[str] = None
    contract_content: Optional[str] = None
    additional_clauses: Optional[str] = None
    status: Optional[str] = None
    signed_at: Optional[datetime] = None
    terminated_at: Optional[datetime] = None


# --- Pydantic Models for ContractReview ---
class ContractReviewCreate(BaseModel):
    """创建审查记录的数据模型"""
    contract_id: int = Field(..., description="合同ID")
    review_result: dict = Field(..., description="审查结果（JSON）")
    overall_risk: str = Field(..., description="整体风险等级")
    high_risks: int = Field(default=0, description="高风险数量")
    medium_risks: int = Field(default=0, description="中风险数量")
    low_risks: int = Field(default=0, description="低风险数量")


# --- Pydantic Models for ContractTemplate ---
class ContractTemplateCreate(BaseModel):
    """创建模板的数据模型"""
    template_name: str = Field(..., description="模板名称")
    template_type: str = Field(..., description="模板类型")
    template_content: str = Field(..., description="模板内容")
    description: Optional[str] = Field(None, description="模板描述")
    is_active: bool = Field(default=True, description="是否启用")


class ContractTemplateUpdate(BaseModel):
    """更新模板的数据模型"""
    template_name: Optional[str] = None
    template_type: Optional[str] = None
    template_content: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


# Export all models
__all__ = [
    "ContractCreate",
    "ContractUpdate",
    "ContractReviewCreate",
    "ContractTemplateCreate",
    "ContractTemplateUpdate",
]


# --- Manager Classes ---
class ContractManager:
    """合同管理 Manager"""
    
    def create_contract(self, db: Session, contract_in: ContractCreate) -> Contract:
        """创建新合同"""
        contract_data = contract_in.model_dump()
        db_contract = Contract(**contract_data)
        db.add(db_contract)
        try:
            db.commit()
            db.refresh(db_contract)
            return db_contract
        except Exception as e:
            db.rollback()
            raise Exception(f"创建合同失败: {str(e)}")
    
    def get_contract_by_id(self, db: Session, contract_id: int) -> Optional[Contract]:
        """根据ID获取合同"""
        return db.query(Contract).filter(Contract.id == contract_id).first()
    
    def get_contracts(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        contract_type: Optional[str] = None,
        status: Optional[str] = None,
        user_id: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Contract]:
        """获取合同列表"""
        query = db.query(Contract)
        
        if contract_type:
            query = query.filter(Contract.contract_type == contract_type)
        if status:
            query = query.filter(Contract.status == status)
        if user_id:
            query = query.filter(Contract.user_id == user_id)
        
        # 使用 offset 参数如果提供，否则使用 skip
        skip = offset if offset is not None else skip
        
        return query.order_by(Contract.created_at.desc()).offset(skip).limit(limit).all()
    
    def count_contracts(
        self,
        db: Session,
        contract_type: Optional[str] = None,
        status: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> int:
        """统计合同数量"""
        query = db.query(Contract)
        
        if contract_type:
            query = query.filter(Contract.contract_type == contract_type)
        if status:
            query = query.filter(Contract.status == status)
        if user_id:
            query = query.filter(Contract.user_id == user_id)
        
        return query.count()
    
    def update_contract(self, db: Session, contract_id: int, contract_in: ContractUpdate) -> Optional[Contract]:
        """更新合同"""
        db_contract = self.get_contract_by_id(db, contract_id)
        if not db_contract:
            return None
        
        update_data = contract_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_contract, field):
                setattr(db_contract, field, value)
        
        db.add(db_contract)
        try:
            db.commit()
            db.refresh(db_contract)
            return db_contract
        except Exception as e:
            db.rollback()
            raise Exception(f"更新合同失败: {str(e)}")
    
    def delete_contract(self, db: Session, contract_id: int) -> bool:
        """删除合同"""
        db_contract = self.get_contract_by_id(db, contract_id)
        if not db_contract:
            return False
        
        try:
            db.delete(db_contract)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise Exception(f"删除合同失败: {str(e)}")
    
    def create_new_version(self, db: Session, contract_id: int) -> Optional[Contract]:
        """创建新版本"""
        db_contract = self.get_contract_by_id(db, contract_id)
        if not db_contract:
            return None
        
        # 创建新版本
        new_contract = Contract(
            contract_name=db_contract.contract_name + f" (v{db_contract.version + 1})",
            contract_type=db_contract.contract_type,
            employer_name=db_contract.employer_name,
            employee_name=db_contract.employee_name,
            contract_content=db_contract.contract_content,
            additional_clauses=db_contract.additional_clauses,
            status="draft",
            version=db_contract.version + 1,
            user_id=db_contract.user_id,
        )
        
        db.add(new_contract)
        try:
            db.commit()
            db.refresh(new_contract)
            return new_contract
        except Exception as e:
            db.rollback()
            raise Exception(f"创建新版本失败: {str(e)}")


class ContractReviewManager:
    """合同审查记录管理 Manager"""
    
    def create_review(self, db: Session, review_in: ContractReviewCreate) -> ContractReview:
        """创建审查记录"""
        review_data = review_in.model_dump()
        db_review = ContractReview(**review_data)
        db.add(db_review)
        try:
            db.commit()
            db.refresh(db_review)
            return db_review
        except Exception as e:
            db.rollback()
            raise Exception(f"创建审查记录失败: {str(e)}")
    
    def get_reviews_by_contract_id(self, db: Session, contract_id: int) -> List[ContractReview]:
        """根据合同ID获取审查记录"""
        return db.query(ContractReview).filter(
            ContractReview.contract_id == contract_id
        ).order_by(ContractReview.created_at.desc()).all()
    
    def get_latest_review(self, db: Session, contract_id: int) -> Optional[ContractReview]:
        """获取最新的审查记录"""
        return db.query(ContractReview).filter(
            ContractReview.contract_id == contract_id
        ).order_by(ContractReview.created_at.desc()).first()


class ContractTemplateManager:
    """合同模板管理 Manager"""
    
    def create_template(self, db: Session, template_in: ContractTemplateCreate) -> ContractTemplate:
        """创建新模板"""
        template_data = template_in.model_dump()
        db_template = ContractTemplate(**template_data)
        db.add(db_template)
        try:
            db.commit()
            db.refresh(db_template)
            return db_template
        except Exception as e:
            db.rollback()
            raise Exception(f"创建模板失败: {str(e)}")
    
    def get_template_by_id(self, db: Session, template_id: int) -> Optional[ContractTemplate]:
        """根据ID获取模板"""
        return db.query(ContractTemplate).filter(ContractTemplate.id == template_id).first()
    
    def get_templates(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        template_type: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[ContractTemplate]:
        """获取模板列表"""
        query = db.query(ContractTemplate)
        
        if template_type:
            query = query.filter(ContractTemplate.template_type == template_type)
        if is_active is not None:
            query = query.filter(ContractTemplate.is_active == is_active)
        
        return query.order_by(ContractTemplate.created_at.desc()).offset(skip).limit(limit).all()
    
    def update_template(self, db: Session, template_id: int, template_in: ContractTemplateUpdate) -> Optional[ContractTemplate]:
        """更新模板"""
        db_template = self.get_template_by_id(db, template_id)
        if not db_template:
            return None
        
        update_data = template_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_template, field):
                setattr(db_template, field, value)
        
        db.add(db_template)
        try:
            db.commit()
            db.refresh(db_template)
            return db_template
        except Exception as e:
            db.rollback()
            raise Exception(f"更新模板失败: {str(e)}")
    
    def delete_template(self, db: Session, template_id: int) -> bool:
        """删除模板"""
        db_template = self.get_template_by_id(db, template_id)
        if not db_template:
            return False
        
        try:
            db.delete(db_template)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise Exception(f"删除模板失败: {str(e)}")


# 创建实例
contract_manager = ContractManager()
contract_review_manager = ContractReviewManager()
contract_template_manager = ContractTemplateManager()
