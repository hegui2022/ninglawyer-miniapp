"""
退休返聘协议技能
Retired Reemployment Agreement Skills
"""

from .base import BaseSkill


class RetiredInfoSkill(BaseSkill):
    """退休返聘基本信息技能"""
    
    def __init__(self):
        super().__init__("retired_info", "退休返聘基本信息")
    
    def get_required_fields(self) -> list:
        return [
            "employer_name", "employer_address", "employer_contact", "employer_phone",
            "retiree_name", "id_card", "retirement_certificate", "former_employer",
            "address", "phone", "emergency_contact"
        ]
    
    def get_prompt_template(self) -> str:
        return """
请提供以下基本信息：

【用人单位信息】
1. 单位名称：
2. 单位地址：
3. 联系人：
4. 联系电话：

【退休人员信息】
1. 姓名：
2. 身份证号码：
3. 退休证号码：
4. 原工作单位：
5. 住址：
6. 联系电话：
7. 紧急联系人及电话：
"""
    
    def generate(self, info: dict) -> str:
        return f"""一、基本信息

甲方（用工单位）：{info.get('employer_name', '__________')}
地址：{info.get('employer_address', '__________')}
联系人：{info.get('employer_contact', '__________')}
联系电话：{info.get('employer_phone', '__________')}

乙方（退休人员）：{info.get('retiree_name', '__________')}
身份证号码：{info.get('id_card', '__________')}
退休证号码：{info.get('retirement_certificate', '__________')}
原工作单位：{info.get('former_employer', '__________')}
住址：{info.get('address', '__________')}
联系电话：{info.get('phone', '__________')}
紧急联系人：{info.get('emergency_contact', '__________')}
"""


class RetiredTermSkill(BaseSkill):
    """返聘期限技能"""
    
    def __init__(self):
        super().__init__("retired_term", "返聘期限")
    
    def get_required_fields(self) -> list:
        return ["start_date", "end_date", "location"]
    
    def get_prompt_template(self) -> str:
        return """
请提供返聘期限信息：

1. 返聘开始日期：YYYY-MM-DD
2. 返聘结束日期：YYYY-MM-DD
3. 工作地点：
4. 是否可延长：
   - 是（续签需提前__天协商）
   - 否
"""
    
    def generate(self, info: dict) -> str:
        return f"""二、返聘期限

1. 返聘期限：自{info.get('start_date', '____年__月__日')}起至{info.get('end_date', '____年__月__日')}止。

2. 工作地点：{info.get('location', '__________')}

3. 续聘：返聘期满前{info.get('renewal_notice_days', '30')}天，双方可协商是否续聘。
"""


class RetiredContentSkill(BaseSkill):
    """返聘工作内容技能"""
    
    def __init__(self):
        super().__init__("retired_content", "返聘工作内容")
    
    def get_required_fields(self) -> list:
        return ["position", "job_responsibilities"]
    
    def get_prompt_template(self) -> str:
        return """
请提供工作内容信息：

1. 工作岗位：
2. 主要工作职责：
3. 工作时间：
   - 每周工作____天
   - 每天工作____小时
4. 是否提供加班费：
   - 是（每小时____元）
   - 否（已包含在劳务报酬中）
"""
    
    def generate(self, info: dict) -> str:
        overtime_info = ""
        if info.get('has_overtime'):
            overtime_info = f"\n3. 加班费：确需加班的，按每小时{info.get('overtime_rate', '____')}元支付加班费。"
        
        return f"""三、工作内容

1. 工作岗位：{info.get('position', '__________')}

2. 工作职责：
{info.get('job_responsibilities', '__________')}
{overtime_info}
"""


class RetiredPaymentSkill(BaseSkill):
    """返聘报酬技能"""
    
    def __init__(self):
        super().__init__("retired_payment", "返聘报酬")
    
    def get_required_fields(self) -> list:
        return ["payment", "payment_method", "pay_day"]
    
    def get_prompt_template(self) -> str:
        return """
请提供劳务报酬信息：

1. 劳务报酬：____元/月
2. 支付方式：
   - 银行转账
   - 现金支付
3. 支付日期：每月____日
4. 其他补贴：
   - 交通补贴：____元/月
   - 餐饮补贴：____元/月
5. 是否缴纳个人所得税：
   - 是（由单位代扣代缴）
   - 否（自行申报）
"""
    
    def generate(self, info: dict) -> str:
        payment_info = f"劳务报酬：{info.get('payment', '____')}元/月"
        
        if info.get('transport_allowance'):
            payment_info += f"\n交通补贴：{info.get('transport_allowance', '____')}元/月"
        
        if info.get('meal_allowance'):
            payment_info += f"\n餐饮补贴：{info.get('meal_allowance', '____')}元/月"
        
        tax_info = "个人所得税：由乙方自行申报缴纳。" if not info.get('withhold_tax') else "个人所得税：由甲方代扣代缴。"
        
        return f"""四、劳务报酬

1. {payment_info}

2. 支付方式：{info.get('payment_method', '银行转账')}
3. 支付日期：每月{info.get('pay_day', '____')}日

4. {tax_info}
"""


class RetiredTerminationSkill(BaseSkill):
    """返聘终止技能"""
    
    def __init__(self):
        super().__init__("retired_termination", "返聘终止")
    
    def get_required_fields(self) -> list:
        return ["notice_days", "has_compensation"]
    
    def get_prompt_template(self) -> str:
        return """
请提供终止条件信息：

1. 终止条件：
   - 双方协商一致可以终止
   - 乙方可以提前__天书面通知终止
   - 甲方可以因以下情况随时终止：
     * 身体状况不能胜任工作
     * 严重违反单位规章制度
     * 提供虚假信息
2. 是否有经济补偿：
   - 是（按返聘期限计算）
   - 否（无经济补偿）
"""
    
    def generate(self, info: dict) -> str:
        notice_days = info.get('notice_days', '7')
        has_compensation = info.get('has_compensation', False)
        
        compensation_clause = ""
        if has_compensation:
            compensation_clause = "3. 提前终止的，甲方应按返聘剩余期限支付相应的经济补偿。"
        else:
            compensation_clause = "3. 提前终止的，不享受经济补偿。"
        
        return f"""五、协议终止

1. 返聘期满，本协议自动终止。

2. 经双方协商一致，可以提前终止返聘。乙方需提前{notice_days}天书面通知甲方。

4. 乙方有下列情形之一的，甲方可以随时终止本协议：
   - 身体状况不能胜任工作，经医疗证明确认的；
   - 严重违反甲方规章制度；
   - 提供虚假信息，隐瞒重要事实；
   - 给甲方造成重大损失或不良影响的。

{compensation_clause}
"""


# 创建技能实例
retired_info_skill = RetiredInfoSkill()
retired_term_skill = RetiredTermSkill()
retired_content_skill = RetiredContentSkill()
retired_payment_skill = RetiredPaymentSkill()
retired_termination_skill = RetiredTerminationSkill()
