#!/usr/bin/env python3
"""
深度测试：合同审查技能
测试各类合同的审查功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger


def test_contract_review():
    """测试合同审查技能"""
    logger.info("=" * 60)
    logger.info("深度测试：合同审查技能")
    logger.info("=" * 60)
    
    # 初始化技能注册表
    from src.skills import register_all_skills
    register_all_skills()
    
    # 测试用例
    test_cases = [
        {
            "name": "借款合同审查",
            "input": """请审查这份借款合同：

借款合同
出借人：张三
借款人：李四
借款金额：人民币十万元整
借款期限：自2024年1月1日起至2025年1月1日止
还款方式：到期一次性还本付息
借款利息：年利率24%

双方签字：
出借人：张三
借款人：李四
日期：2024年1月1日""",
            "expected_type": "借款合同"
        },
        {
            "name": "租赁合同审查",
            "input": """帮我看看这份租赁合同有什么风险：

房屋租赁合同
出租方：王五
承租方：赵六
租赁标的：北京市朝阳区XX小区XX号楼XX室（两居室）
租赁期限：自2024年1月1日起至2024年12月31日止
月租金：人民币3000元
付款方式：押一付三
其他约定：承租方不得转租，不得养宠物

双方签字：
出租方：王五
承租方：赵六
日期：2024年1月1日""",
            "expected_type": "租赁合同"
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
        logger.info(f"用户输入：{user_input[:100]}...")
        logger.info(f"期望类型：{expected_type}")
        
        try:
            # 执行合同审查
            logger.info("正在执行合同审查...")
            result = execute_contract(user_input, context={})
            
            if result.get("success"):
                logger.success("✅ 合同审查执行成功")
                passed += 1
                
                # 显示结果摘要
                data = result.get("data", {})
                if isinstance(data, dict):
                    contract_type = data.get("contract_type", "未知")
                    logger.info(f"  合同类型：{contract_type}")
                    
                    if contract_type == expected_type or expected_type in contract_type:
                        logger.success("✅ 合同类型正确")
                    else:
                        logger.warning(f"⚠️  合同类型不匹配：期望{expected_type}，实际{contract_type}")
                    
                    # 显示分析
                    analysis = data.get("analysis", "")
                    if analysis:
                        logger.info(f"  合同分析（前150字符）：{analysis[:150]}...")
                    
                    # 显示风险
                    risks = data.get("risks", [])
                    if risks:
                        logger.info(f"  发现风险：{len(risks)}条")
                        for risk in risks[:3]:
                            if isinstance(risk, dict):
                                level = risk.get("level", "未知")
                                content = risk.get("content", "")
                                logger.info(f"    [{level}] {content[:80]}...")
                            else:
                                logger.info(f"    - {risk[:80]}...")
                    
                    # 显示风险评分
                    score = data.get("score")
                    if score is not None:
                        logger.info(f"  风险评分：{score}/100")
                    
                    # 显示完善建议
                    suggestions = data.get("suggestions", [])
                    if suggestions:
                        logger.info(f"  完善建议：{len(suggestions)}条")
                        for suggestion in suggestions[:2]:
                            logger.info(f"    - {suggestion[:80]}...")
            else:
                logger.error(f"❌ 合同审查执行失败：{result.get('error')}")
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
    logger.info("🧪 合同审查技能深度测试")
    logger.info("=" * 60)
    logger.info("")
    
    success = test_contract_review()
    
    if success:
        logger.success("=" * 60)
        logger.success("🎉 所有测试通过！合同审查技能验证成功！")
        logger.success("=" * 60)
        return 0
    else:
        logger.error("=" * 60)
        logger.error("⚠️  部分测试失败，请检查日志")
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
