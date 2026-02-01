"""
民事咨询技能模块（Civil Consult Skill）
提供民事法律咨询服务
"""

import re
import json
from typing import Dict, Any
from loguru import logger

from prompts.manager import PromptManager


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
            # 构建提示词（直接使用字符串）
            from src.prompts.skills.civil_consult import CIVIL_CONSULT_SYSTEM
            
            # 从提示词模板获取系统提示词
            system_prompt = CIVIL_CONSULT_SYSTEM.format(disclaimer="")
            
            # 构建用户消息
            user_message = f"用户咨询：{user_input}"
            
            # 调用 LLM
            from coze_coding_dev_sdk import LLMClient
            from coze_coding_utils.runtime_ctx.context import new_context
            
            client = LLMClient(ctx=new_context(method="invoke"))
            response = client.invoke(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                model=self.model,
                temperature=0.5,
                max_completion_tokens=3000
            )
            
            content = response.content
            logger.info(f"📝 LLM返回内容（前200字符）：{str(content)[:200] if content else 'None'}")
            
            if isinstance(content, str):
                content = content.strip()
            
            # 如果返回的是纯文本而不是JSON，直接返回
            if not content.startswith('{'):
                logger.info("✅ 返回纯文本内容")
                return {
                    "success": True,
                    "data": {
                        "domain": self.classify_domain(user_input),
                        "legal_advice": content,
                        "legal_basis": [],
                        "solution_suggestions": []
                    }
                }
            
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
        
        # 债务纠纷（关键词扩展）
        if any(keyword in question_lower for keyword in [
            "借款", "欠款", "债务", "借钱", "还钱", "借条", "欠条",
            "不还", "追债", "讨债", "担保", "利息", "高利贷", "朋友借", "借给我", "借了"
        ]):
            return "债务纠纷"
        # 婚姻家庭（关键词扩展）
        elif any(keyword in question_lower for keyword in [
            "离婚", "抚养", "赡养", "继承", "婚姻", "老公", "老婆", "丈夫", "妻子",
            "出轨", "外遇", "分居", "彩礼", "夫妻", "孩子", "前夫", "前妻"
        ]):
            return "婚姻家庭"
        # 劳动争议（关键词扩展）
        elif any(keyword in question_lower for keyword in [
            "劳动", "工资", "加班", "辞退", "裁员", "工伤", "社保", "公积金",
            "公司", "老板", "雇主", "试用期", "合同到期", "辞退", "开除"
        ]):
            return "劳动争议"
        # 侵权责任（关键词扩展）
        elif any(keyword in question_lower for keyword in [
            "侵权", "损害", "赔偿", "人身", "财产", "名誉", "诽谤", "侮辱",
            "打人", "伤人", "撞人", "损坏", "破坏", "打漏", "漏水", "漏水了",
            "楼下的", "楼上", "楼下", "邻居", "装修", "砸"
        ]):
            return "侵权责任"
        # 合同纠纷（关键词扩展）
        elif any(keyword in question_lower for keyword in [
            "违约", "解除合同", "赔偿损失", "合同", "违约金", "定金",
            "履行", "终止合同", "违约", "毁约"
        ]):
            return "合同纠纷"
        # 房产纠纷（关键词扩展）
        elif any(keyword in question_lower for keyword in [
            "房屋", "买卖", "租赁", "物业", "房产", "买房", "卖房",
            "房东", "租客", "开发商", "物业费", "押金", "退租", "赶我走"
        ]):
            return "房产纠纷"
        else:
            return "民事纠纷"


# 全局民事咨询技能实例
civil_consult_skill = CivilConsultSkill()


# 执行函数（用于注册）
def execute_civil_consult(user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """民事咨询技能执行函数"""
    return civil_consult_skill.execute(user_input, context)
