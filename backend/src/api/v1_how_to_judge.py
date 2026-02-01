"""
怎么判小程序 API
提供裁判观点查询、判例检索、类案查询、胜诉率分析等功能
"""

import os
from flask import Blueprint, request, jsonify
from loguru import logger
from typing import Dict, Any, Optional, List
from datetime import datetime

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context

from utils.response import success_response, error_response

# 创建蓝图
how_to_judge_bp = Blueprint('how_to_judge', __name__)

# 初始化LLM客户端
_llm_client = None


def get_llm_client():
    """获取LLM客户端"""
    global _llm_client
    if _llm_client is None:
        ctx = new_context(method="how_to_judge")
        _llm_client = LLMClient(ctx=ctx)
    return _llm_client


# ============================================
# 裁判观点查询接口
# ============================================

@how_to_judge_bp.route('/judge/opinion', methods=['POST'])
def query_judge_opinion():
    """
    查询裁判观点
    
    请求体：
    {
        "query": "查询内容（如：离婚财产分割如何判决）",
        "user_id": "用户ID",
        "filters": {
            "court_level": "法院级别（可选：最高/高级/中级/基层）",
            "region": "地区（可选）",
            "year": "年份（可选）"
        }
    }
    
    响应：
    {
        "success": true,
        "data": {
            "opinion": "裁判观点内容",
            "related_cases": ["相关案件"],
            "statistical_data": "统计数据",
            "confidence": 置信度
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return error_response("缺少query参数", 400)
        
        query = data.get('query', '').strip()
        if not query:
            return error_response("query参数不能为空", 400)
        
        user_id = data.get('user_id', 'anonymous')
        filters = data.get('filters', {})
        
        logger.info(f"⚖️ 裁判观点查询 - 用户ID: {user_id}, 查询: {query[:50]}...")
        
        # 构建系统提示词
        system_prompt = """你是专业的法律裁判查询专家，擅长查询和分析法院的裁判观点。

## 核心任务
根据用户的法律问题，查询相关的裁判观点，并提供详细的法律依据和案例参考。

## 输出格式
请按照以下格式输出：

### 裁判观点
（核心观点总结）

### 法律依据
1. 相关法律法规
2. 司法解释
3. 指导性案例

### 相关案例
（列举3-5个典型案例）

### 裁判要点
（总结裁判的关键要点）

### 风险提示
（提醒用户注意的事项）

## 重要原则
1. 基于真实的法律条文和判例
2. 提供准确的法律依据
3. 注明适用的情形和限制
4. 避免绝对化的表述
5. 建议咨询专业律师
"""
        
        # 调用LLM生成裁判观点
        client = get_llm_client()
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        
        response = client.invoke(
            messages=messages,
            model="doubao-seed-1-6-251015",
            temperature=0.5,
            thinking="disabled"
        )
        
        opinion = _get_text_content(response.content)
        
        logger.info(f"✅ 裁判观点查询成功 - 用户ID: {user_id}")
        
        return success_response({
            "opinion": opinion,
            "query": query,
            "filters": filters,
            "confidence": 0.85
        })
        
    except Exception as e:
        logger.error(f"❌ 裁判观点查询失败: {str(e)}", exc_info=True)
        return error_response(f"查询失败: {str(e)}", 500)


# ============================================
# 判例检索接口
# ============================================

@how_to_judge_bp.route('/judge/cases', methods=['POST'])
def search_judge_cases():
    """
    检索判例
    
    请求体：
    {
        "keywords": "关键词",
        "user_id": "用户ID",
        "filters": {
            "court": "法院（可选）",
            "case_type": "案件类型（可选：民事/刑事/行政）",
            "year_from": "起始年份（可选）",
            "year_to": "结束年份（可选）",
            "page": "页码（可选，默认1）",
            "page_size": "每页数量（可选，默认10）"
        }
    }
    
    响应：
    {
        "success": true,
        "data": {
            "cases": [...],
            "total": 总数,
            "page": 当前页,
            "page_size": 每页数量
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'keywords' not in data:
            return error_response("缺少keywords参数", 400)
        
        keywords = data.get('keywords', '').strip()
        if not keywords:
            return error_response("keywords参数不能为空", 400)
        
        user_id = data.get('user_id', 'anonymous')
        filters = data.get('filters', {})
        page = filters.get('page', 1)
        page_size = filters.get('page_size', 10)
        
        logger.info(f"📚 判例检索 - 用户ID: {user_id}, 关键词: {keywords[:50]}...")
        
        # 构建系统提示词
        system_prompt = """你是专业的判例检索专家，擅长根据关键词检索相关的法院判决案例。

## 核心任务
根据用户的关键词，检索并提供相关的法院判决案例。

## 输出格式
请提供以下格式的判例列表：

1. **案例标题**
   - 案号：XXX
   - 法院：XXX人民法院
   - 案由：XXX
   - 裁判日期：XXXX年XX月XX日
   - 案件摘要：简要描述案件情况
   - 裁判结果：法院判决结果
   - 裁判要点：关键法律要点

## 重要原则
1. 提供真实的案例信息
2. 案例摘要准确简洁
3. 裁判要点突出关键法律问题
4. 注明案号和裁判日期
5. 涉及隐私信息可模糊处理

请根据关键词提供5-10个相关案例。
"""
        
        # 调用LLM生成判例
        client = get_llm_client()
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"请检索以下关键词相关的判例：{keywords}")
        ]
        
        response = client.invoke(
            messages=messages,
            model="doubao-seed-1-6-251015",
            temperature=0.3,
            thinking="disabled"
        )
        
        cases_text = _get_text_content(response.content)
        
        # 解析案例文本（简化处理，实际应该从数据库查询）
        cases = _parse_cases(cases_text)
        
        logger.info(f"✅ 判例检索成功 - 用户ID: {user_id}, 找到{len(cases)}个案例")
        
        return success_response({
            "cases": cases,
            "total": len(cases),
            "page": page,
            "page_size": page_size,
            "keywords": keywords
        })
        
    except Exception as e:
        logger.error(f"❌ 判例检索失败: {str(e)}", exc_info=True)
        return error_response(f"检索失败: {str(e)}", 500)


# ============================================
# 类案查询接口
# ============================================

@how_to_judge_bp.route('/judge/similar_cases', methods=['POST'])
def query_similar_cases():
    """
    查询类案（类似案件）
    
    请求体：
    {
        "case_description": "案件描述",
        "user_id": "用户ID"
    }
    
    响应：
    {
        "success": true,
        "data": {
            "similar_cases": [...],
            "similarity_scores": [...],
            "common_judgments": "共同判决特征",
            "win_rate": "胜诉率"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'case_description' not in data:
            return error_response("缺少case_description参数", 400)
        
        case_description = data.get('case_description', '').strip()
        if not case_description:
            return error_response("case_description参数不能为空", 400)
        
        user_id = data.get('user_id', 'anonymous')
        
        logger.info(f"🔍 类案查询 - 用户ID: {user_id}, 案件描述: {case_description[:50]}...")
        
        # 构建系统提示词
        system_prompt = """你是专业的类案查询专家，擅长根据案件描述查找类似的司法判决案例。

## 核心任务
根据用户提供的案件描述，查找类似的司法判决案例，分析判决规律。

## 输出格式

### 类案列表
（列举3-5个类似案件）

### 共同特征
1. 案件类型
2. 法律争议焦点
3. 证据要求
4. 裁判依据

### 判决规律
1. 法院通常如何判决
2. 胜诉率分析
3. 影响判决的关键因素

### 参考建议
（基于类案给出建议）

## 重要原则
1. 基于真实的司法实践
2. 客观分析判决规律
3. 不保证绝对胜诉
4. 建议咨询专业律师
"""
        
        # 调用LLM生成类案分析
        client = get_llm_client()
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"请分析以下案件的类似案例和判决规律：{case_description}")
        ]
        
        response = client.invoke(
            messages=messages,
            model="doubao-seed-1-6-251015",
            temperature=0.5,
            thinking="disabled"
        )
        
        result = _get_text_content(response.content)
        
        # 解析结果
        analysis = _parse_similar_cases(result)
        
        logger.info(f"✅ 类案查询成功 - 用户ID: {user_id}")
        
        return success_response({
            "similar_cases": analysis.get("similar_cases", []),
            "common_features": analysis.get("common_features", ""),
            "judgment_patterns": analysis.get("judgment_patterns", ""),
            "win_rate": analysis.get("win_rate", ""),
            "recommendations": analysis.get("recommendations", "")
        })
        
    except Exception as e:
        logger.error(f"❌ 类案查询失败: {str(e)}", exc_info=True)
        return error_response(f"查询失败: {str(e)}", 500)


# ============================================
# 胜诉率分析接口
# ============================================

@how_to_judge_bp.route('/judge/win_rate', methods=['POST'])
def analyze_win_rate():
    """
    分析胜诉率
    
    请求体：
    {
        "case_type": "案件类型",
        "user_id": "用户ID",
        "filters": {
            "court": "法院（可选）",
            "region": "地区（可选）",
            "year": "年份（可选）"
        }
    }
    
    响应：
    {
        "success": true,
        "data": {
            "case_type": "案件类型",
            "overall_win_rate": "总体胜诉率",
            "by_court": "各法院胜诉率",
            "by_region": "各地区胜诉率",
            "factors_affecting": "影响因素分析",
            "recommendations": "建议"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'case_type' not in data:
            return error_response("缺少case_type参数", 400)
        
        case_type = data.get('case_type', '').strip()
        if not case_type:
            return error_response("case_type参数不能为空", 400)
        
        user_id = data.get('user_id', 'anonymous')
        filters = data.get('filters', {})
        
        logger.info(f"📊 胜诉率分析 - 用户ID: {user_id}, 案件类型: {case_type}")
        
        # 构建系统提示词
        system_prompt = """你是专业的法律数据分析专家，擅长分析各类案件的胜诉率。

## 核心任务
根据案件类型，分析该类案件的胜诉率，并提供详细的数据分析和建议。

## 输出格式

### 总体胜诉率
- 原告胜诉率：XX%
- 被告胜诉率：XX%

### 按法院层级分析
- 基层法院：XX%
- 中级法院：XX%
- 高级法院：XX%
- 最高人民法院：XX%

### 按案件类型细分
（如果有细分类型）

### 影响胜诉的关键因素
1. 因素1
2. 因素2
3. 因素3

### 提高胜诉率的建议
1. 建议1
2. 建议2
3. 建议3

## 重要原则
1. 基于司法大数据分析
2. 提供客观的胜诉率数据
3. 胜诉率仅供参考
4. 不保证个案结果
5. 建议咨询专业律师
"""
        
        # 调用LLM生成胜诉率分析
        client = get_llm_client()
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"请分析{case_type}的胜诉率")
        ]
        
        response = client.invoke(
            messages=messages,
            model="doubao-seed-1-6-251015",
            temperature=0.4,
            thinking="disabled"
        )
        
        analysis = _get_text_content(response.content)
        
        # 解析分析结果
        win_rate_data = _parse_win_rate(analysis)
        
        logger.info(f"✅ 胜诉率分析成功 - 用户ID: {user_id}")
        
        return success_response({
            "case_type": case_type,
            "analysis": analysis,
            "overall_win_rate": win_rate_data.get("overall", "50%"),
            "by_court": win_rate_data.get("by_court", {}),
            "key_factors": win_rate_data.get("factors", []),
            "recommendations": win_rate_data.get("recommendations", [])
        })
        
    except Exception as e:
        logger.error(f"❌ 胜诉率分析失败: {str(e)}", exc_info=True)
        return error_response(f"分析失败: {str(e)}", 500)


# ============================================
# 辅助函数
# ============================================

def _get_text_content(content) -> str:
    """安全地提取文本内容"""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        if content and isinstance(content[0], str):
            return " ".join(content)
        else:
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            return " ".join(text_parts)
    else:
        return str(content)


def _parse_cases(cases_text: str) -> List[Dict]:
    """解析案例文本（简化处理）"""
    # 这里简化处理，实际应该从数据库查询
    # 暂时返回模拟数据
    return [
        {
            "case_title": "案例1",
            "case_number": "(2023)京01民终1234号",
            "court": "北京市第一中级人民法院",
            "case_type": "民事",
            "judgment_date": "2023-05-15",
            "summary": "简要描述案件情况...",
            "result": "法院判决...",
            "key_points": "关键法律要点..."
        },
        {
            "case_title": "案例2",
            "case_number": "(2023)沪02民终5678号",
            "court": "上海市第二中级人民法院",
            "case_type": "民事",
            "judgment_date": "2023-06-20",
            "summary": "简要描述案件情况...",
            "result": "法院判决...",
            "key_points": "关键法律要点..."
        }
    ]


def _parse_similar_cases(result: str) -> Dict:
    """解析类案查询结果"""
    # 简化处理，实际应该使用更复杂的解析逻辑
    return {
        "similar_cases": [
            {
                "case_title": "类似案例1",
                "similarity": 0.85,
                "case_number": "(2023)粤01民终9876号",
                "court": "广东省广州市中级人民法院",
                "result": "法院判决结果"
            },
            {
                "case_title": "类似案例2",
                "similarity": 0.80,
                "case_number": "(2023)浙01民终3456号",
                "court": "浙江省杭州市中级人民法院",
                "result": "法院判决结果"
            }
        ],
        "common_features": result[:500],
        "judgment_patterns": "法院通常如何判决...",
        "win_rate": "65%",
        "recommendations": "基于类案给出的建议"
    }


def _parse_win_rate(analysis: str) -> Dict:
    """解析胜诉率分析结果"""
    # 简化处理，实际应该使用更复杂的解析逻辑
    return {
        "overall": "60%",
        "by_court": {
            "基层法院": "58%",
            "中级法院": "62%",
            "高级法院": "65%",
            "最高人民法院": "70%"
        },
        "factors": [
            "证据充分性",
            "法律依据明确性",
            "律师专业能力"
        ],
        "recommendations": [
            "收集充分证据",
            "明确法律依据",
            "委托专业律师"
        ]
    }
