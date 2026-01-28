"""
工作内容技能
Work Content Skill
"""

from typing import Dict, Any, List
from .base import BaseSkill


class WorkContentSkill(BaseSkill):
    """工作内容技能 - 处理工作岗位和工作地点"""
    
    def __init__(self):
        super().__init__(
            name="work_content",
            description="处理工作岗位和工作地点"
        )
    
    def get_required_fields(self) -> List[str]:
        """获取必填字段"""
        return [
            "position",             # 工作岗位
            "work_location",        # 工作地点
            "job_responsibilities", # 岗位职责
            "can_change_location",  # 是否可以调整工作地点
        ]
    
    def get_prompt_template(self) -> str:
        """获取信息收集提示"""
        return """
请提供工作内容和岗位信息：

1. 工作岗位（工种）：
   例如：软件工程师、销售经理、行政助理等

2. 工作地点：
   具体地址或城市

3. 岗位职责：
   详细描述工作内容和职责

4. 是否可以调整工作地点：
   - 是（可调动到其他门店或分支机构）
   - 否

请逐项填写。
"""
    
    def generate(self, info: Dict[str, Any]) -> str:
        """生成工作内容条款"""
        position = info.get('position', '')
        work_location = info.get('work_location', '')
        responsibilities = info.get('job_responsibilities', '')
        can_change = info.get('can_change_location', True)
        
        clause = f"""二、工作内容和工作地点
1. 乙方同意在{position}岗位（工种）工作，按时、按质、按量完成该岗位（工种）所承担的各项内容，同时应完成公司或上级交待的其他任务。
乙方同意接受甲方按照制度进行绩效考核，认可考核结果将作为调整乙方岗位、薪酬及判定乙方是否胜任工作的依据。

2. 甲乙双方确认工作地点为{work_location}。"""
        
        # 工作地点调整条款
        if can_change:
            clause += """
甲方在上述工作地点的其他门店、分支机构有需要时，乙方同意服从甲方安排到其他门店或分支机构工作。
如甲方的经营机构搬迁，乙方同意相应变更工作地点。
乙方同意，根据岗位及甲方的经营需要接受到外地出差的安排。"""
        
        # 岗位职责
        if responsibilities:
            clause += f"""

3. 岗位职责：
{responsibilities}"""
        
        return clause


# 创建实例
work_content_skill = WorkContentSkill()
