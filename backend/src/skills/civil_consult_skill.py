"""
民事咨询技能模块（Civil Consult Skill）
提供民事法律咨询服务
"""

import re
import json
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from loguru import logger


class CivilConsultSkill:
    """民事咨询技能"""
    
    def __init__(self, model: str = "doubao-seed-1-8-251228"):
        """
        初始化民事咨询技能
        
        Args:
            model: 使用的模型
        """
        self.model = model
        self.client = LLMClient(ctx=new_context(method="invoke"))
        
        # 系统提示词
        self.system_prompt = """你是宁律师民事咨询专家，提供专业的民事法律咨询服务。

## 你的专业领域
1. **债务纠纷**：借款合同、欠款追讨、担保责任等
2. **婚姻家庭**：离婚、抚养费、赡养费、继承等
3. **劳动争议**：解除劳动合同、工资拖欠、工伤赔偿等
4. **侵权责任**：人身损害、财产损害、名誉权等
5. **合同纠纷**：违约责任、解除合同、赔偿损失等
6. **房产纠纷**：房屋买卖、租赁、物业服务等

## 你的职责
1. 理解用户的问题和需求
2. 提供法律分析和建议
3. 引用相关法律条文
4. 给出实用的解决方案
5. 提醒注意事项和风险

## 回答格式要求
返回JSON格式：
{{
  "domain": "法律领域",
  "question": "用户问题",
  "analysis": "法律分析",
  "legal_basis": [
    "相关法律条文1",
    "相关法律条文2"
  ],
  "suggestions": [
    "建议1",
    "建议2",
    "建议3"
  ],
  "risks": ["风险提示1", "风险提示2"],
  "next_steps": ["下一步行动建议"]
}}

## 注意事项
- 基于现行法律法规回答
- 不做法律效力的保证
- 复杂案件建议咨询专业律师
- 回答要清晰易懂，避免过于专业术语
"""
        
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
            # 使用LLM进行法律分析
            result = self._llm_consult(user_input)
            
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
    
    def _llm_consult(self, question: str) -> Dict[str, Any]:
        """
        使用LLM进行法律咨询
        
        Args:
            question: 用户问题
            
        Returns:
            咨询结果
        """
        prompt = f"""用户咨询：{question}

请提供专业的法律咨询，包括法律分析、法律依据、实用建议、风险提示和下一步行动。

返回JSON格式：
{{
  "domain": "法律领域（如：债务纠纷、婚姻家庭、劳动争议等）",
  "question": "用户问题",
  "analysis": "法律分析",
  "legal_basis": [
    "相关法律条文1",
    "相关法律条文2"
  ],
  "suggestions": [
    "建议1",
    "建议2",
    "建议3"
  ],
  "risks": ["风险提示1", "风险提示2"],
  "next_steps": ["下一步行动建议"]
}}

只返回JSON，不要其他内容。"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.client.invoke(
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
        
        return result
    
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
