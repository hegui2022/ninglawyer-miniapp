"""
合同解除技能
Termination Skill
"""

from typing import Dict, Any, List
from .base import BaseSkill


class TerminationSkill(BaseSkill):
    """合同解除技能 - 处理合同解除和终止"""
    
    def __init__(self):
        super().__init__(
            name="termination",
            description="处理合同解除和终止"
        )
    
    def get_required_fields(self) -> List[str]:
        """获取必填字段"""
        return [
            "has_compensation",      # 是否有经济补偿
            "notice_period",         # 通知期（天）
            "allow_termination",     # 允许单方解除
        ]
    
    def get_prompt_template(self) -> str:
        """获取信息收集提示"""
        return """
请提供合同解除相关信息：

1. 是否约定经济补偿：
   - 是（标准劳动合同通常有经济补偿）
   - 否（非全日制用工通常无经济补偿）

2. 解除通知期：
   - 30天（标准）
   - 15天
   - 7天

3. 是否允许单方解除：
   - 是（双方可协商解除）
   - 否

请根据实际情况选择。
"""
    
    def generate(self, info: Dict[str, Any]) -> str:
        """生成合同解除条款"""
        clause = """十一、违反劳动合同的责任及合同解除、终止

1. 协商解除：
双方协商一致，可以解除本劳动合同。"""

        has_compensation = info.get('has_compensation', True)
        
        if has_compensation:
            clause += """
用人单位依据《劳动合同法》相关规定向劳动者提出解除劳动合同并与劳动者协商一致的，应当依法向劳动者支付经济补偿。"""
        
        clause += """

2. 用人单位单方解除：
乙方具有《劳动合同法》第三十九条、第四十条规定情形之一的，甲方可以依法解除本劳动合同。

3. 劳动者单方解除：
乙方需要解除本劳动合同的，应提前30日以书面形式通知甲方（试用期内提前3日通知）。

4. 合同终止：
本合同期满或双方约定的终止条件出现时，本合同即行终止。"""

        if has_compensation:
            clause += """
符合《劳动合同法》第四十六条规定情形的，甲方应当向乙方支付经济补偿。"""
        
        clause += """

5. 工作交接：
乙方应当按照双方约定或甲方的相关规章制度，办理工作交接，包括但不限于乙方应依据甲方要求交接经办的业务工作、归还当时占有的公司财物和文件资料、结清借款以及签署相关工作交接单等其他相关手续。
双方同意在签署交接单后方视为办结工作交接。"""
        
        return clause


# 创建实例
termination_skill = TerminationSkill()
