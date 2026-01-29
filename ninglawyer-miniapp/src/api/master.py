"""
主脑调度API - 提供统一的调度接口
供小程序调用
"""

from flask import Blueprint, request, jsonify
from loguru import logger
import traceback

from src.agents.master_agent import MasterAgent
from src.utils.logger import log_function_call

# 创建蓝图
master_bp = Blueprint('master', __name__)

# 创建主脑实例
master_agent = MasterAgent(use_coze_bots=True)


@master_bp.route('/route', methods=['POST'])
@log_function_call
def route():
    """
    主脑路由接口
    接收用户输入，路由到对应的Bot
    
    请求格式：
    {
        "user_input": "用户的输入",
        "user_id": "用户ID（可选）",
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
        user_id = data.get('user_id', 'default')
        context = data.get('context', {})
        
        logger.info(f"主脑路由接口被调用，用户输入：{user_input}，用户ID：{user_id}")
        
        # 调用主脑路由
        result = master_agent.route(user_input=user_input, context=context)
        
        logger.info(f"主脑路由结果：{result}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"主脑路由接口异常：{str(e)}")
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
        "name": "姓名",
        "id_card": "身份证号",
        "phone": "手机号",
        "address": "地址"
    }
    
    返回格式：
    {
        "success": true/false,
        "data": {
            "name": "脱敏后姓名",
            "id_card": "脱敏后身份证",
            "phone": "脱敏后手机",
            "address": "脱敏后地址"
        }
    }
    """
    try:
        # 获取请求参数
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '缺少请求参数'
            }), 400
        
        logger.info(f"脱敏接口被调用，数据：{data}")
        
        # 构造查询语句
        query_parts = []
        for key, value in data.items():
            if value:
                query_parts.append(f"{key}：{value}")
        
        query = "帮我脱敏以下数据：" + "，".join(query_parts)
        
        # 调用脱敏Bot
        result = master_agent.route(user_input=query)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"脱敏接口异常：{str(e)}")
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
        "question": "用户的问题",
        "domain": "法律领域（可选）",
        "user_id": "用户ID（可选）"
    }
    
    返回格式：
    {
        "success": true/false,
        "data": {
            "answer": "律师的回答",
            "domain": "法律领域",
            "citations": []  // 法律条文引用
        }
    }
    """
    try:
        # 获取请求参数
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': '缺少question参数'
            }), 400
        
        question = data['question']
        user_id = data.get('user_id', 'default')
        domain = data.get('domain', '')
        
        logger.info(f"法律咨询接口被调用，问题：{question}，领域：{domain}")
        
        # 构造查询
        query = f"{domain}咨询：{question}" if domain else question
        
        # 调用主脑路由
        result = master_agent.route(
            user_input=query,
            context={'user_id': user_id}
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"法律咨询接口异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'服务器错误：{str(e)}'
        }), 500


@master_bp.route('/list-bots', methods=['GET'])
def list_bots():
    """
    列出所有Bot
    
    返回格式：
    {
        "success": true,
        "data": {
            "desensitize": {...},
            "civil_consult": {...}
        }
    }
    """
    try:
        bots = master_agent.bot_registry.list_bots()
        
        return jsonify({
            'success': True,
            'data': bots
        })
        
    except Exception as e:
        logger.error(f"列出Bot接口异常：{str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'服务器错误：{str(e)}'
        }), 500


@master_bp.route('/draft-contract', methods=['POST'])
@log_function_call
def draft_contract():
    """
    合同起草接口
    
    请求格式：
    {
        "contract_type": "合同类型",
        "details": "合同详情"
    }
    
    返回格式：
    {
        "success": true/false,
        "data": {
            "contract": "合同文本",
            "tips": "提示信息"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '缺少请求参数'
            }), 400
        
        contract_type = data.get('contract_type', '')
        details = data.get('details', '')
        
        logger.info(f"合同起草接口被调用，类型：{contract_type}，详情：{details}")
        
        # 构造查询
        if contract_type and details:
            query = f"起草一个{contract_type}，要求：{details}"
        elif contract_type:
            query = f"起草一个{contract_type}"
        else:
            return jsonify({
                'success': False,
                'error': '请提供合同类型'
            }), 400
        
        # 调用主脑路由
        result = master_agent.route(user_input=query)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"合同起草接口异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'服务器错误：{str(e)}'
        }), 500


@master_bp.route('/review-contract', methods=['POST'])
@log_function_call
def review_contract():
    """
    合同审查接口
    
    请求格式：
    {
        "contract_content": "合同内容"
    }
    
    返回格式：
    {
        "success": true/false,
        "data": {
            "risks": "风险点",
            "suggestions": "建议"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'contract_content' not in data:
            return jsonify({
                'success': False,
                'error': '缺少contract_content参数'
            }), 400
        
        contract_content = data['contract_content']
        
        logger.info(f"合同审查接口被调用")
        
        # 构造查询
        query = f"帮我审查这个合同：{contract_content}"
        
        # 调用主脑路由
        result = master_agent.route(user_input=query)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"合同审查接口异常：{str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': f'服务器错误：{str(e)}'
        }), 500


@master_bp.route('/register-bot', methods=['POST'])
def register_bot():
    """
    注册Bot（仅供管理使用）
    
    请求格式：
    {
        "bot_type": "Bot类型",
        "bot_id": "Bot ID",
        "api_token_env": "环境变量名",
        "name": "Bot名称",
        "description": "Bot描述"
    }
    
    返回格式：
    {
        "success": true,
        "message": "注册成功"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '缺少请求参数'
            }), 400
        
        bot_type = data.get('bot_type')
        bot_id = data.get('bot_id')
        api_token_env = data.get('api_token_env')
        name = data.get('name', '')
        description = data.get('description', '')
        
        if not bot_type or not bot_id or not api_token_env:
            return jsonify({
                'success': False,
                'error': '缺少必需参数：bot_type, bot_id, api_token_env'
            }), 400
        
        # 注册Bot
        master_agent.bot_registry.register_bot(
            bot_type=bot_type,
            bot_id=bot_id,
            api_token=api_token_env,
            name=name,
            description=description
        )
        
        return jsonify({
            'success': True,
            'message': f'成功注册Bot：{name}'
        })
        
    except Exception as e:
        logger.error(f"注册Bot接口异常：{str(e)}")
        
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
        'timestamp': str(loguru.logger)
    })


@master_bp.route('/test', methods=['GET'])
def test():
    """测试接口"""
    logger.info("主脑调度接口测试")
    
    return jsonify({
        'message': '宁律师主脑调度接口测试成功',
        'status': 'ok',
        'available_apis': [
            'POST /route - 主脑路由',
            'POST /desensitize - 脱敏',
            'POST /consult - 法律咨询',
            'POST /draft-contract - 合同起草',
            'POST /review-contract - 合同审查',
            'GET /list-bots - 列出Bot',
            'POST /register-bot - 注册Bot',
            'GET /health - 健康检查',
            'GET /test - 测试接口'
        ]
    })
