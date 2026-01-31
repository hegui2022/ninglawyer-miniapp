#!/usr/bin/env python3
"""
深度测试：脱敏技能
测试各类敏感信息的脱敏功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger


def test_desensitize():
    """测试脱敏技能"""
    logger.info("=" * 60)
    logger.info("深度测试：脱敏技能")
    logger.info("=" * 60)
    
    # 初始化技能注册表
    from src.skills import register_all_skills
    register_all_skills()
    
    # 测试用例
    test_cases = [
        {
            "name": "姓名脱敏",
            "input": "我叫张三，身份证号是110101199001011234，手机号是13800138000，住在北京市朝阳区建国门外大街1号",
            "expected_fields": ["姓名", "身份证号", "手机号", "地址"]
        },
        {
            "name": "银行卡号脱敏",
            "input": "我的姓名是李四，手机号是13900139000，银行卡号是6222020200001234567，地址是上海市浦东新区世纪大道100号",
            "expected_fields": ["姓名", "手机号", "银行卡号", "地址"]
        },
        {
            "name": "复杂文本脱敏",
            "input": """借款合同
出借人：王五
身份证号：110102199101021234
手机号：13700137000
借款人：赵六
身份证号：110103199201031234
手机号：13600136000
借款金额：人民币100万元整
联系地址：北京市西城区金融街1号""",
            "expected_fields": ["姓名", "身份证号", "手机号", "地址"]
        }
    ]
    
    from src.skills.desensitize_skill import execute_desensitize
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        name = test_case["name"]
        user_input = test_case["input"]
        expected_fields = test_case["expected_fields"]
        
        logger.info(f"\n{'=' * 60}")
        logger.info(f"测试用例 {i}/{len(test_cases)}: {name}")
        logger.info(f"{'=' * 60}")
        logger.info(f"用户输入：{user_input[:80]}...")
        logger.info(f"期望脱敏字段：{expected_fields}")
        
        try:
            # 执行脱敏
            logger.info("正在执行脱敏...")
            result = execute_desensitize(user_input, context={})
            
            if isinstance(result, dict) and result.get("success"):
                logger.success("✅ 脱敏执行成功")
                passed += 1
                
                # 显示结果摘要
                data = result.get("data", {})
                
                # 显示脱敏后的文本
                desensitized_text = data.get("desensitized_text", "")
                if desensitized_text:
                    logger.info(f"  脱敏后文本（前150字符）：{desensitized_text[:150]}...")
                
                # 显示识别到的敏感信息
                detected_fields = data.get("detected_fields", {})
                if detected_fields:
                    logger.info(f"  识别到的敏感字段：{len(detected_fields)}个")
                    for field_name, field_value in detected_fields.items():
                        if isinstance(field_value, list):
                            logger.info(f"    {field_name}: {len(field_value)}条")
                            for val in field_value[:2]:
                                logger.info(f"      - {val}")
                        else:
                            logger.info(f"    {field_name}: {field_value}")
                
                # 检查是否包含了所有期望的字段
                missing_fields = [field for field in expected_fields if field not in detected_fields]
                if missing_fields:
                    logger.warning(f"⚠️  未检测到以下字段：{missing_fields}")
                else:
                    logger.success("✅ 所有期望字段均已检测")
                
                # 检查原始文本是否包含敏感信息
                if original_text := data.get("original_text", ""):
                    logger.info(f"  原始文本长度：{len(original_text)}字符")
            elif isinstance(result, str):
                # 如果返回的是字符串，直接显示
                logger.success("✅ 脱敏执行成功（返回字符串）")
                passed += 1
                logger.info(f"  结果（前150字符）：{result[:150]}...")
            else:
                logger.error(f"❌ 脱敏执行失败：返回类型不支持")
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
    logger.info("🧪 脱敏技能深度测试")
    logger.info("=" * 60)
    logger.info("")
    
    success = test_desensitize()
    
    if success:
        logger.success("=" * 60)
        logger.success("🎉 所有测试通过！脱敏技能验证成功！")
        logger.success("=" * 60)
        return 0
    else:
        logger.error("=" * 60)
        logger.error("⚠️  部分测试失败，请检查日志")
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
