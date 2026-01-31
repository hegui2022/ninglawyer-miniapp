#!/usr/bin/env python3
"""
测试：风险等级评估技能
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from src.skills import register_all_skills
from src.skills.risk_assessment_skill import execute_risk_assessment


def test_risk_assessment():
    """测试风险等级评估技能"""
    logger.info("=" * 60)
    logger.info("测试：风险等级评估技能")
    logger.info("=" * 60)
    
    register_all_skills()
    
    test_input = """我要和一个陌生人借款20万元，没有抵押物，口头约定月息2%，三个月后还款，没有写借条，请问这个操作风险大吗？"""
    
    logger.info(f"测试输入：{test_input}")
    
    result = execute_risk_assessment(test_input, context={})
    
    if result.get("success"):
        logger.success("✅ 风险评估执行成功")
        data = result.get("data", {})
        
        overall_risk_level = data.get("overall_risk_level", "未知")
        risk_score = data.get("risk_score", 0)
        logger.info(f"  整体风险等级：{overall_risk_level}")
        logger.info(f"  风险评分：{risk_score}/100")
        
        summary = data.get("summary", "")
        if summary:
            logger.info(f"  评估总结：{summary[:100]}...")
        
        return True
    else:
        logger.error(f"❌ 风险评估执行失败：{result.get('error')}")
        return False


def main():
    success = test_risk_assessment()
    
    if success:
        logger.success("🎉 风险等级评估技能验证成功！")
        return 0
    else:
        logger.error("⚠️ 风险等级评估技能验证失败")
        return 1


if __name__ == "__main__":
    exit(main())
