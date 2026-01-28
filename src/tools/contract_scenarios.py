"""
合同场景代理
Contract Scenario Agents
"""

from typing import Dict, Any
from tools.contract_skills import (
    basic_info_skill,
    contract_term_skill,
    work_content_skill,
    salary_skill,
    termination_skill,
)


class BaseScenarioAgent:
    """场景代理基类"""
    
    def __init__(self, scenario: str):
        self.scenario = scenario
        self.current_step = 0
        self.collected_info = {}
    
    def get_step_prompt(self) -> str:
        """获取当前步骤的提示"""
        raise NotImplementedError
    
    def start(self, user_input: str) -> str:
        """开始收集信息"""
        return self.get_step_prompt()
    
    def process(self, user_input: str, collected_info: Dict[str, Any]) -> str:
        """处理用户输入"""
        raise NotImplementedError


class StandardLaborContractAgent(BaseScenarioAgent):
    """标准劳动合同代理"""
    
    def __init__(self):
        super().__init__("standard")
        self.steps = [
            ("basic_info", "基本信息", basic_info_skill),
            ("contract_term", "合同期限", contract_term_skill),
            ("work_content", "工作内容", work_content_skill),
            ("salary", "劳动报酬", salary_skill),
            ("termination", "合同解除", termination_skill),
        ]
        self.current_step = 0
        self.collected_info = {}
    
    def _get_step_prompt(self) -> str:
        """获取当前步骤的提示"""
        if self.current_step >= len(self.steps):
            return self._generate_contract()
        
        step_name, step_title, skill = self.steps[self.current_step]
        prompt = skill.get_prompt_template()
        
        return f"""
## 📝 {step_title}

{prompt}
"""
    
    def process(self, user_input: str, collected_info: Dict[str, Any]) -> str:
        """处理用户输入"""
        # 保存已收集的信息
        self.collected_info = collected_info
        
        # 处理当前步骤的输入
        if self.current_step < len(self.steps):
            step_name, step_title, skill = self.steps[self.current_step]
            
            # 解析用户输入（这里简化处理，实际应该使用 LLM）
            parsed_info = self._parse_input(user_input, step_name)
            self.collected_info.update(parsed_info)
            
            # 移动到下一步
            self.current_step += 1
            
            if self.current_step >= len(self.steps):
                # 所有信息收集完成，生成合同
                return self._generate_contract()
            else:
                # 继续收集下一步
                return self._get_step_prompt()
        
        return "合同已生成！"
    
    def _parse_input(self, user_input: str, step_name: str) -> Dict[str, Any]:
        """解析用户输入（简化版）"""
        # 这里应该使用 LLM 来解析，暂时简化处理
        result = {}
        
        lines = user_input.split('\n')
        for line in lines:
            if '：' in line or ':' in line:
                if '：' in line:
                    key, value = line.split('：', 1)
                else:
                    key, value = line.split(':', 1)
                
                key = key.strip()
                value = value.strip()
                
                # 根据步骤名称映射字段
                if step_name == "basic_info":
                    mapping = {
                        "单位名称": "employer_name",
                        "单位地址": "employer_address",
                        "法定代表人": "employer_legal_rep",
                        "联系电话": "employer_contact",
                        "姓名": "employee_name",
                        "身份证号码": "employee_id",
                        "住址": "employee_address",
                        "紧急联系人": "employee_emergency_contact",
                    }
                    if key in mapping:
                        result[mapping[key]] = value
                
                elif step_name == "contract_term":
                    if "开始日期" in key:
                        result["start_date"] = value
                    elif "结束日期" in key:
                        result["end_date"] = value
                    elif "合同类型" in key:
                        if "固定" in value:
                            result["contract_type"] = "fixed_term"
                        elif "无固定" in value:
                            result["contract_type"] = "no_fixed_term"
                    elif "试用期" in key and ("是" in value or "有" in value):
                        result["has_probation"] = True
                
                elif step_name == "work_content":
                    if "岗位" in key:
                        result["position"] = value
                    elif "地点" in key:
                        result["work_location"] = value
                    elif "职责" in key:
                        result["job_responsibilities"] = value
                
                elif step_name == "salary":
                    if "基本工资" in key:
                        result["base_salary"] = value
                    elif "发薪日" in key:
                        result["pay_day"] = value
                    result["salary_type"] = "monthly"
                    result["performance_bonus"] = 0
                    result["allowances"] = 0
        
        return result
    
    def _generate_contract(self) -> str:
        """生成合同"""
        contract_parts = []
        
        contract_parts.append("# 劳动合同\n")
        contract_parts.append(basic_info_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(contract_term_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(work_content_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(salary_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        
        # 添加社会保险条款（标准劳动合同必备）
        contract_parts.append("""
四、社会保险

1. 甲方应按国家和地方有关规定为乙方缴纳基本养老保险、基本医疗保险、失业保险、工伤保险、生育保险等社会保险费。
其中乙方应缴纳的部分，由甲方从乙方的工资中代扣代缴。

2. 乙方同意按甲方规定参加社会保险，并按甲方要求提供参加社会保险所必需的真实、合法、完整的资料。
""")
        
        contract_parts.append("\n\n")
        contract_parts.append(termination_skill.generate(self.collected_info))
        
        contract_parts.append("\n\n十二、其他\n\n")
        contract_parts.append("本合同一式两份，甲乙双方各执一份，具有同等法律效力。\n\n")
        contract_parts.append("甲方（盖章）：__________\n\n")
        contract_parts.append("乙方（签字）：__________\n\n")
        contract_parts.append(f"签订日期：__________年____月____日\n")
        
        # 重置状态
        self.current_step = 0
        self.collected_info = {}
        
        return "".join(contract_parts)


class PartTimeContractAgent(BaseScenarioAgent):
    """非全日制用工合同代理"""
    
    def __init__(self):
        super().__init__("parttime")
        self.steps = [
            ("basic_info", "基本信息", basic_info_skill),
            ("contract_term", "合同期限", contract_term_skill),
            ("work_content", "工作内容", work_content_skill),
            ("salary", "劳动报酬", salary_skill),
            ("termination", "合同解除", termination_skill),
        ]
        self.current_step = 0
        self.collected_info = {}
    
    def start(self, user_input: str) -> str:
        """开始收集信息"""
        return self.get_step_prompt()
    
    def process(self, user_input: str, collected_info: Dict[str, Any]) -> str:
        """处理用户输入"""
        # 非全日制用工合同的流程与标准劳动合同类似，但有一些特殊处理
        # 这里可以添加非全日制特有的逻辑
        
        # 暂时复用标准劳动合同的逻辑
        standard_agent = StandardLaborContractAgent()
        standard_agent.current_step = self.current_step
        standard_agent.collected_info = collected_info
        standard_agent.collected_info["contract_type"] = "parttime"
        
        result = standard_agent.process(user_input, standard_agent.collected_info)
        
        return result
    
    def _generate_contract(self) -> str:
        """生成非全日制用工合同"""
        # 可以在这里添加非全日制特有的条款
        return "非全日制用工合同生成中..."
