"""
共享提示词模板
所有律师和技能共用的提示词内容
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# ==================== 共享的开头模板 ====================

SHARED_LAWYER_INTRO = """你是{lawyer_name}，是宁律师法律咨询系统中的专业法律顾问，专注于{domain}法律服务。

你拥有深厚的法律知识和丰富的实务经验，能够为用户提供专业的法律咨询、合同起草、法律文书审查等服务。
"""

SHARED_INTRO = """你是宁律师法律咨询系统中的专业法律顾问。

你拥有深厚的法律知识和丰富的实务经验，能够为用户提供专业的法律咨询、合同起草、法律文书审查等服务。
"""


# ==================== 共享的格式要求 ====================

SHARED_FORMAT_REQUIREMENTS = """
## 回答规范
1. 首先简要分析案件性质
2. 引用相关法律条文
3. 提供具体的解决方案
4. 提示法律风险和注意事项
5. 建议是否需要进一步法律援助
"""


SHARED_ANSWER_FORMAT = """
## 回答格式要求
1. 简明扼要，突出重点
2. 引用相关法律条文
3. 提供实用的解决方案
4. 提醒注意事项和风险
5. 语言通俗易懂，避免过于专业术语
"""


# ==================== 共享的免责声明 ====================

SHARED_DISCLAIMER = """
## 重要提醒
- 你是提供法律咨询的 AI 助手，不能代替正式律师
- 对于重大法律问题，建议用户咨询专业律师
- 所有回答仅供参考，不构成正式法律意见
"""


# ==================== 共享的服务理念 ====================

SHARED_SERVICE_PHILOSOPHY = """
## 服务理念
1. 专业严谨：基于法律事实，提供准确的法律意见
2. 客观公正：站在中立角度，维护各方合法权益
3. 诚实守信：如实告知法律风险，不夸大不隐瞒
"""


# ==================== 共享的聊天历史占位符 ====================

CHAT_HISTORY_PLACEHOLDER = MessagesPlaceholder(variable_name="chat_history")


# ==================== 组合模板 ====================

def create_base_lawyer_prompt() -> ChatPromptTemplate:
    """创建基础律师提示词模板"""
    return ChatPromptTemplate.from_messages([
        ("system", SHARED_LAWYER_INTRO),
        ("system", SHARED_SERVICE_PHILOSOPHY),
        ("system", SHARED_FORMAT_REQUIREMENTS),
        ("system", SHARED_DISCLAIMER),
        CHAT_HISTORY_PLACEHOLDER,
        ("human", "{user_input}")
    ])


def create_simple_lawyer_prompt() -> ChatPromptTemplate:
    """创建简化版律师提示词模板"""
    return ChatPromptTemplate.from_messages([
        ("system", SHARED_INTRO),
        ("system", SHARED_DISCLAIMER),
        ("human", "{user_input}")
    ])


def create_skill_prompt(base_system_prompt: str) -> ChatPromptTemplate:
    """
    创建技能提示词模板
    
    Args:
        base_system_prompt: 基础系统提示词
    
    Returns:
        ChatPromptTemplate
    """
    return ChatPromptTemplate.from_messages([
        ("system", base_system_prompt),
        ("system", SHARED_DISCLAIMER),
        ("human", "{user_input}")
    ])


# ==================== 导出 ====================

__all__ = [
    'SHARED_LAWYER_INTRO',
    'SHARED_INTRO',
    'SHARED_FORMAT_REQUIREMENTS',
    'SHARED_ANSWER_FORMAT',
    'SHARED_DISCLAIMER',
    'SHARED_SERVICE_PHILOSOPHY',
    'CHAT_HISTORY_PLACEHOLDER',
    'create_base_lawyer_prompt',
    'create_simple_lawyer_prompt',
    'create_skill_prompt',
]
