"""
合同起草工具
Contract Drafting Tool
"""

from langchain.tools import tool, ToolRuntime


@tool
def contract_drafting_assistant(query: str, runtime: ToolRuntime) -> str:
    """
    合同起草助手 - 帮助用户起草各类劳动合同
    
    功能：
    - 意图识别：识别用户想要创建什么类型的合同
    - 场景分类：根据用户需求选择合适的合同模板
    - AI引导：分步引导用户填写合同信息
    - 合同生成：自动生成符合法律规范的合同文本
    - 法律建议：提供专业的法律风险提示
    
    支持的合同类型：
    - 标准全职劳动合同
    - 非全日制用工合同
    - 实习协议
    - 退休返聘协议
    - 项目制合同
    - 劳务派遣合同
    
    Args:
        query: 用户的输入，例如"我要签一个劳动合同"或"起草一份兼职合同"
        runtime: 工具运行时上下文
        
    Returns:
        合同文本或引导提示
    """
    ctx = runtime.context
    
    # 导入总调度器
    try:
        from tools.contract_drafter_master import ContractDraftingMaster
        
        master = ContractDraftingMaster(ctx=ctx)
        result = master.process(query)
        
        return result
    except Exception as e:
        return f"合同起草助手暂时无法使用，错误：{str(e)}"


@tool
def export_contract_to_word(contract_text: str, filename: str = "contract.docx") -> str:
    """
    导出合同为 Word 格式
    
    Args:
        contract_text: 合同文本
        filename: 文件名
        
    Returns:
        导出文件路径
    """
    try:
        from tools.contract_exporter import contract_exporter
        filepath = contract_exporter.export_to_word(contract_text, filename)
        return f"合同已导出为 Word 格式：{filepath}"
    except Exception as e:
        return f"导出失败：{str(e)}"


@tool
def get_contract_templates(runtime: ToolRuntime) -> str:
    """
    获取可用的合同模板列表
    
    Args:
        runtime: 工具运行时上下文
        
    Returns:
        合同模板列表
    """
    templates = """
## 可用的合同模板

### 1. 标准全职劳动合同 ⭐⭐⭐⭐⭐
- 适用场景：全日制用工，固定期限或无固定期限
- 特点：完整的必备条款，包含试用期
- 包含：社保、竞业限制、培训服务期等

### 2. 非全日制用工合同 ⭐⭐⭐⭐⭐
- 适用场景：每天工作不超过4小时，每周不超过24小时
- 特点：可随时终止，无经济补偿
- 工资：按小时计酬

### 3. 实习协议 ⭐⭐⭐⭐
- 适用场景：在校学生实习
- 特点：实习补贴而非工资，非劳动关系
- 保险：意外保险

### 4. 退休返聘协议 ⭐⭐⭐
- 适用场景：退休人员返聘
- 特点：劳务关系，不缴纳社保
- 灵活：可随时终止

### 5. 项目制合同 ⭐⭐⭐
- 适用场景：以完成项目为期限
- 特点：项目结束合同终止
- 付款：阶段付款

### 6. 劳务派遣合同 ⭐⭐
- 适用场景：劳务派遣用工
- 特点：三方关系
- 责任：派遣公司承担责任
"""
    
    return templates


__all__ = [
    "contract_drafting_assistant",
    "export_contract_to_word",
    "get_contract_templates",
]
