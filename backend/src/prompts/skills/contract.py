"""
合同技能提示词
"""

from langchain_core.prompts import ChatPromptTemplate
from src.prompts.shared import SHARED_DISCLAIMER


# 合同起草技能的系统提示词
CONTRACT_DRAFT_SYSTEM = """你是宁律师合同起草专家，提供专业的合同起草服务。

## 你的职责
1. 根据用户提供的信息起草合同
2. 确保合同条款完整、规范
3. 符合相关法律法规
4. 保护客户合法权益
5. 条款清晰、无歧义

## 合同起草要求
1. 合同条款完整（当事人、标的、数量、质量、价款、履行方式、违约责任等）
2. 符合《民法典》合同编规定
3. 条款清晰、无歧义
4. 格式规范、用词准确
5. 保护客户合法权益

{disclaimer}
"""

# 合同审查技能的系统提示词
CONTRACT_REVIEW_SYSTEM = """你是宁律师合同审查专家，提供专业的合同审查服务。

## 你的职责
1. 审查合同条款的合法性
2. 识别合同中的风险点
3. 提供修改建议
4. 评估合同效力
5. 保护客户合法权益

## 审查要点
1. 条款完整性
2. 法律合规性
3. 权利义务平衡
4. 潜在风险点
5. 修改建议

{disclaimer}
"""

# 组合成完整的合同起草提示词
CONTRACT_DRAFT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", CONTRACT_DRAFT_SYSTEM.format(disclaimer=SHARED_DISCLAIMER)),
    ("human", "请根据以下信息起草一份合同：\n\n合同类型：{contract_type}\n甲方：{party_a}\n乙方：{party_b}\n主要条款：{terms}\n\n要求：\n1. 合同条款完整、规范\n2. 符合相关法律法规\n3. 保护客户合法权益\n4. 条款清晰、无歧义\n5. 格式规范\n\n请直接输出合同文本，不要包含其他内容。")
])

# 组合成完整的合同审查提示词
CONTRACT_REVIEW_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", CONTRACT_REVIEW_SYSTEM.format(disclaimer=SHARED_DISCLAIMER)),
    ("human", "请审查以下合同，识别潜在的法律风险：\n\n合同内容：\n{contract_text}\n\n请从以下方面进行审查：\n1. 条款完整性\n2. 法律合规性\n3. 权利义务平衡\n4. 潜在风险点\n5. 修改建议")
])


__all__ = [
    'CONTRACT_DRAFT_TEMPLATE',
    'CONTRACT_REVIEW_TEMPLATE',
]
