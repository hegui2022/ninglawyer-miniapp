"""
宁律师·劳动 - 完整版
提供劳动法律服务
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


class NingLawyerLabor:
    """宁律师·劳动"""
    
    def __init__(self):
        """初始化宁律师·劳动"""
        self.persona = {
            'name': '宁律师·劳动',
            'avatar': '/assets/images/lawyers/labor.png',
            'temperature': 0.7
        }
        
        # 获取提示词模板（从提示词管理器）
        from src.prompts.manager import PromptManager
        self.prompt_template = PromptManager.get_lawyer_prompt('labor', simple=False)
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=0.7,
            streaming=True
        )
        
        logger.info("宁律师·劳动初始化完成")
    
    @log_function_call
    def consult(self, question: str, context: Dict = None) -> Dict[str, Any]:
        """
        劳动法律咨询
        
        Args:
            question: 用户问题
            context: 上下文信息
        
        Returns:
            咨询结果
        """
        logger.info(f"宁律师·劳动收到咨询：{question}")
        
        try:
            prompt = f"""
            请回答以下劳动法律问题：
            
            问题：{question}
            
            要求：
            1. 引用相关劳动法律条文
            2. 分析权利义务
            3. 提供解决方案
            4. 提醒法律时效
            """
            
            # 使用提示词模板
            messages = self.prompt_template.format_messages(
                chat_history=[],
                user_input=prompt
            )
            
            response = self.llm.invoke(messages)
            answer = response.content
            
            log_business_event('labor_consult', {
                'question': question,
                'answer': answer
            })
            
            return success_response({
                'answer': answer,
                'lawyer': self.persona['name'],
                'category': '劳动法律'
            })
            
        except Exception as e:
            logger.error(f"劳动咨询失败：{str(e)}")
            return error_response(f"咨询失败：{str(e)}")
    
    @log_function_call
    def calculate_compensation(self, case_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算劳动赔偿
        
        Args:
            case_info: 案件信息
        
        Returns:
            计算结果
        """
        logger.info("开始计算劳动赔偿")
        
        try:
            case_type = case_info.get('type', '')
            
            if case_type == 'dismissal':
                prompt = f"""
                请计算违法解除劳动合同赔偿金：
                
                工作年限：{case_info.get('years')}年{case_info.get('months', 0)}个月
                月工资：{case_info.get('monthly_salary')}元
                是否违法解除：{case_info.get('illegal', False)}
                
                请根据《劳动合同法》计算赔偿金额。
                """
            elif case_type == 'overtime':
                prompt = f"""
                请计算加班费：
                
                月工资：{case_info.get('monthly_salary')}元
                加班时长：{case_info.get('overtime_hours')}小时
                加班类型：{case_info.get('overtime_type')}（工作日/周末/法定假日）
                
                请根据《劳动法》第四十四条计算加班费。
                """
            elif case_type == 'work_injury':
                prompt = f"""
                请计算工伤赔偿：
                
                工伤等级：{case_info.get('injury_level')}级
                月工资：{case_info.get('monthly_salary')}元
                工伤发生地：{case_info.get('location')}
                
                请根据《工伤保险条例》计算工伤赔偿金额。
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
    def analyze_dispute(self, dispute_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析劳动纠纷
        
        Args:
            dispute_info: 纠纷信息
        
        Returns:
            分析结果
        """
        logger.info("开始分析劳动纠纷")
        
        try:
            prompt = f"""
            请分析以下劳动纠纷：
            
            纠纷类型：{dispute_info.get('type')}
            纠纷描述：{dispute_info.get('description')}
            涉及金额：{dispute_info.get('amount', 0)}元
            相关证据：{dispute_info.get('evidence')}
            
            请分析：
            1. 纠纷性质
            2. 法律依据
            3. 争议焦点
            4. 胜诉可能性
            5. 解决建议
            6. 仲裁程序
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
            logger.error(f"纠纷分析失败：{str(e)}")
            return error_response(f"纠纷分析失败：{str(e)}")
    
    @log_function_call
    def draft_termination(self, termination_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        起草解除劳动合同通知
        
        Args:
            termination_info: 解除信息
        
        Returns:
            解除通知
        """
        logger.info("开始起草解除劳动合同通知")
        
        try:
            prompt = f"""
            请起草解除劳动合同通知书：
            
            员工姓名：{termination_info.get('employee_name')}
            入职日期：{termination_info.get('join_date')}
            工作岗位：{termination_info.get('position')}
            解除原因：{termination_info.get('reason')}
            解除类型：{termination_info.get('type')}（协商一致/违法解除/合法解除）
            最后工作日：{termination_info.get('last_work_date')}
            
            请根据《劳动合同法》起草规范的解除劳动合同通知书。
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            notice = response.content
            
            return success_response({
                'notice': notice,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"解除通知起草失败：{str(e)}")
            return error_response(f"解除通知起草失败：{str(e)}")
    
    @log_function_call
    def get_info(self) -> Dict[str, Any]:
        """
        获取宁律师信息
        
        Returns:
            宁律师信息
        """
        return {
            'id': 'labor',
            'name': '宁律师·劳动',
            'avatar': self.persona['avatar'],
            'domain': '劳动',
            'description': '专业处理劳动合同、工资纠纷、工伤赔偿、劳动仲裁等问题',
            'skills': [
                '劳动合同审查',
                '工资纠纷',
                '加班费计算',
                '工伤赔偿',
                '社会保险',
                '劳动仲裁'
            ],
            'helpCount': 11200,
            'rating': 4.9,
            'consultCount': 8600,
            'expertise': [
                '劳动法实务',
                '劳动合同法',
                '工伤保险条例',
                '劳动争议调解仲裁法',
                '社会保险法'
            ],
            'reviews': [
                {
                    'user': '张先生',
                    'rating': 5,
                    'content': '帮我讨回拖欠工资，非常专业',
                    'date': '2024-01-25'
                },
                {
                    'user': '李女士',
                    'rating': 5,
                    'content': '工伤赔偿计算很准确，省了很多事',
                    'date': '2024-01-20'
                }
            ]
        }
