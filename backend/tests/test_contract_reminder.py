#!/usr/bin/env python3
"""
测试：合同提醒技能
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from src.skills import register_all_skills
from src.skills.contract_reminder_skill import execute_contract_reminder


def test_contract_reminder():
    """测试合同提醒技能"""
    logger.info("=" * 60)
    logger.info("测试：合同提醒技能")
    logger.info("=" * 60)
    
    register_all_skills()
    
    test_cases = [
        {
            "name": "设置到期提醒",
            "input": "我要设置一个合同到期提醒，合同是房屋租赁合同，2024年12月31日到期，请提前7天提醒我"
        },
        {
            "name": "查询提醒列表",
            "input": "查看我的所有合同提醒"
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
            logger.info("正在处理提醒请求...")
            result = execute_contract_reminder(user_input, context={})
            
            if isinstance(result, dict) and result.get("success"):
                logger.success("✅ 合同提醒执行成功")
                passed += 1
                
                data = result.get("data", {})
                message = result.get("message", "")
                
                if message:
                    logger.info(f"  提示信息：{message}")
                
                # 显示提醒信息
                if "reminder_id" in data:
                    logger.info(f"  提醒ID：{data['reminder_id']}")
                    logger.info(f"  合同名称：{data.get('contract_name', '未知')}")
                    logger.info(f"  提醒类型：{data.get('reminder_type', '未知')}")
                    logger.info(f"  提醒日期：{data.get('reminder_date', '未知')}")
                elif "reminders" in data:
                    reminders = data.get("reminders", [])
                    logger.info(f"  提醒数量：{len(reminders)}个")
                    for rem in reminders[:2]:
                        logger.info(f"    - {rem.get('contract_name', '未知')} ({rem.get('reminder_type', '未知')})")
            else:
                logger.error(f"❌ 合同提醒执行失败：{result.get('error')}")
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
    success = test_contract_reminder()
    
    if success:
        logger.success("🎉 合同提醒技能验证成功！")
        return 0
    else:
        logger.error("⚠️ 合同提醒技能验证失败")
        return 1


if __name__ == "__main__":
    exit(main())
