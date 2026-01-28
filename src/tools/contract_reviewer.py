"""
合同审查工具
Contract Review Tool - 自动识别合同中的风险点，生成审查报告
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
import os
import re
from enum import Enum


class RiskLevel(Enum):
    """风险等级"""
    HIGH = "高风险"      # 可能导致重大法律后果
    MEDIUM = "中风险"    # 需要特别注意
    LOW = "低风险"      # 轻微问题，建议修改
    INFO = "提示"       # 非风险，仅提示


class RiskPoint:
    """风险点"""
    
    def __init__(
        self,
        risk_id: str,
        title: str,
        level: RiskLevel,
        description: str,
        location: str = "",
        suggestion: str = ""
    ):
        self.risk_id = risk_id
        self.title = title
        self.level = level
        self.description = description
        self.location = location
        self.suggestion = suggestion
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "risk_id": self.risk_id,
            "title": self.title,
            "level": self.level.value,
            "description": self.description,
            "location": self.location,
            "suggestion": self.suggestion,
        }


class ContractReviewRule:
    """合同审查规则"""
    
    def __init__(self, rule_id: str, name: str, rule_type: str):
        self.rule_id = rule_id
        self.name = name
        self.rule_type = rule_type
    
    def check(self, contract_text: str) -> List[RiskPoint]:
        """检查合同"""
        raise NotImplementedError


class BasicInfoRule(ContractReviewRule):
    """基本信息检查规则"""
    
    def __init__(self):
        super().__init__("basic_info", "基本信息完整性检查", "basic")
    
    def check(self, contract_text: str) -> List[RiskPoint]:
        """检查基本信息"""
        risks = []
        
        # 检查用人单位名称
        if not re.search(r'(用人单位|甲方).*?[:：]\s*([^，。\n]+)', contract_text):
            risks.append(RiskPoint(
                risk_id="B001",
                title="用人单位信息缺失",
                level=RiskLevel.HIGH,
                description="合同中未明确用人单位名称",
                suggestion="请在合同中明确填写用人单位的全称"
            ))
        
        # 检查劳动者信息
        if not re.search(r'(劳动者|乙方).*?[:：]\s*([^，。\n]+)', contract_text):
            risks.append(RiskPoint(
                risk_id="B002",
                title="劳动者信息缺失",
                level=RiskLevel.HIGH,
                description="合同中未明确劳动者姓名",
                suggestion="请在合同中明确填写劳动者姓名"
            ))
        
        # 检查身份证号
        if not re.search(r'身份证.*?[:：]\s*([1-9]\d{16}[\dXx])', contract_text):
            risks.append(RiskPoint(
                risk_id="B003",
                title="身份证号缺失或格式错误",
                level=RiskLevel.HIGH,
                description="合同中未填写劳动者身份证号，或身份证号格式不正确",
                suggestion="请填写正确的18位身份证号码"
            ))
        
        return risks


class ContractTermRule(ContractReviewRule):
    """合同期限检查规则"""
    
    def __init__(self):
        super().__init__("contract_term", "合同期限检查", "term")
    
    def check(self, contract_text: str) -> List[RiskPoint]:
        """检查合同期限"""
        risks = []
        
        # 检查合同期限是否明确
        if not re.search(r'(合同期限|有效期).*?[:：]', contract_text):
            risks.append(RiskPoint(
                risk_id="T001",
                title="合同期限不明确",
                level=RiskLevel.HIGH,
                description="合同中未明确约定合同期限",
                suggestion="请在合同中明确约定合同起止时间或合同类型（固定期限/无固定期限）"
            ))
        
        # 检查试用期约定
        probation_patterns = [
            r'试用期.*?[:：]\s*(\d+)\s*个月',
            r'试用期.*?[:：]\s*(\d+)\s*天'
        ]
        
        for pattern in probation_patterns:
            match = re.search(pattern, contract_text)
            if match:
                period = int(match.group(1))
                # 检查试用期是否超过法定期限
                if period > 6:
                    risks.append(RiskPoint(
                        risk_id="T002",
                        title="试用期超过法定期限",
                        level=RiskLevel.HIGH,
                        description=f"合同约定试用期为{period}个月，根据《劳动合同法》，试用期不得超过6个月",
                        suggestion="请调整试用期期限，确保符合法律规定"
                    ))
                break
        
        return risks


class SalaryRule(ContractReviewRule):
    """劳动报酬检查规则"""
    
    def __init__(self):
        super().__init__("salary", "劳动报酬检查", "salary")
    
    def check(self, contract_text: str) -> List[RiskPoint]:
        """检查劳动报酬"""
        risks = []
        
        # 检查是否约定工资
        if not re.search(r'(工资|报酬|薪酬).*?[:：]', contract_text):
            risks.append(RiskPoint(
                risk_id="S001",
                title="劳动报酬约定不明确",
                level=RiskLevel.HIGH,
                description="合同中未明确约定劳动报酬",
                suggestion="请在合同中明确约定工资标准、支付时间、支付方式"
            ))
        
        # 检查是否低于最低工资标准
        salary_match = re.search(r'(基本工资|工资).*?[:：]\s*(\d+(?:\.\d+)?)\s*(?:元|块)', contract_text)
        if salary_match:
            salary = float(salary_match.group(2))
            # 假设最低工资标准为2000元（实际应根据地区调整）
            if salary < 2000:
                risks.append(RiskPoint(
                    risk_id="S002",
                    title="工资可能低于最低工资标准",
                    level=RiskLevel.HIGH,
                    description=f"合同约定基本工资为{salary}元，可能低于当地最低工资标准",
                    suggestion="请确认当地最低工资标准，确保工资不低于法定最低标准"
                ))
        
        return risks


class SocialInsuranceRule(ContractReviewRule):
    """社会保险检查规则"""
    
    def __init__(self):
        super().__init__("social_insurance", "社会保险检查", "insurance")
    
    def check(self, contract_text: str) -> List[RiskPoint]:
        """检查社会保险"""
        risks = []
        
        # 检查是否约定社会保险
        if "社会保险" not in contract_text and "社保" not in contract_text:
            risks.append(RiskPoint(
                risk_id="I001",
                title="社会保险约定缺失",
                level=RiskLevel.HIGH,
                description="合同中未约定社会保险缴纳事宜",
                suggestion="根据《劳动合同法》，用人单位应依法为劳动者缴纳社会保险。建议在合同中明确约定"
            ))
        
        # 检查是否有"不缴纳社保"的违法条款
        if re.search(r'(自愿放弃|不缴纳|放弃社保|无需缴纳)', contract_text):
            risks.append(RiskPoint(
                risk_id="I002",
                title="存在违法条款",
                level=RiskLevel.HIGH,
                description="合同中存在要求劳动者放弃社会保险的条款，该条款违反法律强制性规定，无效",
                suggestion="请删除该条款，依法为劳动者缴纳社会保险"
            ))
        
        return risks


class TerminationRule(ContractReviewRule):
    """合同解除检查规则"""
    
    def __init__(self):
        super().__init__("termination", "合同解除检查", "termination")
    
    def check(self, contract_text: str) -> List[RiskPoint]:
        """检查合同解除"""
        risks = []
        
        # 检查是否有"不得解除"的霸王条款
        if re.search(r'(不得解除|禁止离职|不得辞职)', contract_text):
            risks.append(RiskPoint(
                risk_id="U001",
                title="存在限制劳动者解除权的条款",
                level=RiskLevel.HIGH,
                description="合同中存在限制劳动者单方解除劳动合同的条款，违反《劳动合同法》",
                suggestion="劳动者有权依法解除劳动合同，请删除限制性条款"
            ))
        
        # 检查是否约定违约金过高
        penalty_match = re.search(r'违约金.*?[:：]\s*(\d+(?:\.\d+)?)\s*(?:万元|元)', contract_text)
        if penalty_match:
            penalty = float(penalty_match.group(1))
            if penalty > 100000:  # 10万元
                risks.append(RiskPoint(
                    risk_id="U002",
                    title="违约金可能过高",
                    level=RiskLevel.MEDIUM,
                    description=f"合同约定违约金为{penalty}元，可能被认定为过高",
                    suggestion="违约金应当合理，通常不超过用人单位的损失。建议根据实际情况调整"
                ))
        
        return risks


class ContractReviewer:
    """合同审查器"""
    
    def __init__(self, ctx=None):
        """
        初始化审查器
        
        Args:
            ctx: 上下文
        """
        self.ctx = ctx
        
        # 初始化 LLM
        api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
        base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
        
        self.llm = ChatOpenAI(
            model="doubao-seed-1-8-251228",
            api_key=api_key,
            base_url=base_url,
            temperature=0.3,
            top_p=0.9,
            max_tokens=2000,
        )
        
        # 初始化审查规则
        self.rules = [
            BasicInfoRule(),
            ContractTermRule(),
            SalaryRule(),
            SocialInsuranceRule(),
            TerminationRule(),
        ]
    
    def review(self, contract_text: str) -> Dict[str, Any]:
        """
        审查合同
        
        Args:
            contract_text: 合同文本
            
        Returns:
            审查报告
        """
        # 执行所有规则检查
        all_risks = []
        for rule in self.rules:
            risks = rule.check(contract_text)
            all_risks.extend(risks)
        
        # 统计各等级风险数量
        risk_summary = {
            "high": sum(1 for r in all_risks if r.level == RiskLevel.HIGH),
            "medium": sum(1 for r in all_risks if r.level == RiskLevel.MEDIUM),
            "low": sum(1 for r in all_risks if r.level == RiskLevel.LOW),
            "info": sum(1 for r in all_risks if r.level == RiskLevel.INFO),
        }
        
        # 计算整体风险等级
        overall_risk = self._calculate_overall_risk(risk_summary)
        
        # 生成审查报告
        report = {
            "summary": {
                "total_risks": len(all_risks),
                "high_risks": risk_summary["high"],
                "medium_risks": risk_summary["medium"],
                "low_risks": risk_summary["low"],
                "overall_risk": overall_risk,
            },
            "risks": [risk.to_dict() for risk in all_risks],
            "suggestions": self._generate_suggestions(all_risks),
        }
        
        return report
    
    def _calculate_overall_risk(self, risk_summary: Dict[str, int]) -> str:
        """计算整体风险等级"""
        if risk_summary["high"] > 0:
            return "高风险"
        elif risk_summary["medium"] > 2:
            return "中高风险"
        elif risk_summary["medium"] > 0 or risk_summary["low"] > 3:
            return "中风险"
        elif risk_summary["low"] > 0:
            return "低风险"
        else:
            return "无风险"
    
    def _generate_suggestions(self, risks: List[RiskPoint]) -> List[str]:
        """生成修改建议"""
        suggestions = []
        
        # 按风险等级排序
        high_risks = [r for r in risks if r.level == RiskLevel.HIGH]
        medium_risks = [r for r in risks if r.level == RiskLevel.MEDIUM]
        low_risks = [r for r in risks if r.level == RiskLevel.LOW]
        
        if high_risks:
            suggestions.append(f"发现 {len(high_risks)} 个高风险问题，必须立即修改：")
            for risk in high_risks[:3]:  # 只列出前3个
                suggestions.append(f"- {risk.title}：{risk.suggestion}")
        
        if medium_risks:
            suggestions.append(f"\n发现 {len(medium_risks)} 个中风险问题，建议修改：")
            for risk in medium_risks[:3]:
                suggestions.append(f"- {risk.title}：{risk.suggestion}")
        
        if low_risks:
            suggestions.append(f"\n发现 {len(low_risks)} 个低风险问题，可考虑优化：")
            for risk in low_risks[:3]:
                suggestions.append(f"- {risk.title}：{risk.suggestion}")
        
        return suggestions
    
    def generate_report_text(self, report: Dict[str, Any]) -> str:
        """生成文本格式的审查报告"""
        summary = report["summary"]
        risks = report["risks"]
        suggestions = report["suggestions"]
        
        report_text = f"""
# 📋 合同审查报告

## 📊 审查概况
- **整体风险等级**：{summary['overall_risk']}
- **风险点总数**：{summary['total_risks']}
- **高风险**：{summary['high_risks']} 个
- **中风险**：{summary['medium_risks']} 个
- **低风险**：{summary['low_risks']} 个

## ⚠️ 风险详情
"""
        
        # 按等级分组
        high_risks = [r for r in risks if r['level'] == '高风险']
        medium_risks = [r for r in risks if r['level'] == '中风险']
        low_risks = [r for r in risks if r['level'] == '低风险']
        
        if high_risks:
            report_text += "\n### 🔴 高风险问题\n\n"
            for risk in high_risks:
                report_text += f"""
**{risk['title']}**（{risk['risk_id']}）
- 描述：{risk['description']}
- 建议：{risk['suggestion']}

"""
        
        if medium_risks:
            report_text += "\n### 🟡 中风险问题\n\n"
            for risk in medium_risks:
                report_text += f"""
**{risk['title']}**（{risk['risk_id']}）
- 描述：{risk['description']}
- 建议：{risk['suggestion']}

"""
        
        if low_risks:
            report_text += "\n### 🟢 低风险问题\n\n"
            for risk in low_risks:
                report_text += f"""
**{risk['title']}**（{risk['risk_id']}）
- 描述：{risk['description']}
- 建议：{risk['suggestion']}

"""
        
        # 添加修改建议
        if suggestions:
            report_text += "\n## 💡 修改建议\n\n"
            for suggestion in suggestions:
                report_text += f"{suggestion}\n"
        
        # 添加免责声明
        report_text += """

## ⚠️ 免责声明

本审查报告由 AI 自动生成，仅供参考，不构成正式法律意见。对于复杂的法律问题，建议咨询专业律师。

---

*审查时间：{now}*
"""
        
        return report_text


# 创建实例
contract_reviewer = ContractReviewer()
