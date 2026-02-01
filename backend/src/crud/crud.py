"""
数据库操作层（CRUD）
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from loguru import logger

from models.models import (
    User, Session, Message, ConsultationRecord, 
    ContractRecord, DesensitizeRecord, FileRecord, 
    UserProfile, Statistics, SystemConfig
)
from models.schemas import (
    UserCreate, UserUpdate, SessionCreate,
    ConsultationRecordBase, ContractRecordBase, 
    DesensitizeRecordBase, UserProfileBase
)


class CRUDUser:
    """用户CRUD操作"""
    
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """通过ID获取用户"""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_by_openid(self, db: Session, openid: str) -> Optional[User]:
        """通过openid获取用户"""
        return db.query(User).filter(User.openid == openid).first()
    
    def get_by_phone(self, db: Session, phone: str) -> Optional[User]:
        """通过手机号获取用户"""
        return db.query(User).filter(User.phone == phone).first()
    
    def create(self, db: Session, obj_in: UserCreate) -> User:
        """创建用户"""
        db_obj = User(**obj_in.model_dump(exclude_unset=True))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"创建用户：{db_obj.id}")
        return db_obj
    
    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        """更新用户"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_obj)
        logger.info(f"更新用户：{db_obj.id}")
        return db_obj
    
    def delete(self, db: Session, user_id: int) -> bool:
        """删除用户"""
        db_obj = self.get_by_id(db, user_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            logger.info(f"删除用户：{user_id}")
            return True
        return False
    
    def list_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """列出用户"""
        return db.query(User).offset(skip).limit(limit).all()
    
    def count_users(self, db: Session) -> int:
        """统计用户数量"""
        return db.query(func.count(User.id)).scalar()


class CRUDSession:
    """会话CRUD操作"""
    
    def get_by_id(self, db: Session, session_id: int) -> Optional[Session]:
        """通过ID获取会话"""
        return db.query(Session).filter(Session.id == session_id).first()
    
    def create(self, db: Session, obj_in: SessionCreate, user_id: int) -> Session:
        """创建会话"""
        db_obj = Session(**obj_in.model_dump(exclude_unset=True), user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"创建会话：{db_obj.id}")
        return db_obj
    
    def update(self, db: Session, db_obj: Session, **kwargs) -> Session:
        """更新会话"""
        for field, value in kwargs.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_user_sessions(self, db: Session, user_id: int, skill_type: str = None) -> List[Session]:
        """获取用户的会话列表"""
        query = db.query(Session).filter(Session.user_id == user_id)
        if skill_type:
            query = query.filter(Session.skill_type == skill_type)
        return query.order_by(desc(Session.updated_at)).all()
    
    def get_session_messages(self, db: Session, session_id: int) -> List[Message]:
        """获取会话消息"""
        return db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
    
    def add_message(self, db: Session, session_id: int, role: str, content: str) -> Message:
        """添加消息"""
        message = Message(session_id=session_id, role=role, content=content)
        db.add(message)
        
        # 更新会话时间
        session = self.get_by_id(db, session_id)
        if session:
            session.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(message)
        return message


class CRUDConsultation:
    """咨询记录CRUD操作"""
    
    def create(self, db: Session, obj_in: ConsultationRecordBase, user_id: int, session_id: int) -> ConsultationRecord:
        """创建咨询记录"""
        db_obj = ConsultationRecord(
            **obj_in.model_dump(exclude_unset=True),
            user_id=user_id,
            session_id=session_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"创建咨询记录：{db_obj.id}")
        return db_obj
    
    def get_by_id(self, db: Session, record_id: int) -> Optional[ConsultationRecord]:
        """通过ID获取咨询记录"""
        return db.query(ConsultationRecord).filter(ConsultationRecord.id == record_id).first()
    
    def get_user_records(self, db: Session, user_id: int, skip: int = 0, limit: int = 20) -> List[ConsultationRecord]:
        """获取用户的咨询记录"""
        return db.query(ConsultationRecord).filter(
            ConsultationRecord.user_id == user_id
        ).order_by(desc(ConsultationRecord.created_at)).offset(skip).limit(limit).all()
    
    def get_user_records_by_domain(self, db: Session, user_id: int, domain: str) -> List[ConsultationRecord]:
        """根据领域获取用户的咨询记录"""
        return db.query(ConsultationRecord).filter(
            ConsultationRecord.user_id == user_id,
            ConsultationRecord.domain == domain
        ).order_by(desc(ConsultationRecord.created_at)).all()


class CRUDContract:
    """合同记录CRUD操作"""
    
    def create(self, db: Session, obj_in: ContractRecordBase, user_id: int, session_id: int) -> ContractRecord:
        """创建合同记录"""
        db_obj = ContractRecord(
            **obj_in.model_dump(exclude_unset=True),
            user_id=user_id,
            session_id=session_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"创建合同记录：{db_obj.id}")
        return db_obj
    
    def get_by_id(self, db: Session, record_id: int) -> Optional[ContractRecord]:
        """通过ID获取合同记录"""
        return db.query(ContractRecord).filter(ContractRecord.id == record_id).first()
    
    def get_user_records(self, db: Session, user_id: int, skip: int = 0, limit: int = 20) -> List[ContractRecord]:
        """获取用户的合同记录"""
        return db.query(ContractRecord).filter(
            ContractRecord.user_id == user_id
        ).order_by(desc(ContractRecord.created_at)).offset(skip).limit(limit).all()


class CRUDDesensitize:
    """脱敏记录CRUD操作"""
    
    def create(self, db: Session, obj_in: DesensitizeRecordBase, user_id: int, session_id: int) -> DesensitizeRecord:
        """创建脱敏记录"""
        db_obj = DesensitizeRecord(
            **obj_in.model_dump(exclude_unset=True),
            user_id=user_id,
            session_id=session_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"创建脱敏记录：{db_obj.id}")
        return db_obj
    
    def get_by_id(self, db: Session, record_id: int) -> Optional[DesensitizeRecord]:
        """通过ID获取脱敏记录"""
        return db.query(DesensitizeRecord).filter(DesensitizeRecord.id == record_id).first()
    
    def get_user_records(self, db: Session, user_id: int, skip: int = 0, limit: int = 20) -> List[DesensitizeRecord]:
        """获取用户的脱敏记录"""
        return db.query(DesensitizeRecord).filter(
            DesensitizeRecord.user_id == user_id
        ).order_by(desc(DesensitizeRecord.created_at)).offset(skip).limit(limit).all()


class CRUDFile:
    """文件记录CRUD操作"""
    
    def create(self, db: Session, user_id: int, filename: str, file_path: str, 
                file_size: int, file_type: str, mime_type: str = None,
                related_type: str = None, related_id: int = None) -> FileRecord:
        """创建文件记录"""
        db_obj = FileRecord(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
            mime_type=mime_type,
            related_type=related_type,
            related_id=related_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"创建文件记录：{db_obj.id}")
        return db_obj
    
    def get_by_id(self, db: Session, file_id: int) -> Optional[FileRecord]:
        """通过ID获取文件记录"""
        return db.query(FileRecord).filter(FileRecord.id == file_id).first()
    
    def get_user_files(self, db: Session, user_id: int, skip: int = 0, limit: int = 20) -> List[FileRecord]:
        """获取用户的文件列表"""
        return db.query(FileRecord).filter(
            FileRecord.user_id == user_id
        ).order_by(desc(FileRecord.created_at)).offset(skip).limit(limit).all()
    
    def delete(self, db: Session, file_id: int) -> bool:
        """删除文件记录"""
        db_obj = self.get_by_id(db, file_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            logger.info(f"删除文件记录：{file_id}")
            return True
        return False


class CRUDUserProfile:
    """用户档案CRUD操作"""
    
    def get_by_user_id(self, db: Session, user_id: int) -> Optional[UserProfile]:
        """通过用户ID获取档案"""
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    def create_or_update(self, db: Session, obj_in: UserProfileBase, user_id: int) -> UserProfile:
        """创建或更新用户档案"""
        db_obj = self.get_by_user_id(db, user_id)
        if db_obj:
            # 更新
            update_data = obj_in.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            db_obj.updated_at = datetime.utcnow()
        else:
            # 创建
            db_obj = UserProfile(**obj_in.model_dump(exclude_unset=True), user_id=user_id)
            db.add(db_obj)
        
        db.commit()
        db.refresh(db_obj)
        logger.info(f"保存用户档案：{user_id}")
        return db_obj


class CRUDStatistics:
    """统计CRUD操作"""
    
    def record_metric(self, db: Session, metric_type: str, metric_value: int = 1, extra_data: dict = None):
        """记录指标"""
        today = datetime.utcnow().date()
        db_obj = Statistics(
            date=today,
            metric_type=metric_type,
            metric_value=metric_value,
            extra_data=extra_data or {}
        )
        db.add(db_obj)
        db.commit()
        logger.info(f"记录指标：{metric_type}={metric_value}")
    
    def get_daily_stats(self, db: Session, date: datetime = None) -> List[Statistics]:
        """获取每日统计"""
        if date is None:
            date = datetime.utcnow().date()
        return db.query(Statistics).filter(Statistics.date == date).all()
    
    def get_range_stats(self, db: Session, start_date: datetime, end_date: datetime) -> List[Statistics]:
        """获取时间段统计"""
        return db.query(Statistics).filter(
            Statistics.date >= start_date.date(),
            Statistics.date <= end_date.date()
        ).all()


class CRUDSystemConfig:
    """系统配置CRUD操作"""
    
    def get_by_key(self, db: Session, key: str) -> Optional[SystemConfig]:
        """通过键获取配置"""
        return db.query(SystemConfig).filter(SystemConfig.key == key).first()
    
    def set(self, db: Session, key: str, value: str, description: str = None) -> SystemConfig:
        """设置配置"""
        db_obj = self.get_by_key(db, key)
        if db_obj:
            db_obj.value = value
            db_obj.updated_at = datetime.utcnow()
            if description:
                db_obj.description = description
        else:
            db_obj = SystemConfig(key=key, value=value, description=description)
            db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"设置配置：{key}")
        return db_obj
    
    def get_all(self, db: Session) -> List[SystemConfig]:
        """获取所有配置"""
        return db.query(SystemConfig).all()


# 全局CRUD实例
user_crud = CRUDUser()
session_crud = CRUDSession()
consultation_crud = CRUDConsultation()
contract_crud = CRUDContract()
desensitize_crud = CRUDDesensitize()
file_crud = CRUDFile()
user_profile_crud = CRUDUserProfile()
statistics_crud = CRUDStatistics()
system_config_crud = CRUDSystemConfig()
