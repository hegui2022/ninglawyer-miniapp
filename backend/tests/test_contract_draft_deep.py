#!/usr/bin/env python3
"""
深度测试：合同起草技能
测试各类合同的起草功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger


def test_contract_draft():
    """测试合同起草技能"""
    logger.info("=" * 60)
    logger.info("深度测试：合同起草技能")
    logger.info("=" * 60)
    
    # 初始化技能注册表
    from src.skills import register_all_skills
    register_all_skills()
    
    # 测试用例
    test_cases = [
        {
            "name": "借款合同起草",
            "input": "帮我起草一份借款合同，借款人张三向出借人李四借款10万元，期限1年，年利率5%，到期一次性还本付息",
            "expected_type": "借款合同"
        },
        {
            "name": "租赁合同起草",
            "input": "起草一份房屋租赁合同，出租方王五将一套两居室出租给承租方赵六，月租金3000元，押一付三，租期1年",
            "expected_type": "租赁合同"
        },
        {
            "name": "劳动合同起草",
            "input": "帮我写一份劳动合同，公司A录用员工B为软件开发工程师，月薪15000元，试用期3个月，五险一金",
            "expected_type": "劳动合同"
        }
    ]
    
    from src.skills.contract_skill import execute_contract
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        name = test_case["name"]
        user_input = test_case["input"]
        expected_type = test_case["expected_type"]
        
        logger.info(f"\n{'=' * 60}")
        logger.info(f"测试用例 {i}/{len(test_cases)}: {name}")
        logger.info(f"{'=' * 60}")
        logger.info(f"用户输入：{user_input}")
        logger.info(f"期望类型：{expected_type}")
        
        try:
            # 执行合同起草
            logger.info("正在执行合同起草...")
            result = execute_contract(user_input, context={})
            
            if result.get("success"):
                logger.success("✅ 合同起草执行成功")
                passed += 1
                
                # 显示结果摘要
                data = result.get("data", {})
                if isinstance(data, dict):
                    contract_type = data.get("contract_type", "未知")
                    logger.info(f"  合同类型：{contract_type}")
                    
                    if contract_type == expected_type:
                        logger.success("✅ 合同类型正确")
                    else:
                        logger.warning(f"⚠️  合同类型不匹配：期望{expected_type}，实际{contract_type}")
                    
                    # 显示合同片段
                    contract = data.get("contract", "")
                    if contract:
                        logger.info(f"  合同内容（前200字符）：{contract[:200]}...")
                    
                    # 显示关键要点
                    key_points = data.get("key_points", [])
                    if key_points:
                        logger.info(f"  关键要点：{len(key_points)}条")
                        for point in key_points[:3]:
                            logger.info(f"    - {point[:80]}...")
                    
                    # 显示风险提示
                    risks = data.get("risks", [])
                    if risks:
                        logger.info(f"  风险提示：{len(risks)}条")
                        for risk in risks[:2]:
                            logger.info(f"    - {risk[:80]}...")
            else:
                logger.error(f"❌ 合同起草执行失败：{result.get('error')}")
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
    """主函数"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("🧪 合同起草技能深度测试")
    logger.info("=" * 60)
    logger.info("")
    
    success = test_contract_draft()
    
    if success:
        logger.success("=" * 60)
        logger.success("🎉 所有测试通过！合同起草技能验证成功！")
        logger.success("=" * 60)
        return 0
    else:
        logger.error("=" * 60)
        logger.error("⚠️  部分测试失败，请检查日志")
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
