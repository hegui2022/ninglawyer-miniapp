"""
宁律师智能法律咨询 Agent - 后端 API 服务
Flask RESTful API
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from typing import Dict, Any

from coze_coding_dev_sdk.database import get_session
from storage.database.contract_manager import (
    contract_manager,
    contract_review_manager,
    contract_template_manager,
    ContractCreate,
    ContractUpdate,
)
from tools.contract_reviewer import contract_reviewer
from tools.contract_drafter_master import ContractDraftingMaster
from utils.document_generator import document_generator


app = Flask(__name__)
CORS(app)  # 启用跨域支持

# 初始化合同起草器
contract_drafter = ContractDraftingMaster()


def success_response(data: Any = None, message: str = "success") -> Dict[str, Any]:
    """统一成功响应"""
    return {
        "code": 0,
        "message": message,
        "data": data
    }


def error_response(code: int = -1, message: str = "error") -> Dict[str, Any]:
    """统一错误响应"""
    return {
        "code": code,
        "message": message,
        "data": None
    }


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify(success_response({"status": "ok"}))


@app.route('/api/contract/types', methods=['GET'])
def get_contract_types():
    """获取合同类型列表"""
    types = [
        {
            "id": "standard",
            "name": "标准劳动合同",
            "description": "适用于正式员工，有试用期，缴纳社保"
        },
        {
            "id": "parttime",
            "name": "非全日制用工合同",
            "description": "适用于兼职，每天不超过4小时"
        },
        {
            "id": "intern",
            "name": "实习协议",
            "description": "适用于在校学生实习，有实习补贴和意外保险"
        },
        {
            "id": "retired",
            "name": "退休返聘协议",
            "description": "适用于退休人员返聘，不缴纳社保"
        },
        {
            "id": "project",
            "name": "项目制合同",
            "description": "适用于项目制合作，以完成项目为期限"
        },
        {
            "id": "dispatch",
            "name": "劳务派遣合同",
            "description": "适用于劳务派遣，三方关系"
        }
    ]
    return jsonify(success_response(types))


@app.route('/api/contract/draft/start', methods=['POST'])
def start_contract_draft():
    """开始起草合同"""
    try:
        data = request.get_json()
        contract_type = data.get('contract_type', 'standard')
        
        result = contract_drafter._handle_create_contract(f"创建{contract_type}合同")
        
        return jsonify(success_response({
            "contract_type": contract_type,
            "message": result
        }))
    except Exception as e:
        return jsonify(error_response(message=str(e)))


@app.route('/api/contract/draft/step', methods=['POST'])
def process_draft_step():
    """处理起草步骤"""
    try:
        data = request.get_json()
        step_input = data.get('input', '')
        
        result = contract_drafter.process(step_input)
        
        return jsonify(success_response({
            "response": result
        }))
    except Exception as e:
        return jsonify(error_response(message=str(e)))


@app.route('/api/contract/save', methods=['POST'])
def save_contract():
    """保存合同"""
    try:
        data = request.get_json()
        
        db = get_session()
        try:
            contract = contract_manager.create_contract(
                db,
                ContractCreate(
                    contract_name=data.get('contract_name', ''),
                    contract_type=data.get('contract_type', ''),
                    employer_name=data.get('employer_name', ''),
                    employee_name=data.get('employee_name', ''),
                    contract_content=data.get('contract_content', ''),
                    additional_clauses=data.get('additional_clauses', ''),
                    status='draft'
                )
            )
            return jsonify(success_response({
                "contract_id": contract.id,
                "message": "合同保存成功"
            }))
        finally:
            db.close()
    except Exception as e:
        return jsonify(error_response(message=str(e)))


@app.route('/api/contract/list', methods=['GET'])
def list_contracts():
    """获取合同列表（支持分页）"""
    try:
        contract_type = request.args.get('contract_type')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        # 计算偏移量
        offset = (page - 1) * page_size
        limit = page_size
        
        db = get_session()
        try:
            # 获取合同列表
            contracts = contract_manager.get_contracts(
                db,
                contract_type=contract_type,
                status=status,
                offset=offset,
                limit=limit
            )
            
            # 获取总数
            total = contract_manager.count_contracts(
                db,
                contract_type=contract_type,
                status=status
            )
            
            contract_list = []
            for contract in contracts:
                # 获取最新审查记录
                latest_review = contract_review_manager.get_latest_review(db, contract.id)
                
                contract_list.append({
                    "id": contract.id,
                    "contract_name": contract.contract_name,
                    "contract_type": contract.contract_type,
                    "employer_name": contract.employer_name,
                    "employee_name": contract.employee_name,
                    "status": contract.status,
                    "version": contract.version,
                    "created_at": contract.created_at.isoformat(),
                    "has_review": latest_review is not None,
                    "overall_risk": latest_review.overall_risk if latest_review else None
                })
            
            # 计算总页数
            total_pages = (total + page_size - 1) // page_size
            
            return jsonify(success_response({
                "contracts": contract_list,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "total_pages": total_pages,
                    "has_more": page < total_pages
                }
            }))
        finally:
            db.close()
    except Exception as e:
        return jsonify(error_response(message=str(e)))


@app.route('/api/contract/<int:contract_id>', methods=['GET'])
def get_contract(contract_id: int):
    """获取合同详情"""
    try:
        db = get_session()
        try:
            contract = contract_manager.get_contract_by_id(db, contract_id)
            if not contract:
                return jsonify(error_response(code=404, message="合同不存在"))
            
            return jsonify(success_response({
                "id": contract.id,
                "contract_name": contract.contract_name,
                "contract_type": contract.contract_type,
                "employer_name": contract.employer_name,
                "employee_name": contract.employee_name,
                "contract_content": contract.contract_content,
                "additional_clauses": contract.additional_clauses,
                "status": contract.status,
                "version": contract.version,
                "created_at": contract.created_at.isoformat(),
                "updated_at": contract.updated_at.isoformat() if contract.updated_at else None,
            }))
        finally:
            db.close()
    except Exception as e:
        return jsonify(error_response(message=str(e)))


@app.route('/api/contract/<int:contract_id>', methods=['PUT'])
def update_contract(contract_id: int):
    """更新合同"""
    try:
        data = request.get_json()
        
        db = get_session()
        try:
            updated_contract = contract_manager.update_contract(
                db,
                contract_id,
                ContractUpdate(
                    contract_content=data.get('contract_content'),
                    status=data.get('status')
                )
            )
            
            if not updated_contract:
                return jsonify(error_response(code=404, message="合同不存在"))
            
            return jsonify(success_response({
                "contract_id": contract_id,
                "message": "合同更新成功"
            }))
        finally:
            db.close()
    except Exception as e:
        return jsonify(error_response(message=str(e)))


@app.route('/api/contract/<int:contract_id>/review', methods=['POST'])
def review_contract(contract_id: int):
    """审查合同"""
    try:
        db = get_session()
        try:
            # 获取合同内容
            contract = contract_manager.get_contract_by_id(db, contract_id)
            if not contract:
                return jsonify(error_response(code=404, message="合同不存在"))
            
            # 审查合同
            review_report = contract_reviewer.review(contract.contract_content)
            
            # 保存审查记录
            review = contract_review_manager.create_review(
                db,
                ContractReviewCreate(
                    contract_id=contract_id,
                    review_result=review_report,
                    overall_risk=review_report['summary']['overall_risk'],
                    high_risks=review_report['summary']['high_risks'],
                    medium_risks=review_report['summary']['medium_risks'],
                    low_risks=review_report['summary']['low_risks']
                )
            )
            
            return jsonify(success_response({
                "review_id": review.id,
                "report": review_report
            }))
        finally:
            db.close()
    except Exception as e:
        return jsonify(error_response(message=str(e)))


@app.route('/api/contract/<int:contract_id>/review', methods=['GET'])
def get_contract_review(contract_id: int):
    """获取合同审查记录"""
    try:
        db = get_session()
        try:
            review = contract_review_manager.get_latest_review(db, contract_id)
            if not review:
                return jsonify(success_response({
                    "has_review": False,
                    "message": "该合同暂无审查记录"
                }))
            
            return jsonify(success_response({
                "has_review": True,
                "review_id": review.id,
                "overall_risk": review.overall_risk,
                "high_risks": review.high_risks,
                "medium_risks": review.medium_risks,
                "low_risks": review.low_risks,
                "review_result": review.review_result,
                "created_at": review.created_at.isoformat(),
            }))
        finally:
            db.close()
    except Exception as e:
        return jsonify(error_response(message=str(e)))


@app.route('/api/contract/<int:contract_id>/download', methods=['GET'])
def download_contract(contract_id: int):
    """下载合同文件（PDF/Word）"""
    try:
        # 获取格式参数，默认 pdf
        file_format = request.args.get('format', 'pdf')
        if file_format not in ['pdf', 'docx']:
            return jsonify(error_response(code=400, message="不支持的文件格式，仅支持 pdf 和 docx"))
        
        # 获取合同数据
        db = get_session()
        try:
            contract = contract_manager.get_contract_by_id(db, contract_id)
            if not contract:
                return jsonify(error_response(code=404, message="合同不存在"))
            
            # 构造合同数据
            contract_data = {
                'id': contract.id,
                'contract_name': contract.contract_name,
                'contract_type': contract.contract_type,
                'contract_content': contract.contract_content if isinstance(contract.contract_content, dict) else {},
            }
            
            # 生成文件
            if file_format == 'pdf':
                filepath = document_generator.generate_pdf(contract_data)
                filename = f"{contract.contract_name or '合同'}.pdf"
                mimetype = 'application/pdf'
            else:
                filepath = document_generator.generate_word(contract_data)
                filename = f"{contract.contract_name or '合同'}.docx"
                mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            
            # 返回文件
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype=mimetype
            )
        finally:
            db.close()
    except Exception as e:
        return jsonify(error_response(message=str(e)))


@app.route('/api/template/list', methods=['GET'])
def list_templates():
    """获取模板列表"""
    try:
        template_type = request.args.get('template_type')
        is_active = request.args.get('is_active', 'true').lower() == 'true'
        limit = int(request.args.get('limit', 100))
        
        db = get_session()
        try:
            templates = contract_template_manager.get_templates(
                db,
                template_type=template_type,
                is_active=is_active,
                limit=limit
            )
            
            template_list = []
            for template in templates:
                template_list.append({
                    "id": template.id,
                    "template_name": template.template_name,
                    "template_type": template.template_type,
                    "description": template.description,
                    "is_active": template.is_active,
                    "created_at": template.created_at.isoformat(),
                })
            
            return jsonify(success_response(template_list))
        finally:
            db.close()
    except Exception as e:
        return jsonify(error_response(message=str(e)))


@app.route('/api/template/<int:template_id>', methods=['GET'])
def get_template(template_id: int):
    """获取模板详情"""
    try:
        db = get_session()
        try:
            template = contract_template_manager.get_template_by_id(db, template_id)
            if not template:
                return jsonify(error_response(code=404, message="模板不存在"))
            
            return jsonify(success_response({
                "id": template.id,
                "template_name": template.template_name,
                "template_type": template.template_type,
                "template_content": template.template_content,
                "description": template.description,
                "is_active": template.is_active,
                "created_at": template.created_at.isoformat(),
                "updated_at": template.updated_at.isoformat() if template.updated_at else None,
            }))
        finally:
            db.close()
    except Exception as e:
        return jsonify(error_response(message=str(e)))


@app.route('/api/template/<int:template_id>/use', methods=['POST'])
def use_template(template_id: int):
    """使用模板创建合同"""
    try:
        data = request.get_json()
        contract_name = data.get('contract_name')
        
        if not contract_name:
            return jsonify(error_response(code=400, message="请提供合同名称"))
        
        db = get_session()
        try:
            # 获取模板
            template = contract_template_manager.get_template_by_id(db, template_id)
            if not template:
                return jsonify(error_response(code=404, message="模板不存在"))
            
            # 创建合同
            contract = contract_manager.create_contract(
                db,
                ContractCreate(
                    contract_name=contract_name,
                    contract_type=template.template_type,
                    employer_name=template.template_content.get('party_a', ''),
                    employee_name=template.template_content.get('party_b', ''),
                    contract_content=template.template_content,
                    status='draft'
                )
            )
            
            return jsonify(success_response({
                "contract_id": contract.id,
                "message": "合同创建成功"
            }))
        finally:
            db.close()
    except Exception as e:
        return jsonify(error_response(message=str(e)))


if __name__ == '__main__':
    # 从环境变量获取端口
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
