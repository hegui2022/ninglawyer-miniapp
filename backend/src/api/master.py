"""
主脑调度API - 基于独立架构的版本
使用主脑智能体进行任务路由和协调
"""

from flask import Blueprint, request, jsonify
from loguru import logger
import traceback

from agents.master_brain import master_brain
from utils.logger import log_function_call

# 创建蓝图
master_bp = Blueprint('master', __name__)


@master_bp.route('/route', methods=['POST'])
@log_function_call
def route():
    """
    主脑路由接口
    接收用户输入，自动路由到对应的技能模块
    
    请求格式：
    {
        "user_input": "用户的输入",
        "context": {}  // 上下文信息（可选）
    }
    
    返回格式：
    {
        "success": true/false,
        "data": {},
        "error": ""
    }
    """
    try:
        # 获取请求参数
        data = request.get_json()
        
        if not data or 'user_input' not in data:
            return jsonify({
                'success': False,
                'error': '缺少user_input参数'
            }), 400
        
        user_input = data['user_input']
        context = data.get('context', {})
        
        logger.info(f"🔍 主脑路由接口被调用，用户输入：{user_input[:50]}...")
        
        # 调用主脑路由
        result = master_brain.route(user_input=user_input, context=context)
        
        logger.info(f"✅ 主脑路由完成：{result['success']}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ 主脑路由接口异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'服务器错误：{str(e)}'
        }), 500


@master_bp.route('/desensitize', methods=['POST'])
@log_function_call
def desensitize():
    """
    脱敏接口
    对证据数据进行脱敏处理
    
    请求格式：
    {
        "text": "包含敏感信息的文本"
    }
    
    返回格式：
    {
        "success": true,
        "data": {
            "original": "原始文本",
            "desensitized": "脱敏后文本",
            "details": [...]
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': '缺少text参数'
            }), 400
        
        text = data['text']
        
        logger.info(f"🔒 脱敏接口被调用")
        
        # 直接调用脱敏技能
        from src.skills.desensitize_skill import desensitize_skill
        result = desensitize_skill.execute(user_input=text)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ 脱敏接口异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'服务器错误：{str(e)}'
        }), 500


@master_bp.route('/consult', methods=['POST'])
@log_function_call
def consult():
    """
    法律咨询接口
    提供法律咨询服务
    
    请求格式：
    {
        "question": "用户的问题"
    }
    
    返回格式：
    {
        "success": true,
        "data": {
            "domain": "法律领域",
            "analysis": "法律分析",
            "suggestions": [...]
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': '缺少question参数'
            }), 400
        
        question = data['question']
        
        logger.info(f"⚖️ 法律咨询接口被调用")
        
        # 直接调用民事咨询技能
        from src.skills.civil_consult_skill import civil_consult_skill
        result = civil_consult_skill.execute(user_input=question)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ 法律咨询接口异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'服务器错误：{str(e)}'
        }), 500


@master_bp.route('/contract', methods=['POST'])
@log_function_call
def contract():
    """
    合同接口
    支持合同起草和审查
    
    请求格式：
    {
        "text": "合同起草请求或合同审查内容"
    }
    
    返回格式：
    {
        "success": true,
        "data": {
            "contract": "合同内容" 或 "审查结果"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': '缺少text参数'
            }), 400
        
        text = data['text']
        
        logger.info(f"📄 合同接口被调用")
        
        # 直接调用合同技能
        from src.skills.contract_skill import contract_skill
        result = contract_skill.execute(user_input=text)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ 合同接口异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'服务器错误：{str(e)}'
        }), 500


@master_bp.route('/list-skills', methods=['GET'])
def list_skills():
    """
    列出所有技能
    
    返回格式：
    {
        "success": true,
        "data": {
            "desensitize": {...},
            "civil_consult": {...},
            "contract": {...}
        }
    }
    """
    try:
        skills = master_brain.list_available_skills()
        
        return jsonify({
            'success': True,
            'data': skills
        })
        
    except Exception as e:
        logger.error(f"❌ 列出技能接口异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'服务器错误：{str(e)}'
        }), 500


@master_bp.route('/health', methods=['GET'])
def health():
    """
    健康检查接口
    
    返回格式：
    {
        "status": "ok",
        "timestamp": "时间戳"
    }
    """
    return jsonify({
        'status': 'ok',
        'service': 'ninglawyer-master-brain',
        'timestamp': str(logger)
    })


@master_bp.route('/test', methods=['GET'])
def test():
    """测试接口"""
    logger.info("🧪 主脑调度接口测试")
    
    skills = master_brain.list_available_skills()
    
    return jsonify({
        'message': '宁律师主脑调度接口测试成功',
        'status': 'ok',
        'available_skills': list(skills.keys()),
        'available_apis': [
            'POST /route - 智能路由',
            'POST /desensitize - 脱敏',
            'POST /consult - 法律咨询',
            'POST /contract - 合同起草/审查',
            'GET /list-skills - 列出技能',
            'GET /health - 健康检查',
            'GET /test - 测试接口'
        ]
    })
