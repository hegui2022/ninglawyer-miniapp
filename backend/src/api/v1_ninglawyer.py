"""
宁律师 V1 API
提供简单、直接的宁律师咨询接口
让用户能够快速看到宁律师的身影
"""

import os
import json
from flask import Blueprint, request, jsonify
from loguru import logger
from typing import Dict, Any, Optional, Union, List

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context

from services.coze_agent_service import CozeAgentService
from services.user_service import UserService
from services.session_service import SessionService
from personas.personality_selector import PersonalitySelector
from prompts.ning_lawyer import NingLawyerPrompt
from utils.response import success_response, error_response
from utils.cache_manager import CacheManager

# 创建蓝图
v1_ninglawyer_bp = Blueprint('v1_ninglawyer', __name__)

# 初始化服务
coze_service = CozeAgentService(access_token=os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY", ""))
user_service = UserService()
session_service = SessionService()
personality_selector = PersonalitySelector()
ninglawyer_prompt = NingLawyerPrompt()

# 缓存管理器（用于对话历史和用户信息）
cache_manager = CacheManager()

# 宁律师Bot ID（从环境变量读取）
NINGLAWYER_BOT_ID = os.getenv("NINGLAWYER_BOT_ID", "7478766030654679080")

# 对话历史存储（使用Redis缓存，24小时过期）
CONVERSATION_TTL = 86400  # 24小时


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
        
        # 6. 调用LLM生成回复
        logger.info(f"🚀 调用LLM - 人设: {personality_id}")
        
        # 调用真实的LLM
        result = _call_llm(
            query=query,
            system_prompt=system_prompt,
            conversation_history=conversation_history
        )
        
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


def _call_llm(query: str, system_prompt: str, conversation_history: list = None) -> Dict[str, Any]:
    """
    调用LLM生成回复
    
    Args:
        query: 用户输入
        system_prompt: 系统提示词
        conversation_history: 对话历史（可选）
        
    Returns:
        LLM回复结果
    """
    try:
        # 创建上下文
        ctx = new_context(method="ninglawyer_chat")
        
        # 创建LLM客户端
        client = LLMClient(ctx=ctx)
        
        # 构建消息列表
        messages = []
        
        # 添加系统提示词
        messages.append(SystemMessage(content=system_prompt))
        
        # 添加对话历史
        if conversation_history and len(conversation_history) > 0:
            for msg in conversation_history:
                if msg.get('role') == 'user':
                    messages.append(HumanMessage(content=msg.get('content', '')))
                elif msg.get('role') == 'assistant':
                    messages.append(AIMessage(content=msg.get('content', '')))
        
        # 添加当前用户输入
        messages.append(HumanMessage(content=query))
        
        # 调用LLM
        logger.info(f"🤖 调用LLM - 消息数量: {len(messages)}, 对话历史轮数: {len(conversation_history) // 2 if conversation_history else 0}")
        
        response = client.invoke(
            messages=messages,
            model="doubao-seed-1-6-251015",  # 使用豆包模型
            temperature=0.7,
            thinking="disabled",
            caching="disabled",
            max_completion_tokens=2000
        )
        
        # 安全处理响应内容
        answer = _get_text_content(response.content)
        
        logger.info(f"✅ LLM调用成功 - 回复长度: {len(answer)} 字符")
        
        return {
            "success": True,
            "data": {
                "answer": answer,
                "conversation_id": f"llm_conv_{hash(query)}"
            }
        }
        
    except Exception as e:
        logger.error(f"❌ LLM调用失败: {str(e)}", exc_info=True)
        return {
            "success": False,
            "message": f"LLM调用失败: {str(e)}"
        }


def _get_text_content(content: Union[str, List[str], List[Dict[str, Any]]]) -> str:
    """
    安全地从LLM响应中提取文本内容
    
    Args:
        content: LLM响应内容（可能是str、list[str]或list[dict]）
        
    Returns:
        提取的文本内容
    """
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        if content and isinstance(content[0], str):
            # List of strings
            return " ".join(content)
        else:
            # List of dicts (multimodal response)
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            return " ".join(text_parts)
    else:
        return str(content)


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
    加载对话历史（从Redis缓存）
    
    Args:
        session_id: 会话ID
        max_history: 最大历史记录数
        
    Returns:
        对话历史列表
    """
    try:
        # 从Redis缓存中加载对话历史
        cache_key = f"conversation:{session_id}"
        history = cache_manager.get(cache_key)
        
        if not history:
            return []
        
        # 返回最近的历史记录
        return history[-max_history:] if len(history) > max_history else history
        
    except Exception as e:
        logger.error(f"❌ 加载对话历史失败: {str(e)}")
        return []


def _save_conversation_history(session_id: str, query: str, answer: str):
    """
    保存对话历史（到Redis缓存）
    
    Args:
        session_id: 会话ID
        query: 用户问题
        answer: 宁律师回复
    """
    try:
        # 从Redis缓存中加载现有历史
        cache_key = f"conversation:{session_id}"
        history_json = cache_manager.get(cache_key)
        
        if history_json:
            history = json.loads(history_json)
        else:
            history = []
        
        # 添加新的对话
        history.append({
            "role": "user",
            "content": query
        })
        history.append({
            "role": "assistant",
            "content": answer
        })
        
        # 限制历史记录数量（最多保留20轮对话）
        max_conversations = 40  # 20轮对话（每轮包含用户和助手各一条）
        if len(history) > max_conversations:
            history = history[-max_conversations:]
        
        # 保存到Redis缓存（24小时过期）
        cache_manager.set(
            cache_key,
            json.dumps(history, ensure_ascii=False),
            ttl=CONVERSATION_TTL
        )
        
        logger.info(f"💾 保存对话历史到Redis - 会话ID: {session_id}, 对话轮数: {len(history) // 2}")
        
    except Exception as e:
        logger.error(f"❌ 保存对话历史失败: {str(e)}")


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

