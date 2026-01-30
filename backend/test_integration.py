"""
测试提示词集成验证
验证重构后的律师和技能类能否正常工作
"""

import sys
sys.path.insert(0, '/workspace/projects/backend')

from loguru import logger


def test_lawyer_integration():
    """测试律师类的集成"""
    logger.info("开始测试律师类集成...")
    
    # 测试民事律师
    try:
        from src.agents.lawyer_civil import NingLawyerCivil
        
        # 创建律师实例
        lawyer = NingLawyerCivil()
        logger.info(f"✅ 民事律师创建成功: {lawyer.persona['name']}")
        
        # 验证提示词是否已更新
        assert lawyer.prompt_template is not None, "提示词模板未正确加载"
        logger.info("✅ 民事律师提示词模板正确")
        
    except Exception as e:
        logger.error(f"❌ 民事律师测试失败: {e}")
        raise
    
    # 测试刑事律师
    try:
        from src.agents.lawyer_criminal import NingLawyerCriminal
        
        lawyer = NingLawyerCriminal()
        logger.info(f"✅ 刑事律师创建成功: {lawyer.persona['name']}")
        
        assert lawyer.prompt_template is not None, "提示词模板未正确加载"
        logger.info("✅ 刑事律师提示词模板正确")
        
    except Exception as e:
        logger.error(f"❌ 刑事律师测试失败: {e}")
        raise
    
    # 测试合同律师
    try:
        from src.agents.lawyer_contract import NingLawyerContract
        
        lawyer = NingLawyerContract()
        logger.info(f"✅ 合同律师创建成功: {lawyer.persona['name']}")
        
        assert lawyer.prompt_template is not None, "提示词模板未正确加载"
        logger.info("✅ 合同律师提示词模板正确")
        
    except Exception as e:
        logger.error(f"❌ 合同律师测试失败: {e}")
        raise
    
    logger.info("🎉 所有律师类集成测试通过！")


def test_skill_integration():
    """测试技能类的集成"""
    logger.info("开始测试技能类集成...")
    
    # 测试民事咨询技能
    try:
        from src.skills.civil_consult_skill import CivilConsultSkill
        from src.prompts.manager import PromptManager
        
        # 验证技能提示词能正确加载
        prompt = PromptManager.get_skill_prompt('civil_consult')
        assert prompt is not None, "民事咨询技能提示词加载失败"
        
        # 测试格式化
        messages = prompt.format_messages(user_input="我的欠款要不回来了怎么办？")
        logger.info("✅ 民事咨询技能提示词正确")
        
    except Exception as e:
        logger.error(f"❌ 民事咨询技能测试失败: {e}")
        raise
    
    # 测试合同起草技能
    try:
        from src.prompts.manager import PromptManager
        
        prompt = PromptManager.get_skill_prompt('contract_draft')
        assert prompt is not None, "合同起草技能提示词加载失败"
        
        messages = prompt.format_messages(
            contract_type="租赁合同",
            party_a="甲方公司",
            party_b="乙方公司",
            terms="租赁期限、租金、违约责任等"
        )
        logger.info("✅ 合同起草技能提示词正确")
        
    except Exception as e:
        logger.error(f"❌ 合同起草技能测试失败: {e}")
        raise
    
    logger.info("🎉 所有技能类集成测试通过！")


def test_master_brain_integration():
    """测试主脑集成"""
    logger.info("开始测试主脑集成...")
    
    try:
        from src.agents.master_brain import MasterBrain
        from src.prompts.manager import PromptManager
        
        # 验证主脑提示词能正确加载
        prompt = PromptManager.get_skill_prompt('master_brain')
        assert prompt is not None, "主脑提示词加载失败"
        
        # 测试格式化
        messages = prompt.format_messages(user_input="我需要咨询一个债务纠纷的问题")
        logger.info("✅ 主脑提示词正确")
        
    except Exception as e:
        logger.error(f"❌ 主脑测试失败: {e}")
        raise
    
    logger.info("🎉 主脑集成测试通过！")


if __name__ == "__main__":
    test_lawyer_integration()
    test_skill_integration()
    test_master_brain_integration()
    logger.info("🎉 所有集成测试通过！提示词重构完成！")
