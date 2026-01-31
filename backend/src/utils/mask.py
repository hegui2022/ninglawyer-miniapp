"""
日志脱敏工具
对敏感信息进行脱敏处理
"""

import re
from typing import Any, Dict

# 脱敏规则
MASK_RULES = {
    # 手机号：隐藏中间4位
    'phone': {
        'pattern': r'(\d{3})\d{4}(\d{4})',
        'replacement': r'\1****\2'
    },
    # 身份证：隐藏中间11位
    'id_card': {
        'pattern': r'(\d{6})\d{11}(\d|[xX])',
        'replacement': r'\1***********\2'
    },
    # 邮箱：隐藏部分字符
    'email': {
        'pattern': r'(\w{2})[\w.-]+@([\w.-]+)',
        'replacement': r'\1***@\2'
    },
    # 银行卡：隐藏中间8位
    'bank_card': {
        'pattern': r'(\d{4})\d{8}(\d{4})',
        'replacement': r'\1********\2'
    },
    # 地址：隐藏详细地址
    'address': {
        'pattern': r'([^\s]+市[^\s]+区)[^\s]+',
        'replacement': r'\1****'
    }
}


def mask_sensitive_data(text: str, mask_types: list = None) -> str:
    """
    脱敏处理
    
    Args:
        text: 原始文本
        mask_types: 脱敏类型列表，None表示全部脱敏
    
    Returns:
        脱敏后的文本
    """
    if not text:
        return text
    
    if mask_types is None:
        mask_types = list(MASK_RULES.keys())
    
    result = text
    
    for mask_type in mask_types:
        if mask_type in MASK_RULES:
            rule = MASK_RULES[mask_type]
            result = re.sub(rule['pattern'], rule['replacement'], result)
    
    return result


def mask_dict(data: Dict[str, Any], mask_fields: list = None) -> Dict[str, Any]:
    """
    脱敏字典中的敏感字段
    
    Args:
        data: 原始字典
        mask_fields: 需要脱敏的字段列表，None表示自动识别
    
    Returns:
        脱敏后的字典
    """
    if not isinstance(data, dict):
        return data
    
    result = {}
    
    # 自动识别需要脱敏的字段
    if mask_fields is None:
        mask_fields = []
        for key in data.keys():
            key_lower = key.lower()
            if any(keyword in key_lower for keyword in ['phone', 'mobile', 'tel', '电话', '手机']):
                mask_fields.append((key, 'phone'))
            elif any(keyword in key_lower for keyword in ['id_card', 'idcard', '身份证']):
                mask_fields.append((key, 'id_card'))
            elif any(keyword in key_lower for keyword in ['email', '邮箱']):
                mask_fields.append((key, 'email'))
            elif any(keyword in key_lower for keyword in ['bank_card', 'bankcard', '银行卡']):
                mask_fields.append((key, 'bank_card'))
            elif any(keyword in key_lower for keyword in ['address', '地址']):
                mask_fields.append((key, 'address'))
    
    # 脱敏处理
    for key, value in data.items():
        field_type = next((t for (f, t) in mask_fields if f == key), None)
        
        if field_type:
            result[key] = mask_sensitive_data(str(value), [field_type])
        elif isinstance(value, dict):
            result[key] = mask_dict(value)
        elif isinstance(value, list):
            result[key] = [mask_dict(item) if isinstance(item, dict) else item for item in value]
        else:
            result[key] = value
    
    return result


def mask_log(message: str) -> str:
    """
    脱敏日志消息
    
    Args:
        message: 日志消息
    
    Returns:
        脱敏后的日志消息
    """
    return mask_sensitive_data(message)
