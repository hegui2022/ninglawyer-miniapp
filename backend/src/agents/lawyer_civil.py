"""
宁律师·民事 - 完整版
提供民事法律服务
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from loguru import logger

from utils.config import get_config
from utils.logger import log_function_call, log_business_event
from utils.response import success_response, error_response
from prompts.manager import PromptManager

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
        }
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=0.7,
            streaming=True
        )
        
        # 获取提示词模板（从提示词管理器）
        self.prompt_template = PromptManager.get_lawyer_prompt('civil', simple=False)
        
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
            # 使用提示词模板
            messages = self.prompt_template.format_messages(
                chat_history=[],
                user_input=question
            )
            
            # 调用模型
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
            # 使用提示词模板
            messages = self.prompt_template.format_messages(
                chat_history=[],
                user_input=f"请分析以下民事合同：\n\n{contract_text}\n\n请分析：\n1. 合同性质和类型\n2. 主要权利义务\n3. 潜在风险点\n4. 法律效力评估\n5. 修改建议"
            )
            
            response = self.llm.invoke(messages)
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
            
            夫妻关系：
            - 结婚时间：{case_info.get('marriage_date', '未知')}
            - 分居时间：{case_info.get('separation_date', '未知')}
            
            财产情况：
            {case_info.get('assets', '未知')}
            
            子女情况：
            {case_info.get('children', '未知')}
            
            主要争议：
            {case_info.get('disputes', '未知')}
            
            请从以下方面分析：
            1. 离婚条件是否满足
            2. 财产分割方案建议
            3. 抚养权归属分析
            4. 抚养费计算标准
            5. 法律风险提示
            """
            
            messages = self.prompt_template.format_messages(
                chat_history=[],
                user_input=prompt
            )
            
            response = self.llm.invoke(messages)
            analysis = response.content
            
            return success_response({
                'analysis': analysis,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"离婚案件分析失败：{str(e)}")
            return error_response(f"离婚案件分析失败：{str(e)}")
    
    @log_function_call
    def query_case_law(self, keyword: str) -> Dict[str, Any]:
        """
        查询案例法
        
        Args:
            keyword: 关键词
        
        Returns:
            案例结果
        """
        logger.info(f"查询案例法：{keyword}")
        
        try:
            # 从案例库中查找
            results = []
            keyword_lower = keyword.lower()
            
            for category, cases in self.case_law.items():
                for case in cases:
                    if keyword_lower in case['case'].lower() or \
                       keyword_lower in case['summary'].lower():
                        results.append({
                            'category': category,
                            'case': case['case'],
                            'summary': case['summary'],
                            'result': case['result']
                        })
            
            return success_response({
                'keyword': keyword,
                'results': results,
                'count': len(results)
            })
            
        except Exception as e:
            logger.error(f"案例法查询失败：{str(e)}")
            return error_response(f"案例法查询失败：{str(e)}")


# 创建全局实例
ning_lawyer_civil = NingLawyerCivil()
