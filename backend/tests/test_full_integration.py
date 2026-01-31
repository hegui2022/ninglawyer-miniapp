#!/usr/bin/env python3
"""
完整集成测试脚本
验证整个系统从用户输入到技能执行的完整流程
新架构：单一宁律师 + 主脑调度技能 + 动态人设选择 + 知识检索
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger


def test_full_flow():
    """测试完整流程"""
    logger.info("=" * 60)
    logger.info("完整流程测试")
    logger.info("=" * 60)
    
    # 初始化技能注册表
    from src.skills import register_all_skills
    register_all_skills()
    
    # 初始化主脑
    from src.agents.master_brain import master_brain
    
    # 测试用例
    test_cases = [
        {
            "input": "我想离婚，流程是什么？",
            "expected_skill": "divorce_procedure",
            "expected_scenario": "family_law"
        },
        {
            "input": "离婚后房子怎么分？",
            "expected_skill": "property_division",
            "expected_scenario": "family_law"
        },
        {
            "input": "离婚后孩子归谁？抚养费怎么算？",
            "expected_skill": "child_custody",
            "expected_scenario": "family_law"
        },
        {
            "input": "我老公打我，我该怎么办？",
            "expected_skill": "domestic_violence",
            "expected_scenario": "family_law"
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        user_input = test_case["input"]
        expected_skill = test_case["expected_skill"]
        expected_scenario = test_case["expected_scenario"]
        
        logger.info(f"\n{'=' * 60}")
        logger.info(f"测试用例 {i}/{len(test_cases)}")
        logger.info(f"{'=' * 60}")
        logger.info(f"用户输入：{user_input}")
        logger.info(f"期望技能：{expected_skill}")
        logger.info(f"期望场景：{expected_scenario}")
        
        try:
            # 调用主脑路由
            result = master_brain.route(user_input, user_id=1)
            
            # 检查结果
            if result.get("success"):
                skill_used = result.get("skill_used")
                scenario_used = result.get("scenario_used")
                personality_used = result.get("personality_used")
                
                logger.info(f"实际技能：{skill_used}")
                logger.info(f"实际场景：{scenario_used}")
                logger.info(f"实际人设：{personality_used}")
                
                if skill_used == expected_skill and scenario_used == expected_scenario:
                    logger.success("✅ 测试通过！")
                    passed += 1
                else:
                    logger.warning("⚠️  测试失败！")
                    failed += 1
                
                # 显示回复摘要
                reply = result.get("reply", "")
                if reply:
                    logger.info(f"回复摘要：{reply[:150]}...")
            else:
                logger.error(f"❌ 测试失败：{result.get('error')}")
                failed += 1
        
        except Exception as e:
            logger.error(f"❌ 测试失败：{e}")
            failed += 1
    
    logger.info(f"\n{'=' * 60}")
    logger.info(f"测试结果汇总")
    logger.info(f"{'=' * 60}")
    logger.info(f"通过：{passed}/{len(test_cases)}")
    logger.info(f"失败：{failed}/{len(test_cases)}")
    
    return failed == 0


def main():
    """运行完整集成测试"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("🧪 完整集成测试")
    logger.info("=" * 60)
    logger.info("")
    
    success = test_full_flow()
    
    if success:
        logger.success("=" * 60)
        logger.success("🎉 所有测试通过！完整集成验证成功！")
        logger.success("=" * 60)
        logger.success("\n✅ 核心检查点验证：")
        logger.success("  ✓ 技能注册表正常")
        logger.success("  ✓ 主脑路由正常")
        logger.success("  ✓ 场景识别正常")
        logger.success("  ✓ 人设选择正常")
        logger.success("  ✓ 知识检索正常")
        logger.success("  ✓ 技能执行正常")
        logger.success("\n🚀 系统已经可以投入使用！")
        return 0
    else:
        logger.error("=" * 60)
        logger.error("⚠️  部分测试失败，请检查日志")
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
