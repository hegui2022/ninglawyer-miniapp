"""
宁律师·知识产权 - 完整版
提供知识产权法律服务
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


class NingLawyerIP:
    """宁律师·知识产权"""
    
    def __init__(self):
        """初始化宁律师·知识产权"""
        self.persona = {
            'name': '宁律师·知识产权',
            'avatar': '/assets/images/lawyers/ip.png',
            'temperature': 0.6,
            'system_prompt': """你是宁律师·知识产权，一位专业的知识产权法律顾问。

你的专业领域：
- 专利申请：发明、实用新型、外观设计专利
- 商标注册：商标申请、异议、复审
- 版权登记：著作权、软件著作权
- 知识产权保护：侵权维权、诉讼代理
- 技术转让：技术许可、技术转让合同
- 知识产权布局：企业知识产权战略

服务理念：
1. 保护创新：保护创新成果和知识产权
2. 价值转化：将知识产权转化为商业价值
3. 风险防控：避免侵犯他人知识产权
4. 专业高效：快速响应，提供专业服务

回答规范：
1. 引用《专利法》《商标法》《著作权法》等法律条文
2. 分析知识产权权利和保护范围
3. 提供申请、注册、维权方案
4. 提醒程序要求和时效
5. 评估侵权风险

重要提醒：
- 知识产权申请有时效性和地域性
- 申请前要进行检索和风险评估
- 你是提供法律咨询的 AI 助手，重大申请建议咨询专业律师"""
        }
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=0.6,
            streaming=True
        )
        
        logger.info("宁律师·知识产权初始化完成")
    
    @log_function_call
    def consult(self, question: str, context: Dict = None) -> Dict[str, Any]:
        """
        知识产权咨询
        
        Args:
            question: 用户问题
            context: 上下文信息
        
        Returns:
            咨询结果
        """
        logger.info(f"宁律师·知识产权收到咨询：{question}")
        
        try:
            prompt = f"""
            请回答以下知识产权法律问题：
            
            问题：{question}
            
            要求：
            1. 引用相关知识产权法律条文
            2. 分析权利范围
            3. 提供解决方案
            4. 提醒程序要求
            """
            
            # 使用提示词模板
            messages = self.prompt_template.format_messages(
                chat_history=[],
                user_input=prompt
            )
            
            response = self.llm.invoke(messages)
            answer = response.content
            
            log_business_event('ip_consult', {
                'question': question,
                'answer': answer
            })
            
            return success_response({
                'answer': answer,
                'lawyer': self.persona['name'],
                'category': '知识产权'
            })
            
        except Exception as e:
            logger.error(f"知识产权咨询失败：{str(e)}")
            return error_response(f"咨询失败：{str(e)}")
    
    @log_function_call
    def analyze_infringement(self, infringement_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析知识产权侵权
        
        Args:
            infringement_info: 侵权信息
        
        Returns:
            分析结果
        """
        logger.info("开始分析知识产权侵权")
        
        try:
            ip_type = infringement_info.get('type', 'patent')
            
            if ip_type == 'patent':
                prompt = f"""
                请分析专利侵权：
                
                专利名称：{infringement_info.get('patent_name')}
                专利号：{infringement_info.get('patent_number')}
                侵权产品：{infringement_info.get('infringing_product')}
                侵权方式：{infringement_info.get('infringement_method')}
                
                请根据《专利法》分析：
                1. 是否构成侵权
                2. 侵权类型
                3. 侵权责任
                4. 维权方案
                """
            elif ip_type == 'trademark':
                prompt = f"""
                请分析商标侵权：
                
                商标名称：{infringement_info.get('trademark_name')}
                商标类别：{infringement_info.get('trademark_class')}
                侵权商品：{infringement_info.get('infringing_product')}
                侵权行为：{infringement_info.get('infringement_behavior')}
                
                请根据《商标法》分析：
                1. 是否构成侵权
                2. 侵权认定标准
                3. 侵权责任
                4. 维权方案
                """
            elif ip_type == 'copyright':
                prompt = f"""
                请分析著作权侵权：
                
                作品名称：{infringement_info.get('work_name')}
                作品类型：{infringement_info.get('work_type')}
                侵权行为：{infringement_info.get('infringement_behavior')}
                
                请根据《著作权法》分析：
                1. 是否构成侵权
                2. 合理使用范围
                3. 侵权责任
                4. 维权方案
                """
            else:
                return error_response("不支持的知识产权类型")
            
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
            logger.error(f"侵权分析失败：{str(e)}")
            return error_response(f"侵权分析失败：{str(e)}")
    
    @log_function_call
    def draft_license_agreement(self, license_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        起草许可协议
        
        Args:
            license_info: 许可信息
        
        Returns:
            许可协议
        """
        logger.info("开始起草许可协议")
        
        try:
            prompt = f"""
            请起草知识产权许可协议：
            
            许可方：{license_info.get('licensor')}
            被许可方：{license_info.get('licensee')}
            知识产权类型：{license_info.get('ip_type')}
            知识产权内容：{license_info.get('ip_content')}
            许可方式：{license_info.get('license_type')}（独占许可/排他许可/普通许可）
            许可期限：{license_info.get('term')}
            许可费用：{license_info.get('fee', 0)}元
            
            请起草规范的知识产权许可协议。
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
            logger.error(f"许可协议起草失败：{str(e)}")
            return error_response(f"许可协议起草失败：{str(e)}")
    
    @log_function_call
    def get_info(self) -> Dict[str, Any]:
        """
        获取宁律师信息
        
        Returns:
            宁律师信息
        """
        return {
            'id': 'ip',
            'name': '宁律师·知识产权',
            'avatar': self.persona['avatar'],
            'domain': '知识产权',
            'description': '专业提供专利申请、商标注册、版权登记、侵权维权等服务',
            'skills': [
                '专利申请',
                '商标注册',
                '版权登记',
                '侵权维权',
                '技术转让',
                '知识产权布局'
            ],
            'helpCount': 7800,
            'rating': 4.9,
            'consultCount': 5600,
            'expertise': [
                '专利法实务',
                '商标法实务',
                '著作权法',
                '知识产权保护',
                '技术转让法律'
            ],
            'reviews': [
                {
                    'user': '张工',
                    'rating': 5,
                    'content': '专利申请很专业，授权很快',
                    'date': '2024-01-30'
                },
                {
                    'user': '李总',
                    'rating': 5,
                    'content': '帮我们成功维权，获得了赔偿',
                    'date': '2024-01-25'
                }
            ]
        }
