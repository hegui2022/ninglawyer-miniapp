"""
初始化合同模板数据
Initialize Contract Templates
"""

import json
from coze_coding_dev_sdk.database import get_session
from storage.database.contract_manager import (
    contract_template_manager,
    ContractTemplateCreate
)


# 预置合同模板
PRESET_TEMPLATES = [
    {
        "template_name": "标准劳动合同模板",
        "template_type": "standard",
        "template_content": {
            "party_a": "甲方（用人单位）",
            "party_b": "乙方（劳动者）",
            "start_date": "2025-01-01",
            "end_date": "2026-12-31",
            "probation_months": 3,
            "job_content": "根据甲方工作需要，乙方同意在甲方安排的工作岗位工作，完成甲方安排的工作任务。",
            "workplace": "甲方所在地",
            "salary": "8000",
            "payment_method": "每月10日通过银行转账支付",
            "work_hours": "标准工时制，每周工作40小时",
            "has_insurance": True,
            "has_housing_fund": True,
            "has_confidentiality": False,
            "has_non_compete": False,
            "has_ip_clause": False
        },
        "description": "适用于正式员工的全日制劳动合同，包含试用期、社保、公积金等标准条款",
        "is_active": True
    },
    {
        "template_name": "非全日制用工合同模板",
        "template_type": "parttime",
        "template_content": {
            "party_a": "甲方（用人单位）",
            "party_b": "乙方（劳动者）",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "probation_months": 0,
            "job_content": "乙方同意根据甲方工作需要，在非全日制工作岗位上为甲方提供服务。",
            "workplace": "甲方所在地",
            "salary": "2000",
            "payment_method": "按小时计费，每月结算一次",
            "work_hours": "非全日制用工，每周工作不超过24小时",
            "has_insurance": False,
            "has_housing_fund": False,
            "has_confidentiality": False,
            "has_non_compete": False,
            "has_ip_clause": False
        },
        "description": "适用于兼职、小时工等非全日制用工场景",
        "is_active": True
    },
    {
        "template_name": "实习协议模板",
        "template_type": "intern",
        "template_content": {
            "party_a": "甲方（用人单位）",
            "party_b": "乙方（实习生）",
            "start_date": "2025-01-01",
            "end_date": "2025-06-30",
            "probation_months": 0,
            "job_content": "乙方同意在甲方实习，协助完成相关工作任务，提升专业技能。",
            "workplace": "甲方所在地",
            "salary": "3000",
            "payment_method": "实习补贴，每月10日发放",
            "work_hours": "根据实习安排，每周工作不超过40小时",
            "has_insurance": False,
            "has_housing_fund": False,
            "has_confidentiality": True,
            "has_non_compete": False,
            "has_ip_clause": True
        },
        "description": "适用于在校学生实习场景，包含实习补贴、保密协议等条款",
        "is_active": True
    },
    {
        "template_name": "退休返聘协议模板",
        "template_type": "retired",
        "template_content": {
            "party_a": "甲方（用人单位）",
            "party_b": "乙方（退休人员）",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "probation_months": 0,
            "job_content": "乙方退休后，同意继续为甲方提供专业技术服务和咨询。",
            "workplace": "甲方所在地",
            "salary": "10000",
            "payment_method": "每月15日通过银行转账支付",
            "work_hours": "弹性工作制，根据工作需要安排",
            "has_insurance": False,
            "has_housing_fund": False,
            "has_confidentiality": True,
            "has_non_compete": False,
            "has_ip_clause": False
        },
        "description": "适用于退休人员返聘场景，不缴纳社保，包含保密协议",
        "is_active": True
    },
    {
        "template_name": "项目制合同模板",
        "template_type": "project",
        "template_content": {
            "party_a": "甲方（发包方）",
            "party_b": "乙方（承包方）",
            "start_date": "2025-01-01",
            "end_date": "2025-03-31",
            "probation_months": 0,
            "job_content": "乙方同意按照甲方要求完成项目开发任务，保证项目质量和进度。",
            "workplace": "项目所在地或甲方指定地点",
            "salary": "50000",
            "payment_method": "项目款项按阶段支付：签约时30%，中期30%，验收通过后40%",
            "work_hours": "根据项目进度安排，不固定工作时间",
            "has_insurance": False,
            "has_housing_fund": False,
            "has_confidentiality": True,
            "has_non_compete": True,
            "has_ip_clause": True
        },
        "description": "适用于项目承包、工程承揽等场景，以完成项目为期限",
        "is_active": True
    },
    {
        "template_name": "劳务派遣合同模板",
        "template_type": "dispatch",
        "template_content": {
            "party_a": "甲方（用工单位）",
            "party_b": "乙方（被派遣劳动者）",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "probation_months": 3,
            "job_content": "乙方同意由派遣单位派遣至甲方工作，完成甲方安排的工作任务。",
            "workplace": "甲方所在地",
            "salary": "6000",
            "payment_method": "由派遣单位负责发放，每月10日支付",
            "work_hours": "与甲方同岗位员工一致",
            "has_insurance": True,
            "has_housing_fund": True,
            "has_confidentiality": True,
            "has_non_compete": False,
            "has_ip_clause": False
        },
        "description": "适用于劳务派遣三方合作场景",
        "is_active": True
    }
]


def init_templates():
    """初始化合同模板"""
    db = get_session()
    try:
        print("开始初始化合同模板...")
        
        for template_data in PRESET_TEMPLATES:
            # 检查是否已存在相同名称的模板
            from storage.database.shared.model import ContractTemplate
            existing = db.query(ContractTemplate).filter(
                ContractTemplate.template_name == template_data["template_name"]
            ).first()
            
            if existing:
                print(f"模板已存在，跳过：{template_data['template_name']}")
                continue
            
            # 将 template_content 序列化为 JSON 字符串
            template_data_for_create = template_data.copy()
            template_data_for_create['template_content'] = json.dumps(template_data['template_content'], ensure_ascii=False)
            
            # 创建新模板
            template = contract_template_manager.create_template(
                db,
                ContractTemplateCreate(**template_data_for_create)
            )
            print(f"✓ 创建模板成功：{template.template_name}")
        
        print("\n模板初始化完成！")
        
        # 统计模板数量
        total = db.query(ContractTemplate).filter(ContractTemplate.is_active == True).count()
        print(f"当前共有 {total} 个可用模板")
        
    except Exception as e:
        print(f"初始化失败：{str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_templates()
