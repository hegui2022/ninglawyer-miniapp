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
)
from tools.contract_scenarios import (
    StandardLaborContractAgent,
    PartTimeContractAgent,
    InternAgreementAgent,
    RetiredReemploymentAgent,
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
        scores["project"] = sum(1 for kw in keywords_project if kw in user_input)
        scores["dispatch"] = sum(1 for kw in keywords_dispatch if kw in user_input)
        
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
        }
        
        # 技能库
        self.skill_library = {
            "basic_info": basic_info_skill,
            "contract_term": contract_term_skill,
            "work_content": work_content_skill,
            "salary": salary_skill,
            "termination": termination_skill,
        }
        
        # 当前状态
        self.current_scenario = None
        self.collected_info = {}
        self.current_step = 0
    
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

请告诉我你想创建哪种类型的合同？
"""
    
    def _handle_create_contract(self, user_input: str) -> str:
        """处理创建合同请求"""
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

请回复数字或描述你的需求。
"""
        else:
            # 场景已确定，调用对应的代理
            agent = self.scenario_agents.get(self.current_scenario)
            if agent:
                return agent.process(user_input, self.collected_info)
            else:
                return "抱歉，该合同类型暂不支持。"
