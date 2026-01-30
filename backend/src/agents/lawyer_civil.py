"""
宁律师·民事 - 完整版
提供民事法律服务
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from loguru import logger

from src.utils.config import get_config
from src.utils.logger import log_function_call, log_business_event
from src.utils.response import success_response, error_response

# 获取配置
config = get_config()


class NingLawyerCivil:
    """宁律师·民事"""
    
    def __init__(self):
        """初始化宁律师·民事"""
        self.persona = {
            'name': '宁律师·民事',
            'avatar': '/assets/images/lawyers/civil.png',
            'temperature': 0.7,
            'system_prompt': """你是宁律师·民事，一位专业的民事法律顾问。

你的专业领域：
- 合同纠纷：买卖合同、借款合同、租赁合同等
- 侵权责任：人身损害、财产损害、产品责任等
- 婚姻家庭：离婚、抚养权、赡养费、继承等
- 物权纠纷：房产纠纷、土地纠纷、相邻关系等

服务理念：
1. 专业严谨：基于法律事实，提供准确的法律意见
2. 客观公正：站在中立角度，维护各方合法权益
3. 通俗易懂：用通俗易懂的语言解释法律问题

回答规范：
1. 首先简要分析案件性质
2. 引用相关法律条文
3. 提供具体的解决方案
4. 提示法律风险和注意事项
5. 建议是否需要进一步法律援助

重要提醒：
- 你是提供法律咨询的 AI 助手，不能代替正式律师
- 对于重大法律问题，建议用户咨询专业律师
- 所有回答仅供参考，不构成正式法律意见"""
        }
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=0.7,
            streaming=True
        )
        
        # 民事案例库（模拟）
        self.case_law = {
            'contract_dispute': [
                {
                    'case': '买卖合同纠纷',
                    'summary': '甲方未按期付款，乙方要求解除合同',
                    'result': '支持解除合同，甲方承担违约责任'
                },
                {
                    'case': '租赁合同纠纷',
                    'summary': '租客提前退租，房东要求赔偿损失',
                    'result': '租客承担违约责任，赔偿一个月租金'
                }
            ],
            'injury': [
                {
                    'case': '人身损害赔偿',
                    'summary': '交通事故导致受伤，要求赔偿',
                    'result': '支持医疗费、误工费、精神损害抚慰金'
                }
            ],
            'divorce': [
                {
                    'case': '离婚财产分割',
                    'summary': '夫妻共同财产分配纠纷',
                    'result': '一般平均分割，照顾无过错方'
                },
                {
                    'case': '抚养权争夺',
                    'summary': '离婚后子女抚养权归属',
                    'result': '以子女利益为重，2岁以下一般判给母亲'
                }
            ]
        }
        
        logger.info("宁律师·民事初始化完成")
    
    @log_function_call
    def consult(self, question: str, context: Dict = None) -> Dict[str, Any]:
        """
        民事法律咨询
        
        Args:
            question: 用户问题
            context: 上下文信息
        
        Returns:
            咨询结果
        """
        logger.info(f"宁律师·民事收到咨询：{question}")
        
        try:
            # 构建提示词
            prompt = f"""
            请回答以下民事法律问题：
            
            问题：{question}
            
            要求：
            1. 分析案件性质
            2. 引用相关法律
            3. 提供解决方案
            4. 提示风险
            5. 语言通俗易懂
            """
            
            # 调用模型
            messages = [
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            answer = response.content
            
            # 记录业务事件
            log_business_event('civil_consult', {
                'question': question,
                'answer': answer
            })
            
            return success_response({
                'answer': answer,
                'lawyer': self.persona['name'],
                'category': '民事法律'
            })
            
        except Exception as e:
            logger.error(f"民事咨询失败：{str(e)}")
            return error_response(f"咨询失败：{str(e)}")
    
    @log_function_call
    def analyze_contract(self, contract_text: str) -> Dict[str, Any]:
        """
        分析合同
        
        Args:
            contract_text: 合同文本
        
        Returns:
            分析结果
        """
        logger.info("开始分析合同")
        
        try:
            prompt = f"""
            请分析以下民事合同：
            
            合同内容：
            {contract_text}
            
            请分析：
            1. 合同性质和类型
            2. 主要权利义务
            3. 潜在风险点
            4. 法律效力评估
            5. 修改建议
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            analysis = response.content
            
            return success_response({
                'analysis': analysis,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"合同分析失败：{str(e)}")
            return error_response(f"合同分析失败：{str(e)}")
    
    @log_function_call
    def analyze_divorce(self, case_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        离婚法律分析
        
        Args:
            case_info: 案件信息
        
        Returns:
            分析结果
        """
        logger.info("开始分析离婚案件")
        
        try:
            prompt = f"""
            请分析以下离婚案件：
            
            婚姻状况：{case_info.get('marriage_status')}
            是否有子女：{case_info.get('has_children')}
            是否有共同财产：{case_info.get('has_common_property')}
            离婚原因：{case_info.get('reason')}
            
            请分析：
            1. 离婚法律依据
            2. 子女抚养权归属可能性
            3. 财产分割原则
            4. 抚养费计算方式
            5. 离婚程序和流程
            6. 注意事项
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            analysis = response.content
            
            return success_response({
                'analysis': analysis,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"离婚分析失败：{str(e)}")
            return error_response(f"离婚分析失败：{str(e)}")
    
    @log_function_call
    def calculate_compensation(self, case_type: str, details: Dict) -> Dict[str, Any]:
        """
        计算赔偿金额
        
        Args:
            case_type: 案件类型
            details: 案件详情
        
        Returns:
            赔偿计算结果
        """
        logger.info(f"计算赔偿金额：{case_type}")
        
        try:
            if case_type == 'injury':
                # 人身损害赔偿
                prompt = f"""
                请计算人身损害赔偿金额：
                
                医疗费：{details.get('medical_cost')}元
                误工费：{details.get('lost_wages')}元
                护理费：{details.get('nursing_fee')}元
                住院伙食补助费：{details.get('hospital_subsidy')}元
                残疾等级：{details.get('disability_level')}
                
                请根据《民法典》及相关司法解释计算赔偿总额。
                """
            elif case_type == 'contract_breach':
                # 合同违约
                prompt = f"""
                请计算合同违约赔偿：
                
                合同金额：{details.get('contract_amount')}元
                违约金比例：{details.get('penalty_rate')}%
                实际损失：{details.get('actual_loss')}元
                合同履行进度：{details.get('fulfillment_progress')}%
                
                请根据《民法典》计算违约金和赔偿总额。
                """
            else:
                return error_response("不支持的赔偿类型")
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            calculation = response.content
            
            return success_response({
                'calculation': calculation,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"赔偿计算失败：{str(e)}")
            return error_response(f"赔偿计算失败：{str(e)}")
    
    @log_function_call
    def get_case_reference(self, category: str) -> Dict[str, Any]:
        """
        获取相关案例参考
        
        Args:
            category: 案例分类
        
        Returns:
            案例参考
        """
        logger.info(f"查询案例参考：{category}")
        
        try:
            cases = self.case_law.get(category, [])
            
            return success_response({
                'cases': cases,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"查询案例失败：{str(e)}")
            return error_response(f"查询案例失败：{str(e)}")
    
    @log_function_call
    def get_info(self) -> Dict[str, Any]:
        """
        获取宁律师信息
        
        Returns:
            宁律师信息
        """
        return {
            'id': 'civil',
            'name': '宁律师·民事',
            'avatar': self.persona['avatar'],
            'domain': '民事',
            'description': '专业处理合同纠纷、侵权责任、婚姻家庭、物权纠纷等民事法律问题',
            'skills': [
                '合同纠纷处理',
                '侵权责任分析',
                '婚姻家庭咨询',
                '财产分割',
                '抚养权争夺',
                '遗产继承',
                '人身损害赔偿',
                '劳动争议'
            ],
            'helpCount': 12580,
            'rating': 4.9,
            'consultCount': 8900,
            'expertise': [
                '民法典实务',
                '合同法',
                '婚姻法',
                '侵权责任法',
                '继承法'
            ],
            'reviews': [
                {
                    'user': '张先生',
                    'rating': 5,
                    'content': '非常专业，帮我解决了合同纠纷问题',
                    'date': '2024-01-15'
                },
                {
                    'user': '李女士',
                    'rating': 5,
                    'content': '离婚咨询很详细，给了我很中肯的建议',
                    'date': '2024-01-10'
                }
            ]
        }
