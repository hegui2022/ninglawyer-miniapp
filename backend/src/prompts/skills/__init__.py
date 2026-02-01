"""
技能提示词模块
"""

from prompts.skills.civil_consult import CIVIL_CONSULT_TEMPLATE
from prompts.skills.contract import CONTRACT_DRAFT_TEMPLATE, CONTRACT_REVIEW_TEMPLATE
from prompts.skills.desensitize import DESENSITIZE_TEMPLATE
from prompts.skills.master_brain import MASTER_BRAIN_TEMPLATE

__all__ = [
    'CIVIL_CONSULT_TEMPLATE',
    'CONTRACT_DRAFT_TEMPLATE',
    'CONTRACT_REVIEW_TEMPLATE',
    'DESENSITIZE_TEMPLATE',
    'MASTER_BRAIN_TEMPLATE',
]
