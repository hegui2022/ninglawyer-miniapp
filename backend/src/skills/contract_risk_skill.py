"""
合同风险识别技能模块（Contract Risk Identification Skill）
识别合同中的各类法律风险
"""

import re
import json
from typing import Dict, Any
from loguru import logger

from src.prompts.manager import PromptManager


class ContractRiskSkill:
    """合同风险识别技能"""
    
    def __init__(self, model: str = "doubao-seed-1-8-251228"):
        """
        初始化合同风险识别技能
        
        Args:
            model: 使用的模型
        """
        self.model = model
        
        logger.info("🔍 合同风险识别技能初始化完成")
    
    def execute(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行合同风险识别
        
        Args:
            user_input: 用户输入（合同内容）
            context: 上下文信息
            
        Returns:
            风险识别结果
        """
        logger.info(f"🔍 开始识别合同风险...")
        
        try:
            # 构建提示词
            from src.prompts.skills.contract_risk import CONTRACT_RISK_IDENTIFICATION_SYSTEM
            
            system_prompt = CONTRACT_RISK_IDENTIFICATION_SYSTEM.format(disclaimer="")
            user_message = f"""请识别以下合同中的风险：

{user_input}

请以JSON格式返回结果，包含以下字段：
{{
  "contract_type": "合同类型",
  "overall_risk_level": "整体风险等级（高/中/低）",
  "risk_score": 风险评分(0-100),
  "risks": [
    {{
      "risk_id": "风险编号",
      "risk_name": "风险名称",
      "risk_type": "风险类型（主体风险/条款风险/法律风险/履行风险/争议解决风险/其他风险）",
      "risk_level": "风险等级（高/中/低）",
      "risk_description": "风险描述",
      "legal_consequence": "可能的法律后果",
      "economic_loss": "可能的经济损失",
      "prevention_suggestion": "防控建议"
    }}
  ],
  "missing_clauses": ["缺失条款1", "缺失条款2"],
  "summary": "风险总结",
  "recommendations": ["完善建议1", "完善建议2"]
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
                max_completion_tokens=4000
            )
            
            content = response.content
            logger.info(f"📝 LLM返回内容（前200字符）：{str(content)[:200] if content else 'None'}")
            
            if isinstance(content, str):
                content = content.strip()
            
            # 如果返回的是纯文本而不是JSON，尝试解析
            if not content.startswith('{'):
                logger.info("返回内容不是JSON格式，尝试提取JSON...")
                # 尝试从文本中提取JSON
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    content = json_match.group()
            
            # 解析JSON
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(content)
            
            logger.info("✅ 合同风险识别完成")
            return {
                "success": True,
                "data": result
            }
            
        except Exception as e:
            logger.error(f"❌ 合同风险识别失败：{str(e)}")
            # 降级：返回空风险列表
            return {
                "success": True,
                "data": {
                    "contract_type": "未知",
                    "overall_risk_level": "无法评估",
                    "risk_score": 0,
                    "risks": [],
                    "missing_clauses": [],
                    "summary": "风险识别失败，请检查输入内容",
                    "recommendations": ["请输入完整的合同内容"]
                }
            }


# 全局实例
contract_risk_skill = ContractRiskSkill()


# 执行函数（用于注册）
def execute_contract_risk(user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """合同风险识别技能执行函数"""
    return contract_risk_skill.execute(user_input, context)
