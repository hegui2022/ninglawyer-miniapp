"""
宁律师·刑事 - 完整版
提供刑事法律辩护服务
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from loguru import logger

from src.utils.config import get_config
from src.utils.logger import log_function_call, log_business_event
from src.utils.response import success_response, error_response

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
            'system_prompt': """你是宁律师·刑事，一位专业的刑事辩护律师。

你的专业领域：
- 刑事辩护：为犯罪嫌疑人、被告人提供法律辩护
- 取保候审：申请取保候审，争取释放
- 减刑假释：为服刑人员提供减刑假释服务
- 刑事附带民事：处理刑事附带民事赔偿
- 申诉控告：代理申诉、控告、举报案件

服务理念：
1. 捍卫人权：维护当事人的合法权益
2. 依法辩护：以事实为依据，以法律为准绳
3. 专业严谨：深入分析案情，制定最佳辩护策略
4. 诚实守信：如实告知法律风险，不夸大不隐瞒

回答规范：
1. 分析案件性质和可能罪名
2. 引用相关刑法条文
3. 评估法律风险和量刑标准
4. 提供辩护策略建议
5. 提醒注意事项和法律程序

重要提醒：
- 刑事案件专业性强，建议尽早委托专业律师
- 你是提供法律咨询的 AI 助手，不能代替正式律师
- 所有回答仅供参考，重大案件请咨询专业刑事律师"""
        }
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=0.6,
            streaming=True
        )
        
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
            prompt = f"""
            请回答以下刑事法律问题：
            
            问题：{question}
            
            要求：
            1. 分析可能涉及的罪名
            2. 引用相关刑法条文
            3. 评估法律风险和量刑标准
            4. 提供法律建议
            5. 提醒注意事项
            """
            
            messages = [
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            answer = response.content
            
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
            
            案件类型：{case_info.get('type')}
            案件描述：{case_info.get('description')}
            涉案金额：{case_info.get('amount', 0)}元
            涉案人员：{case_info.get('suspects')}
            案件阶段：{case_info.get('stage', '侦查阶段')}
            
            请分析：
            1. 可能的罪名
            2. 构成要件分析
            3. 法律后果和量刑标准
            4. 辩护策略
            5. 取保候审可能性
            6. 法律风险提示
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
            logger.error(f"案件分析失败：{str(e)}")
            return error_response(f"案件分析失败：{str(e)}")
    
    @log_function_call
    def apply_bail(self, bail_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        申请取保候审
        
        Args:
            bail_info: 取保候审信息
        
        Returns:
            申请结果
        """
        logger.info("开始准备取保候审申请")
        
        try:
            prompt = f"""
            请准备取保候审申请书：
            
            涉嫌罪名：{bail_info.get('charge')}
            申请人：{bail_info.get('applicant')}
            与嫌疑人关系：{bail_info.get('relationship')}
            案情简要：{bail_info.get('case_summary')}
            取保候审理由：{bail_info.get('reasons')}
            
            请根据《刑事诉讼法》第六十七条规定，撰写规范的取保候审申请书。
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            application = response.content
            
            return success_response({
                'application': application,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"取保候审申请失败：{str(e)}")
            return error_response(f"取保候审申请失败：{str(e)}")
    
    @log_function_call
    def get_info(self) -> Dict[str, Any]:
        """
        获取宁律师信息
        
        Returns:
            宁律师信息
        """
        return {
            'id': 'criminal',
            'name': '宁律师·刑事',
            'avatar': self.persona['avatar'],
            'domain': '刑事',
            'description': '专业提供刑事辩护、取保候审、减刑假释等服务',
            'skills': [
                '刑事辩护',
                '取保候审',
                '减刑假释',
                '刑事附带民事',
                '申诉控告'
            ],
            'helpCount': 9680,
            'rating': 4.8,
            'consultCount': 7200,
            'expertise': [
                '刑法实务',
                '刑事诉讼法',
                '刑事辩护技巧',
                '取保候审申请',
                '减刑假释程序'
            ],
            'reviews': [
                {
                    'user': '王先生',
                    'rating': 5,
                    'content': '非常专业，成功取保候审',
                    'date': '2024-01-20'
                },
                {
                    'user': '李女士',
                    'rating': 5,
                    'content': '辩护很到位，从轻判决',
                    'date': '2024-01-15'
                }
            ]
        }
