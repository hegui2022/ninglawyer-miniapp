"""
基本信息技能
Basic Information Skill
"""

from typing import Dict, Any, List
from .base import BaseSkill


class BasicInfoSkill(BaseSkill):
    """基本信息技能 - 处理甲乙双方基本信息"""
    
    def __init__(self):
        super().__init__(
            name="basic_info",
            description="处理甲乙双方基本信息"
        )
    
    def get_required_fields(self) -> List[str]:
        """获取必填字段"""
        return [
            "employer_name",        # 用人单位名称
            "employer_address",     # 用人单位地址
            "employer_legal_rep",   # 法定代表人
            "employer_contact",     # 联系电话
            
            "employee_name",        # 劳动者姓名
            "employee_id",          # 身份证号码
            "employee_address",     # 住址
            "employee_contact",     # 联系电话
            "employee_emergency_contact",  # 紧急联系人
        ]
    
    def get_prompt_template(self) -> str:
        """获取信息收集提示"""
        return """
请提供以下双方基本信息：

【用人单位信息】
1. 单位名称：
2. 单位地址：
3. 法定代表人：
4. 联系电话：

【劳动者信息】
1. 姓名：
2. 身份证号码：
3. 住址：
4. 联系电话：
5. 紧急联系人及电话：

请逐项填写，我会根据你的输入生成合同条款。
"""
    
    def generate(self, info: Dict[str, Any]) -> str:
        """生成基本信息条款"""
        clause = f"""
        甲方（用人单位）：
        名称：{info.get('employer_name', '')}
        住所：{info.get('employer_address', '')}
        法定代表人：{info.get('employer_legal_rep', '')}
        联系电话：{info.get('employer_contact', '')}

        乙方（劳动者）：
        姓名：{info.get('employee_name', '')}
        身份证号码：{info.get('employee_id', '')}
        住址：{info.get('employee_address', '')}
        联系电话：{info.get('employee_contact', '')}
        紧急联系人：{info.get('employee_emergency_contact', '')}
        """
        return clause.strip()


# 创建实例
basic_info_skill = BasicInfoSkill()
