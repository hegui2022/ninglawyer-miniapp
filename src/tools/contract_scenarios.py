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
from tools.contract_skills.intern_skills import (
    intern_info_skill,
    intern_term_skill,
    intern_content_skill,
    intern_allowance_skill,
    intern_insurance_skill,
    intern_termination_skill,
)
from tools.contract_skills.retired_skills import (
    retired_info_skill,
    retired_term_skill,
    retired_content_skill,
    retired_payment_skill,
    retired_termination_skill,
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
        # 暂时复用标准劳动合同的逻辑
        standard_agent = StandardLaborContractAgent()
        standard_agent.current_step = self.current_step
        standard_agent.collected_info = collected_info
        standard_agent.collected_info["contract_type"] = "parttime"
        
        result = standard_agent.process(user_input, standard_agent.collected_info)
        
        return result
    
    def _generate_contract(self) -> str:
        """生成非全日制用工合同"""
        return "非全日制用工合同生成中..."


class InternAgreementAgent(BaseScenarioAgent):
    """实习协议代理"""
    
    def __init__(self):
        super().__init__("intern")
        self.steps = [
            ("intern_info", "实习基本信息", intern_info_skill),
            ("intern_term", "实习期限", intern_term_skill),
            ("intern_content", "实习内容", intern_content_skill),
            ("intern_allowance", "实习补贴", intern_allowance_skill),
            ("intern_insurance", "实习保险", intern_insurance_skill),
            ("intern_termination", "实习终止", intern_termination_skill),
        ]
        self.current_step = 0
        self.collected_info = {}
    
    def get_step_prompt(self) -> str:
        """获取当前步骤的提示"""
        if self.current_step >= len(self.steps):
            return self._generate_contract()
        
        step_name, step_title, skill = self.steps[self.current_step]
        prompt = skill.get_prompt_template()
        
        return f"""
## 📝 {step_title}

{prompt}
"""
    
    def start(self, user_input: str) -> str:
        """开始收集信息"""
        return self.get_step_prompt()
    
    def process(self, user_input: str, collected_info: Dict[str, Any]) -> str:
        """处理用户输入"""
        # 保存已收集的信息
        self.collected_info = collected_info
        
        # 处理当前步骤的输入
        if self.current_step < len(self.steps):
            step_name, step_title, skill = self.steps[self.current_step]
            
            # 解析用户输入（简化处理）
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
        
        return "实习协议已生成！"
    
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
    
    def _parse_input(self, user_input: str, step_name: str) -> Dict[str, Any]:
        """解析用户输入"""
        # 简化处理，实际应该使用智能解析器
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
                
                if step_name == "intern_info":
                    if "单位名称" in key:
                        result["employer_name"] = value
                    elif "单位地址" in key:
                        result["employer_address"] = value
                    elif "联系人" in key:
                        result["employer_contact"] = value
                    elif "联系电话" in key and "单位" in user_input[:20]:
                        result["employer_phone"] = value
                    elif "姓名" in key:
                        result["intern_name"] = value
                    elif "学校" in key:
                        result["school_name"] = value
                    elif "专业" in key:
                        result["major"] = value
                    elif "学号" in key:
                        result["student_id"] = value
                    elif "电话" in key:
                        result["phone"] = value
                    elif "紧急联系人" in key:
                        result["emergency_contact"] = value
                
                elif step_name == "intern_term":
                    if "开始日期" in key:
                        result["start_date"] = value
                    elif "结束日期" in key:
                        result["end_date"] = value
                    elif "实习地点" in key:
                        result["location"] = value
                
                elif step_name == "intern_content":
                    if "实习岗位" in key:
                        result["position"] = value
                    elif "工作内容" in key:
                        result["job_content"] = value
                    elif "指导老师" in key:
                        result["mentor"] = value
                
                elif step_name == "intern_allowance":
                    if "实习补贴" in key:
                        result["allowance"] = value
                    elif "发放方式" in key:
                        result["payment_method"] = value
                    elif "发放日期" in key:
                        result["pay_day"] = value
                
                elif step_name == "intern_insurance":
                    if "保险金额" in key:
                        result["insurance_amount"] = value
                
                elif step_name == "intern_termination":
                    if "提前" in key and "天" in value:
                        import re
                        match = re.search(r'(\d+)', value)
                        if match:
                            result["notice_days"] = match.group(1)
        
        return result
    
    def _generate_contract(self) -> str:
        """生成实习协议"""
        contract_parts = []
        
        contract_parts.append("# 实习协议\n\n")
        contract_parts.append(intern_info_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(intern_term_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(intern_content_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(intern_allowance_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(intern_insurance_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(intern_termination_skill.generate(self.collected_info))
        
        contract_parts.append("\n\n七、其他\n\n")
        contract_parts.append("1. 本协议一式两份，甲乙双方各执一份。\n")
        contract_parts.append("2. 本协议未尽事宜，双方可另行协商补充。\n")
        contract_parts.append("3. 乙方在实习期间应遵守甲方规章制度，保守甲方商业秘密。\n\n")
        contract_parts.append("甲方（盖章）：__________\n\n")
        contract_parts.append("乙方（签字）：__________\n\n")
        contract_parts.append(f"签订日期：__________年____月____日\n")
        
        # 重置状态
        self.current_step = 0
        self.collected_info = {}
        
        return "".join(contract_parts)


class RetiredReemploymentAgent(BaseScenarioAgent):
    """退休返聘协议代理"""
    
    def __init__(self):
        super().__init__("retired")
        self.steps = [
            ("retired_info", "返聘基本信息", retired_info_skill),
            ("retired_term", "返聘期限", retired_term_skill),
            ("retired_content", "工作内容", retired_content_skill),
            ("retired_payment", "劳务报酬", retired_payment_skill),
            ("retired_termination", "协议终止", retired_termination_skill),
        ]
        self.current_step = 0
        self.collected_info = {}
    
    def get_step_prompt(self) -> str:
        """获取当前步骤的提示"""
        if self.current_step >= len(self.steps):
            return self._generate_contract()
        
        step_name, step_title, skill = self.steps[self.current_step]
        prompt = skill.get_prompt_template()
        
        return f"""
## 📝 {step_title}

{prompt}
"""
    
    def start(self, user_input: str) -> str:
        """开始收集信息"""
        return self.get_step_prompt()
    
    def process(self, user_input: str, collected_info: Dict[str, Any]) -> str:
        """处理用户输入"""
        # 保存已收集的信息
        self.collected_info = collected_info
        
        # 处理当前步骤的输入
        if self.current_step < len(self.steps):
            step_name, step_title, skill = self.steps[self.current_step]
            
            # 解析用户输入（简化处理）
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
        
        return "退休返聘协议已生成！"
    
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
    
    def _parse_input(self, user_input: str, step_name: str) -> Dict[str, Any]:
        """解析用户输入"""
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
                
                if step_name == "retired_info":
                    if "单位名称" in key:
                        result["employer_name"] = value
                    elif "单位地址" in key:
                        result["employer_address"] = value
                    elif "联系人" in key:
                        result["employer_contact"] = value
                    elif "联系电话" in key and "用工单位" in user_input[:20]:
                        result["employer_phone"] = value
                    elif "姓名" in key:
                        result["retiree_name"] = value
                    elif "身份证" in key:
                        result["id_card"] = value
                    elif "退休证" in key:
                        result["retirement_certificate"] = value
                    elif "原工作单位" in key:
                        result["former_employer"] = value
                    elif "住址" in key:
                        result["address"] = value
                    elif "电话" in key:
                        result["phone"] = value
                    elif "紧急联系人" in key:
                        result["emergency_contact"] = value
                
                elif step_name == "retired_term":
                    if "开始日期" in key:
                        result["start_date"] = value
                    elif "结束日期" in key:
                        result["end_date"] = value
                    elif "工作地点" in key:
                        result["location"] = value
                
                elif step_name == "retired_content":
                    if "工作岗位" in key:
                        result["position"] = value
                    elif "工作职责" in key:
                        result["job_responsibilities"] = value
                
                elif step_name == "retired_payment":
                    if "劳务报酬" in key:
                        result["payment"] = value
                    elif "支付方式" in key:
                        result["payment_method"] = value
                    elif "支付日期" in key:
                        result["pay_day"] = value
                    elif "交通补贴" in key:
                        result["transport_allowance"] = value
                    elif "餐饮补贴" in key:
                        result["meal_allowance"] = value
                    elif "代扣代缴" in value:
                        result["withhold_tax"] = True
                
                elif step_name == "retired_termination":
                    if "提前" in key and "天" in value:
                        import re
                        match = re.search(r'(\d+)', value)
                        if match:
                            result["notice_days"] = match.group(1)
                    elif "有经济补偿" in value or "经济补偿" in key and "是" in value:
                        result["has_compensation"] = True
        
        return result
    
    def _generate_contract(self) -> str:
        """生成退休返聘协议"""
        contract_parts = []
        
        contract_parts.append("# 退休返聘协议\n\n")
        contract_parts.append(retired_info_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(retired_term_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(retired_content_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(retired_payment_skill.generate(self.collected_info))
        contract_parts.append("\n\n")
        contract_parts.append(retired_termination_skill.generate(self.collected_info))
        
        contract_parts.append("\n\n六、其他\n\n")
        contract_parts.append("1. 本协议为劳务协议，不属于劳动合同，不适用劳动法及相关社会保险制度。\n")
        contract_parts.append("2. 乙方应遵守甲方规章制度，保守甲方商业秘密。\n")
        contract_parts.append("3. 乙方在返聘期间因工作原因发生人身损害，甲方应承担相应责任。\n")
        contract_parts.append("4. 本协议一式两份，甲乙双方各执一份。\n\n")
        contract_parts.append("甲方（盖章）：__________\n\n")
        contract_parts.append("乙方（签字）：__________\n\n")
        contract_parts.append(f"签订日期：__________年____月____日\n")
        
        # 重置状态
        self.current_step = 0
        self.collected_info = {}
        
        return "".join(contract_parts)
