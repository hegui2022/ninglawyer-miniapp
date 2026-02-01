"""
法律教官 API
提供案例录入、案例查询等功能
"""

import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from loguru import logger
from sqlalchemy.orm import joinedload

from models.case_model import LegalCase, CaseProceeding, CaseLaw, case_to_dict
from utils.database import get_db
from utils.response import success_response, error_response

# 创建蓝图
legal_instructor_bp = Blueprint('legal_instructor', __name__)


# ============================================
# 案例：创建案例（PC端录入）
# ============================================

@legal_instructor_bp.route('/cases', methods=['POST'])
def create_case():
    """
    创建案例（PC端录入）
    
    请求体：
    {
        "title": "标题",
        "subtitle": "副标题",
        "keywords": [
            {"type": "裁判类型", "value": "判决"},
            {"type": "案由", "value": "盗窃"},
            {"value": "关键词1"},
            {"value": "关键词2"}
        ],
        "basic_facts": "<p>基本案情HTML</p>",
        "judgment_essence": "<p>裁判要旨HTML</p>",
        "judgment_result": "<p>裁判结果HTML</p>",
        "dispute_foci": ["焦点1", "焦点2"],
        "related_index": {
            "laws": [
                {"law_name": "刑法", "article_numbers": "第1条、第2条"}
            ],
            "proceedings": [
                {
                    "procedure_type": "一审",
                    "court": "北京市朝阳区人民法院",
                    "case_number": "...",
                    "judgment_type": "...",
                    "judgment_date": "2024-01-01"
                }
            ]
        },
        "status": "published",  // 可选，默认draft
        "created_by": "admin"  // 可选
    }
    """
    try:
        data = request.json
        
        # 验证必填字段
        required_fields = ['title', 'subtitle', 'keywords']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"缺少必填字段: {field}")
        
        # 创建案例主记录
        case = LegalCase(
            title=data['title'],
            subtitle=data['subtitle'],
            keywords=json.dumps(data.get('keywords', []), ensure_ascii=False),
            basic_facts=data.get('basic_facts'),
            judgment_essence=data.get('judgment_essence'),
            judgment_result=data.get('judgment_result'),
            dispute_foci=json.dumps(data.get('dispute_foci', []), ensure_ascii=False),
            related_index=json.dumps(data.get('related_index', {}), ensure_ascii=False),
            status=data.get('status', 'published'),
            created_by=data.get('created_by', 'legal_instructor')
        )
        
        db = get_db()
        db.add(case)
        db.flush()  # 获取case.id
        
        # 添加历审程序
        if data.get('related_index', {}).get('proceedings'):
            for proc_data in data['related_index']['proceedings']:
                proceeding = CaseProceeding(
                    case_id=case.id,
                    procedure_type=proc_data.get('procedure_type'),
                    court=proc_data.get('court'),
                    case_number=proc_data.get('case_number'),
                    judgment_type=proc_data.get('judgment_type'),
                    judgment_date=datetime.fromisoformat(proc_data['judgment_date']) if proc_data.get('judgment_date') else None
                )
                db.add(proceeding)
        
        # 添加主要法条
        if data.get('related_index', {}).get('laws'):
            for law_data in data['related_index']['laws']:
                law = CaseLaw(
                    case_id=case.id,
                    law_name=law_data.get('law_name'),
                    article_numbers=law_data.get('article_numbers')
                )
                db.add(law)
        
        db.commit()
        
        logger.info(f"案例创建成功: case_id={case.id}, title={case.title}")
        
        return success_response(
            data=case_to_dict(case),
            message="案例创建成功"
        )
        
    except Exception as e:
        logger.error(f"创建案例失败: {str(e)}")
        return error_response(f"创建案例失败: {str(e)}")


# ============================================
# 案例：获取案例列表（小程序）
# ============================================

@legal_instructor_bp.route('/cases', methods=['GET'])
def get_cases():
    """
    获取案例列表（小程序）
    
    查询参数：
    - keyword: 关键词搜索（可选）
    - page: 页码（默认1）
    - page_size: 每页数量（默认10）
    """
    try:
        keyword = request.args.get('keyword', '').strip()
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        db = get_db()
        
        # 构建查询
        query = db.query(LegalCase).filter(LegalCase.status == 'published')
        
        # 关键词搜索
        if keyword:
            query = query.filter(
                (LegalCase.title.ilike(f'%{keyword}%')) |
                (LegalCase.subtitle.ilike(f'%{keyword}%'))
            )
        
        # 分页
        total = query.count()
        cases = query.order_by(LegalCase.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        
        # 转换为字典
        cases_list = [case_to_dict(case) for case in cases]
        
        return success_response(
            data={
                'cases': cases_list,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            }
        )
        
    except Exception as e:
        logger.error(f"获取案例列表失败: {str(e)}")
        return error_response(f"获取案例列表失败: {str(e)}")


# ============================================
# 案例：获取案例详情（小程序）
# ============================================

@legal_instructor_bp.route('/cases/<int:case_id>', methods=['GET'])
def get_case_detail(case_id):
    """
    获取案例详情（小程序）
    """
    try:
        db = get_db()
        
        case = db.query(LegalCase).options(
            joinedload(LegalCase.proceedings),
            joinedload(LegalCase.laws)
        ).filter(
            LegalCase.id == case_id,
            LegalCase.status == 'published'
        ).first()
        
        if not case:
            return error_response("案例不存在", code=404)
        
        return success_response(data=case_to_dict(case))
        
    except Exception as e:
        logger.error(f"获取案例详情失败: {str(e)}")
        return error_response(f"获取案例详情失败: {str(e)}")


# ============================================
# 案例：更新案例
# ============================================

@legal_instructor_bp.route('/cases/<int:case_id>', methods=['PUT'])
def update_case(case_id):
    """
    更新案例
    
    请求体：同创建案例
    """
    try:
        data = request.json
        
        db = get_db()
        
        # 查找案例
        case = db.query(LegalCase).options(
            joinedload(LegalCase.proceedings),
            joinedload(LegalCase.laws)
        ).filter(LegalCase.id == case_id).first()
        
        if not case:
            return error_response("案例不存在", code=404)
        
        # 更新主表数据
        case.title = data['title']
        case.subtitle = data['subtitle']
        case.keywords = json.dumps(data.get('keywords', []), ensure_ascii=False)
        case.basic_facts = data.get('basic_facts')
        case.judgment_essence = data.get('judgment_essence')
        case.judgment_result = data.get('judgment_result')
        case.dispute_foci = json.dumps(data.get('dispute_foci', []), ensure_ascii=False)
        case.related_index = json.dumps(data.get('related_index', {}), ensure_ascii=False)
        case.updated_at = datetime.utcnow()
        
        # 删除原有的历审程序和法条
        for proc in case.proceedings:
            db.delete(proc)
        for law in case.laws:
            db.delete(law)
        
        # 重新添加历审程序
        if data.get('related_index', {}).get('proceedings'):
            for proc_data in data['related_index']['proceedings']:
                proceeding = CaseProceeding(
                    case_id=case.id,
                    procedure_type=proc_data.get('procedure_type'),
                    court=proc_data.get('court'),
                    case_number=proc_data.get('case_number'),
                    judgment_type=proc_data.get('judgment_type'),
                    judgment_date=datetime.fromisoformat(proc_data['judgment_date']) if proc_data.get('judgment_date') else None
                )
                db.add(proceeding)
        
        # 重新添加法条
        if data.get('related_index', {}).get('laws'):
            for law_data in data['related_index']['laws']:
                law = CaseLaw(
                    case_id=case.id,
                    law_name=law_data.get('law_name'),
                    article_numbers=law_data.get('article_numbers')
                )
                db.add(law)
        
        db.commit()
        
        logger.info(f"案例更新成功: case_id={case_id}, title={case.title}")
        
        return success_response(
            data=case_to_dict(case),
            message="案例更新成功"
        )
        
    except Exception as e:
        logger.error(f"更新案例失败: {str(e)}")
        return error_response(f"更新案例失败: {str(e)}")


# ============================================
# 案例：删除案例（可选）
# ============================================

@legal_instructor_bp.route('/cases/<int:case_id>', methods=['DELETE'])
def delete_case(case_id):
    """
    删除案例
    """
    try:
        db = get_db()
        
        case = db.query(LegalCase).filter(LegalCase.id == case_id).first()
        
        if not case:
            return error_response("案例不存在", code=404)
        
        db.delete(case)
        db.commit()
        
        logger.info(f"案例删除成功: case_id={case_id}")
        
        return success_response(message="案例删除成功")
        
    except Exception as e:
        logger.error(f"删除案例失败: {str(e)}")
        return error_response(f"删除案例失败: {str(e)}")


# ============================================
# 案例：根据关键词搜索案例（用于怎么判的判例检索功能）
# ============================================

@legal_instructor_bp.route('/cases/search', methods=['POST'])
def search_cases():
    """
    根据关键词搜索案例（用于怎么判的判例检索功能）
    
    请求体：
    {
        "keywords": "盗窃",
        "filters": {
            "court": "基层法院",  // 可选
            "case_type": "刑事"   // 可选
        }
    }
    """
    try:
        data = request.json
        keywords = data.get('keywords', '').strip()
        filters = data.get('filters', {})
        
        db = get_db()
        
        # 构建查询
        query = db.query(LegalCase).filter(LegalCase.status == 'published')
        
        # 关键词搜索（标题、副标题、关键词）
        if keywords:
            query = query.filter(
                (LegalCase.title.ilike(f'%{keywords}%')) |
                (LegalCase.subtitle.ilike(f'%{keywords}%')) |
                (LegalCase.basic_facts.ilike(f'%{keywords}%'))
            )
        
        # 应用筛选条件（从keywords中筛选）
        if filters.get('case_type'):
            # 从keywords中筛选案由
            query = query.filter(
                LegalCase.keywords.ilike(f'%{filters["case_type"]}%')
            )
        
        cases = query.order_by(LegalCase.created_at.desc()).limit(20).all()
        
        # 转换为判例检索格式
        search_results = []
        for case in cases:
            # 使用 case_to_dict 解析数据
            case_dict = case_to_dict(case)
            
            # 从keywords中提取裁判类型和案由
            judgment_type = None
            cause_of_action = None
            for kw in case_dict.get('keywords', []):
                if isinstance(kw, dict):
                    if kw.get('type') == '裁判类型':
                        judgment_type = kw.get('value')
                    elif kw.get('type') == '案由':
                        cause_of_action = kw.get('value')
            
            search_results.append({
                'case_id': case_dict['id'],
                'case_title': case_dict['title'],
                'case_number': case_dict['proceedings'][0]['case_number'] if case_dict['proceedings'] else '',
                'court': case_dict['proceedings'][0]['court'] if case_dict['proceedings'] else '',
                'judgment_type': judgment_type,
                'cause_of_action': cause_of_action,
                'result': case_dict['judgment_result'][:100] + '...' if case_dict['judgment_result'] and len(case_dict['judgment_result']) > 100 else case_dict['judgment_result'] or '',
                'judgment_essence': case_dict['judgment_essence']
            })
        
        return success_response(
            data={
                'cases': search_results,
                'total': len(search_results)
            }
        )
        
    except Exception as e:
        logger.error(f"搜索案例失败: {str(e)}")
        return error_response(f"搜索案例失败: {str(e)}")
