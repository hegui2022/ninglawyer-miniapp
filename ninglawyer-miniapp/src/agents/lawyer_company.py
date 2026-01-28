"""
宁律师·公司 - 完整版
提供公司法律服务
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


class NingLawyerCompany:
    """宁律师·公司"""
    
    def __init__(self):
        """初始化宁律师·公司"""
        self.persona = {
            'name': '宁律师·公司',
            'avatar': '/assets/images/lawyers/company.png',
            'temperature': 0.6,
            'system_prompt': """你是宁律师·公司，一位专业的公司法律顾问。

你的专业领域：
- 公司设立：公司注册、章程制定、股权结构设计
- 公司治理：股东会、董事会、监事会运作规范
- 股权转让：股权变更、股权激励、股权融资
- 公司并购：尽职调查、并购方案设计
- 公司解散：清算注销、债务处理
- 合规管理：公司合规体系建设

服务理念：
1. 合规经营：确保公司运营合法合规
2. 风险防控：提前识别和防范法律风险
3. 保护权益：维护公司和股东合法权益
4. 专业高效：快速响应，解决公司法律问题

回答规范：
1. 引用《公司法》等法律条文
2. 分析法律风险和责任
3. 提供具体的操作方案
4. 提醒程序要求和时效
5. 维护公司利益

重要提醒：
- 公司法律事务涉及重大利益，建议咨询专业律师
- 公司设立、变更、注销有严格程序要求
- 你是提供法律咨询的 AI 助手，重大决策请咨询专业律师"""
        }
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=config['MODEL_NAME'],
            base_url=config['MODEL_BASE_URL'],
            api_key=config['MODEL_API_KEY'],
            temperature=0.6,
            streaming=True
        )
        
        logger.info("宁律师·公司初始化完成")
    
    @log_function_call
    def consult(self, question: str, context: Dict = None) -> Dict[str, Any]:
        """
        公司法律咨询
        
        Args:
            question: 用户问题
            context: 上下文信息
        
        Returns:
            咨询结果
        """
        logger.info(f"宁律师·公司收到咨询：{question}")
        
        try:
            prompt = f"""
            请回答以下公司法律问题：
            
            问题：{question}
            
            要求：
            1. 引用《公司法》等法律条文
            2. 分析法律风险
            3. 提供解决方案
            4. 提醒程序要求
            """
            
            messages = [
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            answer = response.content
            
            log_business_event('company_consult', {
                'question': question,
                'answer': answer
            })
            
            return success_response({
                'answer': answer,
                'lawyer': self.persona['name'],
                'category': '公司法律'
            })
            
        except Exception as e:
            logger.error(f"公司咨询失败：{str(e)}")
            return error_response(f"咨询失败：{str(e)}")
    
    @log_function_call
    def design_equity_structure(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        设计股权结构
        
        Args:
            company_info: 公司信息
        
        Returns:
            股权结构方案
        """
        logger.info("开始设计股权结构")
        
        try:
            prompt = f"""
            请设计公司股权结构：
            
            公司名称：{company_info.get('company_name')}
            股东数量：{company_info.get('shareholder_count')}人
            创始股东：{company_info.get('founders')}
            融资需求：{company_info.get('funding_needs', 0)}元
            行业类型：{company_info.get('industry')}
            
            请设计：
            1. 初始股权分配方案
            2. 股权激励池设置
            3. 股权稀释考虑
            4. 股权锁定和退出机制
            5. 公司治理结构
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            structure = response.content
            
            return success_response({
                'structure': structure,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"股权结构设计失败：{str(e)}")
            return error_response(f"股权结构设计失败：{str(e)}")
    
    @log_function_call
    def draft_articles(self, articles_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        起草公司章程
        
        Args:
            articles_info: 章程信息
        
        Returns:
            公司章程
        """
        logger.info("开始起草公司章程")
        
        try:
            prompt = f"""
            请起草公司章程：
            
            公司名称：{articles_info.get('company_name')}
            公司类型：{articles_info.get('company_type')}
            注册资本：{articles_info.get('registered_capital')}万元
            股东信息：{articles_info.get('shareholders')}
            经营范围：{articles_info.get('business_scope')}
            
            请根据《公司法》起草规范的公司章程，包含：
            1. 总则
            2. 经营宗旨和范围
            3. 注册资本和股东
            4. 股东会
            5. 董事会
            6. 经营管理机构
            7. 财务会计
            8. 解散和清算
            """
            
            response = self.llm.invoke([
                SystemMessage(content=self.persona['system_prompt']),
                HumanMessage(content=prompt)
            ])
            
            articles = response.content
            
            return success_response({
                'articles': articles,
                'lawyer': self.persona['name']
            })
            
        except Exception as e:
            logger.error(f"公司章程起草失败：{str(e)}")
            return error_response(f"公司章程起草失败：{str(e)}")
    
    @log_function_call
    def analyze_merger(self, merger_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析并购方案
        
        Args:
            merger_info: 并购信息
        
        Returns:
            分析结果
        """
        logger.info("开始分析并购方案")
        
        try:
            prompt = f"""
            请分析以下公司并购方案：
            
            收购方：{merger_info.get('buyer')}
            目标公司：{merger_info.get('target')}
            并购方式：{merger_info.get('method')}
            交易价格：{merger_info.get('price', 0)}万元
            并购目的：{merger_info.get('purpose')}
            
            请分析：
            1. 并购的法律风险
            2. 尽职调查要点
            3. 交易结构设计
            4. 交割条件
            5. 过渡期安排
            6. 反收购措施
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
            logger.error(f"并购分析失败：{str(e)}")
            return error_response(f"并购分析失败：{str(e)}")
    
    @log_function_call
    def get_info(self) -> Dict[str, Any]:
        """
        获取宁律师信息
        
        Returns:
            宁律师信息
        """
        return {
            'id': 'company',
            'name': '宁律师·公司',
            'avatar': self.persona['avatar'],
            'domain': '公司',
            'description': '专业提供公司设立、治理、股权、并购等法律服务',
            'skills': [
                '公司设立',
                '公司治理',
                '股权设计',
                '股权激励',
                '公司并购',
                '合规管理'
            ],
            'helpCount': 8900,
            'rating': 4.8,
            'consultCount': 6800,
            'expertise': [
                '公司法实务',
                '公司并购法律',
                '股权设计',
                '公司治理',
                '企业合规'
            ],
            'reviews': [
                {
                    'user': '王总',
                    'rating': 5,
                    'content': '股权结构设计很专业，避了很多坑',
                    'date': '2024-01-28'
                },
                {
                    'user': '李总',
                    'rating': 5,
                    'content': '并购方案分析很到位，帮我们节省了很多成本',
                    'date': '2024-01-22'
                }
            ]
        }
