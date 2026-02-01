"""
宁律师·婚姻 - 完整版
提供婚姻家庭法律服务
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from loguru import logger

from utils.config import get_config
from utils.logger import log_function_call, log_business_event
from utils.response import success_response, error_response

# 获取配置
config = get_config()


class NingLawyerMarriage:
    """宁律师·婚姻"""
    
    def __init__(self):
        """初始化宁律师·婚姻"""
        self.persona = {
            'name': '宁律师·婚姻',
            'avatar': '/assets/images/lawyers/marriage.png',
            'temperature': 0.7,
            'system_prompt': """你是宁律师·婚姻，一位专业的婚姻家庭法律顾问。

你的专业领域：
- 离婚诉讼：协议离婚、诉讼离婚、涉外离婚
- 抚养权争夺：子女抚养权归属、抚养费计算
- 财产分割：共同财产、个人财产分割
- 婚内协议：婚前协议、婚内财产协议
- 继承纠纷：遗嘱继承、法定继承
- 家庭暴力：人身保护令、维权

服务理念：
1. 保护权益：保护妇女儿童合法权益
2. 化解矛盾：尽量通过调解解决纠纷
3. 专业严谨：依法维护当事人利益
4. 温情服务：理解当事人情感需求

回答规范：
1. 引用《民法典》婚姻家庭编条文
2. 分析法律关系和权利义务
3. 提供具体的解决方案
4. 提醒证据收集
5. 关注子女最佳利益

重要提醒：
- 婚姻案件涉及情感，建议保持冷静
- 重要证据要及时收集和保全
- 你是提供法律咨询的 AI 助手，重大案件建议咨询专业律师"""
        }
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=0.7,
            streaming=True
        )
        
        logger.info("宁律师·婚姻初始化完成")
    
    @log_function_call
    def consult(self, question: str, context: Dict = None) -> Dict[str, Any]:
        """
        婚姻家庭咨询
        
        Args:
            question: 用户问题
            context: 上下文信息
        
        Returns:
            咨询结果
        """
        logger.info(f"宁律师·婚姻收到咨询：{question}")
        
        try:
            prompt = f"""
            请回答以下婚姻家庭法律问题：
            
            问题：{question}
            
            要求：
            1. 引用《民法典》婚姻家庭编条文
            2. 分析权利义务
            3. 提供解决方案
            4. 提醒注意事项
            5. 关注子女利益
            """
            
            # 使用提示词模板
            messages = self.prompt_template.format_messages(
                chat_history=[],
                user_input=prompt
            )
            
            response = self.llm.invoke(messages)
            answer = response.content
            
            log_business_event('marriage_consult', {
                'question': question,
                'answer': answer
            })
            
            return success_response({
                'answer': answer,
                'lawyer': self.persona['name'],
                'category': '婚姻家庭'
            })
            
        except Exception as e:
            logger.error(f"婚姻咨询失败：{str(e)}")
            return error_response(f"咨询失败：{str(e)}")
    
    @log_function_call
    def analyze_divorce(self, case_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析离婚案件
        
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
            子女年龄：{case_info.get('children_ages', [])}
            是否有共同财产：{case_info.get('has_common_property')}
            共同财产清单：{case_info.get('common_property')}
            是否有共同债务：{case_info.get('has_common_debt')}
            离婚原因：{case_info.get('reason')}
            
            请分析：
            1. 离婚法律依据
            2. 子女抚养权归属可能性
            3. 抚养费计算方式
            4. 共同财产分割原则和方案
            5. 共同债务承担
            6. 离婚程序和流程
            7. 证据收集建议
            8. 注意事项
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
    def calculate_child_support(self, support_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算抚养费
        
        Args:
            support_info: 抚养费信息
        
        Returns:
            计算结果
        """
        logger.info("开始计算抚养费")
        
        try:
            prompt = f"""
            请计算子女抚养费：
            
            子女数量：{support_info.get('child_count')}个
            子女年龄：{support_info.get('children_ages', [])}
            非直接抚养方月收入：{support_info.get('parent_income')}元
            当地生活水平：{support_info.get('living_standard')}
            子女实际需要：{support_info.get('actual_needs')}
            
            请根据《民法典》第一千零八十五条规定计算抚养费金额。
            """
            
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
            logger.error(f"抚养费计算失败：{str(e)}")
            return error_response(f"抚养费计算失败：{str(e)}")
    
    @log_function_call
    def draft_prenuptial_agreement(self, agreement_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        起草婚前协议
        
        Args:
            agreement_info: 协议信息
        
        Returns:
            婚前协议
        """
        logger.info("开始起草婚前协议")
        
        try:
            prompt = f"""
            请起草婚前协议：
            
            甲方（男方）：{agreement_info.get('partyA')}
            乙方（女方）：{agreement_info.get('partyB')}
            主要财产：{agreement_info.get('assets')}
            协议内容：{agreement_info.get('content')}
            
            请起草规范的婚前协议，包含：
            1. 基本信息
            2. 财产归属约定
            3. 债务承担约定
            4. 财产增值处理
            5. 协议生效条件
            6. 争议解决方式
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            agreement = response.content
            
            return success_response({
                'agreement': agreement,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"婚前协议起草失败：{str(e)}")
            return error_response(f"婚前协议起草失败：{str(e)}")
    
    @log_function_call
    def get_info(self) -> Dict[str, Any]:
        """
        获取宁律师信息
        
        Returns:
            宁律师信息
        """
        return {
            'id': 'marriage',
            'name': '宁律师·婚姻',
            'avatar': self.persona['avatar'],
            'domain': '婚姻',
            'description': '专业处理离婚、抚养权、财产分割、继承等婚姻家庭法律问题',
            'skills': [
                '离婚诉讼',
                '抚养权争夺',
                '抚养费计算',
                '财产分割',
                '婚前协议',
                '继承纠纷'
            ],
            'helpCount': 13500,
            'rating': 4.9,
            'consultCount': 9800,
            'expertise': [
                '民法典婚姻家庭编',
                '离婚法律实务',
                '抚养权法律',
                '继承法',
                '家庭暴力维权'
            ],
            'reviews': [
                {
                    'user': '张女士',
                    'rating': 5,
                    'content': '帮我争取到孩子的抚养权，非常感谢',
                    'date': '2024-01-28'
                },
                {
                    'user': '李先生',
                    'rating': 5,
                    'content': '财产分割很公平，双方都满意',
                    'date': '2024-01-22'
                }
            ]
        }
