"""
咨询 API
提供法律咨询服务
"""

from flask import Blueprint, request, jsonify
from loguru import logger

from src.agents.master_agent import MasterAgent
from src.agents.lawyer_factory import LawyerAgentFactory
from src.utils.response import success_response, error_response
from src.utils.logger import log_api_request
from src.middleware.permission import check_skill_permission, check_usage_limit

# 创建蓝图
consultation_bp = Blueprint('consultation', __name__)

# 初始化 Agent
master_agent = MasterAgent()
lawyer_factory = LawyerAgentFactory()


@consultation_bp.route('/route', methods=['POST'])
@log_api_request
def route_consultation():
    """
    路由咨询请求
    """
    try:
        data = request.get_json()
        user_input = data.get('input', '')
        user_id = data.get('user_id')  # 添加用户ID
        context = data.get('context', {})
        
        if not user_input:
            return error_response("请输入咨询内容", 400)
        
        # 路由到对应的宁律师
        route_result = master_agent.route(user_input, user_id=user_id, context=context)
        
        return success_response(route_result)
        
    except Exception as e:
        logger.error(f"路由咨询失败：{str(e)}")
        return error_response(f"路由咨询失败：{str(e)}", 500)


@consultation_bp.route('/consult', methods=['POST'])
@log_api_request
@check_skill_permission("civil_consult")
@check_usage_limit("consultations_this_month", 100)
def text_consult():
    """
    文字咨询（带权限检查和使用量限制）
    """
    try:
        data = request.get_json()
        domain = data.get('domain', 'civil')
        question = data.get('question', '')
        chat_history = data.get('chat_history', [])
        
        if not question:
            return error_response("请输入咨询问题", 400)
        
        # 获取对应的宁律师
        lawyer = lawyer_factory.get_lawyer(domain)
        
        # 进行咨询
        result = lawyer.consult(question, chat_history)
        
        return success_response(result)
        
    except Exception as e:
        logger.error(f"文字咨询失败：{str(e)}")
        return error_response(f"文字咨询失败：{str(e)}", 500)


@consultation_bp.route('/voice', methods=['POST'])
@log_api_request
def voice_consult():
    """
    语音咨询（预留接口）
    """
    try:
        data = request.get_json()
        audio_url = data.get('audio_url')
        domain = data.get('domain', 'civil')
        
        if not audio_url:
            return error_response("请提供音频文件", 400)
        
        # TODO: 实现语音识别
        # 1. 语音转文字
        # 2. 文字咨询
        # 3. 文字转语音
        
        # 暂时返回文本咨询结果
        result = {
            'message': '语音咨询功能正在开发中',
            'audio_url': audio_url,
            'domain': domain
        }
        
        return success_response(result)
        
    except Exception as e:
        logger.error(f"语音咨询失败：{str(e)}")
        return error_response(f"语音咨询失败：{str(e)}", 500)


@consultation_bp.route('/lawyers', methods=['GET'])
@log_api_request
def get_lawyers():
    """
    获取所有宁律师列表
    """
    try:
        lawyers = lawyer_factory.list_lawyers()
        return success_response(lawyers)
    except Exception as e:
        logger.error(f"获取宁律师列表失败：{str(e)}")
        return error_response(f"获取宁律师列表失败：{str(e)}", 500)


@consultation_bp.route('/lawyer/<domain>', methods=['GET'])
@log_api_request
def get_lawyer_info(domain):
    """
    获取宁律师详细信息
    """
    try:
        lawyer_info = lawyer_factory.get_lawyer_info(domain)
        
        if not lawyer_info:
            return error_response("宁律师不存在", 404)
        
        return success_response(lawyer_info)
    except Exception as e:
        logger.error(f"获取宁律师信息失败：{str(e)}")
        return error_response(f"获取宁律师信息失败：{str(e)}", 500)


@consultation_bp.route('/domains', methods=['GET'])
@log_api_request
def get_domains():
    """
    获取所有法律领域
    """
    try:
        domains = [
            {
                'id': 'civil',
                'name': '民事',
                'description': '合同纠纷、侵权责任、婚姻家庭'
            },
            {
                'id': 'criminal',
                'name': '刑事',
                'description': '刑事辩护、取保候审、减刑假释'
            },
            {
                'id': 'contract',
                'name': '合同',
                'description': '合同起草、合同审查、纠纷分析'
            },
            {
                'id': 'labor',
                'name': '劳动',
                'description': '劳动合同、工资纠纷、工伤赔偿'
            },
            {
                'id': 'company',
                'name': '公司',
                'description': '公司设立、股权结构、公司治理'
            },
            {
                'id': 'ip',
                'name': '知识产权',
                'description': '专利申请、商标注册、版权保护'
            },
            {
                'id': 'marriage',
                'name': '婚姻',
                'description': '离婚调解、财产分割、抚养权'
            }
        ]
        
        return success_response(domains)
    except Exception as e:
        logger.error(f"获取法律领域失败：{str(e)}")
        return error_response(f"获取法律领域失败：{str(e)}", 500)
