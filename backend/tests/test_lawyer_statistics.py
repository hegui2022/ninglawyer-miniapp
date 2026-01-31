#!/usr/bin/env python3
"""
测试：律师统计技能
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from src.skills import register_all_skills
from src.skills.lawyer_statistics_skill import execute_lawyer_statistics


def test_lawyer_statistics():
    """测试律师统计技能"""
    logger.info("=" * 60)
    logger.info("测试：律师统计技能")
    logger.info("=" * 60)
    
    register_all_skills()
    
    test_cases = [
        {
            "name": "案件统计",
            "input": "统计我的案件数量和类型分布"
        },
        {
            "name": "业绩统计",
            "input": "统计我的业绩和收入情况"
        },
        {
            "name": "胜诉率统计",
            "input": "统计我的胜诉率和败诉率"
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        name = test_case["name"]
        user_input = test_case["input"]
        
        logger.info(f"\n{'=' * 60}")
        logger.info(f"测试用例 {i}/{len(test_cases)}: {name}")
        logger.info(f"{'=' * 60}")
        logger.info(f"用户输入：{user_input}")
        
        try:
            logger.info("正在执行统计...")
            result = execute_lawyer_statistics(user_input, context={})
            
            if isinstance(result, dict) and result.get("success"):
                logger.success("✅ 律师统计执行成功")
                passed += 1
                
                data = result.get("data", {})
                message = result.get("message", "")
                
                if message:
                    logger.info(f"  提示信息：{message}")
                
                # 显示关键统计数据
                if "total_cases" in data:
                    logger.info(f"  案件总数：{data['total_cases']}")
                if "total_income" in data:
                    logger.info(f"  总收入：{data['total_income']}元")
                if "win_rate" in data:
                    logger.info(f"  胜诉率：{data['win_rate']}")
                if "by_type" in data:
                    logger.info(f"  案件类型分布：{data['by_type']}")
            else:
                logger.error(f"❌ 律师统计执行失败：{result.get('error')}")
                failed += 1
        
        except Exception as e:
            logger.error(f"❌ 测试失败：{e}")
            import traceback
            logger.error(traceback.format_exc())
            failed += 1
    
    logger.info(f"\n{'=' * 60}")
    logger.info(f"测试结果汇总")
    logger.info(f"{'=' * 60}")
    logger.info(f"通过：{passed}/{len(test_cases)}")
    logger.info(f"失败：{failed}/{len(test_cases)}")
    
    return failed == 0


def main():
    success = test_lawyer_statistics()
    
    if success:
        logger.success("🎉 律师统计技能验证成功！")
        return 0
    else:
        logger.error("⚠️ 律师统计技能验证失败")
        return 1


if __name__ == "__main__":
    exit(main())
