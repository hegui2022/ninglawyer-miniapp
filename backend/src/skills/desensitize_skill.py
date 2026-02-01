"""
脱敏技能模块（Desensitize Skill）
对敏感信息进行脱敏处理
"""

import re
import json
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from loguru import logger

from prompts.manager import PromptManager
from prompts.skills.desensitize import DESENSITIZE_SYSTEM


class DesensitizeSkill:
    """脱敏技能"""
    
    def __init__(self, model: str = "doubao-seed-1-8-251228"):
        """
        初始化脱敏技能
        
        Args:
            model: 使用的模型
        """
        self.model = model
        self.client = LLMClient(ctx=new_context(method="invoke"))
        
        # 获取提示词模板（从提示词管理器）
        self.system_prompt = DESENSITIZE_SYSTEM
        
        logger.info("🔒 脱敏技能初始化完成")
    
    def execute(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行脱敏
        
        Args:
            user_input: 用户输入（包含敏感信息的文本）
            context: 上下文信息
            
        Returns:
            脱敏结果
        """
        logger.info(f"🔒 开始脱敏处理：{user_input[:50]}...")
        
        try:
            prompt = f"""请对以下文本进行脱敏处理：

{user_input}

请按照脱敏规则进行处理，返回JSON格式：
{{
  "original": "原始文本",
  "desensitized": "脱敏后文本",
  "details": [
    {{
      "type": "信息类型",
      "original": "原始值",
      "desensitized": "脱敏后值"
    }}
  ]
}}

只返回JSON，不要其他内容。"""
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.client.invoke(
                messages=messages,
                model=self.model,
                temperature=0.3,
                max_completion_tokens=2000
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
            
            logger.info("✅ 脱敏处理完成")
            return {
                "success": True,
                "data": result
            }
            
        except Exception as e:
            logger.error(f"❌ 脱敏处理失败：{str(e)}")
            return {
                "success": False,
                "error": f"脱敏处理失败：{str(e)}"
            }


# 全局实例
_desensitize_skill = DesensitizeSkill()


def execute_desensitize(user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    执行脱敏技能（全局函数，用于注册到技能注册表）
    
    Args:
        user_input: 用户输入
        context: 上下文信息
        
    Returns:
        脱敏结果
    """
    return _desensitize_skill.execute(user_input, context)
