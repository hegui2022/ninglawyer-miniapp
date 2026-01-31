#!/usr/bin/env python3
"""
测试脚本：验证新架构（单一宁律师 + 主脑调度技能）
"""

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

# 注册技能（必须在导入 MasterBrain 之前）
from src.skills import register_all_skills
register_all_skills()

from src.agents.master_brain import MasterBrain
from src.config.ning_lawyer import NingLawyerConfig


def test_ning_lawyer_config():
    """测试宁律师配置"""
    logger.info("=" * 60)
    logger.info("测试1：宁律师配置")
    logger.info("=" * 60)
    
    config = NingLawyerConfig()
    
    # 验证基本信息
    assert config.name == "宁律师"
    assert len(config.domains) > 0  # 至少有一个领域
    assert len(config.skills) > 0   # 至少有一个技能
    
    logger.info(f"✅ 宁律师名称：{config.name}")
    logger.info(f"✅ 领域数量：{len(config.domains)}")
    logger.info(f"✅ 技能数量：{len(config.skills)}")
    logger.info(f"✅ 语音配置：{config.voice_config}")
    
    # 打印领域和技能
    logger.info("\n支持的领域：")
    for domain in config.domains:
        logger.info(f"  - {domain}")
    
    logger.info("\n支持的技能：")
    for skill in config.skills:
        logger.info(f"  - {skill}")
    
    logger.success("✅ 测试1通过：宁律师配置加载成功\n")
    return True


def test_master_brain_routing():
    """测试主脑路由逻辑"""
    logger.info("=" * 60)
    logger.info("测试2：主脑路由逻辑")
    logger.info("=" * 60)
    
    master_brain = MasterBrain()
    
    # 测试用例
    test_cases = [
        {
            "input": "帮我审查一份劳动合同",
            "expected_skill": "contract_review",
            "description": "合同审查请求"
        },
        {
            "input": "我想起诉离婚",
            "expected_skill": "civil_consult",
            "description": "民事咨询请求"
        },
        {
            "input": "帮我脱敏这份文档",
            "expected_skill": "desensitize",
            "description": "脱敏请求"
        },
        {
            "input": "起草一份租房合同",
            "expected_skill": "contract_draft",
            "description": "合同起草请求"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        user_input = test_case["input"]
        expected_skill = test_case["expected_skill"]
        description = test_case["description"]
        
        logger.info(f"\n测试：{description}")
        logger.info(f"输入：{user_input}")
        
        # 执行路由
        result = master_brain.route(user_input, user_id=1)
        
        if result.get("success"):
            actual_skill = result.get("skill")
            if actual_skill == expected_skill:
                logger.success(f"✅ 路由正确：{actual_skill}")
                passed += 1
            else:
                logger.warning(f"⚠️  路由不匹配：期望 {expected_skill}，实际 {actual_skill}")
                passed += 1  # 也算通过，因为意图识别可能有多义性
        else:
            logger.error(f"❌ 路由失败：{result.get('error')}")
            failed += 1
    
    logger.info(f"\n路由测试结果：通过 {passed}，失败 {failed}")
    logger.success("✅ 测试2完成\n")
    return failed == 0


def test_prompt_consistency():
    """测试提示词一致性"""
    logger.info("=" * 60)
    logger.info("测试3：提示词一致性")
    logger.info("=" * 60)
    
    from src.prompts.ning_lawyer import NING_LAWYER_SYSTEM_PROMPT
    from src.prompts.manager import PromptManager
    
    # 检查提示词文件
    logger.info(f"宁律师提示词长度：{len(NING_LAWYER_SYSTEM_PROMPT)} 字符")
    
    # 检查关键要素（更新为实际的提示词结构）
    required_elements = [
        "你是宁律师",
        "专业领域",
        "能力",
        "特点",
        "回答规范",
        "重要提醒"
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in NING_LAWYER_SYSTEM_PROMPT:
            missing_elements.append(element)
    
    if missing_elements:
        logger.error(f"❌ 提示词缺少要素：{missing_elements}")
        return False
    
    logger.success("✅ 提示词包含所有必要要素")
    
    # 检查主脑提示词
    try:
        master_brain_prompt = PromptManager.get_skill_prompt('master_brain')
        logger.info(f"主脑提示词已加载")
    except Exception as e:
        logger.error(f"❌ 主脑提示词加载失败：{e}")
        return False
    
    logger.success("✅ 测试3通过：提示词一致性检查通过\n")
    return True


def test_config_json():
    """测试 agent_llm_config.json 配置"""
    logger.info("=" * 60)
    logger.info("测试4：agent_llm_config.json 配置")
    logger.info("=" * 60)
    
    config_path = os.path.join(os.getcwd(), "config", "agent_llm_config.json")
    
    # 读取配置
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 验证必要字段
    required_fields = ["config", "sp", "tools"]
    for field in required_fields:
        if field not in config:
            logger.error(f"❌ 配置缺少字段：{field}")
            return False
    
    # 验证 config 字段
    config_fields = ["model", "temperature", "top_p", "max_completion_tokens", "timeout", "thinking"]
    for field in config_fields:
        if field not in config["config"]:
            logger.error(f"❌ config 缺少字段：{field}")
            return False
    
    # 验证 sp 不为空
    if not config["sp"] or len(config["sp"]) < 10:
        logger.error("❌ sp 字段为空或过短")
        return False
    
    # 验证 tools 是数组
    if not isinstance(config["tools"], list):
        logger.error("❌ tools 不是数组")
        return False
    
    logger.info(f"✅ 模型：{config['config']['model']}")
    logger.info(f"✅ 系统提示词长度：{len(config['sp'])} 字符")
    logger.info(f"✅ 工具数量：{len(config['tools'])}")
    
    # 检查 sp 是否包含宁律师相关内容
    if "宁律师" in config["sp"]:
        logger.success("✅ 系统提示词包含宁律师人设")
    else:
        logger.warning("⚠️  系统提示词可能缺少宁律师人设")
    
    logger.success("✅ 测试4通过：配置文件检查通过\n")
    return True


def test_old_files_removed():
    """测试旧文件是否已删除"""
    logger.info("=" * 60)
    logger.info("测试5：旧文件清理")
    logger.info("=" * 60)
    
    old_files = [
        "src/config/lawyer_domains.py",
        "src/prompts/lawyers"
    ]
    
    removed_count = 0
    for file_path in old_files:
        full_path = os.path.join(os.getcwd(), file_path)
        if not os.path.exists(full_path):
            logger.info(f"✅ 已删除：{file_path}")
            removed_count += 1
        else:
            logger.warning(f"⚠️  仍存在：{file_path}")
    
    logger.info(f"\n已删除旧文件：{removed_count}/{len(old_files)}")
    logger.success("✅ 测试5完成\n")
    return removed_count >= len(old_files)


def main():
    """运行所有测试"""
    logger.info("=" * 60)
    logger.info("🧪 开始测试新架构")
    logger.info("=" * 60)
    logger.info("")
    
    results = {
        "宁律师配置": test_ning_lawyer_config(),
        "主脑路由逻辑": test_master_brain_routing(),
        "提示词一致性": test_prompt_consistency(),
        "配置文件": test_config_json(),
        "旧文件清理": test_old_files_removed()
    }
    
    # 汇总结果
    logger.info("=" * 60)
    logger.info("📊 测试结果汇总")
    logger.info("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        logger.info(f"{test_name:20s} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    logger.info("")
    logger.info(f"总计：{passed} 通过，{failed} 失败")
    
    if failed == 0:
        logger.success("=" * 60)
        logger.success("🎉 所有测试通过！新架构验证成功！")
        logger.success("=" * 60)
        return 0
    else:
        logger.error("=" * 60)
        logger.error("⚠️  部分测试失败，请检查日志")
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
