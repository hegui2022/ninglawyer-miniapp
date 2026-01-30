"""
测试提示词管理器
验证所有提示词是否正常加载
"""

import sys
sys.path.insert(0, '/workspace/projects/backend')

from src.prompts.manager import PromptManager
from loguru import logger


def test_prompt_manager():
    """测试提示词管理器"""
    logger.info("开始测试提示词管理器...")
    
    # 测试 1: 列出所有律师
    lawyers = PromptManager.list_lawyers()
    logger.info(f"✅ 可用律师：{lawyers}")
    assert len(lawyers) == 7, f"应该有7个律师，实际有{len(lawyers)}个"
    
    # 测试 2: 列出所有技能
    skills = PromptManager.list_skills()
    logger.info(f"✅ 可用技能：{skills}")
    assert len(skills) == 5, f"应该有5个技能，实际有{len(skills)}个"
    
    # 测试 3: 获取律师提示词
    for lawyer_type in lawyers:
        prompt = PromptManager.get_lawyer_prompt(lawyer_type, simple=False)
        assert prompt is not None, f"律师提示词 {lawyer_type} 加载失败"
        logger.info(f"✅ {lawyer_type} 律师提示词加载成功")
        
        # 测试格式化
        try:
            messages = prompt.format_messages(chat_history=[], user_input="测试问题")
            logger.info(f"✅ {lawyer_type} 律师提示词格式化成功")
        except Exception as e:
            logger.error(f"❌ {lawyer_type} 律师提示词格式化失败：{e}")
            raise
    
    # 测试 4: 获取技能提示词
    for skill_name in skills:
        prompt = PromptManager.get_skill_prompt(skill_name)
        assert prompt is not None, f"技能提示词 {skill_name} 加载失败"
        logger.info(f"✅ {skill_name} 技能提示词加载成功")
        
        # 测试格式化
        try:
            if skill_name == 'civil_consult':
                messages = prompt.format_messages(user_input="测试问题")
            elif skill_name == 'contract_draft':
                messages = prompt.format_messages(
                    contract_type="租赁合同",
                    party_a="甲方公司",
                    party_b="乙方公司",
                    terms="租赁期限、租金、违约责任等"
                )
            elif skill_name == 'contract_review':
                messages = prompt.format_messages(contract_text="测试合同")
            elif skill_name == 'desensitize':
                messages = prompt.format_messages(text="测试文本")
            elif skill_name == 'master_brain':
                messages = prompt.format_messages(user_input="测试问题")
            logger.info(f"✅ {skill_name} 技能提示词格式化成功")
        except Exception as e:
            logger.error(f"❌ {skill_name} 技能提示词格式化失败：{e}")
            raise
    
    # 测试 5: 获取律师名称
    lawyer_names = PromptManager.get_lawyer_names()
    logger.info(f"✅ 律师名称：{lawyer_names}")
    
    # 测试 6: 验证律师类型
    for lawyer_type in lawyers:
        assert PromptManager.validate_lawyer_type(lawyer_type), f"律师类型 {lawyer_type} 验证失败"
        assert not PromptManager.validate_lawyer_type(f"invalid_{lawyer_type}"), "应该返回 False"
    logger.info(f"✅ 律师类型验证成功")
    
    # 测试 7: 验证技能名称
    for skill_name in skills:
        assert PromptManager.validate_skill_name(skill_name), f"技能名称 {skill_name} 验证失败"
        assert not PromptManager.validate_skill_name(f"invalid_{skill_name}"), "应该返回 False"
    logger.info(f"✅ 技能名称验证成功")
    
    logger.info("🎉 所有测试通过！")


if __name__ == "__main__":
    test_prompt_manager()
