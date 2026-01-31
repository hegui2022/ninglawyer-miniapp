"""
技能模块初始化
注册所有技能到服务注册表
"""

import os

# 只有在显式调用 register_all_skills() 时才注册技能，避免循环导入
HAS_REGISTERED = False


def register_all_skills():
    """注册所有技能"""
    global HAS_REGISTERED
    
    if HAS_REGISTERED:
        return
    
    from src.utils.skill_registry import skill_registry
    from src.skills.desensitize_skill import execute_desensitize
    from src.skills.civil_consult_skill import execute_civil_consult
    from src.skills.contract_skill import execute_contract
    from loguru import logger
    
    logger.info("=" * 60)
    logger.info("开始注册所有技能模块")
    logger.info("=" * 60)
    
    # 注册脱敏技能
    skill_registry.register(
        skill_name="desensitize",
        description="对敏感信息进行脱敏处理（姓名、身份证、手机号、地址等）",
        execute_func=execute_desensitize,
        category="privacy",
        required_subscription="basic"
    )
    
    # 注册民事咨询技能
    skill_registry.register(
        skill_name="civil_consult",
        description="提供民事法律咨询服务（债务纠纷、婚姻家庭、劳动争议等）",
        execute_func=execute_civil_consult,
        category="legal",
        required_subscription="basic"
    )
    
    # 注册合同起草技能
    skill_registry.register(
        skill_name="contract_draft",
        description="起草各类合同（借款合同、租赁合同、劳动合同等）",
        execute_func=execute_contract,
        category="legal",
        required_subscription="premium"
    )
    
    # 注册合同审查技能
    skill_registry.register(
        skill_name="contract_review",
        description="审查各类合同的风险并提供修改建议",
        execute_func=execute_contract,
        category="legal",
        required_subscription="premium"
    )
    
    # 注册婚姻家事技能
    _register_family_law_skills()
    
    logger.info("=" * 60)
    logger.info("所有技能模块注册完成！")
    logger.info("=" * 60)
    
    # 列出所有技能
    skills = skill_registry.list_skills()
    logger.info(f"✅ 已注册技能数量：{len(skills)}")
    for name, skill in skills.items():
        required = skill.get("required_subscription", "basic")
        logger.info(f"  - {name} ({skill['category']}) - 需要{required}套餐")
    
    HAS_REGISTERED = True


def _register_family_law_skills():
    """注册婚姻家事技能"""
    from src.utils.skill_registry import skill_registry
    from src.skills.divorce_procedure_skill import execute_divorce_procedure
    from src.skills.property_division_skill import execute_property_division
    from src.skills.child_custody_skill import execute_child_custody
    from src.skills.domestic_violence_skill import execute_domestic_violence
    
    # 注册离婚流程技能
    skill_registry.register(
        skill_name="divorce_procedure",
        description="离婚流程说明",
        execute_func=execute_divorce_procedure,
        category="family_law",
        required_subscription="basic"
    )
    
    # 注册财产分割技能
    skill_registry.register(
        skill_name="property_division",
        description="财产分割计算",
        execute_func=execute_property_division,
        category="family_law",
        required_subscription="basic"
    )
    
    # 注册子女抚养技能
    skill_registry.register(
        skill_name="child_custody",
        description="子女抚养权",
        execute_func=execute_child_custody,
        category="family_law",
        required_subscription="basic"
    )
    
    # 注册家暴维权技能
    skill_registry.register(
        skill_name="domestic_violence",
        description="家暴维权",
        execute_func=execute_domestic_violence,
        category="family_law",
        required_subscription="basic"
    )


# 不自动注册，避免循环导入
# register_all_skills()
