"""
劳务派遣合同技能
Labor Dispatch Contract Skills
"""

from .base import BaseSkill


class DispatchInfoSkill(BaseSkill):
    """劳务派遣基本信息技能"""
    
    def __init__(self):
        super().__init__("dispatch_info", "劳务派遣基本信息")
    
    def get_required_fields(self) -> list:
        return [
            "dispatch_company", "dispatch_address", "dispatch_contact", "dispatch_phone",
            "workplace_name", "workplace_address", "workplace_contact", "workplace_phone",
            "employee_name", "employee_id", "employee_address", "employee_phone"
        ]
    
    def get_prompt_template(self) -> str:
        return """
请提供以下基本信息：

【劳务派遣单位（甲方）】
1. 单位名称：
2. 单位地址：
3. 法定代表人：
4. 联系电话：

【用工单位（乙方）】
1. 单位名称：
2. 单位地址：
3. 联系人：
4. 联系电话：

【劳动者（丙方）】
1. 姓名：
2. 身份证号码：
3. 住址：
4. 联系电话：
"""
    
    def generate(self, info: dict) -> str:
        return f"""一、基本信息

甲方（劳务派遣单位）：{info.get('dispatch_company', '__________')}
地址：{info.get('dispatch_address', '__________')}
法定代表人：{info.get('dispatch_legal_rep', '__________')}
联系电话：{info.get('dispatch_contact', '__________')}

乙方（用工单位）：{info.get('workplace_name', '__________')}
地址：{info.get('workplace_address', '__________')}
联系人：{info.get('workplace_contact', '__________')}
联系电话：{info.get('workplace_phone', '__________')}

丙方（劳动者）：{info.get('employee_name', '__________')}
身份证号码：{info.get('employee_id', '__________')}
住址：{info.get('employee_address', '__________')}
联系电话：{info.get('employee_phone', '__________')}
"""


class DispatchTermSkill(BaseSkill):
    """劳务派遣期限技能"""
    
    def __init__(self):
        super().__init__("dispatch_term", "劳务派遣期限")
    
    def get_required_fields(self) -> list:
        return ["start_date", "end_date", "trial_period", "work_location"]
    
    def get_prompt_template(self) -> str:
        return """
请提供派遣期限信息：

1. 派遣开始日期：YYYY-MM-DD
2. 派遣结束日期：YYYY-MM-DD
3. 工作地点：
4. 试用期：____个月（可选，一般不超过2个月）
5. 派遣岗位：
"""
    
    def generate(self, info: dict) -> str:
        trial_info = ""
        if info.get('has_trial'):
            trial_info = f"\n3. 试用期：{info.get('trial_period', '____')}个月（自{info.get('start_date', '____年__月__日')}起计算）"
        
        return f"""二、派遣期限与工作岗位

1. 派遣期限：自{info.get('start_date', '____年__月__日')}起至{info.get('end_date', '____年__月__日')}止。
{trial_info}

2. 工作地点：{info.get('work_location', '__________')}

3. 派遣岗位：{info.get('dispatch_position', '__________')}
"""


class DispatchContentSkill(BaseSkill):
    """派遣工作内容技能"""
    
    def __init__(self):
        super().__init__("dispatch_content", "派遣工作内容")
    
    def get_required_fields(self) -> list:
        return ["work_hours", "job_responsibilities"]
    
    def get_prompt_template(self) -> str:
        return """
请提供工作内容信息：

1. 工作时间：
   - 每周工作____天
   - 每天工作____小时
2. 工作职责：
3. 工作条件和劳动保护：
"""
    
    def generate(self, info: dict) -> str:
        return f"""三、工作内容

1. 工作时间：每周{info.get('work_days', '____')}天，每天{info.get('work_hours', '____')}小时。

2. 工作职责：
{info.get('job_responsibilities', '__________')}

3. 工作条件和劳动保护：乙方应提供符合国家规定的劳动条件和必要的劳动保护措施。
"""


class DispatchPaymentSkill(BaseSkill):
    """派遣报酬技能"""
    
    def __init__(self):
        super().__init__("dispatch_payment", "派遣报酬")
    
    def get_required_fields(self) -> list:
        return ["dispatch_fee", "employee_salary", "social_insurance"]
    
    def get_prompt_template(self) -> str:
        return """
请提供报酬信息：

1. 派遣服务费：____元/月（乙方支付给甲方）
2. 劳动者工资：____元/月（甲方支付给丙方）
3. 社会保险：
   - 甲方为丙方缴纳
   - 乙方承担社会保险费用
4. 加班费：
   - 按法律规定支付
   - 已包含在工资中
"""
    
    def generate(self, info: dict) -> str:
        insurance_info = "社会保险：甲方为丙方缴纳基本养老保险、基本医疗保险、失业保险、工伤保险、生育保险。"
        if info.get('employer_pays_insurance'):
            insurance_info = "社会保险：乙方应承担丙方的社会保险费用，由甲方代为缴纳。"
        
        return f"""四、报酬与福利

1. 派遣服务费：{info.get('dispatch_fee', '____')}元/月，由乙方按月支付给甲方。

2. 丙方工资：{info.get('employee_salary', '____')}元/月，由甲方按月支付给丙方。

3. {insurance_info}

4. 加班费：丙方加班的，乙方应按法律规定支付加班费，通过甲方发放给丙方。
"""


class DispatchResponsibilitySkill(BaseSkill):
    """派遣责任技能"""
    
    def __init__(self):
        super().__init__("dispatch_responsibility", "派遣责任")
    
    def get_required_fields(self) -> list:
        return ["accident_responsibility", "performance_management"]
    
    def get_prompt_template(self) -> str:
        return """
请提供责任划分信息：

1. 工伤责任：
   - 工作期间工伤由乙方负责
   - 工伤由甲方负责
2. 绩效管理：
   - 乙方负责绩效考核
   - 甲方负责绩效考核
3. 退回条件：
   - 劳动者不符合录用条件
   - 劳动者严重违反规章制度
   - 其他：
"""
    
    def generate(self, info: dict) -> str:
        accident_info = "工作期间发生工伤的，由乙方承担相应责任，甲方协助办理工伤认定和理赔手续。"
        if info.get('dispatch_responsible'):
            accident_info = "工作期间发生工伤的，由甲方承担相应责任。"
        
        performance_info = "乙方负责丙方的工作安排、岗位管理和绩效考核。"
        if info.get('dispatch_manages'):
            performance_info = "甲方负责丙方的工作安排、岗位管理和绩效考核。"
        
        return f"""五、责任与义务

1. 工伤责任：{accident_info}

2. 绩效管理：{performance_info}

3. 退回条件：丙方有下列情形之一的，乙方可以将其退回甲方：
   - 在试用期内被证明不符合录用条件的；
   - 严重违反乙方规章制度的；
   - 严重失职、营私舞弊，给乙方造成重大损害的；
   - 被依法追究刑事责任的。
"""


# 创建技能实例
dispatch_info_skill = DispatchInfoSkill()
dispatch_term_skill = DispatchTermSkill()
dispatch_content_skill = DispatchContentSkill()
dispatch_payment_skill = DispatchPaymentSkill()
dispatch_responsibility_skill = DispatchResponsibilitySkill()
