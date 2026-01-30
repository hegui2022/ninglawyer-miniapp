"""
响应工具
"""

from typing import Any, Dict, Optional
from enum import Enum


class ResponseCode(Enum):
    """响应状态码"""
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_ERROR = 500


def success_response(
    data: Any = None,
    message: str = "操作成功",
    code: int = ResponseCode.SUCCESS.value
) -> Dict[str, Any]:
    """
    成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        code: 响应状态码
    
    Returns:
        响应字典
    """
    return {
        'code': code,
        'success': True,
        'message': message,
        'data': data
    }


def error_response(
    message: str = "操作失败",
    code: int = ResponseCode.INTERNAL_ERROR.value,
    errors: Optional[list] = None
) -> Dict[str, Any]:
    """
    错误响应
    
    Args:
        message: 错误消息
        code: 错误状态码
        errors: 错误详情列表
    
    Returns:
        响应字典
    """
    response = {
        'code': code,
        'success': False,
        'message': message
    }
    
    if errors:
        response['errors'] = errors
    
    return response


def paginate_response(
    data: list,
    total: int,
    page: int = 1,
    page_size: int = 20
) -> Dict[str, Any]:
    """
    分页响应
    
    Args:
        data: 数据列表
        total: 总数
        page: 当前页码
        page_size: 每页数量
    
    Returns:
        分页响应字典
    """
    return success_response({
        'list': data,
        'pagination': {
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        }
    })


def validation_error_response(errors: list) -> Dict[str, Any]:
    """
    验证错误响应
    
    Args:
        errors: 错误列表
    
    Returns:
        响应字典
    """
    return error_response(
        message="数据验证失败",
        code=ResponseCode.BAD_REQUEST.value,
        errors=errors
    )
