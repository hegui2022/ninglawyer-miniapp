"""
Master Agent - 主脑 AGENT
负责任务路由和协调
"""

from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState, END
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

from src.utils.config import get_config
from src.utils.logger import log_function_call, log_business_event

# 获取配置
config = get_config()


class MasterAgent:
    """主脑 AGENT - 负责任务路由"""
    
    def __init__(self):
        """初始化 Master Agent"""
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=0.3,
            streaming=True
        )
        
        # 意图识别提示词
        self.intent_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""你是宁律师法律咨询系统的任务路由器。

你的任务是分析用户的输入，识别其法律咨询意图，并路由到对应的专业律师。

请识别以下信息：
1. domain: 法律领域（civil民事/criminal刑事/contract合同/labor劳动/company公司/ip知识产权/marriage婚姻）
2. intent: 具体意图（consult咨询/draft起草/review审查/signing签署/fulfillment履约/dispute纠纷/litigation诉讼）
3. urgency: 紧急程度（high高/medium中/low低）
4. skill_id: 需要调用的技能ID

返回JSON格式，不要包含其他内容。"""),
            HumanMessage(content="用户输入：{user_input}")
        ])
    
    @log_function_call
    def route(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        路由到对应的宁律师
        
        Args:
            user_input: 用户输入
            context: 上下文信息
        
        Returns:
            路由结果
        """
        if context is None:
            context = {}
        
        logger.info(f"Master Agent 开始路由，用户输入：{user_input}")
        
        # 1. 意图识别
        intent_result = self._identify_intent(user_input)
        
        # 2. 记录业务事件
        log_business_event('user_intent_identified', {
            'user_input': user_input,
            'intent': intent_result
        })
        
        # 3. 返回路由结果
        return {
            'success': True,
            'domain': intent_result.get('domain'),
            'intent': intent_result.get('intent'),
            'skill_id': intent_result.get('skill_id'),
            'urgency': intent_result.get('urgency'),
            'context': context
        }
    
    @log_function_call
    def _identify_intent(self, user_input: str) -> Dict[str, Any]:
        """
        识别用户意图
        
        Args:
            user_input: 用户输入
        
        Returns:
            意识识别结果
        """
        try:
            # 使用 LLM 识别意图
            response = self.llm.invoke(
                self.intent_prompt.format_messages(user_input=user_input)
            )
            
            # 解析响应
            import json
            result = json.loads(response.content)
            
            logger.info(f"意图识别结果：{result}")
            return result
            
        except Exception as e:
            logger.error(f"意图识别失败：{str(e)}")
            # 默认返回民事咨询
            return {
                'domain': 'civil',
                'intent': 'consult',
                'urgency': 'medium',
                'skill_id': 'legal_consult'
            }
    
    @log_function_call
    def get_lawyer_recommendation(self, domain: str) -> Dict[str, Any]:
        """
        获取推荐的宁律师
        
        Args:
            domain: 法律领域
        
        Returns:
            推荐的宁律师信息
        """
        # 律师信息映射
        lawyer_info = {
            'civil': {
                'id': 'ning-lawyer-civil',
                'name': '宁律师·民事',
                'icon': '👨‍⚖️',
                'description': '专注民事法律服务',
                'skills': ['legal_consult', 'contract_dispute', 'tort_responsibility']
            },
            'criminal': {
                'id': 'ning-lawyer-criminal',
                'name': '宁律师·刑事',
                'icon': '⚖️',
                'description': '专注刑事法律服务',
                'skills': ['legal_consult', 'criminal_defense', 'bail_application']
            },
            'contract': {
                'id': 'ning-lawyer-contract',
                'name': '宁律师·合同',
                'icon': '📄',
                'description': '专注合同法律服务',
                'skills': ['legal_consult', 'contract_draft', 'contract_review']
            },
            'labor': {
                'id': 'ning-lawyer-labor',
                'name': '宁律师·劳动',
                'icon': '👷',
                'description': '专注劳动法律服务',
                'skills': ['legal_consult', 'labor_contract', 'wage_dispute']
            },
            'company': {
                'id': 'ning-lawyer-company',
                'name': '宁律师·公司',
                'icon': '🏢',
                'description': '专注公司法律服务',
                'skills': ['legal_consult', 'company_establishment', 'compliance_check']
            },
            'ip': {
                'id': 'ning-lawyer-ip',
                'name': '宁律师·知识产权',
                'icon': '©️',
                'description': '专注知识产权法律服务',
                'skills': ['legal_consult', 'patent_application', 'trademark_registration']
            },
            'marriage': {
                'id': 'ning-lawyer-marriage',
                'name': '宁律师·婚姻',
                'icon': '💑',
                'description': '专注婚姻家庭法律服务',
                'skills': ['legal_consult', 'divorce_mediation', 'property_division']
            }
        }
        
        return lawyer_info.get(domain, lawyer_info['civil'])
