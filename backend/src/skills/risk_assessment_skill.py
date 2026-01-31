"""
风险等级评估技能模块（Risk Assessment Skill）
对业务场景、法律问题或合同进行整体风险评估
"""

import re
import json
from typing import Dict, Any
from loguru import logger


class RiskAssessmentSkill:
    """风险等级评估技能"""
    
    def __init__(self, model: str = "doubao-seed-1-8-251228"):
        """
        初始化风险等级评估技能
        
        Args:
            model: 使用的模型
        """
        self.model = model
        
        logger.info("📊 风险等级评估技能初始化完成")
    
    def execute(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行风险等级评估
        
        Args:
            user_input: 用户输入（业务场景、法律问题或合同内容）
            context: 上下文信息
            
        Returns:
            风险评估结果
        """
        logger.info(f"📊 开始评估风险等级...")
        
        try:
            # 构建提示词
            from src.prompts.skills.risk_assessment import RISK_ASSESSMENT_SYSTEM
            
            system_prompt = RISK_ASSESSMENT_SYSTEM.format(disclaimer="")
            user_message = f"""请对以下场景进行风险评估：

{user_input}

请以JSON格式返回结果，包含以下字段：
{{
  "scenario_type": "场景类型（合同/业务/法律问题）",
  "overall_risk_level": "整体风险等级（高/中/低）",
  "risk_score": 风险评分(0-100),
  "risk_factors": [
    {{
      "factor_name": "风险因素名称",
      "risk_level": "风险等级（高/中/低）",
      "weight": 权重(0-1),
      "score": 得分(0-100),
      "description": "风险描述"
    }}
  ],
  "risk_analysis": "风险分析",
  "potential_impacts": ["可能影响1", "可能影响2"],
  "control_measures": ["防控措施1", "防控措施2"],
  "recommendations": ["建议1", "建议2"],
  "summary": "评估总结"
}}

只返回JSON，不要其他内容。"""
            
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
                temperature=0.3,
                max_completion_tokens=3000
            )
            
            content = response.content
            logger.info(f"📝 LLM返回内容（前200字符）：{str(content)[:200] if content else 'None'}")
            
            if isinstance(content, str):
                content = content.strip()
            
            # 如果返回的是纯文本而不是JSON，尝试解析
            if not content.startswith('{'):
                logger.info("返回内容不是JSON格式，尝试提取JSON...")
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    content = json_match.group()
            
            # 解析JSON
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(content)
            
            logger.info("✅ 风险等级评估完成")
            return {
                "success": True,
                "data": result
            }
            
        except Exception as e:
            logger.error(f"❌ 风险等级评估失败：{str(e)}")
            # 降级：返回默认评估结果
            return {
                "success": True,
                "data": {
                    "scenario_type": "未知",
                    "overall_risk_level": "无法评估",
                    "risk_score": 0,
                    "risk_factors": [],
                    "risk_analysis": "风险评估失败，请检查输入内容",
                    "potential_impacts": [],
                    "control_measures": [],
                    "recommendations": ["请提供更详细的场景描述"],
                    "summary": "评估失败"
                }
            }


# 全局实例
risk_assessment_skill = RiskAssessmentSkill()


# 执行函数（用于注册）
def execute_risk_assessment(user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """风险等级评估技能执行函数"""
    return risk_assessment_skill.execute(user_input, context)
