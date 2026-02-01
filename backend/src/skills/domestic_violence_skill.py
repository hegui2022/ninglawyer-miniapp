"""
家暴维权技能（Domestic Violence Skill）
提供家暴维权相关的法律咨询
"""

import json
from typing import Dict, Any
from loguru import logger
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context

from prompts.skills.family_law import DOMESTIC_VIOLENCE_PROMPT
from utils.exception_handler import exception_handler


def execute_domestic_violence(user_input: str, context: Dict[str, Any] = None) -> str:
    """
    执行家暴维权咨询
    
    Args:
        user_input: 用户输入
        context: 上下文信息（包含 user_type, scenario, personality_id, knowledge）
    
    Returns:
        咨询结果
    """
    logger.info(f"⚖️ 执行家暴维权咨询：{user_input[:50]}...")
    
    try:
        # 初始化上下文
        if context is None:
            context = {}
        
        # 获取知识检索结果
        knowledge = context.get("knowledge", "")
        
        # 获取人设信息
        personality_id = context.get("personality_id", "warm_personal")
        
        # 构建提示词
        prompt = DOMESTIC_VIOLENCE_PROMPT.format(
            knowledge=knowledge,
            user_input=user_input
        )
        
        # 调用 LLM
        client = LLMClient(ctx=new_context(method="invoke"))
        response = client.invoke(
            messages=[{"role": "user", "content": prompt}],
            model="doubao-seed-1-8-251228",
            temperature=0.7,
            max_completion_tokens=2000
        )
        
        result = response.content.strip()
        logger.info(f"✅ 家暴维权咨询完成")
        return result
    
    except Exception as e:
        logger.error(f"❌ 家暴维权咨询失败：{e}")
        raise


# 技能元数据（用于技能注册表）
SKILL_NAME = "domestic_violence"
SKILL_DESCRIPTION = "家暴维权"
SKILL_CATEGORY = "family_law"
