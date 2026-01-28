"""
合同期限技能
Contract Term Skill
"""

from typing import Dict, Any, List
from .base import BaseSkill


class ContractTermSkill(BaseSkill):
    """合同期限技能 - 处理合同期限和试用期"""
    
    def __init__(self):
        super().__init__(
            name="contract_term",
            description="处理合同期限和试用期"
        )
    
    def get_required_fields(self) -> List[str]:
        """获取必填字段"""
        return [
            "contract_type",        # 合同类型：fixed_term/no_fixed_term/task_based
            "start_date",           # 合同开始日期
            "end_date",             # 合同结束日期（固定期限）
            "has_probation",        # 是否约定试用期
            "probation_start_date", # 试用期开始日期
            "probation_end_date",   # 试用期结束日期
            "probation_salary_ratio",  # 试用期工资比例（80%）
        ]
    
    def get_prompt_template(self) -> str:
        """获取信息收集提示"""
        return """
请提供合同期限相关信息：

1. 合同期限类型：
   - 固定期限合同
   - 无固定期限合同
   - 完成一定工作任务为期限

2. 合同开始日期：
   格式：YYYY年MM月DD日

3. 合同结束日期（如果是固定期限）：
   格式：YYYY年MM月DD日

4. 是否约定试用期：
   - 是
   - 否

5. 如果有试用期：
   - 试用期开始日期：YYYY年MM月DD日
   - 试用期结束日期：YYYY年MM月DD日
   - 试用期工资：基本工资的80%

请根据实际情况填写。
"""
    
    def generate(self, info: Dict[str, Any]) -> str:
        """生成合同期限条款"""
        contract_type = info.get('contract_type', 'fixed_term')
        has_probation = info.get('has_probation', False)
        
        clause = "一、劳动合同期限\n"
        
        if contract_type == 'fixed_term':
            start_date = info.get('start_date', '')
            end_date = info.get('end_date', '')
            clause += f"""
（一）本合同为固定期限的劳动合同。
合同期从 {start_date} 至 {end_date}。"""
        elif contract_type == 'no_fixed_term':
            clause += """
（一）本合同为无固定期限劳动合同。"""
        elif contract_type == 'task_based':
            task = info.get('task_description', '')
            clause += f"""
（一）本合同为以完成一定工作任务为期限的合同。
工作任务为：{task}。
乙方同意，甲方有权根据工作任务完成及收尾工作的需要安排合同终止的具体时间。"""
        
        # 试用期条款
        if has_probation and contract_type != 'parttime':
            probation_start = info.get('probation_start_date', '')
            probation_end = info.get('probation_end_date', '')
            probation_ratio = info.get('probation_salary_ratio', '80%')
            
            clause += f"""
其中试用期从 {probation_start} 至 {probation_end}。
试用期工资标准为基本工资的 {probation_ratio}，并不得低于本市最低工资标准。"""
        
        return clause.strip()


# 创建实例
contract_term_skill = ContractTermSkill()
