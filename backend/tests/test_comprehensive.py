#!/usr/bin/env python3
"""
综合测试脚本
测试所有技能和系统功能
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from src.skills import register_all_skills
from src.utils.skill_registry import skill_registry


def test_all_skills():
    """测试所有技能注册"""
    logger.info("=" * 60)
    logger.info("测试1：所有技能注册")
    logger.info("=" * 60)
    
    register_all_skills()
    
    skills = skill_registry.list_skills()
    logger.info(f"已注册技能数量：{len(skills)}")
    
    for name, skill in skills.items():
        category = skill.get("category", "未分类")
        description = skill.get("description", "")
        logger.success(f"✅ {name} [{category}]")
    
    return len(skills) > 0


def test_skill_execution():
    """测试技能执行"""
    logger.info("\n" + "=" * 60)
    logger.info("测试2：技能执行")
    logger.info("=" * 60)
    
    test_cases = [
        {
            "skill": "civil_consult",
            "input": "朋友借钱不还怎么办？"
        },
        {
            "skill": "contract_draft",
            "input": "起草一份借款合同"
        },
        {
            "skill": "desensitize",
            "input": "我叫张三，身份证号110101199001011234"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        skill_name = test_case["skill"]
        user_input = test_case["input"]
        
        logger.info(f"\n测试技能：{skill_name}")
        logger.info(f"输入：{user_input}")
        
        try:
            result = skill_registry.execute(skill_name, user_input, {})
            
            if isinstance(result, dict) and result.get("success"):
                logger.success(f"✅ {skill_name} 执行成功")
                passed += 1
            elif isinstance(result, str) and len(result) > 0:
                logger.success(f"✅ {skill_name} 执行成功（返回字符串）")
                passed += 1
            else:
                logger.error(f"❌ {skill_name} 执行失败：返回结果为空")
                failed += 1
        
        except Exception as e:
            logger.error(f"❌ {skill_name} 执行异常：{e}")
            failed += 1
    
    logger.info(f"\n通过：{passed}/{len(test_cases)}")
    logger.info(f"失败：{failed}/{len(test_cases)}")
    
    return failed == 0


def test_master_brain():
    """测试主脑"""
    logger.info("\n" + "=" * 60)
    logger.info("测试3：主脑路由")
    logger.info("=" * 60)
    
    from src.agents.master_brain import MasterBrain
    
    master_brain = MasterBrain()
    
    test_inputs = [
        "朋友借钱不还怎么办？",
        "帮我起草一份合同",
        "我想离婚，流程是什么？"
    ]
    
    passed = 0
    failed = 0
    
    for user_input in test_inputs:
        logger.info(f"\n输入：{user_input}")
        
        try:
            result = master_brain.route(user_input, user_id=1001)
            
            if result.get("success"):
                logger.success(f"✅ 路由成功")
                logger.info(f"  技能：{result.get('skill_used', '未知')}")
                logger.info(f"  人设：{result.get('personality_used', '未知')}")
                logger.info(f"  场景：{result.get('scenario_used', 'unknown')}")
                passed += 1
            else:
                logger.error(f"❌ 路由失败：{result.get('error')}")
                failed += 1
        
        except Exception as e:
            logger.error(f"❌ 路由异常：{e}")
            failed += 1
    
    logger.info(f"\n通过：{passed}/{len(test_inputs)}")
    logger.info(f"失败：{failed}/{len(test_inputs)}")
    
    return failed == 0


def test_prompt_manager():
    """测试提示词管理器"""
    logger.info("\n" + "=" * 60)
    logger.info("测试4：提示词管理器")
    logger.info("=" * 60)
    
    from src.prompts.manager import PromptManager
    
    skills = PromptManager.list_skills()
    
    logger.info(f"提示词数量：{len(skills)}")
    
    for skill_name in skills:
        prompt = PromptManager.get_skill_prompt(skill_name)
        if prompt:
            logger.success(f"✅ {skill_name} 提示词加载成功")
        else:
            logger.error(f"❌ {skill_name} 提示词加载失败")
    
    return len(skills) > 0


def main():
    """主函数"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("🧪 综合测试")
    logger.info("=" * 60)
    logger.info("")
    
    results = []
    
    # 测试1：技能注册
    results.append(("技能注册", test_all_skills()))
    
    # 测试2：技能执行
    results.append(("技能执行", test_skill_execution()))
    
    # 测试3：主脑路由
    results.append(("主脑路由", test_master_brain()))
    
    # 测试4：提示词管理
    results.append(("提示词管理", test_prompt_manager()))
    
    # 汇总
    logger.info("\n" + "=" * 60)
    logger.info("测试汇总")
    logger.info("=" * 60)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        logger.info(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        logger.success("\n🎉 所有测试通过！")
        return 0
    else:
        logger.error("\n⚠️ 部分测试失败")
        return 1


if __name__ == "__main__":
    exit(main())
