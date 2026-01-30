"""
宁律师·合同 - 合同起草和审查专家
提供合同起草、审查、分析服务
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from loguru import logger

from src.utils.config import get_config
from src.utils.logger import log_function_call, log_business_event
from src.utils.response import success_response, error_response
from src.prompts.manager import PromptManager

# 获取配置
config = get_config()


class NingLawyerContract:
    """宁律师·合同"""
    
    def __init__(self):
        """初始化宁律师·合同"""
        self.persona = {
            'name': '宁律师·合同',
            'avatar': '/assets/images/lawyers/contract.png',
            'temperature': 0.5,
        }
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=0.5,
            streaming=True
        )
        
        # 获取提示词模板（从提示词管理器）
        self.prompt_template = PromptManager.get_lawyer_prompt('contract', simple=False)
        
        # 合同模板库
        self.contract_templates = {
            'purchase': {
                'name': '采购合同',
                'structure': [
                    '合同主体信息',
                    '标的物描述',
                    '数量和质量',
                    '价款和支付方式',
                    '交货时间、地点和方式',
                    '检验验收',
                    '违约责任',
                    '争议解决',
                    '其他条款'
                ]
            },
            'service': {
                'name': '服务合同',
                'structure': [
                    '合同主体信息',
                    '服务内容和标准',
                    '服务期限',
                    '服务费用和支付方式',
                    '双方权利义务',
                    '服务质量保证',
                    '违约责任',
                    '争议解决',
                    '其他条款'
                ]
            },
            'lease': {
                'name': '租赁合同',
                'structure': [
                    '合同主体信息',
                    '租赁物描述',
                    '租赁期限',
                    '租金及支付方式',
                    '房屋使用和维护',
                    '转租约定',
                    '违约责任',
                    '合同解除',
                    '争议解决',
                    '其他条款'
                ]
            }
        }
        
        logger.info("宁律师·合同初始化完成")
    
    @log_function_call
    def draft_contract(self, contract_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        起草合同
        
        Args:
            contract_info: 合同信息
        
        Returns:
            合同草稿
        """
        logger.info(f"开始起草合同：{contract_info.get('contract_type')}")
        
        try:
            contract_type = contract_info.get('contract_type', '通用合同')
            partyA = contract_info.get('partyA', '')
            partyB = contract_info.get('partyB', '')
            terms = contract_info.get('terms', '')
            additional_requirements = contract_info.get('requirements', '')
            
            # 获取模板结构
            template = self.contract_templates.get(contract_type.lower())
            structure = template['structure'] if template else None
            
            prompt = f"""
            请起草一份{contract_type}：
            
            合同信息：
            - 甲方：{partyA}
            - 乙方：{partyB}
            - 主要条款：{terms}
            - 特殊要求：{additional_requirements}
            
            起草要求：
            1. 合同结构完整，包括首部、正文、尾部
            2. 条款清晰明确，无歧义
            3. 权利义务平衡
            4. 符合《民法典》等相关法律法规
            5. 格式规范统一
            6. 包含以下部分：合同主体、标的物/服务内容、价格/费用、履行期限、违约责任、争议解决等
            7. 注重风险防控，保护各方合法权益
            
            请直接输出完整的合同文本，格式规范，不要包含其他说明文字。
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            contract_text = response.content
            
            # 记录业务事件
            log_business_event('contract_draft', {
                'contract_type': contract_type,
                'partyA': partyA,
                'partyB': partyB,
                'contract_length': len(contract_text)
            })
            
            return success_response({
                'contract': contract_text,
                'contract_type': contract_type,
                'lawyer': self.persona['name'],
                'template': template
            })
            
        except Exception as e:
            logger.error(f"合同起草失败：{str(e)}")
            return error_response(f"合同起草失败：{str(e)}")
    
    @log_function_call
    def review_contract(self, contract_text: str, review_focus: List = None) -> Dict[str, Any]:
        """
        审查合同
        
        Args:
            contract_text: 合同文本
            review_focus: 审查重点
        
        Returns:
            审查结果
        """
        logger.info("开始审查合同")
        
        try:
            if review_focus is None:
                review_focus = ['完整性', '合法性', '风险点', '权利义务']
            
            focus_str = '、'.join(review_focus)
            
            prompt = f"""
            请审查以下合同，重点关注：{focus_str}
            
            合同内容：
            {contract_text}
            
            审查要求：
            1. 合同主体资格审查
            2. 条款完整性检查
            3. 权利义务对等性分析
            4. 违约责任明确性评估
            5. 潜在法律风险识别
            6. 法律合规性检查
            7. 具体修改建议
            8. 风险等级评估（低/中/高）
            
            请输出结构化的审查报告，包括：
            - 总体评价
            - 风险点列表（每个风险点说明严重程度）
            - 修改建议（逐条列出）
            - 综合评分（1-10分）
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            review_result = response.content
            
            return success_response({
                'review': review_result,
                'lawyer': self.persona['name'],
                'review_focus': review_focus
            })
            
        except Exception as e:
            logger.error(f"合同审查失败：{str(e)}")
            return error_response(f"合同审查失败：{str(e)}")
    
    @log_function_call
    def analyze_risks(self, contract_text: str) -> Dict[str, Any]:
        """
        分析合同风险
        
        Args:
            contract_text: 合同文本
        
        Returns:
            风险分析结果
        """
        logger.info("开始分析合同风险")
        
        try:
            prompt = f"""
            请分析以下合同的法律风险：
            
            合同内容：
            {contract_text}
            
            分析维度：
            1. 主体风险（主体资格、履约能力）
            2. 条款风险（条款缺失、条款模糊）
            3. 履约风险（履行障碍、履行成本）
            4. 争议风险（争议解决方式、证据保全）
            5. 法律风险（违法条款、法律冲突）
            
            输出格式：
            - 风险等级：低/中/高
            - 主要风险点（逐条列出，说明影响）
            - 风险防范措施
            - 建议修改条款
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            risk_analysis = response.content
            
            return success_response({
                'risk_analysis': risk_analysis,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"风险分析失败：{str(e)}")
            return error_response(f"风险分析失败：{str(e)}")
    
    @log_function_call
    def compare_contracts(self, contract1: str, contract2: str) -> Dict[str, Any]:
        """
        对比两个合同
        
        Args:
            contract1: 合同1文本
            contract2: 合同2文本
        
        Returns:
            对比结果
        """
        logger.info("开始对比合同")
        
        try:
            prompt = f"""
            请对比以下两个合同的差异：
            
            合同一：
            {contract1}
            
            合同二：
            {contract2}
            
            对比维度：
            1. 条款差异（新增、删除、修改）
            2. 权利义务变化
            3. 风险点变化
            4. 法律效力评估
            5. 优劣势分析
            
            请输出详细的对比报告。
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            comparison = response.content
            
            return success_response({
                'comparison': comparison,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"合同对比失败：{str(e)}")
            return error_response(f"合同对比失败：{str(e)}")
    
    @log_function_call
    def get_templates(self) -> Dict[str, Any]:
        """
        获取合同模板列表
        
        Returns:
            模板列表
        """
        templates = []
        for key, value in self.contract_templates.items():
            templates.append({
                'id': key,
                'name': value['name'],
                'structure': value['structure']
            })
        
        return success_response({
            'templates': templates,
            'lawyer': self.persona['name']
        })
    
    @log_function_call
    def consult(self, question: str, context: Dict = None) -> Dict[str, Any]:
        """
        合同咨询
        
        Args:
            question: 用户问题
            context: 上下文信息
        
        Returns:
            咨询结果
        """
        logger.info(f"收到合同咨询：{question}")
        
        try:
            prompt = f"""
            请回答以下合同法律问题：
            
            问题：{question}
            
            要求：
            1. 引用相关法律条文
            2. 分析法律风险
            3. 提供解决方案
            4. 说明注意事项
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            answer = response.content
            
            return success_response({
                'answer': answer,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"咨询失败：{str(e)}")
            return error_response(f"咨询失败：{str(e)}")
    
    @log_function_call
    def get_info(self) -> Dict[str, Any]:
        """
        获取宁律师信息
        
        Returns:
            宁律师信息
        """
        return {
            'id': 'contract',
            'name': '宁律师·合同',
            'avatar': self.persona['avatar'],
            'domain': '合同',
            'description': '专业的合同起草、审查和风险分析专家',
            'skills': [
                '合同起草',
                '合同审查',
                '风险分析',
                '合同对比',
                '条款优化',
                '纠纷预防'
            ],
            'helpCount': 8650,
            'rating': 4.8,
            'consultCount': 6800,
            'expertise': [
                '合同法实务',
                '民法典合同编',
                '商业合同',
                '劳动合同',
                '建设工程合同'
            ],
            'templates': list(self.contract_templates.keys()),
            'reviews': [
                {
                    'user': '王总',
                    'rating': 5,
                    'content': '起草的合同非常专业，风险把控到位',
                    'date': '2024-01-20'
                },
                {
                    'user': '李经理',
                    'rating': 5,
                    'content': '合同审查很仔细，发现了几个关键风险点',
                    'date': '2024-01-18'
                }
            ]
        }
