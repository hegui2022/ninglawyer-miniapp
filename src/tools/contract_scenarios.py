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
from tools.contract_skills.smart_parser import smart_input_parser


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
    
    def get_step_prompt(self) -> str:
        """获取当前步骤的提示"""
        return self._get_step_prompt()
    
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
        """解析用户输入（使用智能解析器）"""
        # 使用智能解析器
        if step_name == "basic_info":
            return smart_input_parser.parse_basic_info(user_input)
        elif step_name == "contract_term":
            return smart_input_parser.parse_contract_term(user_input)
        elif step_name == "work_content":
            return smart_input_parser.parse_work_content(user_input)
        elif step_name == "salary":
            return smart_input_parser.parse_salary(user_input)
        elif step_name == "termination":
            return smart_input_parser.parse_termination(user_input)
        else:
            return {}
    
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
    
    def get_step_prompt(self) -> str:
        """获取当前步骤的提示"""
        return "非全日制用工合同的信息收集流程与标准劳动合同类似，请按标准流程填写信息。"
    
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
