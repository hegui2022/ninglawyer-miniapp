#!/usr/bin/env python3
"""
深度测试：民事咨询技能
测试各种民事纠纷场景
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger


def test_civil_consult():
    """测试民事咨询技能"""
    logger.info("=" * 60)
    logger.info("深度测试：民事咨询技能")
    logger.info("=" * 60)
    
    # 初始化技能注册表
    from src.skills import register_all_skills
    register_all_skills()
    
    # 测试用例
    test_cases = [
        {
            "name": "债务纠纷",
            "input": "朋友借了我5万块钱，现在不还，我该怎么办？",
            "expected_domain": "债务纠纷"
        },
        {
            "name": "婚姻家庭",
            "input": "我老公出轨，我想离婚，财产怎么分？",
            "expected_domain": "婚姻家庭"
        },
        {
            "name": "劳动争议",
            "input": "公司无故辞退我，没有给赔偿，我该怎么办？",
            "expected_domain": "劳动争议"
        },
        {
            "name": "侵权责任",
            "input": "邻居装修把我家楼下的防水打漏了，造成损失，我该怎么办？",
            "expected_domain": "侵权责任"
        },
        {
            "name": "合同纠纷",
            "input": "租房合同还没到期，房东就要赶我走，我该怎么办？",
            "expected_domain": "合同纠纷"
        },
        {
            "name": "房产纠纷",
            "input": "买的房子有质量问题，开发商不维修，我该怎么办？",
            "expected_domain": "房产纠纷"
        }
    ]
    
    from src.skills.civil_consult_skill import civil_consult_skill
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        name = test_case["name"]
        user_input = test_case["input"]
        expected_domain = test_case["expected_domain"]
        
        logger.info(f"\n{'=' * 60}")
        logger.info(f"测试用例 {i}/{len(test_cases)}: {name}")
        logger.info(f"{'=' * 60}")
        logger.info(f"用户输入：{user_input}")
        logger.info(f"期望领域：{expected_domain}")
        
        try:
            # 测试领域分类
            domain = civil_consult_skill.classify_domain(user_input)
            logger.info(f"分类结果：{domain}")
            
            if domain == expected_domain:
                logger.success("✅ 领域分类正确")
            else:
                logger.warning(f"⚠️  领域分类错误：期望{expected_domain}，实际{domain}")
            
            # 测试完整咨询
            logger.info("正在执行完整咨询...")
            result = civil_consult_skill.execute(user_input, context={})
            
            if result.get("success"):
                logger.success("✅ 咨询执行成功")
                passed += 1
                
                # 显示结果摘要
                data = result.get("data", {})
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, str):
                            logger.info(f"  {key}: {value[:100]}...")
                        else:
                            logger.info(f"  {key}: {value}")
                else:
                    logger.info(f"结果：{str(data)[:100]}...")
            else:
                logger.error(f"❌ 咨询执行失败：{result.get('error')}")
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
    """主函数"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("🧪 民事咨询技能深度测试")
    logger.info("=" * 60)
    logger.info("")
    
    success = test_civil_consult()
    
    if success:
        logger.success("=" * 60)
        logger.success("🎉 所有测试通过！民事咨询技能验证成功！")
        logger.success("=" * 60)
        return 0
    else:
        logger.error("=" * 60)
        logger.error("⚠️  部分测试失败，请检查日志")
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
