"""
共享数据 API
提供小程序间数据交互服务
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
from loguru import logger

from src.utils.response import success_response, error_response
from src.utils.logger import log_api_request

# 创建蓝图
shared_data_bp = Blueprint('shared-data', __name__)

# 模拟数据存储（生产环境应该使用 Redis）
_shared_data_store = {}

def _generate_data_id():
    """生成数据 ID"""
    return f"data_{datetime.now().timestamp()}_{hash(str(datetime.now()))}"


@shared_data_bp.route('', methods=['POST'])
@log_api_request
def save_shared_data():
    """
    保存共享数据
    """
    try:
        data = request.get_json()
        data_type = data.get('type')
        content = data.get('data')
        expire_time = data.get('expireTime', 3600)  # 默认 1 小时
        
        if not data_type or not content:
            return error_response("缺少必要参数", 400)
        
        data_id = _generate_data_id()
        
        # 保存数据
        _shared_data_store[data_id] = {
            'id': data_id,
            'type': data_type,
            'content': content,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=expire_time)
        }
        
        logger.info(f"保存共享数据: {data_id}, 类型: {data_type}")
        
        return success_response({
            'data_id': data_id,
            'type': data_type,
            'expires_at': _shared_data_store[data_id]['expires_at'].isoformat()
        })
        
    except Exception as e:
        logger.error(f"保存共享数据失败：{str(e)}")
        return error_response(f"保存共享数据失败：{str(e)}", 500)


@shared_data_bp.route('/scene', methods=['POST'])
@log_api_request
def set_scene_data():
    """
    设置场景数据（用于小程序跳转）
    """
    try:
        data = request.get_json()
        scene = data.get('scene')
        content = data.get('data')
        expire_time = data.get('expireTime', 3600)
        
        if not scene or not content:
            return error_response("缺少必要参数", 400)
        
        data_id = _generate_data_id()
        
        # 保存场景数据
        _shared_data_store[f"scene:{scene}"] = {
            'id': data_id,
            'scene': scene,
            'content': content,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=expire_time)
        }
        
        logger.info(f"设置场景数据: {scene}")
        
        return success_response({
            'scene': scene,
            'data_id': data_id,
            'expires_at': _shared_data_store[f"scene:{scene}"]['expires_at'].isoformat()
        })
        
    except Exception as e:
        logger.error(f"设置场景数据失败：{str(e)}")
        return error_response(f"设置场景数据失败：{str(e)}", 500)


@shared_data_bp.route('/scene', methods=['GET'])
@log_api_request
def get_scene_data():
    """
    获取场景数据
    """
    try:
        scene = request.args.get('scene')
        
        if not scene:
            return error_response("缺少场景参数", 400)
        
        scene_key = f"scene:{scene}"
        
        if scene_key not in _shared_data_store:
            return error_response("场景数据不存在", 404)
        
        scene_data = _shared_data_store[scene_key]
        
        # 检查是否过期
        if datetime.now() > scene_data['expires_at']:
            del _shared_data_store[scene_key]
            return error_response("场景数据已过期", 404)
        
        logger.info(f"获取场景数据: {scene}")
        
        return success_response(scene_data['content'])
        
    except Exception as e:
        logger.error(f"获取场景数据失败：{str(e)}")
        return error_response(f"获取场景数据失败：{str(e)}", 500)


@shared_data_bp.route('/<data_type>/<data_id>', methods=['GET'])
@log_api_request
def get_shared_data(data_type, data_id):
    """
    获取共享数据
    """
    try:
        if data_id not in _shared_data_store:
            return error_response("数据不存在", 404)
        
        data = _shared_data_store[data_id]
        
        # 检查类型
        if data['type'] != data_type:
            return error_response("数据类型不匹配", 400)
        
        # 检查是否过期
        if datetime.now() > data['expires_at']:
            del _shared_data_store[data_id]
            return error_response("数据已过期", 404)
        
        logger.info(f"获取共享数据: {data_id}")
        
        return success_response(data['content'])
        
    except Exception as e:
        logger.error(f"获取共享数据失败：{str(e)}")
        return error_response(f"获取共享数据失败：{str(e)}", 500)


@shared_data_bp.route('/<data_type>/<data_id>', methods=['DELETE'])
@log_api_request
def delete_shared_data(data_type, data_id):
    """
    删除共享数据
    """
    try:
        if data_id not in _shared_data_store:
            return error_response("数据不存在", 404)
        
        data = _shared_data_store[data_id]
        
        # 检查类型
        if data['type'] != data_type:
            return error_response("数据类型不匹配", 400)
        
        del _shared_data_store[data_id]
        
        logger.info(f"删除共享数据: {data_id}")
        
        return success_response({'message': '删除成功'})
        
    except Exception as e:
        logger.error(f"删除共享数据失败：{str(e)}")
        return error_response(f"删除共享数据失败：{str(e)}", 500)


@shared_data_bp.route('/cleanup', methods=['POST'])
@log_api_request
def cleanup_expired_data():
    """
    清理过期数据
    """
    try:
        expired_keys = []
        current_time = datetime.now()
        
        for key, data in _shared_data_store.items():
            if current_time > data['expires_at']:
                expired_keys.append(key)
        
        for key in expired_keys:
            del _shared_data_store[key]
        
        logger.info(f"清理过期数据: {len(expired_keys)} 条")
        
        return success_response({
            'cleaned_count': len(expired_keys)
        })
        
    except Exception as e:
        logger.error(f"清理过期数据失败：{str(e)}")
        return error_response(f"清理过期数据失败：{str(e)}", 500)
