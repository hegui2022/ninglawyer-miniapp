"""
合同起草 API
提供合同起草、审查、管理服务
"""

from flask import Blueprint, request, jsonify
from loguru import logger

from src.agents.lawyer_factory import LawyerAgentFactory
from src.utils.response import success_response, error_response
from src.utils.logger import log_api_request

# 创建蓝图
contract_bp = Blueprint('contract', __name__)

# 初始化 Lawyer Factory
lawyer_factory = LawyerAgentFactory()


@contract_bp.route('/draft', methods=['POST'])
@log_api_request
def draft_contract():
    """
    起草合同
    """
    try:
        data = request.get_json()
        contract_type = data.get('contract_type', '通用合同')
        partyA = data.get('partyA', '')
        partyB = data.get('partyB', '')
        terms = data.get('terms', '')
        domain = data.get('domain', 'contract')
        
        if not partyA or not partyB:
            return error_response("请提供甲方和乙方信息", 400)
        
        contract_info = {
            'type': contract_type,
            'partyA': partyA,
            'partyB': partyB,
            'terms': terms
        }
        
        # 获取宁律师
        lawyer = lawyer_factory.get_lawyer(domain)
        
        # 起草合同
        result = lawyer.draft_contract(contract_info)
        
        return success_response(result)
        
    except Exception as e:
        logger.error(f"合同起草失败：{str(e)}")
        return error_response(f"合同起草失败：{str(e)}", 500)


@contract_bp.route('/review', methods=['POST'])
@log_api_request
def review_contract():
    """
    审查合同
    """
    try:
        data = request.get_json()
        contract_text = data.get('contract_text', '')
        domain = data.get('domain', 'contract')
        
        if not contract_text:
            return error_response("请提供合同文本", 400)
        
        # 获取宁律师
        lawyer = lawyer_factory.get_lawyer(domain)
        
        # 审查合同
        result = lawyer.review_contract(contract_text)
        
        return success_response(result)
        
    except Exception as e:
        logger.error(f"合同审查失败：{str(e)}")
        return error_response(f"合同审查失败：{str(e)}", 500)


@contract_bp.route('/templates', methods=['GET'])
@log_api_request
def get_contract_templates():
    """
    获取合同模板列表
    """
    try:
        templates = [
            {
                'id': 'purchase',
                'name': '采购合同',
                'category': '商业',
                'description': '适用于商品采购服务'
            },
            {
                'id': 'service',
                'name': '服务合同',
                'category': '商业',
                'description': '适用于服务提供和接受'
            },
            {
                'id': 'lease',
                'name': '租赁合同',
                'category': '房产',
                'description': '适用于房屋、设备租赁'
            },
            {
                'id': 'employment',
                'name': '劳动合同',
                'category': '劳动',
                'description': '适用于企业员工用工'
            },
            {
                'id': 'partnership',
                'name': '合作协议',
                'category': '商业',
                'description': '适用于商业合作和投资'
            },
            {
                'id': 'nondisclosure',
                'name': '保密协议',
                'category': '知识产权',
                'description': '适用于商业秘密保护'
            },
            {
                'id': 'loan',
                'name': '借款合同',
                'category': '金融',
                'description': '适用于民间借贷'
            }
        ]
        
        return success_response(templates)
    except Exception as e:
        logger.error(f"获取合同模板失败：{str(e)}")
        return error_response(f"获取合同模板失败：{str(e)}", 500)


@contract_bp.route('/template/<template_id>', methods=['GET'])
@log_api_request
def get_template_detail(template_id):
    """
    获取合同模板详情
    """
    try:
        # 模拟模板详情
        templates = {
            'purchase': {
                'id': 'purchase',
                'name': '采购合同',
                'category': '商业',
                'description': '适用于商品采购服务',
                'fields': [
                    {'name': 'partyA', 'label': '甲方', 'type': 'text', 'required': True},
                    {'name': 'partyB', 'label': '乙方', 'type': 'text', 'required': True},
                    {'name': 'product', 'label': '产品名称', 'type': 'text', 'required': True},
                    {'name': 'quantity', 'label': '数量', 'type': 'number', 'required': True},
                    {'name': 'price', 'label': '单价', 'type': 'number', 'required': True},
                    {'name': 'totalAmount', 'label': '总金额', 'type': 'number', 'required': True},
                    {'name': 'deliveryDate', 'label': '交付日期', 'type': 'date', 'required': True},
                    {'name': 'paymentTerms', 'label': '付款方式', 'type': 'select', 'options': ['一次性付款', '分期付款']}
                ]
            },
            'service': {
                'id': 'service',
                'name': '服务合同',
                'category': '商业',
                'description': '适用于服务提供和接受',
                'fields': [
                    {'name': 'partyA', 'label': '甲方', 'type': 'text', 'required': True},
                    {'name': 'partyB', 'label': '乙方', 'type': 'text', 'required': True},
                    {'name': 'serviceName', 'label': '服务名称', 'type': 'text', 'required': True},
                    {'name': 'serviceContent', 'label': '服务内容', 'type': 'textarea', 'required': True},
                    {'name': 'serviceDuration', 'label': '服务期限', 'type': 'text', 'required': True},
                    {'name': 'serviceFee', 'label': '服务费用', 'type': 'number', 'required': True},
                    {'name': 'paymentTerms', 'label': '付款方式', 'type': 'select', 'options': ['一次性付款', '分期付款']}
                ]
            },
            'lease': {
                'id': 'lease',
                'name': '租赁合同',
                'category': '房产',
                'description': '适用于房屋、设备租赁',
                'fields': [
                    {'name': 'partyA', 'label': '出租方', 'type': 'text', 'required': True},
                    {'name': 'partyB', 'label': '承租方', 'type': 'text', 'required': True},
                    {'name': 'propertyAddress', 'label': '房产地址', 'type': 'text', 'required': True},
                    {'name': 'area', 'label': '面积', 'type': 'number', 'required': True},
                    {'name': 'leaseTerm', 'label': '租赁期限', 'type': 'text', 'required': True},
                    {'name': 'monthlyRent', 'label': '月租金', 'type': 'number', 'required': True},
                    {'name': 'paymentMethod', 'label': '付款方式', 'type': 'select', 'options': ['现金', '银行转账']}
                ]
            }
        }
        
        template = templates.get(template_id)
        
        if not template:
            return error_response("模板不存在", 404)
        
        return success_response(template)
    except Exception as e:
        logger.error(f"获取模板详情失败：{str(e)}")
        return error_response(f"获取模板详情失败：{str(e)}", 500)


@contract_bp.route('/analyze', methods=['POST'])
@log_api_request
def analyze_dispute():
    """
    分析纠纷
    """
    try:
        data = request.get_json()
        dispute_type = data.get('dispute_type', '')
        description = data.get('description', '')
        amount = data.get('amount', 0)
        evidence = data.get('evidence', '')
        domain = data.get('domain', 'civil')
        
        if not description:
            return error_response("请提供纠纷描述", 400)
        
        dispute_info = {
            'type': dispute_type,
            'description': description,
            'amount': amount,
            'evidence': evidence
        }
        
        # 获取宁律师
        lawyer = lawyer_factory.get_lawyer(domain)
        
        # 分析纠纷
        result = lawyer.analyze_dispute(dispute_info)
        
        return success_response(result)
        
    except Exception as e:
        logger.error(f"纠纷分析失败：{str(e)}")
        return error_response(f"纠纷分析失败：{str(e)}", 500)
