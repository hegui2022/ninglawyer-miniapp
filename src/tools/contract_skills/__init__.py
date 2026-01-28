"""
合同起草技能库
Contract Drafting Skills Library
"""

from .basic_info_skill import basic_info_skill
from .contract_term_skill import contract_term_skill
from .work_content_skill import work_content_skill
from .salary_skill import salary_skill
from .termination_skill import termination_skill
from .additional_clauses import (
    ConfidentialityClause,
    NonCompeteClause,
    IntellectualPropertyClause,
    CustomClause,
    AdditionalClausesManager,
)

__all__ = [
    "basic_info_skill",
    "contract_term_skill",
    "work_content_skill",
    "salary_skill",
    "termination_skill",
    "ConfidentialityClause",
    "NonCompeteClause",
    "IntellectualPropertyClause",
    "CustomClause",
    "AdditionalClausesManager",
]
