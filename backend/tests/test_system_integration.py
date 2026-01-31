"""
完整系统集成测试
测试主脑路由和技能集成
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


def test_system_integration():
    """测试完整系统集成"""
    
    # 1. 注册所有技能
    logger.info("=" * 60)
    logger.info("📋 步骤1: 注册所有技能")
    logger.info("=" * 60)
    register_all_skills()
    
    # 列出已注册的技能
    all_skills = skill_registry.list_skills()
    logger.info(f"✅ 已注册 {len(all_skills)} 个技能：")
    for skill_name, skill_info in all_skills.items():
        logger.info(f"   - {skill_name}: {skill_info['description']}")
    
    # 2. 测试路由逻辑
    logger.info("\n" + "=" * 60)
    logger.info("🧠 步骤2: 测试主脑路由逻辑")
    logger.info("=" * 60)
    
    test_cases = [
        {
            "input": "我想离婚，需要什么材料？",
            "expected_skill": "divorce_procedure",
            "expected_scenario": "family_law",
            "description": "离婚流程咨询"
        },
        {
            "input": "我们家房产和存款怎么分？",
            "expected_skill": "property_division",
            "expected_scenario": "family_law",
            "description": "财产分割咨询"
        },
        {
            "input": "孩子抚养权怎么判？",
            "expected_skill": "child_custody",
            "expected_scenario": "family_law",
            "description": "子女抚养咨询"
        },
        {
            "input": "老公经常打我，我该怎么办？",
            "expected_skill": "domestic_violence",
            "expected_scenario": "family_law",
            "description": "家暴维权咨询"
        },
        {
            "input": "帮我起草一份房屋租赁合同",
            "expected_skill": "contract_draft",
            "expected_scenario": "commercial",
            "description": "合同起草"
        },
        {
            "input": "请审查这份合同的风险",
            "expected_skill": "contract_review",
            "expected_scenario": "commercial",
            "description": "合同审查"
        },
        {
            "input": "帮我脱敏这段文字：张三和李四是夫妻",
            "expected_skill": "desensitize",
            "expected_scenario": "general",
            "description": "文本脱敏"
        },
        {
            "input": "一般民事纠纷怎么处理？",
            "expected_skill": "civil_consult",
            "expected_scenario": "general",
            "description": "通用法律咨询"
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n{'=' * 60}")
        logger.info(f"测试用例 {i}/{len(test_cases)}: {test_case['description']}")
        logger.info(f"{'=' * 60}")
        logger.info(f"📝 输入: {test_case['input']}")
        logger.info(f"🎯 期望技能: {test_case['expected_skill']}")
        logger.info(f"🏷️  期望场景: {test_case['expected_scenario']}")
        
        try:
            # 调用主脑
            result = master_brain.route(
                user_input=test_case["input"],
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
            
            if is_success and actual_skill == test_case['expected_skill'] and actual_scenario == test_case['expected_scenario']:
                logger.info(f"✅ 测试通过")
                passed += 1
            else:
                logger.warning(f"❌ 测试失败")
                if not is_success:
                    logger.warning(f"   原因: success 为 False")
                if actual_skill != test_case['expected_skill']:
                    logger.warning(f"   原因: 技能不匹配 (期望: {test_case['expected_skill']}, 实际: {actual_skill})")
                if actual_scenario != test_case['expected_scenario']:
                    logger.warning(f"   原因: 场景不匹配 (期望: {test_case['expected_scenario']}, 实际: {actual_scenario})")
                failed += 1
        
        except Exception as e:
            logger.error(f"❌ 测试异常: {e}")
            failed += 1
    
    # 3. 输出测试总结
    logger.info("\n" + "=" * 60)
    logger.info("📊 测试总结")
    logger.info("=" * 60)
    logger.info(f"✅ 通过: {passed}/{len(test_cases)}")
    logger.info(f"❌ 失败: {failed}/{len(test_cases)}")
    
    if failed == 0:
        logger.info("🎉 所有测试通过！")
        return True
    else:
        logger.warning(f"⚠️  有 {failed} 个测试失败")
        return False


if __name__ == "__main__":
    success = test_system_integration()
    sys.exit(0 if success else 1)
