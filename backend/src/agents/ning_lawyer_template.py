"""
NingLawyer Template - 宁律师模板
可复用的宁律师 AGENT 基类
"""

from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

from utils.config import get_config
from utils.logger import log_function_call, log_business_event
from utils.response import success_response, error_response

# 获取配置
config = get_config()


class NingLawyerTemplate:
    """宁律师模板 - 可复用的 AGENT 基类"""
    
    def __init__(self, lawyer_config: Dict[str, Any]):
        """
        初始化宁律师
        
        Args:
            lawyer_config: 律师配置
        """
        self.config = lawyer_config
        self.domain = lawyer_config['domain']
        self.persona = lawyer_config['persona']
        self.skills = lawyer_config.get('skills', [])
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=self.persona.get('temperature', 0.7),
            streaming=True
        )
        
        # 创建提示词模板
        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.persona['system_prompt']),
            ("placeholder", "{chat_history}"),
            HumanMessage(content="{user_input}")
        ])
        
        logger.info(f"宁律师初始化完成：{self.persona['name']}")
    
    @log_function_call
    def consult(self, question: str, chat_history: List = None) -> Dict[str, Any]:
        """
        法律咨询
        
        Args:
            question: 用户问题
            chat_history: 聊天历史
        
        Returns:
            咨询结果
        """
        if chat_history is None:
            chat_history = []
        
        logger.info(f"{self.persona['name']} 收到咨询：{question}")
        
        try:
            # 生成响应
            messages = self.prompt_template.format_messages(
                user_input=question,
                chat_history=chat_history
            )
            
            response = self.llm.invoke(messages)
            answer = response.content
            
            # 记录业务事件
            log_business_event('legal_consult', {
                'lawyer': self.persona['name'],
                'domain': self.domain,
                'question': question,
                'answer': answer
            })
            
            return success_response({
                'answer': answer,
                'lawyer': self.persona['name'],
                'domain': self.domain
            })
            
        except Exception as e:
            logger.error(f"咨询失败：{str(e)}")
            return error_response(f"咨询失败：{str(e)}")
    
    @log_function_call
    def draft_contract(self, contract_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        起草合同
        
        Args:
            contract_info: 合同信息
        
        Returns:
            合同草稿
        """
        if 'contract_draft' not in self.skills:
            return error_response("该宁律师不具备合同起草技能")
        
        logger.info(f"{self.persona['name']} 开始起草合同")
        
        try:
            prompt = f"""
            请根据以下信息起草一份{contract_info.get('type', '合同')}：
            
            合同类型：{contract_info.get('type')}
            甲方：{contract_info.get('partyA')}
            乙方：{contract_info.get('partyB')}
            主要条款：{contract_info.get('terms')}
            
            要求：
            1. 合同条款完整、规范
            2. 符合相关法律法规
            3. 保护客户合法权益
            4. 条款清晰、无歧义
            5. 格式规范
            
            请直接输出合同文本，不要包含其他内容。
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            contract_text = response.content
            
            # 记录业务事件
            log_business_event('contract_draft', {
                'lawyer': self.persona['name'],
                'contract_type': contract_info.get('type'),
                'partyA': contract_info.get('partyA'),
                'partyB': contract_info.get('partyB')
            })
            
            return success_response({
                'contract': contract_text,
                'contract_type': contract_info.get('type'),
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"合同起草失败：{str(e)}")
            return error_response(f"合同起草失败：{str(e)}")
    
    @log_function_call
    def review_contract(self, contract_text: str) -> Dict[str, Any]:
        """
        审查合同
        
        Args:
            contract_text: 合同文本
        
        Returns:
            审查结果
        """
        if 'contract_review' not in self.skills:
            return error_response("该宁律师不具备合同审查技能")
        
        logger.info(f"{self.persona['name']} 开始审查合同")
        
        try:
            prompt = f"""
            请审查以下合同，识别潜在的法律风险：
            
            合同内容：
            {contract_text}
            
            请从以下方面进行审查：
            1. 条款完整性
            2. 法律合规性
            3. 权利义务平衡
            4. 潜在风险点
            5. 修改建议
            
            返回JSON格式，包含：
            - risks: 风险点列表
            - suggestions: 修改建议
            - overall_rating: 综合评分（1-10）
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            review_result = response.content
            
            # 记录业务事件
            log_business_event('contract_review', {
                'lawyer': self.persona['name'],
                'contract_length': len(contract_text)
            })
            
            return success_response({
                'review': review_result,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"合同审查失败：{str(e)}")
            return error_response(f"合同审查失败：{str(e)}")
    
    @log_function_call
    def analyze_dispute(self, dispute_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析纠纷
        
        Args:
            dispute_info: 纠纷信息
        
        Returns:
            分析结果
        """
        logger.info(f"{self.persona['name']} 开始分析纠纷")
        
        try:
            prompt = f"""
            请分析以下法律纠纷：
            
            纠纷类型：{dispute_info.get('type')}
            纠纷描述：{dispute_info.get('description')}
            涉及金额：{dispute_info.get('amount')}
            相关证据：{dispute_info.get('evidence')}
            
            请分析：
            1. 纠纷性质
            2. 法律依据
            3. 胜诉概率
            4. 维权建议
            5. 需要的证据
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            analysis = response.content
            
            # 记录业务事件
            log_business_event('dispute_analysis', {
                'lawyer': self.persona['name'],
                'dispute_type': dispute_info.get('type')
            })
            
            return success_response({
                'analysis': analysis,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"纠纷分析失败：{str(e)}")
            return error_response(f"纠纷分析失败：{str(e)}")
    
    @log_function_call
    def get_info(self) -> Dict[str, Any]:
        """
        获取宁律师信息
        
        Returns:
            宁律师信息
        """
        return {
            'id': self.persona['name'],
            'name': self.persona['name'],
            'avatar': self.persona['avatar'],
            'domain': self.domain,
            'description': self.config.get('description', ''),
            'skills': self.skills,
            'helpCount': self.config.get('helpCount', 0),
            'rating': self.config.get('rating', 0),
            'consultCount': self.config.get('consultCount', 0),
            'expertise': self.config.get('expertise', []),
            'reviews': self.config.get('reviews', [])
        }
