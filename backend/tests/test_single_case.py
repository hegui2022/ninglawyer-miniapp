"""
快速测试单个用例
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from loguru import logger
from src.agents.master_brain import master_brain
from src.utils.skill_registry import skill_registry
from src.skills import register_all_skills

# 配置日志
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")

# 注册所有技能
register_all_skills()

# 测试单个用例
test_input = "我们家房产和存款怎么分？"
expected_skill = "property_division"
expected_scenario = "family_law"

logger.info(f"📝 输入: {test_input}")
logger.info(f"🎯 期望技能: {expected_skill}")
logger.info(f"🏷️  期望场景: {expected_scenario}")

# 调用主脑
result = master_brain.route(
    user_input=test_input,
    user_id=1001,
    context={}
)

logger.info(f"📊 实际结果:")
logger.info(f"   - success: {result.get('success')}")
logger.info(f"   - skill_used: {result.get('skill_used')}")
logger.info(f"   - scenario_used: {result.get('scenario_used')}")
logger.info(f"   - personality_used: {result.get('personality_used')}")

if 'reply' in result:
    logger.info(f"   - reply: {result['reply'][:100]}...")

if 'error' in result:
    logger.warning(f"   - error: {result['error']}")

# 验证结果
is_success = result.get('success', False)
actual_skill = result.get('skill_used')
actual_scenario = result.get('scenario_used')

if is_success and actual_skill == expected_skill and actual_scenario == expected_scenario:
    logger.info(f"✅ 测试通过")
else:
    logger.warning(f"❌ 测试失败")
    if not is_success:
        logger.warning(f"   原因: success 为 False")
    if actual_skill != expected_skill:
        logger.warning(f"   原因: 技能不匹配 (期望: {expected_skill}, 实际: {actual_skill})")
    if actual_scenario != expected_scenario:
        logger.warning(f"   原因: 场景不匹配 (期望: {expected_scenario}, 实际: {actual_scenario})")
