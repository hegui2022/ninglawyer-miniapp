"""
律师提示词模块
"""

from src.prompts.lawyers.civil import CIVIL_LAWYER_TEMPLATE
from src.prompts.lawyers.criminal import CRIMINAL_LAWYER_TEMPLATE
from src.prompts.lawyers.contract import CONTRACT_LAWYER_TEMPLATE
from src.prompts.lawyers.labor import LABOR_LAWYER_TEMPLATE
from src.prompts.lawyers.company import COMPANY_LAWYER_TEMPLATE
from src.prompts.lawyers.ip import IP_LAWYER_TEMPLATE
from src.prompts.lawyers.marriage import MARRIAGE_LAWYER_TEMPLATE

__all__ = [
    'CIVIL_LAWYER_TEMPLATE',
    'CRIMINAL_LAWYER_TEMPLATE',
    'CONTRACT_LAWYER_TEMPLATE',
    'LABOR_LAWYER_TEMPLATE',
    'COMPANY_LAWYER_TEMPLATE',
    'IP_LAWYER_TEMPLATE',
    'MARRIAGE_LAWYER_TEMPLATE',
]
