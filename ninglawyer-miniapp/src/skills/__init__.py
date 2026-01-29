"""
技能模块初始化
注册所有技能到服务注册表
"""

from src.utils.skill_registry import skill_registry
from src.skills.desensitize_skill import execute_desensitize
from src.skills.civil_consult_skill import execute_civil_consult
from src.skills.contract_skill import execute_contract
from loguru import logger


def register_all_skills():
    """注册所有技能"""
    logger.info("=" * 60)
    logger.info("开始注册所有技能模块")
    logger.info("=" * 60)
    
    # 注册脱敏技能
    skill_registry.register(
        skill_name="desensitize",
        description="对敏感信息进行脱敏处理（姓名、身份证、手机号、地址等）",
        execute_func=execute_desensitize,
        category="privacy"
    )
    
    # 注册民事咨询技能
    skill_registry.register(
        skill_name="civil_consult",
        description="提供民事法律咨询服务（债务纠纷、婚姻家庭、劳动争议等）",
        execute_func=execute_civil_consult,
        category="legal"
    )
    
    # 注册合同起草技能
    skill_registry.register(
        skill_name="contract",
        description="起草和审查各类合同（借款合同、租赁合同、劳动合同等）",
        execute_func=execute_contract,
        category="legal"
    )
    
    logger.info("=" * 60)
    logger.info("所有技能模块注册完成！")
    logger.info("=" * 60)
    
    # 列出所有技能
    skills = skill_registry.list_skills()
    logger.info(f"✅ 已注册技能数量：{len(skills)}")
    for name, skill in skills.items():
        logger.info(f"  - {name} ({skill['category']})")


# 自动注册
register_all_skills()
