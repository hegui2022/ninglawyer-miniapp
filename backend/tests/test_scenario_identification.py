"""
测试场景识别逻辑
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents.master_brain import master_brain

# 测试用例
test_cases = [
    "我想离婚，需要什么材料？",
    "我们家房产和存款怎么分？",
    "孩子抚养权怎么判？",
    "老公经常打我，我该怎么办？",
    "帮我起草一份房屋租赁合同",
    "请审查这份合同的风险",
    "帮我脱敏这段文字：张三和李四是夫妻",
    "一般民事纠纷怎么处理？"
]

for test_input in test_cases:
    scenario = master_brain._identify_scenario(test_input)
    print(f"输入: {test_input}")
    print(f"场景: {scenario}")
    print(f"关键词: {master_brain.scenario_keywords.get(scenario, [])}")
    print("-" * 60)
