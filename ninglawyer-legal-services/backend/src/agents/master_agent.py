"""
Master Agent - 主脑 AGENT
负责任务路由和协调
支持调用扣子Bot
"""

import os
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class ConfigLoader:
    """配置加载器"""
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """获取配置"""
        # 这里可以添加更多配置加载逻辑
        return {
            'MODEL_NAME': 'doubao-seed-1-6-251015',
            'MODEL_BASE_URL': os.getenv('MODEL_BASE_URL', 'https://ark.cn-beijing.volces.com/api/v3'),
            'MODEL_API_KEY': os.getenv('COZE_WORKLOAD_IDENTITY_API_KEY', '')
        }


def get_config():
    """获取配置（兼容旧代码）"""
    return ConfigLoader.get_config()


class MasterAgent:
    """主脑 AGENT - 负责任务路由和Bot调用"""
    
    def __init__(self, use_coze_bots: bool = True):
        """
        初始化 Master Agent
        
        Args:
            use_coze_bots: 是否使用扣子Bot（默认True）
        """
        config = get_config()
        
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=0.3,
            streaming=True
        )
        
        self.use_coze_bots = use_coze_bots
        
        # 意图识别提示词
        self.intent_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""你是宁律师法律咨询系统的任务路由器。

你的任务是分析用户的输入，识别其法律咨询意图，并路由到对应的专业律师。

请识别以下信息：
1. domain: 法律领域（civil民事/criminal刑事/contract合同/labor劳动/company公司/ip知识产权/marriage婚姻）
2. intent: 具体意图（consult咨询/draft起草/review审查/desensitize脱敏）
3. bot_type: 需要调用的Bot类型（civil_consult/desensitize/contract_draft/contract_review等）
4. urgency: 紧急程度（high高/medium中/low低）

返回JSON格式，不要包含其他内容。"""),
            HumanMessage(content="用户输入：{user_input}")
        ])
        
        # 延迟加载Bot注册表（避免循环导入）
        self._bot_registry = None
    
    @property
    def bot_registry(self):
        """获取Bot注册表"""
        if self._bot_registry is None:
            from src.utils.bot_registry import get_bot_registry
            self._bot_registry = get_bot_registry()
        return self._bot_registry
    
    def route(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        路由到对应的Bot或律师
        
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
        
        logger.info(f"意图识别结果：{intent_result}")
        
        # 2. 根据意图选择处理方式
        if self.use_coze_bots and intent_result.get('bot_type'):
            # 调用扣子Bot
            return self._call_coze_bot(
                bot_type=intent_result.get('bot_type'),
                query=user_input,
                context=context
            )
        else:
            # 调用本地律师Agent
            return self._call_local_agent(
                domain=intent_result.get('domain'),
                intent=intent_result.get('intent'),
                query=user_input,
                context=context
            )
    
    def _identify_intent(self, user_input: str) -> Dict[str, Any]:
        """
        识别用户意图
        
        Args:
            user_input: 用户输入
        
        Returns:
            意图识别结果
        """
        try:
            # 使用简单的规则匹配（比LLM更快）
            user_input_lower = user_input.lower()
            
            # 脱敏意图
            if any(keyword in user_input_lower for keyword in ['脱敏', '隐私', '隐藏信息', '匿名']):
                return {
                    'domain': 'civil',
                    'intent': 'desensitize',
                    'bot_type': 'desensitize',
                    'urgency': 'medium'
                }
            
            # 合同起草意图
            elif any(keyword in user_input_lower for keyword in ['起草合同', '写合同', '生成合同']):
                return {
                    'domain': 'contract',
                    'intent': 'draft',
                    'bot_type': 'contract_draft',
                    'urgency': 'medium'
                }
            
            # 合同审查意图
            elif any(keyword in user_input_lower for keyword in ['审查合同', '检查合同', '审核合同', '合同风险']):
                return {
                    'domain': 'contract',
                    'intent': 'review',
                    'bot_type': 'contract_review',
                    'urgency': 'medium'
                }
            
            # 默认为民事咨询
            else:
                return {
                    'domain': 'civil',
                    'intent': 'consult',
                    'bot_type': 'civil_consult',
                    'urgency': 'medium'
                }
            
        except Exception as e:
            logger.error(f"意图识别失败：{str(e)}")
            # 默认返回民事咨询
            return {
                'domain': 'civil',
                'intent': 'consult',
                'bot_type': 'civil_consult',
                'urgency': 'medium'
            }
    
    def _call_coze_bot(self, bot_type: str, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        调用扣子Bot
        
        Args:
            bot_type: Bot类型
            query: 用户输入
            context: 上下文信息
        
        Returns:
            Bot的回复结果
        """
        if context is None:
            context = {}
        
        logger.info(f"调用扣子Bot：{bot_type}")
        
        # 调用Bot注册表
        result = self.bot_registry.call_bot(
            bot_type=bot_type,
            query=query,
            user_id=context.get('user_id', 'default')
        )
        
        return result
    
    def _call_local_agent(self, domain: str, intent: str, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        调用本地律师Agent
        
        Args:
            domain: 法律领域
            intent: 意图
            query: 用户输入
            context: 上下文信息
        
        Returns:
            律师Agent的回复结果
        """
        if context is None:
            context = {}
        
        logger.info(f"调用本地Agent：{domain} - {intent}")
        
        # 这里可以添加本地Agent的调用逻辑
        # 为了简化，暂时返回一个占位符
        return {
            'success': False,
            'error': '本地Agent暂未实现，请使用扣子Bot'
        }
    
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
