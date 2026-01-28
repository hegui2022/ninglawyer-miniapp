"""
实习协议技能
Intern Agreement Skills
"""

from .base import BaseSkill


class InternInfoSkill(BaseSkill):
    """实习基本信息技能"""
    
    def __init__(self):
        super().__init__("intern_info", "实习基本信息")
    
    def get_required_fields(self) -> list:
        return [
            "employer_name", "employer_address", "employer_contact", "employer_phone",
            "intern_name", "school_name", "major", "student_id", "phone", "emergency_contact"
        ]
    
    def get_prompt_template(self) -> str:
        return """
请提供以下基本信息：

【实习单位信息】
1. 单位名称：
2. 单位地址：
3. 联系人：
4. 联系电话：

【实习生信息】
1. 姓名：
2. 学校名称：
3. 所学专业：
4. 学号：
5. 联系电话：
6. 紧急联系人及电话：
"""
    
    def generate(self, info: dict) -> str:
        return f"""一、基本信息

甲方（实习单位）：{info.get('employer_name', '__________')}
地址：{info.get('employer_address', '__________')}
联系人：{info.get('employer_contact', '__________')}
联系电话：{info.get('employer_phone', '__________')}

乙方（实习生）：{info.get('intern_name', '__________')}
学校：{info.get('school_name', '__________')}
专业：{info.get('major', '__________')}
学号：{info.get('student_id', '__________')}
联系电话：{info.get('phone', '__________')}
紧急联系人：{info.get('emergency_contact', '__________')}
"""


class InternTermSkill(BaseSkill):
    """实习期限技能"""
    
    def __init__(self):
        super().__init__("intern_term", "实习期限")
    
    def get_required_fields(self) -> list:
        return ["start_date", "end_date", "location"]
    
    def get_prompt_template(self) -> str:
        return """
请提供实习期限信息：

1. 实习开始日期：YYYY-MM-DD
2. 实习结束日期：YYYY-MM-DD
3. 实习地点：
4. 是否可延长实习期：
   - 是（延长时间：____个月）
   - 否
"""
    
    def generate(self, info: dict) -> str:
        return f"""二、实习期限

1. 实习期限：自{info.get('start_date', '____年__月__日')}起至{info.get('end_date', '____年__月__日')}止，共计{info.get('duration', '____')}个月。

2. 实习地点：{info.get('location', '__________')}

3. 延期：{info.get('extendable', '经双方协商一致，可以延长实习期限。')}
"""


class InternContentSkill(BaseSkill):
    """实习内容技能"""
    
    def __init__(self):
        super().__init__("intern_content", "实习内容")
    
    def get_required_fields(self) -> list:
        return ["position", "job_content", "work_days", "work_hours"]
    
    def get_prompt_template(self) -> str:
        return """
请提供实习内容信息：

1. 实习岗位：
2. 主要工作内容：
3. 工作时间：
   - 每周工作____天
   - 每天工作____小时
4. 指导老师：
"""
    
    def generate(self, info: dict) -> str:
        return f"""三、实习内容

1. 实习岗位：{info.get('position', '__________')}

2. 实习内容：
{info.get('job_content', '__________')}

3. 工作时间：每周{info.get('work_days', '____')}天，每天{info.get('work_hours', '____')}小时

4. 指导老师：{info.get('mentor', '__________')}
"""


class InternAllowanceSkill(BaseSkill):
    """实习补贴技能"""
    
    def __init__(self):
        super().__init__("intern_allowance", "实习补贴")
    
    def get_required_fields(self) -> list:
        return ["allowance", "payment_method", "pay_day"]
    
    def get_prompt_template(self) -> str:
        return """
请提供实习补贴信息：

1. 实习补贴：____元/月
2. 发放方式：
   - 现金发放
   - 银行转账（提供账号）
3. 发放日期：每月____日
4. 其他待遇：
   - 是否提供餐补：是/否
   - 是否提供交通补贴：是/否
"""
    
    def generate(self, info: dict) -> str:
        allowance_info = f"""实习补贴：{info.get('allowance', '____')}元/月"""
        
        if info.get('meal_allowance'):
            allowance_info += f"\n餐补：{info.get('meal_allowance', '____')}元/月"
        
        if info.get('transport_allowance'):
            allowance_info += f"\n交通补贴：{info.get('transport_allowance', '____')}元/月"
        
        return f"""四、实习补贴

{allowance_info}

发放方式：{info.get('payment_method', '银行转账')}
发放日期：每月{info.get('pay_day', '____')}日
"""


class InternInsuranceSkill(BaseSkill):
    """实习保险技能"""
    
    def __init__(self):
        super().__init__("intern_insurance", "实习保险")
    
    def get_required_fields(self) -> list:
        return ["insurance_amount"]
    
    def get_prompt_template(self) -> str:
        return """
请提供保险信息：

1. 意外险：
   - 实习单位购买
   - 学校购买
   - 实习生自行购买
2. 保险金额：____万元
3. 保险期限：
"""
    
    def generate(self, info: dict) -> str:
        return f"""五、保险保障

1. 甲方为乙方购买意外伤害保险，保险金额为{info.get('insurance_amount', '____')}万元。

2. 保险期限与实习期限一致。

3. 乙方在实习期间因工作原因发生意外伤害，按保险合同约定享受保险待遇。
"""


class InternTerminationSkill(BaseSkill):
    """实习终止技能"""
    
    def __init__(self):
        super().__init__("intern_termination", "实习终止")
    
    def get_required_fields(self) -> list:
        return ["notice_days", "has_certificate"]
    
    def get_prompt_template(self) -> str:
        return """
请提供实习终止信息：

1. 终止条件：
   - 实习期满自动终止
   - 经双方协商一致可以提前终止
   - 实习生可以提前__天书面通知终止
   - 实习单位可以因实习生严重违纪随时终止

2. 实习证明：
   - 实习结束后，单位是否提供实习证明：是/否
"""
    
    def generate(self, info: dict) -> str:
        notice_days = info.get('notice_days', '7')
        has_certificate = info.get('has_certificate', True)
        
        return f"""六、实习终止

1. 实习期满，本协议自动终止。

2. 经双方协商一致，可以提前终止实习。乙方需提前{notice_days}天书面通知甲方。

3. 乙方有下列情形之一的，甲方可以随时终止实习，不承担任何责任：
   - 严重违反甲方规章制度；
   - 不能胜任实习工作，经指导老师提示后仍无明显改进；
   - 提供虚假信息，隐瞒重要事实；
   - 因健康原因不能继续实习。

4. 实习结束后，{'' if has_certificate else '不'}向乙方出具实习证明。
"""


# 创建技能实例
intern_info_skill = InternInfoSkill()
intern_term_skill = InternTermSkill()
intern_content_skill = InternContentSkill()
intern_allowance_skill = InternAllowanceSkill()
intern_insurance_skill = InternInsuranceSkill()
intern_termination_skill = InternTerminationSkill()
