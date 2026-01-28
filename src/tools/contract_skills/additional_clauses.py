"""
合同附加条款
Contract Additional Clauses - 保密协议、竞业限制、知识产权、自定义条款
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


class BaseClause(ABC):
    """条款基类"""
    
    def __init__(self, clause_name: str, clause_type: str):
        self.clause_name = clause_name
        self.clause_type = clause_type
    
    @abstractmethod
    def get_prompt_template(self) -> str:
        """获取提示模板"""
        pass
    
    @abstractmethod
    def generate(self, data: Dict[str, Any]) -> str:
        """生成条款内容"""
        pass
    
    @abstractmethod
    def get_required_fields(self) -> List[str]:
        """获取必填字段"""
        pass


class ConfidentialityClause(BaseClause):
    """保密协议条款"""
    
    def __init__(self):
        super().__init__("保密协议", "confidentiality")
    
    def get_prompt_template(self) -> str:
        """获取提示模板"""
        return """
是否需要在合同中添加保密协议条款？

保密协议条款通常包括：
1. 保密信息的定义
2. 保密义务
3. 保密期限
4. 违约责任

【选择】
1. 是，需要添加保密协议
2. 否，不需要

如果选择"是"，请提供以下信息：
- 保密期限（如：劳动合同期内及解除后2年）
- 违约金金额（如：人民币10万元）
"""
    
    def generate(self, data: Dict[str, Any]) -> str:
        """生成保密协议条款"""
        confidentiality_period = data.get("confidentiality_period", "劳动合同期内及解除后2年")
        penalty_amount = data.get("penalty_amount", "人民币10万元")
        
        return f"""
## 九、保密义务

1. 乙方在劳动合同期内及解除劳动合同后，对甲方的商业秘密（包括但不限于技术资料、客户信息、经营数据等）承担保密义务。

2. 保密期限：{confidentiality_period}。

3. 乙方不得以任何方式向任何第三方泄露甲方的商业秘密，也不得将商业秘密用于劳动合同以外的目的。

4. 乙方在劳动合同解除或终止后，仍应遵守保密义务，不得利用或泄露在劳动合同期间知悉的甲方商业秘密。

5. 若乙方违反保密义务，应承担违约责任，并赔偿甲方因此遭受的全部损失，违约金为{penalty_amount}。
"""
    
    def get_required_fields(self) -> List[str]:
        return ["confidentiality_period", "penalty_amount"]


class NonCompeteClause(BaseClause):
    """竞业限制条款"""
    
    def __init__(self):
        super().__init__("竞业限制", "non_compete")
    
    def get_prompt_template(self) -> str:
        """获取提示模板"""
        return """
是否需要在合同中添加竞业限制条款？

竞业限制条款适用于接触商业秘密的核心员工，离职后一定期限内不得在同行业竞争企业任职。

【选择】
1. 是，需要添加竞业限制
2. 否，不需要

如果选择"是"，请提供以下信息：
- 竞业限制期限（不得超过2年）
- 竞业限制补偿金（月补偿金额）
- 竞业限制范围（具体的竞争对手或行业）
"""
    
    def generate(self, data: Dict[str, Any]) -> str:
        """生成竞业限制条款"""
        non_compete_period = data.get("non_compete_period", "2年")
        compensation_amount = data.get("compensation_amount", "劳动合同解除前十二个月平均工资的30%")
        non_compete_scope = data.get("non_compete_scope", "与甲方有竞争关系的企业")
        
        return f"""
## 十、竞业限制

1. 乙方在劳动合同解除或终止后，在{non_compete_period}内不得入职与甲方有直接竞争关系的企业，也不得从事与甲方业务相同或相近的工作。

2. 竞业限制范围：{non_compete_scope}。

3. 甲方按月向乙方支付竞业限制补偿金，标准为{compensation_amount}。

4. 乙方违反竞业限制约定的，应停止违约行为，向甲方支付违约金，并赔偿甲方因此遭受的经济损失。违约金金额为竞业限制补偿金总额的2倍。

5. 乙方遵守竞业限制约定的，甲方按月支付竞业限制补偿金；若甲方连续3个月未支付补偿金，乙方可以解除竞业限制约定。
"""
    
    def get_required_fields(self) -> List[str]:
        return ["non_compete_period", "compensation_amount", "non_compete_scope"]


class IntellectualPropertyClause(BaseClause):
    """知识产权条款"""
    
    def __init__(self):
        super().__init__("知识产权", "intellectual_property")
    
    def get_prompt_template(self) -> str:
        """获取提示模板"""
        return """
是否需要在合同中添加知识产权条款？

知识产权条款适用于研发、设计、创作类岗位，明确在职期间产生的知识产权归属。

【选择】
1. 是，需要添加知识产权条款
2. 否，不需要

如果选择"是"，请提供以下信息：
- 知识产权范围（如：软件、设计、文档、专利等）
- 使用权限说明（如：甲方拥有全部知识产权，乙方享有署名权）
"""
    
    def generate(self, data: Dict[str, Any]) -> str:
        """生成知识产权条款"""
        ip_scope = data.get("ip_scope", "软件、设计、文档、技术方案、专利申请等")
        usage_rights = data.get("usage_rights", "甲方拥有全部知识产权，乙方享有署名权")
        
        return f"""
## 十一、知识产权

1. 乙方在劳动合同期间，因履行职务或利用甲方物质技术条件所完成的发明创造、作品、技术方案、软件、设计、文档等（统称"职务成果"），其知识产权全部归甲方所有。

2. 职务成果范围包括：{ip_scope}。

3. 乙方有义务配合甲方申请专利、软件著作权、商标等知识产权登记，甲方有权使用、转让、许可第三方使用上述职务成果。

4. 知识产权使用权限：{usage_rights}。

5. 乙方违反本条款约定，将职务成果据为己有或向第三方泄露的，应承担违约责任，并赔偿甲方因此遭受的全部损失。
"""
    
    def get_required_fields(self) -> List[str]:
        return ["ip_scope", "usage_rights"]


class CustomClause(BaseClause):
    """自定义条款"""
    
    def __init__(self):
        super().__init__("自定义条款", "custom")
    
    def get_prompt_template(self) -> str:
        """获取提示模板"""
        return """
是否需要添加自定义条款？

自定义条款可以根据双方的实际情况和特殊需求进行添加，如特殊福利、培训协议、住房补贴等。

【选择】
1. 是，需要添加自定义条款
2. 否，不需要

如果选择"是"，请提供以下信息：
- 条款标题（如：培训协议）
- 条款内容（详细的条款文字）
"""
    
    def generate(self, data: Dict[str, Any]) -> str:
        """生成自定义条款"""
        clause_title = data.get("clause_title", "其他约定")
        clause_content = data.get("clause_content", "")
        
        return f"""
## {clause_title}

{clause_content}
"""
    
    def get_required_fields(self) -> List[str]:
        return ["clause_title", "clause_content"]


class AdditionalClausesManager:
    """附加条款管理器"""
    
    def __init__(self):
        self.available_clauses = {
            "confidentiality": ConfidentialityClause(),
            "non_compete": NonCompeteClause(),
            "intellectual_property": IntellectualPropertyClause(),
            "custom": CustomClause(),
        }
        self.selected_clauses = []
        self.clause_data = {}
    
    def get_available_clauses(self) -> Dict[str, BaseClause]:
        """获取可用的条款列表"""
        return self.available_clauses
    
    def select_clause(self, clause_type: str) -> BaseClause:
        """选择条款"""
        if clause_type in self.available_clauses:
            return self.available_clauses[clause_type]
        return None
    
    def add_clause(self, clause_type: str, data: Dict[str, Any]):
        """添加条款"""
        self.selected_clauses.append(clause_type)
        self.clause_data[clause_type] = data
    
    def generate_all_clauses(self) -> str:
        """生成所有已选择的条款"""
        if not self.selected_clauses:
            return ""
        
        clauses_text = ""
        for clause_type in self.selected_clauses:
            if clause_type in self.available_clauses and clause_type in self.clause_data:
                clause = self.available_clauses[clause_type]
                data = self.clause_data[clause_type]
                clauses_text += clause.generate(data)
                clauses_text += "\n\n"
        
        return clauses_text
    
    def get_clause_count(self) -> int:
        """获取已选择的条款数量"""
        return len(self.selected_clauses)
    
    def clear_clauses(self):
        """清空已选择的条款"""
        self.selected_clauses = []
        self.clause_data = {}


# 创建实例
additional_clauses_manager = AdditionalClausesManager()
