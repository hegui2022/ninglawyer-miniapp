"""
合同相关API路由
包括合同起草、合同审查等
"""

from flask import Blueprint, request, jsonify, Response, stream_with_context
from datetime import datetime, date
from decimal import Decimal
import logging

from services.coze_agent import CozeAgentService
from utils.database import get_db
from models.v1_models import Contract
from routes.auth import require_auth

logger = logging.getLogger(__name__)

contract_bp = Blueprint('contract', __name__, url_prefix='/api/contract')


# ============================================
# 合同起草
# ============================================

@contract_bp.route('/draft', methods=['POST'])
@require_auth
def draft_contract(user_id):
    """
    起草合同
    
    Request Body:
        {
            "query": "合同需求描述",
            "contract_type": "合同类型（采购合同/服务合同/租赁合同/劳动合同/合作协议/保密协议/借款合同）",
            "session_id": "会话ID（可选）",
            "stream": false,
            "save_to_db": false  // 是否保存到数据库（可选，默认false）
        }
    
    Response (非流式):
        {
            "success": true,
            "data": {
                "session_id": "会话ID",
                "answer": "合同内容",
                "bot_id": "Bot ID",
                "bot_name": "Bot名称",
                "conversation_type": "contract_drafter"
            }
        }
    
    Response (流式):
        事件流格式（SSE）
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "success": False,
                "message": "缺少query参数"
            }), 400
        
        query = data.get('query')
        contract_type = data.get('contract_type', 'service_contract')
        session_id = data.get('session_id')
        stream = data.get('stream', False)
        save_to_db = data.get('save_to_db', False)
        
        # 验证合同类型
        valid_types = [
            '采购合同', '服务合同', '租赁合同', 
            '劳动合同', '合作协议', '保密协议', '借款合同'
        ]
        if contract_type not in valid_types:
            return jsonify({
                "success": False,
                "message": f"无效的合同类型，可选：{', '.join(valid_types)}"
            }), 400
        
        db = get_db()
        agent_service = CozeAgentService(db)
        
        # 构建额外数据
        extra_data = {
            "contract_type": contract_type,
            "action": "draft"
        }
        
        if stream:
            # 流式输出
            def generate():
                result = agent_service.chat(
                    user_id=user_id,
                    app_type="contract",
                    agent_type="contract_drafter",
                    query=query,
                    session_id=session_id,
                    stream=True,
                    save_to_db=save_to_db,
                    extra_data=extra_data
                )
                
                for chunk in result:
                    if isinstance(chunk, dict):
                        if chunk.get("success"):
                            data_chunk = chunk.get("data", {})
                            chunk_type = data_chunk.get("type")
                            
                            if chunk_type == "chunk":
                                yield f"data: {json.dumps(data_chunk, ensure_ascii=False)}\n\n"
                            elif chunk_type == "end":
                                # 如果需要保存到数据库，在这里保存
                                if save_to_db:
                                    try:
                                        contract = Contract(
                                            user_id=user_id,
                                            contract_type=contract_type,
                                            contract_title=f"{contract_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                                            contract_text=data_chunk.get('answer', ''),
                                            status='draft',
                                            bot_id=data_chunk.get('bot_id'),
                                            bot_name=data_chunk.get('bot_name')
                                        )
                                        db.add(contract)
                                        db.commit()
                                    except Exception as e:
                                        logger.error(f"保存合同到数据库失败: {str(e)}")
                                        db.rollback()
                                
                                yield f"data: {json.dumps(data_chunk, ensure_ascii=False)}\n\n"
                                yield "data: [DONE]\n\n"
                        else:
                            error_chunk = {
                                "type": "error",
                                "message": chunk.get("message", "未知错误")
                            }
                            yield f"data: {json.dumps(error_chunk, ensure_ascii=False)}\n\n"
                            yield "data: [DONE]\n\n"
            
            return Response(
                stream_with_context(generate()),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'X-Accel-Buffering': 'no'
                }
            )
        else:
            # 非流式输出
            result = agent_service.chat(
                user_id=user_id,
                app_type="contract",
                agent_type="contract_drafter",
                query=query,
                session_id=session_id,
                stream=False,
                save_to_db=False,
                extra_data=extra_data
            )
            
            if result.get('success'):
                data = result.get('data', {})
                answer = data.get('answer', '')
                
                # 保存到数据库
                if save_to_db:
                    try:
                        contract = Contract(
                            user_id=user_id,
                            contract_type=contract_type,
                            contract_title=f"{contract_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                            contract_text=answer,
                            status='draft',
                            bot_id=data.get('bot_id'),
                            bot_name=data.get('bot_name')
                        )
                        db.add(contract)
                        db.commit()
                        data['contract_id'] = contract.id
                        result['data'] = data
                    except Exception as e:
                        logger.error(f"保存合同到数据库失败: {str(e)}")
                        db.rollback()
                
                return jsonify(result), 200
            else:
                return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"起草合同失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"起草失败: {str(e)}"
        }), 500


# ============================================
# 合同审查
# ============================================

@contract_bp.route('/review', methods=['POST'])
@require_auth
def review_contract(user_id):
    """
    审查合同
    
    Request Body:
        {
            "contract_text": "合同内容",
            "contract_type": "合同类型（可选）",
            "session_id": "会话ID（可选）",
            "stream": false,
            "save_to_db": false
        }
    
    Response: 同合同起草
    """
    try:
        data = request.get_json()
        
        if not data or 'contract_text' not in data:
            return jsonify({
                "success": False,
                "message": "缺少contract_text参数"
            }), 400
        
        contract_text = data.get('contract_text')
        contract_type = data.get('contract_type', '通用合同')
        session_id = data.get('session_id')
        stream = data.get('stream', False)
        save_to_db = data.get('save_to_db', False)
        
        # 构建查询
        query = f"请审查以下{contract_type}，分析其中存在的问题、风险点、缺失条款，并给出修改建议：\n\n{contract_text}"
        
        db = get_db()
        agent_service = CozeAgentService(db)
        
        # 构建额外数据
        extra_data = {
            "contract_type": contract_type,
            "action": "review"
        }
        
        if stream:
            # 流式输出
            def generate():
                result = agent_service.chat(
                    user_id=user_id,
                    app_type="contract",
                    agent_type="contract_reviewer",
                    query=query,
                    session_id=session_id,
                    stream=True,
                    save_to_db=save_to_db,
                    extra_data=extra_data
                )
                
                for chunk in result:
                    if isinstance(chunk, dict):
                        if chunk.get("success"):
                            data_chunk = chunk.get("data", {})
                            chunk_type = data_chunk.get("type")
                            
                            if chunk_type == "chunk":
                                yield f"data: {json.dumps(data_chunk, ensure_ascii=False)}\n\n"
                            elif chunk_type == "end":
                                yield f"data: {json.dumps(data_chunk, ensure_ascii=False)}\n\n"
                                yield "data: [DONE]\n\n"
                        else:
                            error_chunk = {
                                "type": "error",
                                "message": chunk.get("message", "未知错误")
                            }
                            yield f"data: {json.dumps(error_chunk, ensure_ascii=False)}\n\n"
                            yield "data: [DONE]\n\n"
            
            return Response(
                stream_with_context(generate()),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'X-Accel-Buffering': 'no'
                }
            )
        else:
            # 非流式输出
            result = agent_service.chat(
                user_id=user_id,
                app_type="contract",
                agent_type="contract_reviewer",
                query=query,
                session_id=session_id,
                stream=False,
                save_to_db=False,
                extra_data=extra_data
            )
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"审查合同失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"审查失败: {str(e)}"
        }), 500


# ============================================
# 获取合同列表
# ============================================

@contract_bp.route('/list', methods=['GET'])
@require_auth
def get_contract_list(user_id):
    """
    获取用户的合同列表
    
    Query Params:
        - page: 页码（默认1）
        - page_size: 每页数量（默认20）
        - contract_type: 合同类型（可选）
        - status: 状态（可选）
    
    Response:
        {
            "success": true,
            "data": {
                "total": 100,
                "page": 1,
                "page_size": 20,
                "contracts": [...]
            }
        }
    """
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        contract_type = request.args.get('contract_type')
        status = request.args.get('status')
        
        db = get_db()
        
        # 构建查询
        query = db.query(Contract).filter(Contract.user_id == user_id)
        
        if contract_type:
            query = query.filter(Contract.contract_type == contract_type)
        
        if status:
            query = query.filter(Contract.status == status)
        
        # 排序
        query = query.order_by(Contract.created_at.desc())
        
        # 分页
        total = query.count()
        contracts = query.offset((page - 1) * page_size).limit(page_size).all()
        
        # 格式化结果
        contract_list = []
        for contract in contracts:
            contract_list.append({
                "id": contract.id,
                "contract_type": contract.contract_type,
                "contract_title": contract.contract_title,
                "status": contract.status,
                "created_at": contract.created_at.isoformat() if contract.created_at else None,
                "updated_at": contract.updated_at.isoformat() if contract.updated_at else None
            })
        
        return jsonify({
            "success": True,
            "data": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "contracts": contract_list
            }
        }), 200
        
    except Exception as e:
        logger.error(f"获取合同列表失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取失败: {str(e)}"
        }), 500


# ============================================
# 获取合同详情
# ============================================

@contract_bp.route('/detail/<int:contract_id>', methods=['GET'])
@require_auth
def get_contract_detail(user_id, contract_id):
    """
    获取合同详情
    
    Response:
        {
            "success": true,
            "data": {
                "id": 1,
                "contract_type": "服务合同",
                "contract_title": "合同标题",
                "contract_text": "合同内容",
                "status": "draft",
                "party_a": "甲方",
                "party_b": "乙方",
                "contract_amount": 100000.00,
                "contract_start_date": "2025-01-01",
                "contract_end_date": "2025-12-31",
                "created_at": "2025-01-10T00:00:00",
                "updated_at": "2025-01-10T00:00:00"
            }
        }
    """
    try:
        db = get_db()
        
        contract = db.query(Contract).filter(
            Contract.id == contract_id,
            Contract.user_id == user_id
        ).first()
        
        if not contract:
            return jsonify({
                "success": False,
                "message": "合同不存在"
            }), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": contract.id,
                "contract_type": contract.contract_type,
                "contract_title": contract.contract_title,
                "contract_text": contract.contract_text,
                "status": contract.status,
                "party_a": contract.party_a,
                "party_b": contract.party_b,
                "contract_amount": float(contract.contract_amount) if contract.contract_amount else None,
                "contract_start_date": contract.contract_start_date.isoformat() if contract.contract_start_date else None,
                "contract_end_date": contract.contract_end_date.isoformat() if contract.contract_end_date else None,
                "created_at": contract.created_at.isoformat() if contract.created_at else None,
                "updated_at": contract.updated_at.isoformat() if contract.updated_at else None
            }
        }), 200
        
    except Exception as e:
        logger.error(f"获取合同详情失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取失败: {str(e)}"
        }), 500


# ============================================
# 更新合同
# ============================================

@contract_bp.route('/update/<int:contract_id>', methods=['PUT'])
@require_auth
def update_contract(user_id, contract_id):
    """
    更新合同
    
    Request Body:
        {
            "contract_title": "合同标题",
            "contract_text": "合同内容",
            "status": "signed",
            "party_a": "甲方",
            "party_b": "乙方",
            "contract_amount": 100000.00,
            "contract_start_date": "2025-01-01",
            "contract_end_date": "2025-12-31"
        }
    
    Response:
        {
            "success": true,
            "message": "更新成功"
        }
    """
    try:
        data = request.get_json()
        
        db = get_db()
        
        contract = db.query(Contract).filter(
            Contract.id == contract_id,
            Contract.user_id == user_id
        ).first()
        
        if not contract:
            return jsonify({
                "success": False,
                "message": "合同不存在"
            }), 404
        
        # 更新字段
        if 'contract_title' in data:
            contract.contract_title = data['contract_title']
        if 'contract_text' in data:
            contract.contract_text = data['contract_text']
        if 'status' in data:
            contract.status = data['status']
        if 'party_a' in data:
            contract.party_a = data['party_a']
        if 'party_b' in data:
            contract.party_b = data['party_b']
        if 'contract_amount' in data:
            contract.contract_amount = Decimal(str(data['contract_amount']))
        if 'contract_start_date' in data and data['contract_start_date']:
            contract.contract_start_date = datetime.strptime(data['contract_start_date'], '%Y-%m-%d').date()
        if 'contract_end_date' in data and data['contract_end_date']:
            contract.contract_end_date = datetime.strptime(data['contract_end_date'], '%Y-%m-%d').date()
        
        contract.updated_at = datetime.utcnow()
        
        db.commit()
        
        return jsonify({
            "success": True,
            "message": "更新成功"
        }), 200
        
    except Exception as e:
        logger.error(f"更新合同失败: {str(e)}")
        db.rollback()
        return jsonify({
            "success": False,
            "message": f"更新失败: {str(e)}"
        }), 500


# ============================================
# 删除合同
# ============================================

@contract_bp.route('/delete/<int:contract_id>', methods=['DELETE'])
@require_auth
def delete_contract(user_id, contract_id):
    """
    删除合同
    
    Response:
        {
            "success": true,
            "message": "删除成功"
        }
    """
    try:
        db = get_db()
        
        contract = db.query(Contract).filter(
            Contract.id == contract_id,
            Contract.user_id == user_id
        ).first()
        
        if not contract:
            return jsonify({
                "success": False,
                "message": "合同不存在"
            }), 404
        
        db.delete(contract)
        db.commit()
        
        return jsonify({
            "success": True,
            "message": "删除成功"
        }), 200
        
    except Exception as e:
        logger.error(f"删除合同失败: {str(e)}")
        db.rollback()
        return jsonify({
            "success": False,
            "message": f"删除失败: {str(e)}"
        }), 500
