"""
案例查询技能模块（Case Query Skill）
查询相关案例和判决结果（怎么判小程序）
"""

import re
import json
from typing import Dict, Any
from loguru import logger


class CaseQuerySkill:
    """案例查询技能"""
    
    def __init__(self, model: str = "doubao-seed-1-8-251228"):
        """
        初始化案例查询技能
        
        Args:
            model: 使用的模型
        """
        self.model = model
        
        logger.info("⚖️ 案例查询技能初始化完成")
    
    def execute(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行案例查询
        
        Args:
            user_input: 用户输入（案件描述或法律问题）
            context: 上下文信息
            
        Returns:
            案例查询结果
        """
        logger.info(f"⚖️ 开始查询案例...")
        
        try:
            # 获取知识库内容（如果上下文中提供）
            knowledge = ""
            if context and "knowledge" in context:
                knowledge = context["knowledge"]
                logger.info(f"📚 使用知识库内容（{len(knowledge)}字符）")
            
            # 构建提示词
            from src.prompts.skills.case_query import CASE_QUERY_SYSTEM
            
            system_prompt = CASE_QUERY_SYSTEM.format(disclaimer="")
            
            # 构建用户消息
            if knowledge:
                user_message = f"""知识库中的相关案例：
{knowledge}

用户咨询：
{user_input}

请基于知识库中的案例，为用户提供参考建议。如果没有找到完全匹配的案例，请提供最相似的案例并说明相似点。"""
            else:
                user_message = f"""用户咨询：
{user_input}

请根据你的知识库，为用户提供相关案例和判决参考。"""
            
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
            
            # 案例查询返回文本即可，不需要JSON
            logger.info("✅ 案例查询完成")
            return content
            
        except Exception as e:
            logger.error(f"❌ 案例查询失败：{str(e)}")
            # 降级：返回提示信息
            return "抱歉，案例查询暂时失败。您可以尝试提供更详细的案件描述，或咨询专业律师获取针对性建议。"


# 全局实例
case_query_skill = CaseQuerySkill()


# 执行函数（用于注册）
def execute_case_query(user_input: str, context: Dict[str, Any] = None) -> str:
    """案例查询技能执行函数"""
    return case_query_skill.execute(user_input, context)
