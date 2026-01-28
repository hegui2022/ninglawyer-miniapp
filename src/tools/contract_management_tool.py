"""
合同管理工具
Contract Management Tool - 提供给 Agent 使用的合同管理工具函数
"""

from langchain.tools import tool, ToolRuntime
from storage.database.contract_manager import (
    contract_manager,
    contract_review_manager,
    contract_template_manager,
    ContractCreate,
    ContractUpdate,
    ContractTemplateCreate,
    ContractTemplateUpdate,
    ContractReviewCreate,
)
from coze_coding_dev_sdk.database import get_session


@tool
def save_contract(
    contract_name: str,
    contract_type: str,
    employer_name: str,
    employee_name: str,
    contract_content: str,
    runtime: ToolRuntime,
    additional_clauses: str = ""
) -> str:
    """
    保存合同到数据库
    
    Args:
        contract_name: 合同名称
        contract_type: 合同类型（如：standard、parttime、intern等）
        employer_name: 用人单位名称
        employee_name: 劳动者姓名
        contract_content: 合同内容
        runtime: 运行时上下文
        additional_clauses: 附加条款内容（可选）
        
    Returns:
        保存结果
    """
    try:
        db = get_session()
        try:
            contract = contract_manager.create_contract(
                db,
                ContractCreate(
                    contract_name=contract_name,
                    contract_type=contract_type,
                    employer_name=employer_name,
                    employee_name=employee_name,
                    contract_content=contract_content,
                    additional_clauses=additional_clauses,
                    status="draft"
                )
            )
            return f"✅ 合同已保存，合同ID：{contract.id}"
        finally:
            db.close()
    except Exception as e:
        return f"❌ 保存合同失败：{str(e)}"


@tool
def get_contract(contract_id: int, runtime: ToolRuntime) -> str:
    """
    获取合同详情
    
    Args:
        contract_id: 合同ID
        runtime: 运行时上下文
        
    Returns:
        合同详情
    """
    try:
        db = get_session()
        try:
            contract = contract_manager.get_contract_by_id(db, contract_id)
            if not contract:
                return f"❌ 未找到ID为 {contract_id} 的合同"
            
            return f"""
## 📄 合同详情

**合同ID**：{contract.id}
**合同名称**：{contract.contract_name}
**合同类型**：{contract.contract_type}
**用人单位**：{contract.employer_name}
**劳动者**：{contract.employee_name}
**状态**：{contract.status}
**版本**：v{contract.version}
**创建时间**：{contract.created_at.strftime('%Y-%m-%d %H:%M:%S')}

---

**合同内容**：

{contract.contract_content if len(contract.contract_content) < 500 else contract.contract_content[:500] + '...'}
"""
        finally:
            db.close()
    except Exception as e:
        return f"❌ 获取合同失败：{str(e)}"


@tool
def list_contracts(
    contract_type: str = "",
    status: str = "",
    limit: int = 10,
    runtime: ToolRuntime = None
) -> str:
    """
    列出合同
    
    Args:
        contract_type: 合同类型（可选，如：standard、parttime等）
        status: 合同状态（可选，如：draft、signed等）
        limit: 返回数量限制（默认10）
        runtime: 运行时上下文
        
    Returns:
        合同列表
    """
    try:
        db = get_session()
        try:
            contracts = contract_manager.get_contracts(
                db,
                contract_type=contract_type if contract_type else None,
                status=status if status else None,
                limit=limit
            )
            
            if not contracts:
                return "📭 暂无合同记录"
            
            result = "## 📋 合同列表\n\n"
            for contract in contracts:
                status_icon = {
                    "draft": "📝",
                    "signed": "✅",
                    "terminated": "❌"
                }.get(contract.status, "📄")
                
                result += f"""
**{status_icon} {contract.contract_name}** (ID: {contract.id})
- 类型：{contract.contract_type}
- 用人单位：{contract.employer_name}
- 劳动者：{contract.employee_name}
- 状态：{contract.status}
- 版本：v{contract.version}
- 创建时间：{contract.created_at.strftime('%Y-%m-%d')}

---
"""
            return result
        finally:
            db.close()
    except Exception as e:
        return f"❌ 获取合同列表失败：{str(e)}"


@tool
def update_contract(
    contract_id: int,
    runtime: ToolRuntime = None,
    contract_content: str = "",
    status: str = ""
) -> str:
    """
    更新合同
    
    Args:
        contract_id: 合同ID
        runtime: 运行时上下文
        contract_content: 新的合同内容（可选）
        status: 新的状态（可选）
        
    Returns:
        更新结果
    """
    try:
        db = get_session()
        try:
            # 构建更新数据
            update_data = {}
            if contract_content:
                update_data["contract_content"] = contract_content
            if status:
                update_data["status"] = status
            
            if not update_data:
                return "❌ 没有提供更新内容"
            
            updated_contract = contract_manager.update_contract(
                db,
                contract_id,
                ContractUpdate(**update_data)
            )
            
            if not updated_contract:
                return f"❌ 未找到ID为 {contract_id} 的合同"
            
            return f"✅ 合同已更新，合同ID：{contract_id}"
        finally:
            db.close()
    except Exception as e:
        return f"❌ 更新合同失败：{str(e)}"


@tool
def create_contract_version(contract_id: int, runtime: ToolRuntime) -> str:
    """
    创建合同新版本
    
    Args:
        contract_id: 合同ID
        runtime: 运行时上下文
        
    Returns:
        新版本信息
    """
    try:
        db = get_session()
        try:
            new_contract = contract_manager.create_new_version(db, contract_id)
            if not new_contract:
                return f"❌ 未找到ID为 {contract_id} 的合同"
            
            return f"✅ 已创建新版本，新版本ID：{new_contract.id}，版本号：v{new_contract.version}"
        finally:
            db.close()
    except Exception as e:
        return f"❌ 创建新版本失败：{str(e)}"


@tool
def save_contract_review(
    contract_id: int,
    review_result: str,
    overall_risk: str,
    runtime: ToolRuntime = None,
    high_risks: int = 0,
    medium_risks: int = 0,
    low_risks: int = 0
) -> str:
    """
    保存合同审查记录
    
    Args:
        contract_id: 合同ID
        review_result: 审查结果（JSON字符串）
        overall_risk: 整体风险等级
        runtime: 运行时上下文
        high_risks: 高风险数量
        medium_risks: 中风险数量
        low_risks: 低风险数量
        
    Returns:
        保存结果
    """
    try:
        import json
        
        db = get_session()
        try:
            review = contract_review_manager.create_review(
                db,
                ContractReviewCreate(
                    contract_id=contract_id,
                    review_result=json.loads(review_result),
                    overall_risk=overall_risk,
                    high_risks=high_risks,
                    medium_risks=medium_risks,
                    low_risks=low_risks
                )
            )
            return f"✅ 审查记录已保存，审查ID：{review.id}"
        finally:
            db.close()
    except Exception as e:
        return f"❌ 保存审查记录失败：{str(e)}"


@tool
def get_contract_review(contract_id: int, runtime: ToolRuntime) -> str:
    """
    获取合同的最新审查记录
    
    Args:
        contract_id: 合同ID
        runtime: 运行时上下文
        
    Returns:
        审查记录
    """
    try:
        db = get_session()
        try:
            review = contract_review_manager.get_latest_review(db, contract_id)
            if not review:
                return f"ℹ️ 该合同暂无审查记录"
            
            return f"""
## 📋 合同审查记录

**审查ID**：{review.id}
**整体风险**：{review.overall_risk}
**高风险**：{review.high_risks} 个
**中风险**：{review.medium_risks} 个
**低风险**：{review.low_risks} 个
**审查时间**：{review.created_at.strftime('%Y-%m-%d %H:%M:%S')}

详细结果请查看数据库记录。
"""
        finally:
            db.close()
    except Exception as e:
        return f"❌ 获取审查记录失败：{str(e)}"
