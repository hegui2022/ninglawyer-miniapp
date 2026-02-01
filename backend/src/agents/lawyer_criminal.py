"""
宁律师·刑事 - 完整版
提供刑事法律辩护服务
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from loguru import logger

from utils.config import get_config
from utils.logger import log_function_call, log_business_event
from utils.response import success_response, error_response
from prompts.manager import PromptManager

# 获取配置
config = get_config()


class NingLawyerCriminal:
    """宁律师·刑事"""
    
    def __init__(self):
        """初始化宁律师·刑事"""
        self.persona = {
            'name': '宁律师·刑事',
            'avatar': '/assets/images/lawyers/criminal.png',
            'temperature': 0.6,
        }
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=0.6,
            streaming=True
        )
        
        # 获取提示词模板（从提示词管理器）
        self.prompt_template = PromptManager.get_lawyer_prompt('criminal', simple=False)
        
        # 刑事案例库（模拟）
        self.case_law = {
            'theft': [
                {
                    'case': '盗窃案',
                    'summary': '盗窃他人财物，价值3万元',
                    'result': '有期徒刑3年，罚金2万元'
                }
            ],
            'fraud': [
                {
                    'case': '诈骗案',
                    'summary': '虚构事实诈骗他人钱财5万元',
                    'result': '有期徒刑5年，罚金5万元'
                }
            ],
            'injury': [
                {
                    'case': '故意伤害案',
                    'summary': '持刀伤人致轻伤',
                    'result': '有期徒刑2年，赔偿经济损失'
                }
            ]
        }
        
        logger.info("宁律师·刑事初始化完成")
    
    @log_function_call
    def consult(self, question: str, context: Dict = None) -> Dict[str, Any]:
        """
        刑事法律咨询
        
        Args:
            question: 用户问题
            context: 上下文信息
        
        Returns:
            咨询结果
        """
        logger.info(f"宁律师·刑事收到咨询：{question}")
        
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
            log_business_event('criminal_consult', {
                'question': question,
                'answer': answer
            })
            
            return success_response({
                'answer': answer,
                'lawyer': self.persona['name'],
                'category': '刑事法律'
            })
            
        except Exception as e:
            logger.error(f"刑事咨询失败：{str(e)}")
            return error_response(f"咨询失败：{str(e)}")
    
    @log_function_call
    def analyze_case(self, case_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析刑事案件
        
        Args:
            case_info: 案件信息
        
        Returns:
            分析结果
        """
        logger.info("开始分析刑事案件")
        
        try:
            prompt = f"""
            请分析以下刑事案件：
            
            案件事实：{case_info.get('facts', '未知')}
            涉及罪名：{case_info.get('charges', '未知')}
            涉案金额：{case_info.get('amount', '未知')}
            
            请从以下方面分析：
            1. 案件性质和罪名认定
            2. 相关刑法条文
            3. 法律风险和量刑标准
            4. 辩护策略建议
            5. 注意事项和法律程序
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
            logger.error(f"刑事案分析失败：{str(e)}")
            return error_response(f"刑事案分析失败：{str(e)}")
    
    @log_function_call
    def apply_bail(self, case_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        申请取保候审
        
        Args:
            case_info: 案件信息
        
        Returns:
            申请结果
        """
        logger.info("开始准备取保候审申请")
        
        try:
            prompt = f"""
            请为以下案件准备取保候审申请：
            
            案件事实：{case_info.get('facts', '未知')}
            涉及罪名：{case_info.get('charges', '未知')}
            申请人情况：{case_info.get('applicant_info', '未知')}
            
            请提供：
            1. 取保候审的法律依据
            2. 申请取保候审的理由
            3. 取保候审申请书草案
            4. 注意事项
            """
            
            messages = self.prompt_template.format_messages(
                chat_history=[],
                user_input=prompt
            )
            
            response = self.llm.invoke(messages)
            application = response.content
            
            return success_response({
                'application': application,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"取保候审申请失败：{str(e)}")
            return error_response(f"取保候审申请失败：{str(e)}")


# 创建全局实例
ning_lawyer_criminal = NingLawyerCriminal()
