"""
文件上传API接口
"""

from flask import Blueprint, request, jsonify, send_file
from loguru import logger
import traceback
from pathlib import Path

from api.user import require_auth, get_current_user
from services.file_service import file_service

# 创建蓝图
files_bp = Blueprint('files', __name__)


@files_bp.route('/upload', methods=['POST'])
@require_auth
def upload_file():
    """
    上传文件
    
    参数：
    - file: 文件数据
    - category: 文件类别（evidence/contract/avatar，默认evidence）
    - session_id: 会话ID（可选）
    
    返回格式：
    {
        "success": true,
        "data": {
            "file_id": 1,
            "filename": "test.pdf",
            "file_size": 123456,
            "content_type": "application/pdf",
            "category": "evidence",
            "created_at": "2024-01-01T00:00:00"
        }
    }
    """
    try:
        user_id = get_current_user()
        
        # 检查文件
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '未找到文件'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '文件名为空'
            }), 400
        
        # 获取参数
        category = request.form.get('category', 'evidence')
        session_id = request.form.get('session_id')
        
        # 读取文件数据
        file_data = file.read()
        content_type = file.content_type or 'application/octet-stream'
        
        # 验证文件
        is_valid, error_msg = file_service.validate_file(file_data, content_type, category)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        # 保存文件
        file_record = file_service.save_file(
            user_id=user_id,
            session_id=int(session_id) if session_id else None,
            file_data=file_data,
            filename=file.filename,
            content_type=content_type,
            category=category
        )
        
        return jsonify({
            'success': True,
            'data': {
                'file_id': file_record.id,
                'filename': file_record.filename,
                'file_size': file_record.file_size,
                'content_type': file_record.content_type,
                'category': file_record.category,
                'created_at': file_record.created_at.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"上传文件异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'上传文件失败：{str(e)}'
        }), 500


@files_bp.route('/<int:file_id>', methods=['GET'])
@require_auth
def get_file(file_id: int):
    """
    获取文件信息
    """
    try:
        file_record = file_service.get_file(file_id)
        
        if not file_record:
            return jsonify({
                'success': False,
                'error': '文件不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'file_id': file_record.id,
                'filename': file_record.filename,
                'file_size': file_record.file_size,
                'content_type': file_record.content_type,
                'category': file_record.category,
                'created_at': file_record.created_at.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"获取文件信息异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取文件信息失败：{str(e)}'
        }), 500


@files_bp.route('/<int:file_id>/download', methods=['GET'])
@require_auth
def download_file(file_id: int):
    """
    下载文件
    """
    try:
        user_id = get_current_user()
        file_record = file_service.get_file(file_id)
        
        if not file_record:
            return jsonify({
                'success': False,
                'error': '文件不存在'
            }), 404
        
        if file_record.user_id != user_id:
            return jsonify({
                'success': False,
                'error': '无权访问该文件'
            }), 403
        
        file_path = Path(file_record.file_path)
        if not file_path.exists():
            return jsonify({
                'success': False,
                'error': '文件不存在'
            }), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=file_record.filename
        )
        
    except Exception as e:
        logger.error(f"下载文件异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'下载文件失败：{str(e)}'
        }), 500


@files_bp.route('/<int:file_id>', methods=['DELETE'])
@require_auth
def delete_file(file_id: int):
    """
    删除文件
    """
    try:
        user_id = get_current_user()
        success = file_service.delete_file(file_id, user_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': '删除失败，文件不存在或无权限'
            }), 404
        
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
        
    except Exception as e:
        logger.error(f"删除文件异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'删除文件失败：{str(e)}'
        }), 500


@files_bp.route('', methods=['GET'])
@require_auth
def list_files():
    """
    获取用户文件列表
    
    查询参数：
    - skip: 跳过数量（默认0）
    - limit: 限制数量（默认20）
    - category: 文件类别（可选）
    - session_id: 会话ID（可选）
    """
    try:
        user_id = get_current_user()
        
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 20))
        category = request.args.get('category')
        session_id = request.args.get('session_id')
        
        if session_id:
            files = file_service.get_session_files(int(session_id), skip, limit)
        else:
            files = file_service.get_user_files(user_id, skip, limit, category)
        
        result = [
            {
                'file_id': f.id,
                'filename': f.filename,
                'file_size': f.file_size,
                'content_type': f.content_type,
                'category': f.category,
                'session_id': f.session_id,
                'created_at': f.created_at.isoformat()
            }
            for f in files
        ]
        
        return jsonify({
            'success': True,
            'data': {
                'files': result,
                'total': len(result)
            }
        })
        
    except Exception as e:
        logger.error(f"获取文件列表异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'获取文件列表失败：{str(e)}'
        }), 500
