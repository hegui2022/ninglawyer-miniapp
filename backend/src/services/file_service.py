"""
文件服务
"""

from loguru import logger
from datetime import datetime
from pathlib import Path

from database import get_db_context
from crud.crud import file_crud
from models.models import FileRecord
from models.schemas import FileCreate, FileUpdate


class FileService:
    """文件服务"""
    
    def __init__(self):
        self.upload_dir = Path('uploads')
        self.upload_dir.mkdir(exist_ok=True)
    
    def save_file(self, user_id: int, session_id: int, file_data: bytes, 
                  filename: str, content_type: str, category: str = 'evidence') -> FileRecord:
        """
        保存文件
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            file_data: 文件数据
            filename: 文件名
            content_type: 内容类型
            category: 文件类别（evidence/contract/avatar等）
        
        Returns:
            FileRecord: 文件记录
        """
        try:
            # 生成唯一文件名
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            ext = Path(filename).suffix
            unique_filename = f"{user_id}_{timestamp}_{filename}"
            file_path = self.upload_dir / unique_filename
            
            # 保存文件
            with open(file_path, 'wb') as f:
                f.write(file_data)
            
            # 计算文件大小
            file_size = len(file_data)
            
            # 创建文件记录
            file_record = FileCreate(
                user_id=user_id,
                session_id=session_id,
                filename=filename,
                file_path=str(file_path),
                file_size=file_size,
                content_type=content_type,
                category=category
            )
            
            with get_db_context() as db:
                db_file = file_crud.create(db, obj_in=file_record)
                db.refresh(db_file)
                return db_file
                
        except Exception as e:
            logger.error(f"保存文件异常：{str(e)}")
            raise
    
    def get_user_files(self, user_id: int, skip: int = 0, limit: int = 20, category: str = None):
        """
        获取用户文件列表
        """
        try:
            with get_db_context() as db:
                if category:
                    return file_crud.get_user_files_by_category(db, user_id, category, skip, limit)
                else:
                    return file_crud.get_user_files(db, user_id, skip, limit)
        except Exception as e:
            logger.error(f"获取用户文件列表异常：{str(e)}")
            raise
    
    def get_session_files(self, session_id: int, skip: int = 0, limit: int = 20):
        """
        获取会话文件列表
        """
        try:
            with get_db_context() as db:
                return file_crud.get_session_files(db, session_id, skip, limit)
        except Exception as e:
            logger.error(f"获取会话文件列表异常：{str(e)}")
            raise
    
    def get_file(self, file_id: int) -> FileRecord:
        """
        获取文件记录
        """
        try:
            with get_db_context() as db:
                return file_crud.get_by_id(db, file_id)
        except Exception as e:
            logger.error(f"获取文件记录异常：{str(e)}")
            raise
    
    def delete_file(self, file_id: int, user_id: int) -> bool:
        """
        删除文件
        """
        try:
            with get_db_context() as db:
                file_record = file_crud.get_by_id(db, file_id)
                
                if not file_record or file_record.user_id != user_id:
                    return False
                
                # 删除物理文件
                file_path = Path(file_record.file_path)
                if file_path.exists():
                    file_path.unlink()
                
                # 删除数据库记录
                file_crud.remove(db, id=file_id)
                return True
                
        except Exception as e:
            logger.error(f"删除文件异常：{str(e)}")
            raise
    
    def validate_file(self, file_data: bytes, content_type: str, category: str) -> tuple[bool, str]:
        """
        验证文件
        
        Returns:
            (是否有效, 错误信息)
        """
        try:
            # 文件大小限制（10MB）
            MAX_SIZE = 10 * 1024 * 1024
            if len(file_data) > MAX_SIZE:
                return False, f"文件大小超过限制（最大 {MAX_SIZE // 1024 // 1024}MB）"
            
            # 根据类别验证文件类型
            allowed_types = {
                'evidence': ['application/pdf', 'image/jpeg', 'image/png', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
                'contract': ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
                'avatar': ['image/jpeg', 'image/png']
            }
            
            if category in allowed_types and content_type not in allowed_types[category]:
                return False, f"不支持的文件类型：{content_type}"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"验证文件异常：{str(e)}")
            return False, f"文件验证失败：{str(e)}"


# 创建文件服务实例
file_service = FileService()
