"""
合同起草技能模块（Contract Skill）
支持合同起草和审查
"""

import re
import json
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from loguru import logger

from prompts.manager import PromptManager


class ContractSkill:
    """合同起草技能"""
    
    def __init__(self, model: str = "doubao-seed-1-8-251228"):
        """
        初始化合同起草技能
        
        Args:
            model: 使用的模型
        """
        self.model = model
        self.client = LLMClient(ctx=new_context(method="invoke"))
        
        # 获取提示词模板（从提示词管理器）
        # 注意：由于这个技能使用了 LLMClient 和特殊的 JSON 格式输出，
        # 这里我们保留原有的实现方式，但提示词需要从配置中读取
        from src.prompts.skills.contract import CONTRACT_DRAFT_SYSTEM, CONTRACT_REVIEW_SYSTEM
        self.system_prompt_draft = CONTRACT_DRAFT_SYSTEM
        self.system_prompt_review = CONTRACT_REVIEW_SYSTEM
        
        logger.info("📄 合同起草技能初始化完成")
    
    def execute(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行合同起草或审查
        
        Args:
            user_input: 用户输入
            context: 上下文信息
            
        Returns:
            合同结果
        """
        logger.info(f"📄 处理合同请求：{user_input[:50]}...")
        
        try:
            # 判断是起草还是审查
            action = self._detect_action(user_input)
            
            if action == "draft":
                result = self._draft_contract(user_input)
            elif action == "review":
                result = self._review_contract(user_input)
            else:
                result = {
                    "success": False,
                    "error": "无法识别您的需求，请问您是要起草合同还是审查合同？"
                }
            
            logger.info("✅ 合同处理完成")
            return {
                "success": True,
                "data": result
            }
            
        except Exception as e:
            logger.error(f"❌ 合同处理失败：{str(e)}")
            return {
                "success": False,
                "error": f"合同处理失败：{str(e)}"
            }
    
    def _detect_action(self, user_input: str) -> str:
        """
        检测用户意图（起草或审查）
        
        Args:
            user_input: 用户输入
            
        Returns:
            action: draft/review
        """
        input_lower = user_input.lower()
        
        if any(keyword in input_lower for keyword in ["起草", "写", "生成", "模板", "帮我写"]):
            return "draft"
        elif any(keyword in input_lower for keyword in ["审查", "检查", "分析", "风险", "帮我看看"]):
            return "review"
        else:
            return "draft"  # 默认起草
    
    def _draft_contract(self, request: str) -> Dict[str, Any]:
        """
        起草合同
        
        Args:
            request: 起草请求
            
        Returns:
            合同内容
        """
        prompt = f"""合同起草请求：{request}

请起草一份完整规范的合同，包含所有必要的法律条款。

返回JSON格式：
{{
  "contract_type": "合同类型",
  "contract": "合同完整文本",
  "key_points": ["要点1", "要点2", "要点3"],
  "tips": ["注意事项1", "注意事项2"],
  "risks": ["风险提示1"]
}}

只返回JSON，不要其他内容。"""
        
        messages = [
            SystemMessage(content=self.system_prompt_draft),
            HumanMessage(content=prompt)
        ]
        
        response = self.client.invoke(
            messages=messages,
            model=self.model,
            temperature=0.4,
            max_completion_tokens=5000
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
    
    def _review_contract(self, contract_content: str) -> Dict[str, Any]:
        """
        审查合同
        
        Args:
            contract_content: 合同内容
            
        Returns:
            审查结果
        """
        prompt = f"""合同审查请求：
{contract_content}

请审查这份合同，识别潜在的法律风险。

返回JSON格式：
{{
  "contract_type": "合同类型",
  "analysis": "合同分析",
  "risks": [
    {{
      "level": "风险等级（高/中/低）",
      "content": "风险内容",
      "suggestion": "修改建议"
    }}
  ],
  "suggestions": ["完善建议1", "完善建议2"],
  "score": 风险评分(0-100),
  "missing_clauses": ["缺失条款1", "缺失条款2"]
}}

只返回JSON，不要其他内容。"""
        
        messages = [
            SystemMessage(content=self.system_prompt_review),
            HumanMessage(content=prompt)
        ]
        
        response = self.client.invoke(
            messages=messages,
            model=self.model,
            temperature=0.4,
            max_completion_tokens=5000
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


# 全局实例
_contract_skill = ContractSkill()


def execute_contract(user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    执行合同技能（全局函数，用于注册到技能注册表）
    
    Args:
        user_input: 用户输入
        context: 上下文信息
        
    Returns:
        合同处理结果
    """
    return _contract_skill.execute(user_input, context)
