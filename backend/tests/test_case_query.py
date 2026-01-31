#!/usr/bin/env python3
"""
测试：案例查询技能
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from src.skills import register_all_skills
from src.skills.case_query_skill import execute_case_query


def test_case_query():
    """测试案例查询技能"""
    logger.info("=" * 60)
    logger.info("测试：案例查询技能")
    logger.info("=" * 60)
    
    register_all_skills()
    
    test_cases = [
        {
            "name": "借款纠纷案例",
            "input": "朋友借了我5万块钱不还，我想知道类似案件一般是怎么判的？"
        },
        {
            "name": "离婚财产分割案例",
            "input": "婚前买的房子，婚后一起还贷款，离婚时怎么分？有没有类似的判决案例？"
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
            logger.info("正在查询案例...")
            result = execute_case_query(user_input, context={})
            
            if isinstance(result, str) and len(result) > 0:
                logger.success("✅ 案例查询执行成功")
                passed += 1
                logger.info(f"  结果（前150字符）：{result[:150]}...")
            else:
                logger.error(f"❌ 案例查询返回结果为空")
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
    success = test_case_query()
    
    if success:
        logger.success("🎉 案例查询技能验证成功！")
        return 0
    else:
        logger.error("⚠️ 案例查询技能验证失败")
        return 1


if __name__ == "__main__":
    exit(main())
