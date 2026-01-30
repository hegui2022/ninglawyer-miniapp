"""
套餐配置文件（Subscription Plans）
定义不同套餐的功能权限和限制
"""

from typing import Dict, List, Any


# 套餐配置
SUBSCRIPTION_PLANS: Dict[str, Dict[str, Any]] = {
    "basic": {
        "id": "basic",
        "name": "基础版",
        "price": 0,
        "duration": 30,  # 30天
        "description": "适合个人用户的基础法律咨询服务",
        "features": [
            "法律咨询服务",
            "隐私脱敏功能",
            "10次/月咨询次数",
            "历史记录查询"
        ],
        "modules": [
            "consultation",      # 法律咨询
            "desensitize"        # 隐私脱敏
        ],
        "skills": [
            "civil_consult",     # 民事咨询
            "desensitize"        # 脱敏
        ],
        "limits": {
            "consultations_per_month": 10,
            "contracts_per_month": 0,
            "desensitize_per_month": 20,
            "risk_scans_per_month": 0,
            "max_file_size": 5,  # MB
            "max_sessions": 5
        },
        "ui_config": {
            "show_ads": True,
            "priority_support": False,
            "export_reports": False
        }
    },
    
    "premium": {
        "id": "premium",
        "name": "专业版",
        "price": 99,
        "duration": 30,  # 30天
        "description": "适合专业人士和企业用户，提供全面的合同服务",
        "features": [
            "无限次法律咨询",
            "隐私脱敏功能",
            "合同起草功能",
            "合同审查功能",
            "历史记录查询",
            "优先技术支持"
        ],
        "modules": [
            "consultation",
            "desensitize",
            "contract_draft",    # 合同起草
            "contract_review"    # 合同审查
        ],
        "skills": [
            "civil_consult",
            "desensitize",
            "contract_draft",
            "contract_review"
        ],
        "limits": {
            "consultations_per_month": 100,
            "contracts_per_month": 50,
            "desensitize_per_month": 200,
            "risk_scans_per_month": 0,
            "max_file_size": 20,  # MB
            "max_sessions": 20
        },
        "ui_config": {
            "show_ads": False,
            "priority_support": True,
            "export_reports": True
        }
    },
    
    "enterprise": {
        "id": "enterprise",
        "name": "企业版",
        "price": 999,
        "duration": 30,  # 30天
        "description": "适合企业用户，提供全方位的风险管理和签约服务",
        "features": [
            "无限次法律咨询",
            "隐私脱敏功能",
            "合同起草功能",
            "合同审查功能",
            "风险扫描功能",
            "合规检查功能",
            "电子签约功能",
            "合同管理功能",
            "历史记录查询",
            "专属客服支持",
            "数据导出功能",
            "团队协作功能"
        ],
        "modules": [
            "consultation",
            "desensitize",
            "contract_draft",
            "contract_review",
            "risk_scan",         # 风险扫描
            "compliance_check",  # 合规检查
            "e_signing",         # 电子签约
            "contract_management"  # 合同管理
        ],
        "skills": [
            "civil_consult",
            "desensitize",
            "contract_draft",
            "contract_review",
            "risk_scan",
            "compliance_check",
            "e_signing"
        ],
        "limits": {
            "consultations_per_month": 1000,
            "contracts_per_month": 500,
            "desensitize_per_month": 1000,
            "risk_scans_per_month": 100,
            "max_file_size": 100,  # MB
            "max_sessions": 100
        },
        "ui_config": {
            "show_ads": False,
            "priority_support": True,
            "export_reports": True,
            "team_collaboration": True,
            "api_access": True
        }
    }
}


# 模块到小程序的映射
MODULE_TO_MINIPROGRAM = {
    "consultation": {
        "name": "法律咨询",
        "icon": "consult",
        "path": "/pages/consultation/consultation",
        "miniprogram": "miniprogram",
        "description": "提供专业的法律咨询服务"
    },
    "desensitize": {
        "name": "隐私脱敏",
        "icon": "privacy",
        "path": "/pages/desensitize/desensitize",
        "miniprogram": "miniprogram",
        "description": "对敏感信息进行脱敏处理"
    },
    "contract_draft": {
        "name": "合同起草",
        "icon": "contract-draft",
        "path": "/pages/contract/contract?action=draft",
        "miniprogram": "miniprogram",
        "description": "起草各类合同文档"
    },
    "contract_review": {
        "name": "合同审查",
        "icon": "contract-review",
        "path": "/pages/contract/contract?action=review",
        "miniprogram": "miniprogram",
        "description": "审查合同风险并提供修改建议"
    },
    "risk_scan": {
        "name": "风险扫描",
        "icon": "risk-scan",
        "path": "/pages/scan/scan",
        "miniprogram": "prevent-risk",
        "description": "扫描企业法律风险"
    },
    "compliance_check": {
        "name": "合规检查",
        "icon": "compliance",
        "path": "/pages/compliance/compliance",
        "miniprogram": "prevent-risk",
        "description": "检查企业合规性"
    },
    "e_signing": {
        "name": "电子签约",
        "icon": "sign",
        "path": "/pages/sign/sign",
        "miniprogram": "code-signing",
        "description": "在线电子合同签署"
    },
    "contract_management": {
        "name": "合同管理",
        "icon": "contract-manage",
        "path": "/pages/record/record",
        "miniprogram": "lyue",
        "description": "管理合同和到期提醒"
    }
}


# 小程序AppID配置（需要根据实际情况填写）
MINIPROGRAM_APPIDS = {
    "miniprogram": "",        # 主小程序AppID
    "prevent-risk": "",       # 防风险小程序AppID
    "legal-instructor": "",   # 法律教官小程序AppID
    "code-signing": "",       # 码上签约小程序AppID
    "lyue": "",               # 理约小程序AppID
    "zenme-pan": ""           # 怎么判小程序AppID
}


def get_subscription_plan(plan_id: str) -> Dict[str, Any]:
    """获取套餐配置"""
    return SUBSCRIPTION_PLANS.get(plan_id, SUBSCRIPTION_PLANS["basic"])


def get_module_info(module_id: str) -> Dict[str, Any]:
    """获取模块信息"""
    return MODULE_TO_MINIPROGRAM.get(module_id, {})


def get_available_modules(plan_id: str) -> List[str]:
    """获取套餐可用的模块列表"""
    plan = get_subscription_plan(plan_id)
    return plan.get("modules", [])


def check_permission(user_subscription: str, required_subscription: str) -> bool:
    """
    检查用户是否有权限
    
    Args:
        user_subscription: 用户套餐类型
        required_subscription: 需要的套餐类型
    
    Returns:
        是否有权限
    """
    # 套餐级别：basic < premium < enterprise
    subscription_levels = {
        "basic": 1,
        "premium": 2,
        "enterprise": 3
    }
    
    user_level = subscription_levels.get(user_subscription, 1)
    required_level = subscription_levels.get(required_subscription, 1)
    
    return user_level >= required_level


def get_upgrade_path(current_plan: str) -> List[str]:
    """获取升级路径"""
    levels = ["basic", "premium", "enterprise"]
    try:
        current_index = levels.index(current_plan)
        return levels[current_index + 1:]
    except ValueError:
        return levels
