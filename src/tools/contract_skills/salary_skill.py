"""
劳动报酬技能
Salary Skill
"""

from typing import Dict, Any, List
from .base import BaseSkill


class SalarySkill(BaseSkill):
    """劳动报酬技能 - 处理工资标准和发放"""
    
    def __init__(self):
        super().__init__(
            name="salary",
            description="处理工资标准和发放"
        )
    
    def get_required_fields(self) -> List[str]:
        """获取必填字段"""
        return [
            "salary_type",          # 工资类型：monthly/hourly/daily
            "base_salary",          # 基本工资
            "performance_bonus",    # 绩效奖金
            "allowances",           # 津贴补贴
            "pay_day",              # 发薪日
            "overtime_calculation_base",  # 加班费计算基数
        ]
    
    def get_prompt_template(self) -> str:
        """获取信息收集提示"""
        return """
请提供劳动报酬相关信息：

1. 工资类型：
   - 月薪制
   - 时薪制（非全日制）
   - 日薪制

2. 基本工资：
   金额：_______ 元

3. 绩效奖金：
   金额：_______ 元（如果没有，填0）

4. 津贴补贴：
   餐补、交通补、住房补等：_______ 元（如果没有，填0）

5. 发薪日：
   每月_______ 日左右发放

6. 加班费计算基数：
   以基本工资为基数计算

请逐项填写。
"""
    
    def generate(self, info: Dict[str, Any]) -> str:
        """生成劳动报酬条款"""
        salary_type = info.get('salary_type', 'monthly')
        base_salary = info.get('base_salary', 0)
        performance_bonus = info.get('performance_bonus', 0)
        allowances = info.get('allowances', 0)
        pay_day = info.get('pay_day', '15')
        overtime_base = info.get('overtime_calculation_base', 'base_salary')
        
        clause = "三、劳动报酬\n"
        
        if salary_type == 'monthly':
            # 月薪制
            total_salary = base_salary + performance_bonus + allowances
            
            clause += f"""1. 甲乙双方协商确定，工资标准按下列标准执行：
月基本工资：{base_salary}元
绩效奖金：{performance_bonus}元
津贴补贴：{allowances}元
月合计工资：{total_salary}元（税前）

试用期工资标准：基本工资的80%，即{base_salary * 0.8}元，并不得低于本市最低工资标准。

2. 甲方于每月{pay_day}日左右发放工资。
乙方同意，如遇客观情况变化、生产经营困难等，甲方可告知乙方适当推迟工资发放时间，但延迟发放不得超过1个月。

3. 乙方同意，甲方有权根据经营情况、甲方规章制度和乙方的工作内容、工作岗位、工作职务、工作地点、工作业绩、工作表现等因素，调整乙方的劳动报酬，但数额不得低于实际工作所在地的最低工资标准。"""

            # 加班费条款
            clause += """
4. 乙方同意计算加班工资的基数按本条第1款约定的基本工资计算。
甲方在该月工资标准之外另外发放的津贴、补贴、奖金等项目不计算在加班工资的计算基数之内。

5. 乙方若对某月工资、奖金或福利待遇有异议，应在发放之日起3日内向甲方书面提出，逾期未提出的，视为对该月工资、奖金或福利待遇的认可。"""
        
        elif salary_type == 'hourly':
            # 时薪制（非全日制）
            clause += f"""1. 甲乙双方协商确定，小时工资标准为：{base_salary}元/小时
劳动报酬结算支付周期最长不得超过15日。

2. 双方同意，乙方每天工作时间不超过4小时，每周工作时间累计不超过24小时。

3. 乙方的小时工资标准不得低于用人单位所在地人民政府规定的最低小时工资标准。"""
        
        elif salary_type == 'daily':
            # 日薪制
            clause += f"""1. 甲乙双方协商确定，日工资标准为：{base_salary}元/天

2. 工资按实际工作天数计算，每月发放一次。"""
        
        return clause


# 创建实例
salary_skill = SalarySkill()
