"""
合同审查工具
Contract Review Tool - 提供给 Agent 使用的合同审查工具函数
"""

from langchain.tools import tool, ToolRuntime
from tools.contract_reviewer import contract_reviewer
from datetime import datetime


@tool
def review_contract(contract_text: str, runtime: ToolRuntime) -> str:
    """
    审查合同文本，识别风险点并生成审查报告
    
    Args:
        contract_text: 合同文本内容
        runtime: 运行时上下文
        
    Returns:
        审查报告（文本格式）
    """
    try:
        # 调用审查器
        report = contract_reviewer.review(contract_text)
        
        # 生成文本报告
        report_text = contract_reviewer.generate_report_text(report)
        
        # 添加时间戳
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_text = report_text.replace("{now}", now)
        
        return report_text
        
    except Exception as e:
        return f"合同审查失败：{str(e)}\n\n请检查合同文本格式是否正确。"


@tool
def quick_contract_check(contract_text: str, runtime: ToolRuntime) -> str:
    """
    快速检查合同是否存在明显风险
    
    Args:
        contract_text: 合同文本内容
        runtime: 运行时上下文
        
    Returns:
        快速检查结果
    """
    try:
        # 调用审查器
        report = contract_reviewer.review(contract_text)
        
        # 统计风险
        summary = report["summary"]
        
        # 生成快速检查结果
        if summary["high_risks"] > 0:
            result = f"⚠️ 发现 {summary['high_risks']} 个高风险问题，建议立即修改。"
        elif summary["medium_risks"] > 0:
            result = f"⚠️ 发现 {summary['medium_risks']} 个中风险问题，建议修改。"
        elif summary["low_risks"] > 0:
            result = f"ℹ️ 发现 {summary['low_risks']} 个低风险问题，可考虑优化。"
        else:
            result = "✅ 未发现明显风险问题。"
        
        result += f"\n\n整体风险等级：{summary['overall_risk']}"
        result += f"\n风险点总数：{summary['total_risks']}"
        
        # 列出高风险问题
        high_risks = [r for r in report["risks"] if r['level'] == '高风险']
        if high_risks:
            result += "\n\n高风险问题列表："
            for risk in high_risks:
                result += f"\n- {risk['title']}：{risk['description']}"
        
        result += "\n\n如需详细审查报告，请使用 review_contract 工具。"
        
        return result
        
    except Exception as e:
        return f"快速检查失败：{str(e)}"
