"""
人设库 - 宁律师的多种人设
支持根据用户类型和场景动态选择不同人设，实现千人千面
"""

from .warm_personal import WARM_PERSONALITY
from .personality_selector import PersonalitySelector

__all__ = [
    'WARM_PERSONALITY',
    'PersonalitySelector',
]
