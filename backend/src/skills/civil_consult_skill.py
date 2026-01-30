"""
民事咨询技能模块（Civil Consult Skill）
提供民事法律咨询服务
"""

import re
import json
from typing import Dict, Any
from loguru import logger

from src.prompts.manager import PromptManager


class CivilConsultSkill:
    """民事咨询技能"""
    
    def __init__(self, model: str = "doubao-seed-1-8-251228"):
        """
        初始化民事咨询技能
        
        Args:
            model: 使用的模型
        """
        self.model = model
        
        # 获取提示词模板（从提示词管理器）
        self.prompt_template = PromptManager.get_skill_prompt('civil_consult')
        
        logger.info("⚖️ 民事咨询技能初始化完成")
    
    def execute(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行民事咨询
        
        Args:
            user_input: 用户输入（法律问题）
            context: 上下文信息
            
        Returns:
            咨询结果
        """
        logger.info(f"⚖️ 开始法律咨询：{user_input[:50]}...")
        
        try:
            # 使用提示词模板
            messages = self.prompt_template.format_messages(
                user_input=user_input
            )
            
            # 这里需要传入 LLM 客户端
            # 由于原始代码使用了 LLMClient，这里保留接口
            # 实际使用时需要传入 client 参数
            from coze_coding_dev_sdk import LLMClient
            from coze_coding_utils.runtime_ctx.context import new_context
            
            client = LLMClient(ctx=new_context(method="invoke"))
            response = client.invoke(
                messages=messages,
                model=self.model,
                temperature=0.5,
                max_completion_tokens=3000
            )
            
            content = response.content
            if isinstance(content, str):
                content = content.strip()
            
            # 解析JSON
            json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(content)
            
            logger.info("✅ 法律咨询完成")
            return {
                "success": True,
                "data": result
            }
            
        except Exception as e:
            logger.error(f"❌ 法律咨询失败：{str(e)}")
            return {
                "success": False,
                "error": f"法律咨询失败：{str(e)}"
            }
    
    def classify_domain(self, question: str) -> str:
        """
        分类法律领域
        
        Args:
            question: 用户问题
            
        Returns:
            法律领域
        """
        question_lower = question.lower()
        
        if any(keyword in question_lower for keyword in ["借款", "欠款", "债务", "借钱", "还钱"]):
            return "债务纠纷"
        elif any(keyword in question_lower for keyword in ["离婚", "抚养", "赡养", "继承", "婚姻"]):
            return "婚姻家庭"
        elif any(keyword in question_lower for keyword in ["劳动", "工资", "加班", "辞退", "裁员"]):
            return "劳动争议"
        elif any(keyword in question_lower for keyword in ["侵权", "损害", "赔偿", "人身", "财产"]):
            return "侵权责任"
        elif any(keyword in question_lower for keyword in ["违约", "解除合同", "赔偿损失"]):
            return "合同纠纷"
        elif any(keyword in question_lower for keyword in ["房屋", "买卖", "租赁", "物业", "房产"]):
            return "房产纠纷"
        else:
            return "民事纠纷"


# 全局民事咨询技能实例
civil_consult_skill = CivilConsultSkill()


# 执行函数（用于注册）
def execute_civil_consult(user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """民事咨询技能执行函数"""
    return civil_consult_skill.execute(user_input, context)
