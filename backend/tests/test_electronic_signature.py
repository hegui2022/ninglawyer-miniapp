#!/usr/bin/env python3
"""
测试：电子签名技能
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from src.skills import register_all_skills
from src.skills.electronic_signature_skill import execute_electronic_signature


def test_electronic_signature():
    """测试电子签名技能"""
    logger.info("=" * 60)
    logger.info("测试：电子签名技能")
    logger.info("=" * 60)
    
    register_all_skills()
    
    test_cases = [
        {
            "name": "签署合同",
            "input": "我要签署借款合同，我是甲方张三"
        },
        {
            "name": "签名指导",
            "input": "电子签名的流程是什么？需要注意什么？"
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
            logger.info("正在处理签名请求...")
            result = execute_electronic_signature(user_input, context={})
            
            if isinstance(result, dict) and result.get("success"):
                logger.success("✅ 电子签名执行成功")
                passed += 1
                
                data = result.get("data", {})
                message = result.get("message", "")
                
                if message:
                    logger.info(f"  提示信息：{message}")
                
                # 显示签名信息
                if "signature_id" in data:
                    logger.info(f"  签名ID：{data['signature_id']}")
                    logger.info(f"  签名状态：{data.get('status', '未知')}")
                    logger.info(f"  法律效力：{data.get('legal_validity', '未知')}")
                
                # 显示指导信息
                if "steps" in data:
                    steps = data.get("steps", [])
                    logger.info(f"  操作步骤：{len(steps)}步")
                    for step in steps[:3]:
                        logger.info(f"    - {step}")
            else:
                logger.error(f"❌ 电子签名执行失败：{result.get('error')}")
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
    success = test_electronic_signature()
    
    if success:
        logger.success("🎉 电子签名技能验证成功！")
        return 0
    else:
        logger.error("⚠️ 电子签名技能验证失败")
        return 1


if __name__ == "__main__":
    exit(main())
