"""
合同起草总调度器
Contract Drafting Master Dispatcher
"""

from typing import Dict, Any, Optional
from tools.contract_skills import (
    basic_info_skill,
    contract_term_skill,
    work_content_skill,
    salary_skill,
    termination_skill,
    AdditionalClausesManager,
)
from tools.contract_scenarios import (
    StandardLaborContractAgent,
    PartTimeContractAgent,
    InternAgreementAgent,
    RetiredReemploymentAgent,
    ProjectContractAgent,
    DispatchContractAgent,
)


class IntentRecognizer:
    """意图识别器"""
    
    INTENTS = {
        "create_contract": "创建新合同",
        "modify_contract": "修改现有合同",
        "consult_questions": "咨询问题",
        "get_templates": "获取模板列表",
    }
    
    def recognize(self, user_input: str) -> str:
        """
        识别用户意图
        
        Args:
            user_input: 用户输入
            
        Returns:
            意图类型
        """
        keywords_create = ["签", "起草", "生成", "创建", "制定", "合同"]
        keywords_modify = ["修改", "更改", "调整", "编辑"]
        keywords_consult = ["咨询", "问", "如何", "什么是"]
        keywords_templates = ["模板", "类型", "种类", "有哪些"]
        
        for keyword in keywords_create:
            if keyword in user_input:
                return "create_contract"
        
        for keyword in keywords_modify:
            if keyword in user_input:
                return "modify_contract"
        
        for keyword in keywords_consult:
            if keyword in user_input:
                return "consult_questions"
        
        for keyword in keywords_templates:
            if keyword in user_input:
                return "get_templates"
        
        # 默认返回创建合同
        return "create_contract"


class ScenarioClassifier:
    """场景分类器"""
    
    SCENARIOS = {
        "standard": "标准全职劳动合同",
        "parttime": "非全日制用工合同",
        "intern": "实习生协议",
        "retired": "退休返聘协议",
        "project": "项目制合同",
        "dispatch": "劳务派遣合同",
    }
    
    def classify(self, user_input: str, intent: str) -> tuple:
        """
        分类场景
        
        Args:
            user_input: 用户输入
            intent: 用户意图
            
        Returns:
            (场景类型, 确信度)
        """
        if intent != "create_contract":
            return None, 0.0
        
        # 关键词匹配
        keywords_standard = ["全职", "固定期限", "无固定期限", "标准", "正式"]
        keywords_parttime = ["兼职", "非全日制", "小时工", "钟点工", "4小时", "24小时"]
        keywords_intern = ["实习", "实习生", "在校生", "学生"]
        keywords_retired = ["退休", "返聘", "已退休"]
        keywords_project = ["项目", "完工", "阶段性"]
        keywords_dispatch = ["派遣", "劳务派遣", "外包", "三方"]
        
        # 计算匹配分数
        scores = {}
        scores["standard"] = sum(1 for kw in keywords_standard if kw in user_input)
        scores["parttime"] = sum(1 for kw in keywords_parttime if kw in user_input) * 2  # 权重更高
        scores["intern"] = sum(1 for kw in keywords_intern if kw in user_input) * 2  # 权重提高
        scores["retired"] = sum(1 for kw in keywords_retired if kw in user_input) * 2  # 权重提高
        scores["project"] = sum(1 for kw in keywords_project if kw in user_input) * 2  # 权重提高
        scores["dispatch"] = sum(1 for kw in keywords_dispatch if kw in user_input) * 2  # 权重提高
        
        # 找到最高分
        max_score = max(scores.values())
        
        if max_score == 0:
            # 没有匹配，需要询问用户
            return None, 0.0
        
        # 找到对应的场景
        for scenario, score in scores.items():
            if score == max_score:
                # 提高确信度计算
                confidence = min(score * 0.5, 1.0)
                return scenario, confidence
        
        return None, 0.0


class ContractDraftingMaster:
    """合同起草总调度器"""
    
    def __init__(self, ctx=None):
        """
        初始化总调度器
        
        Args:
            ctx: 上下文
        """
        self.ctx = ctx
        self.intent_recognizer = IntentRecognizer()
        self.scenario_classifier = ScenarioClassifier()
        
        # 初始化场景代理
        self.scenario_agents = {
            "standard": StandardLaborContractAgent(),
            "parttime": PartTimeContractAgent(),
            "intern": InternAgreementAgent(),
            "retired": RetiredReemploymentAgent(),
            "project": ProjectContractAgent(),
            "dispatch": DispatchContractAgent(),
        }
        
        # 技能库
        self.skill_library = {
            "basic_info": basic_info_skill,
            "contract_term": contract_term_skill,
            "work_content": work_content_skill,
            "salary": salary_skill,
            "termination": termination_skill,
        }
        
        # 附加条款管理器
        self.additional_clauses = AdditionalClausesManager()
        
        # 当前状态
        self.current_scenario = None
        self.collected_info = {}
        self.current_step = 0
        self.waiting_for_additional_clauses = False  # 是否等待附加条款输入
    
    def process(self, user_input: str) -> str:
        """
        处理用户请求
        
        Args:
            user_input: 用户输入
            
        Returns:
            处理结果
        """
        # 1. 意图识别
        intent = self.intent_recognizer.recognize(user_input)
        
        # 2. 根据意图处理
        if intent == "get_templates":
            return self._get_templates()
        
        elif intent == "create_contract":
            return self._handle_create_contract(user_input)
        
        else:
            return "抱歉，当前只支持创建合同功能。"
    
    def _get_templates(self) -> str:
        """获取模板列表"""
        return """
## 可用的合同类型

1. **标准全职劳动合同** - 全日制用工，固定期限或无固定期限
2. **非全日制用工合同** - 每天不超过4小时，每周不超过24小时
3. **实习协议** - 适用于在校学生实习，有实习补贴和意外保险
4. **退休返聘协议** - 适用于退休人员返聘，劳务关系而非劳动关系
5. **项目制合同** - 以完成项目为期限，灵活安排
6. **劳务派遣合同** - 三方关系，派遣单位、用工单位、劳动者

请告诉我你想创建哪种类型的合同？
"""
    
    def _handle_create_contract(self, user_input: str) -> str:
        """处理创建合同请求"""
        
        # 处理附加条款输入
        if self.waiting_for_additional_clauses:
            return self._handle_additional_clauses(user_input)
        
        # 如果还没有确定场景
        if self.current_scenario is None:
            # 场景分类
            scenario, confidence = self.scenario_classifier.classify(user_input, "create_contract")
            
            if scenario and confidence > 0.5:
                # 场景明确
                self.current_scenario = scenario
                agent = self.scenario_agents.get(scenario)
                if agent:
                    return agent.start(user_input)
            else:
                # 场景不明确，询问用户
                return """
请问你想创建哪种类型的合同？

1. **标准全职劳动合同** - 适用于正式员工，有试用期，缴纳社保
2. **非全日制用工合同** - 适用于兼职，每天不超过4小时
3. **实习协议** - 适用于在校学生实习，有实习补贴和意外保险
4. **退休返聘协议** - 适用于退休人员返聘，不缴纳社保
5. **项目制合同** - 适用于项目制合作，以完成项目为期限
6. **劳务派遣合同** - 适用于劳务派遣，三方关系

请回复数字或描述你的需求。
"""
        else:
            # 场景已确定，调用对应的代理
            agent = self.scenario_agents.get(self.current_scenario)
            if agent:
                result = agent.process(user_input, self.collected_info)
                
                # 检查是否合同生成完成
                if "合同已生成" in result or "协议已生成" in result:
                    # 询问是否需要添加附加条款
                    self.waiting_for_additional_clauses = True
                    return result + "\n\n" + self._get_additional_clauses_prompt()
                
                return result
            else:
                return "抱歉，该合同类型暂不支持。"
    
    def _get_additional_clauses_prompt(self) -> str:
        """获取附加条款选择提示"""
        return """
## 📋 添加附加条款

是否需要在合同中添加附加条款？

1. **保密协议** - 约定双方对商业秘密的保密义务
2. **竞业限制** - 限制离职后在竞争对手处工作（需支付补偿金）
3. **知识产权** - 明确职务成果的知识产权归属
4. **自定义条款** - 根据双方特殊需求添加条款
5. **跳过附加条款** - 不添加，直接完成合同

请回复数字选择，或输入"完成"跳过。
"""
    
    def _handle_additional_clauses(self, user_input: str) -> str:
        """处理附加条款选择"""
        user_input = user_input.strip()
        
        # 检查是否完成或跳过
        if user_input in ["完成", "跳过", "5", "no"]:
            self.waiting_for_additional_clauses = False
            
            # 生成最终的合同（包含附加条款）
            return "合同已完成！你可以选择导出为 Word 或 PDF 格式。"
        
        # 处理附加条款选择
        clause_mapping = {
            "1": "confidentiality",
            "2": "non_compete",
            "3": "intellectual_property",
            "4": "custom",
        }
        
        if user_input in clause_mapping:
            clause_type = clause_mapping[user_input]
            clause = self.additional_clauses.select_clause(clause_type)
            
            if clause:
                return f"""
## {clause.clause_name}

{clause.get_prompt_template()}

请填写相关信息，或回复"返回"回到附加条款选择。
"""
        
        # 尝试解析附加条款信息（简化处理）
        # 在实际应用中，这里应该使用智能解析器解析用户输入
        
        return "请选择附加条款类型，或输入'完成'跳过。"
