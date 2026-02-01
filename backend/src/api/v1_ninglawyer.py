"""
宁律师 V1 API
提供简单、直接的宁律师咨询接口
让用户能够快速看到宁律师的身影
"""

import os
from flask import Blueprint, request, jsonify
from loguru import logger
from typing import Dict, Any, Optional

from src.services.coze_agent_service import CozeAgentService
from src.services.user_service import UserService
from src.services.session_service import SessionService
from src.personas.personality_selector import PersonalitySelector
from src.prompts.ning_lawyer import NingLawyerPrompt
from src.utils.response import success_response, error_response

# 创建蓝图
v1_ninglawyer_bp = Blueprint('v1_ninglawyer', __name__)

# 初始化服务
coze_service = CozeAgentService(access_token=os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY", ""))
user_service = UserService()
session_service = SessionService()
personality_selector = PersonalitySelector()
ninglawyer_prompt = NingLawyerPrompt()

# 宁律师Bot ID（从环境变量读取）
NINGLAWYER_BOT_ID = os.getenv("NINGLAWYER_BOT_ID", "7478766030654679080")

# 对话历史存储（暂时使用内存存储，生产环境使用Redis）
_conversation_history = {}


@v1_ninglawyer_bp.route('/chat', methods=['POST'])
def chat():
    """
    宁律师简单聊天接口
    
    请求体：
    {
        "query": "用户输入的问题",
        "user_id": "用户ID（可选）",
        "session_id": "会话ID（可选，用于多轮对话）",
        "user_type": "用户类型（可选）：individual | company",
        "stream": "是否流式输出（可选，默认false）"
    }
    
    响应：
    {
        "success": true,
        "data": {
            "session_id": "会话ID",
            "answer": "宁律师的回复",
            "bot_id": "Bot ID",
            "bot_name": "宁律师",
            "personality": "使用的人设",
            "intent": "识别的意图",
            "conversation_id": "对话ID"
        }
    }
    """
    try:
        data = request.get_json()
        
        # 1. 参数校验
        if not data or 'query' not in data:
            return error_response("缺少query参数", 400)
        
        query = data.get('query', '').strip()
        if not query:
            return error_response("query参数不能为空", 400)
        
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id')
        user_type = data.get('user_type', 'individual')
        stream = data.get('stream', False)
        
        logger.info(f"🤖 宁律师收到用户咨询 - 用户ID: {user_id}, 问题: {query[:50]}...")
        
        # 2. 获取或创建会话（暂时跳过会话管理，直接使用session_id）
        if not session_id:
            session_id = f"temp_{user_id}_{hash(query) % 10000}"
        
        # 3. 加载历史对话（如果有）
        conversation_history = _load_conversation_history(session_id)
        
        # 4. 动态选择人设（根据用户类型和场景）
        # 先根据query判断场景
        scenario = _identify_scenario(query)
        # 转换user_type格式（individual -> personal, corporate -> corporate）
        user_type_mapped = "personal" if user_type == "individual" else user_type
        personality_id = personality_selector.select(
            user_type=user_type_mapped,
            scenario=scenario,
            app_id="ninglawyer"
        )
        personality = personality_selector.get_personality(personality_id)
        logger.info(f"🎭 选择人设: {personality_id} - {personality.get('name', '')}")
        
        # 4. 识别意图（导流到对应小程序）
        intent_result = _identify_intent(query)
        logger.info(f"🎯 识别意图: {intent_result['intent']}")
        
        # 5. 构建系统提示词（宁律师+人设）
        system_prompt = ninglawyer_prompt.build_prompt(personality=personality['name'])
        
        # 6. 调用扣子智能体（暂时使用模拟数据，快速展示功能）
        logger.info(f"🚀 调用智能体 - Bot ID: {NINGLAWYER_BOT_ID}")
        
        # 暂时使用模拟数据（快速展示功能）
        # TODO: 配置好扣子API后，切换到真实调用
        result = _mock_bot_response(query, personality_id, conversation_history)
        
        # 真实调用扣子API（暂时注释）
        # result = coze_service.run_bot(
        #     bot_id=NINGLAWYER_BOT_ID,
        #     query=query,
        #     user_id=user_id,
        #     conversation_id=session_id,
        #     stream=stream,
        #     additional_messages=conversation_history
        # )
        
        # 7. 处理结果
        if not result.get('success'):
            logger.error(f"❌ 扣子智能体调用失败: {result.get('message')}")
            return error_response(f"咨询失败: {result.get('message')}", 500)
        
        bot_data = result.get('data', {})
        answer = bot_data.get('answer', '')
        conversation_id = bot_data.get('conversation_id', '')
        
        # 8. 保存对话历史
        _save_conversation_history(session_id, query, answer)
        
        # 9. 案源识别（判断用户是否需要律师服务）
        lead_info = _identify_lead(query, intent_result, user_id, session_id)
        if lead_info['is_lead']:
            logger.info(f"🎯 案源识别成功 - 用户ID: {user_id}, 案源类型: {lead_info['lead_type']}")
        
        logger.info(f"✅ 宁律师回复成功 - 会话ID: {session_id}")
        
        # 8. 返回结果
        response_data = {
            'session_id': session_id,
            'answer': answer,
            'bot_id': NINGLAWYER_BOT_ID,
            'bot_name': '宁律师',
            'personality': {
                'id': personality_id,
                'name': personality.get('name', ''),
                'description': personality.get('target_scenario', '')
            },
            'intent': intent_result['intent'],
            'intent_desc': intent_result['description'],
            'conversation_id': conversation_id
        }
        
        return success_response(response_data)
        
    except Exception as e:
        logger.error(f"❌ 宁律师咨询异常: {str(e)}", exc_info=True)
        return error_response(f"咨询失败: {str(e)}", 500)


@v1_ninglawyer_bp.route('/info', methods=['GET'])
def get_info():
    """
    获取宁律师信息
    
    响应：
    {
        "success": true,
        "data": {
            "name": "宁律师",
            "description": "你的智能法律助手",
            "version": "1.0",
            "personalities": [...],
            "features": [...]
        }
    }
    """
    try:
        info = {
            'name': '宁律师',
            'description': '你的智能法律助手，提供专业、高效的法律咨询服务',
            'version': '1.0',
            'bot_id': NINGLAWYER_BOT_ID,
            'personalities': [
                {
                    'id': 'warm',
                    'name': '温暖陪伴型',
                    'description': '适合焦虑当事人，温柔体贴，提供情感支持'
                },
                {
                    'id': 'professional',
                    'name': '专业严谨型',
                    'description': '适合理性用户，专业严谨，逻辑清晰'
                },
                {
                    'id': 'business',
                    'name': '企业商务型',
                    'description': '适合企业用户，高效务实，注重商业价值'
                }
            ],
            'features': [
                '智能法律咨询',
                '人设动态选择',
                '意图识别',
                '多轮对话',
                '案源识别'
            ]
        }
        
        return success_response(info)
        
    except Exception as e:
        logger.error(f"❌ 获取宁律师信息失败: {str(e)}")
        return error_response(f"获取信息失败: {str(e)}", 500)


@v1_ninglawyer_bp.route('/personalities', methods=['GET'])
def get_personalities():
    """
    获取所有人设列表
    
    响应：
    {
        "success": true,
        "data": [...]
    }
    """
    try:
        personalities = personality_selector.get_all_personalities()
        return success_response(personalities)
        
    except Exception as e:
        logger.error(f"❌ 获取人设列表失败: {str(e)}")
        return error_response(f"获取人设列表失败: {str(e)}", 500)


def _mock_bot_response(query: str, personality_id: str, conversation_history: list = None) -> Dict[str, Any]:
    """
    模拟智能体回复（用于快速展示功能）
    
    Args:
        query: 用户输入
        personality_id: 人设ID
        conversation_history: 对话历史（可选）
        
    Returns:
        模拟的回复结果
    """
    # 如果有对话历史，可以在回复中引用之前的对话
    history_context = ""
    if conversation_history and len(conversation_history) > 0:
        history_context = "\n\n（基于我们之前的对话）"
    
    # 根据人设生成不同的回复
    personality_responses = {
        "warm_personal": f"您好！我是宁律师，很高兴为您服务😊{history_context}\n\n关于您提到的「{query}」，我理解您现在的心情。别担心，我会帮您理清楚这个问题。\n\n首先，让我简单跟您说一下相关的法律要点：\n\n1. 这个问题属于民事纠纷范畴，可以通过协商、调解或诉讼解决\n2. 根据法律规定，您有权维护自己的合法权益\n3. 建议您先收集相关证据，如合同、聊天记录、转账记录等\n\n如果您想了解更多细节，可以跟我说说具体情况，我会根据您的具体情况给出更详细的建议。我在这里陪着你，有需要随时问我～",
        
        "professional_personal": f"您好，我是宁律师。关于您咨询的「{query}」问题，我将从法律专业角度为您分析。{history_context}\n\n## 一、法律关系分析\n根据您提供的情况，这是一个法律问题，需要从法律角度进行分析。\n\n## 二、法律依据\n1. 根据《民法典》相关规定，当事人享有合法权益\n2. 根据相关司法解释，您的诉求具有法律依据\n\n## 三、法律分析\n基于您提供的情况：\n1. 您有权维护自己的合法权益\n2. 建议您保留相关证据\n3. 可通过法律途径解决纠纷\n\n## 四、法律建议\n建议您：\n1. 先与对方协商\n2. 协商不成可发送律师函\n3. 必要时向法院提起诉讼\n\n以上是我的法律分析和建议，供您参考。",
        
        "business_corporate": f"您好，我是宁律师，为企业提供高效、务实的法律服务。{history_context}\n\n关于您提到的「{query}」问题，我将从企业风险管理的角度为您分析。\n\n## 风险点分析\n\n### 1. 合规风险\n- 需要检查是否符合相关法律法规\n- 需要完善相关制度和流程\n\n### 2. 商业风险\n- 评估对业务运营的影响\n- 识别潜在的商业风险\n\n### 3. 成本风险\n- 预估可能的经济损失\n- 评估管理成本\n\n## 应对措施\n\n### 1. 建立完善的风险防控机制\n- 完善相关制度和流程\n- 建立风险预警机制\n\n### 2. 加强管理\n- 定期进行风险评估\n- 及时发现和整改问题\n\n### 3. 定期评估\n- 建议定期进行法律风险评估\n- 建立长效机制\n\n如需更详细的合规方案，建议安排专项法律评估。"
    }
    
    # 获取对应人设的回复，如果找不到则使用默认回复
    answer = personality_responses.get(personality_id, personality_responses["warm_personal"])
    
    return {
        "success": True,
        "data": {
            "answer": answer,
            "conversation_id": f"mock_conv_{hash(query)}"
        }
    }


def _identify_scenario(query: str) -> str:
    """
    识别用户场景（用于人设选择）
    
    Args:
        query: 用户输入
        
    Returns:
        场景类型
    """
    query_lower = query.lower()
    
    # 场景识别规则
    scenario_rules = [
        {
            'scenario': 'family_law',
            'keywords': ['离婚', '抚养', '财产分割', '家暴', '婚姻', '夫妻', '孩子']
        },
        {
            'scenario': 'commercial',
            'keywords': ['合同', '违约', '纠纷', '赔偿', '欠款', '债务', '企业']
        },
        {
            'scenario': 'compliance',
            'keywords': ['合规', '风险', '劳动', '税务', '知识产权', '刑事']
        }
    ]
    
    # 匹配场景
    for rule in scenario_rules:
        for keyword in rule['keywords']:
            if keyword in query_lower:
                return rule['scenario']
    
    # 默认场景
    return 'general'


def _identify_intent(query: str) -> Dict[str, str]:
    """
    识别用户意图（导流到对应小程序）
    
    Args:
        query: 用户输入
        
    Returns:
        意图信息
    """
    query_lower = query.lower()
    
    # 意图识别规则
    intent_rules = [
        {
            'intent': 'contract_signing',
            'description': '合同签署',
            'keywords': ['签合同', '签署', '签约', '在线签署', '电子签名']
        },
        {
            'intent': 'contract_management',
            'description': '合同管理',
            'keywords': ['合同管理', '履行', '违约', '催款', '理约']
        },
        {
            'intent': 'judgment_query',
            'description': '裁判观点查询',
            'keywords': ['怎么判', '裁判', '判决', '判例', '胜诉率', '类案']
        },
        {
            'intent': 'lawyer_matching',
            'description': '找律师',
            'keywords': ['找律师', '法律教官', '委托律师', '律师服务']
        },
        {
            'intent': 'compliance_risk',
            'description': '合规风险',
            'keywords': ['合规', '风险防控', '防风险', '企业合规']
        },
        {
            'intent': 'general_consultation',
            'description': '普通法律咨询',
            'keywords': ['咨询', '法律问题', '问律师']
        }
    ]
    
    # 匹配意图
    for rule in intent_rules:
        for keyword in rule['keywords']:
            if keyword in query_lower:
                return {
                    'intent': rule['intent'],
                    'description': rule['description']
                }
    
    # 默认意图
    return {
        'intent': 'general_consultation',
        'description': '普通法律咨询'
    }


def _load_conversation_history(session_id: str, max_history: int = 10) -> list:
    """
    加载对话历史
    
    Args:
        session_id: 会话ID
        max_history: 最大历史记录数
        
    Returns:
        对话历史列表
    """
    global _conversation_history
    
    if session_id not in _conversation_history:
        return []
    
    # 返回最近的历史记录
    history = _conversation_history[session_id]
    return history[-max_history:] if len(history) > max_history else history


def _save_conversation_history(session_id: str, query: str, answer: str):
    """
    保存对话历史
    
    Args:
        session_id: 会话ID
        query: 用户问题
        answer: 宁律师回复
    """
    global _conversation_history
    
    if session_id not in _conversation_history:
        _conversation_history[session_id] = []
    
    # 添加新的对话
    _conversation_history[session_id].append({
        "role": "user",
        "content": query
    })
    _conversation_history[session_id].append({
        "role": "assistant",
        "content": answer
    })
    
    # 限制历史记录数量（最多保留20轮对话）
    max_conversations = 40  # 20轮对话（每轮包含用户和助手各一条）
    if len(_conversation_history[session_id]) > max_conversations:
        _conversation_history[session_id] = _conversation_history[session_id][-max_conversations:]
    
    logger.info(f"💾 保存对话历史 - 会话ID: {session_id}, 对话轮数: {len(_conversation_history[session_id]) // 2}")


def _identify_lead(query: str, intent_result: dict, user_id: str, session_id: str) -> dict:
    """
    案源识别（判断用户是否需要律师服务）
    
    Args:
        query: 用户输入
        intent_result: 意图识别结果
        user_id: 用户ID
        session_id: 会话ID
        
    Returns:
        案源信息
    """
    query_lower = query.lower()
    
    # 案源识别规则
    lead_rules = [
        {
            'lead_type': 'divorce',
            'description': '离婚咨询',
            'keywords': ['离婚', '财产分割', '抚养权', '家暴'],
            'priority': 'high'
        },
        {
            'lead_type': 'debt',
            'description': '债务纠纷',
            'keywords': ['债务', '欠款', '借钱', '还钱', '追债'],
            'priority': 'medium'
        },
        {
            'lead_type': 'contract_dispute',
            'description': '合同纠纷',
            'keywords': ['合同', '违约', '纠纷', '赔偿'],
            'priority': 'medium'
        },
        {
            'lead_type': 'injury',
            'description': '人身损害',
            'keywords': ['受伤', '赔偿', '医疗', '事故'],
            'priority': 'high'
        },
        {
            'lead_type': 'company',
            'description': '企业法务',
            'keywords': ['公司', '企业', '合规', '劳动'],
            'priority': 'medium'
        }
    ]
    
    # 匹配案源
    for rule in lead_rules:
        for keyword in rule['keywords']:
            if keyword in query_lower:
                return {
                    'is_lead': True,
                    'lead_type': rule['lead_type'],
                    'lead_description': rule['description'],
                    'priority': rule['priority'],
                    'user_id': user_id,
                    'session_id': session_id,
                    'query': query,
                    'intent': intent_result.get('intent', ''),
                    'timestamp': _get_current_timestamp()
                }
    
    # 不是案源
    return {
        'is_lead': False,
        'lead_type': None,
        'lead_description': None,
        'priority': None,
        'user_id': user_id,
        'session_id': session_id,
        'query': query,
        'intent': intent_result.get('intent', ''),
        'timestamp': _get_current_timestamp()
    }


def _get_current_timestamp() -> str:
    """获取当前时间戳"""
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

