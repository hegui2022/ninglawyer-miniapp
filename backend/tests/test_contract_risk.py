#!/usr/bin/env python3
"""
测试：合同风险识别技能
测试合同风险识别功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger


def test_contract_risk():
    """测试合同风险识别技能"""
    logger.info("=" * 60)
    logger.info("测试：合同风险识别技能")
    logger.info("=" * 60)
    
    # 初始化技能注册表
    from src.skills import register_all_skills
    register_all_skills()
    
    # 测试用例
    test_cases = [
        {
            "name": "借款合同风险识别",
            "input": """借款合同
出借人：张三（身份证号：110101199001011234）
借款人：李四（身份证号：110102199002021234）
借款金额：人民币50万元整
借款期限：自2024年1月1日起至2025年1月1日止
借款利息：年利率30%
还款方式：到期一次性还本付息
担保方式：无担保

双方签字：
出借人：张三
借款人：李四
日期：2024年1月1日""",
        },
        {
            "name": "租赁合同风险识别",
            "input": """房屋租赁合同
出租方：王五
承租方：赵六
租赁标的：北京市朝阳区XX小区XX号楼XX室（两居室）
租赁期限：自2024年1月1日起至2024年12月31日止
月租金：人民币3000元
付款方式：押一付三
其他约定：
1. 承租方不得转租
2. 承租方不得养宠物
3. 房屋维修费用由承租方承担

双方签字：
出租方：王五
承租方：赵六
日期：2024年1月1日""",
        }
    ]
    
    from src.skills.contract_risk_skill import execute_contract_risk
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        name = test_case["name"]
        user_input = test_case["input"]
        
        logger.info(f"\n{'=' * 60}")
        logger.info(f"测试用例 {i}/{len(test_cases)}: {name}")
        logger.info(f"{'=' * 60}")
        
        try:
            # 执行风险识别
            logger.info("正在识别合同风险...")
            result = execute_contract_risk(user_input, context={})
            
            if result.get("success"):
                logger.success("✅ 风险识别执行成功")
                passed += 1
                
                # 显示结果摘要
                data = result.get("data", {})
                if isinstance(data, dict):
                    contract_type = data.get("contract_type", "未知")
                    overall_risk_level = data.get("overall_risk_level", "未知")
                    risk_score = data.get("risk_score", 0)
                    
                    logger.info(f"  合同类型：{contract_type}")
                    logger.info(f"  整体风险等级：{overall_risk_level}")
                    logger.info(f"  风险评分：{risk_score}/100")
                    
                    # 显示风险列表
                    risks = data.get("risks", [])
                    if risks:
                        logger.info(f"  识别到风险：{len(risks)}个")
                        for risk in risks[:5]:
                            risk_name = risk.get("risk_name", "未知")
                            risk_level = risk.get("risk_level", "未知")
                            risk_type = risk.get("risk_type", "未知")
                            logger.info(f"    [{risk_level}] {risk_name} ({risk_type})")
                    
                    # 显示缺失条款
                    missing_clauses = data.get("missing_clauses", [])
                    if missing_clauses:
                        logger.info(f"  缺失条款：{len(missing_clauses)}个")
                        for clause in missing_clauses:
                            logger.info(f"    - {clause}")
                    
                    # 显示总结
                    summary = data.get("summary", "")
                    if summary:
                        logger.info(f"  风险总结：{summary[:100]}...")
            else:
                logger.error(f"❌ 风险识别执行失败：{result.get('error')}")
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
    logger.info("🧪 合同风险识别技能测试")
    logger.info("=" * 60)
    logger.info("")
    
    success = test_contract_risk()
    
    if success:
        logger.success("=" * 60)
        logger.success("🎉 所有测试通过！合同风险识别技能验证成功！")
        logger.success("=" * 60)
        return 0
    else:
        logger.error("=" * 60)
        logger.error("⚠️  部分测试失败，请检查日志")
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
