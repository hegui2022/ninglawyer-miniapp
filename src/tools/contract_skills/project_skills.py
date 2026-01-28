"""
项目制合同技能
Project-based Contract Skills
"""

from .base import BaseSkill


class ProjectInfoSkill(BaseSkill):
    """项目基本信息技能"""
    
    def __init__(self):
        super().__init__("project_info", "项目基本信息")
    
    def get_required_fields(self) -> list:
        return [
            "employer_name", "employer_address", "employer_contact", "employer_phone",
            "employee_name", "employee_id", "employee_address", "employee_phone",
            "emergency_contact"
        ]
    
    def get_prompt_template(self) -> str:
        return """
请提供以下基本信息：

【甲方信息】
1. 单位名称：
2. 单位地址：
3. 法定代表人：
4. 联系电话：

【乙方信息】
1. 姓名：
2. 身份证号码：
3. 住址：
4. 联系电话：
5. 紧急联系人及电话：
"""
    
    def generate(self, info: dict) -> str:
        return f"""一、基本信息

甲方（发包方）：{info.get('employer_name', '__________')}
地址：{info.get('employer_address', '__________')}
法定代表人：{info.get('employer_legal_rep', '__________')}
联系电话：{info.get('employer_contact', '__________')}

乙方（承包方）：{info.get('employee_name', '__________')}
身份证号码：{info.get('employee_id', '__________')}
住址：{info.get('employee_address', '__________')}
联系电话：{info.get('employee_phone', '__________')}
紧急联系人：{info.get('emergency_contact', '__________')}
"""


class ProjectTermSkill(BaseSkill):
    """项目期限技能"""
    
    def __init__(self):
        super().__init__("project_term", "项目期限")
    
    def get_required_fields(self) -> list:
        return ["start_date", "project_duration", "project_location"]
    
    def get_prompt_template(self) -> str:
        return """
请提供项目期限信息：

1. 项目开始日期：YYYY-MM-DD
2. 项目预计工期：____个月/天
3. 工作地点：
4. 项目交付标准：
"""
    
    def generate(self, info: dict) -> str:
        return f"""二、项目期限与交付

1. 项目期限：自{info.get('start_date', '____年__月__日')}起，预计工期{info.get('project_duration', '____')}个月。

2. 工作地点：{info.get('project_location', '__________')}

3. 交付标准：{info.get('delivery_standard', '按照项目约定标准交付')}
"""


class ProjectContentSkill(BaseSkill):
    """项目内容技能"""
    
    def __init__(self):
        super().__init__("project_content", "项目内容")
    
    def get_required_fields(self) -> list:
        return ["project_name", "project_scope", "project_deliverables"]
    
    def get_prompt_template(self) -> str:
        return """
请提供项目内容信息：

1. 项目名称：
2. 项目范围：明确工作内容和边界
3. 交付物：需要交付的具体成果
4. 工作时间安排：
"""
    
    def generate(self, info: dict) -> str:
        return f"""三、项目内容

1. 项目名称：{info.get('project_name', '__________')}

2. 项目范围：
{info.get('project_scope', '__________')}

3. 交付物：
{info.get('project_deliverables', '__________')}

4. 工作时间：根据项目进度合理安排
"""


class ProjectPaymentSkill(BaseSkill):
    """项目报酬技能"""
    
    def __init__(self):
        super().__init__("project_payment", "项目报酬")
    
    def get_required_fields(self) -> list:
        return ["total_amount", "payment_terms"]
    
    def get_prompt_template(self) -> str:
        return """
请提供项目报酬信息：

1. 项目总金额：____元
2. 付款方式：
   - 一次性付款
   - 分阶段付款（阶段1：____元，阶段2：____元，...）
   - 按月/按进度付款
3. 付款时间节点：
4. 是否有质保金：
   - 是（金额：____元，期限：____个月）
   - 否
"""
    
    def generate(self, info: dict) -> str:
        payment_info = f"项目总金额：{info.get('total_amount', '____')}元"
        payment_terms = info.get('payment_terms', '项目完成后一次性支付')
        
        warranty_info = ""
        if info.get('has_retention'):
            warranty_info = f"\n4. 质保金：{info.get('retention_amount', '____')}元，期限{info.get('retention_period', '____')}个月"
        
        return f"""四、项目报酬

1. {payment_info}

2. 付款方式：{payment_terms}
{warranty_info}
"""


class ProjectTerminationSkill(BaseSkill):
    """项目终止技能"""
    
    def __init__(self):
        super().__init__("project_termination", "项目终止")
    
    def get_required_fields(self) -> list:
        return ["termination_conditions", "breach_penalty"]
    
    def get_prompt_template(self) -> str:
        return """
请提供项目终止信息：

1. 项目完成条件：
2. 提前终止条件：
   - 双方协商一致
   - 甲方原因导致项目无法继续
   - 乙方原因导致项目无法继续
3. 违约责任：
   - 逾期交付：每天按合同金额的____%支付违约金
   - 质量不合格：需在____天内整改，整改不合格扣除____%
"""
    
    def generate(self, info: dict) -> str:
        return f"""五、项目完成与终止

1. 完成条件：{info.get('completion_conditions', '项目交付并经甲方验收合格')}

2. 提前终止：
   - 双方协商一致，可提前终止项目；
   - 甲方原因导致项目无法继续，应按已完成工作量结算；
   - 乙方原因导致项目无法继续，应承担相应责任。

3. 违约责任：
{info.get('breach_penalty', '乙方逾期交付，每逾期一天按合同总金额的1‰支付违约金')}
"""


# 创建技能实例
project_info_skill = ProjectInfoSkill()
project_term_skill = ProjectTermSkill()
project_content_skill = ProjectContentSkill()
project_payment_skill = ProjectPaymentSkill()
project_termination_skill = ProjectTerminationSkill()
