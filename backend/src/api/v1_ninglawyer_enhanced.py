"""
宁律师 V1 增强版 API
提供完整的宁律师咨询功能，包括：
- 聊天接口（文本输入）
- 语音识别接口（ASR）
- 语音合成接口（TTS）
- 历史记录查询
- 流式输出支持
"""

import os
import json
import base64
from flask import Blueprint, request, jsonify, Response
from loguru import logger
from typing import Dict, Any, Optional, Union, List

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from coze_coding_dev_sdk import LLMClient, TTSClient, ASRClient
from coze_coding_utils.runtime_ctx.context import new_context

from services.coze_agent_service import CozeAgentService
from services.user_service import UserService
from services.session_service import SessionService
from personas.personality_selector import PersonalitySelector
from prompts.ning_lawyer import NingLawyerPrompt
from utils.response import success_response, error_response
from utils.cache_manager import CacheManager

# 创建蓝图
v1_ninglawyer_enhanced_bp = Blueprint('v1_ninglawyer_enhanced', __name__)

# 初始化服务
coze_service = CozeAgentService(access_token=os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY", ""))
user_service = UserService()
session_service = SessionService()
personality_selector = PersonalitySelector()
ninglawyer_prompt = NingLawyerPrompt()
cache_manager = CacheManager()

# 宁律师Bot ID
NINGLAWYER_BOT_ID = os.getenv("NINGLAWYER_BOT_ID", "7478766030654679080")

# 对话历史存储（24小时过期）
CONVERSATION_TTL = 86400

# 语音配置
DEFAULT_SPEAKER = "zh_female_xiaohe_uranus_bigtts"  # 默认女声
AUDIO_FORMAT = "mp3"
SAMPLE_RATE = 24000


# ============================================
# 聊天接口（流式输出）
# ============================================

@v1_ninglawyer_enhanced_bp.route('/chat/stream', methods=['POST'])
def chat_stream():
    """
    宁律师流式聊天接口
    
    请求体：
    {
        "query": "用户输入的问题",
        "user_id": "用户ID",
        "session_id": "会话ID（可选）",
        "user_type": "用户类型（individual | corporate）"
    }
    
    响应：流式JSON数据
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
        
        logger.info(f"🤖 宁律师流式聊天 - 用户ID: {user_id}, 问题: {query[:50]}...")
        
        # 2. 获取或创建会话
        if not session_id:
            session_id = f"temp_{user_id}_{hash(query) % 10000}"
        
        # 3. 加载历史对话
        conversation_history = _load_conversation_history(session_id)
        
        # 4. 动态选择人设
        scenario = _identify_scenario(query)
        user_type_mapped = "personal" if user_type == "individual" else user_type
        personality_id = personality_selector.select(
            user_type=user_type_mapped,
            scenario=scenario,
            app_id="ninglawyer"
        )
        personality = personality_selector.get_personality(personality_id)
        
        # 5. 构建系统提示词
        system_prompt = ninglawyer_prompt.build_prompt(personality=personality['name'])
        
        # 6. 流式调用LLM
        ctx = new_context(method="ninglawyer_chat_stream")
        client = LLMClient(ctx=ctx)
        
        messages = [SystemMessage(content=system_prompt)]
        
        # 添加历史对话
        if conversation_history and len(conversation_history) > 0:
            for msg in conversation_history:
                if msg.get('role') == 'user':
                    messages.append(HumanMessage(content=msg.get('content', '')))
                elif msg.get('role') == 'assistant':
                    messages.append(AIMessage(content=msg.get('content', '')))
        
        messages.append(HumanMessage(content=query))
        
        def generate():
            """生成流式响应"""
            full_response = ""
            
            try:
                for chunk in client.stream(
                    messages=messages,
                    model="doubao-seed-1-6-251015",
                    temperature=0.7,
                    thinking="disabled"
                ):
                    if chunk.content:
                        content = _get_text_content(chunk.content)
                        full_response += content
                        
                        # 发送流式数据
                        yield json.dumps({
                            "type": "chunk",
                            "content": content
                        }, ensure_ascii=False) + "\n"
                
                # 保存对话历史
                _save_conversation_history(session_id, query, full_response)
                
                # 识别意图和案源
                intent_result = _identify_intent(query)
                lead_info = _identify_lead(query, intent_result, user_id, session_id)
                
                # 发送结束标记
                yield json.dumps({
                    "type": "end",
                    "data": {
                        "session_id": session_id,
                        "intent": intent_result['intent'],
                        "intent_desc": intent_result['description'],
                        "is_lead": lead_info['is_lead'],
                        "lead_type": lead_info.get('lead_type'),
                        "personality": {
                            "id": personality_id,
                            "name": personality.get('name', '')
                        }
                    }
                }, ensure_ascii=False) + "\n"
                
            except Exception as e:
                logger.error(f"❌ 流式生成失败: {str(e)}")
                yield json.dumps({
                    "type": "error",
                    "message": str(e)
                }, ensure_ascii=False) + "\n"
        
        return Response(generate(), mimetype='application/json')
        
    except Exception as e:
        logger.error(f"❌ 流式聊天异常: {str(e)}", exc_info=True)
        return error_response(f"聊天失败: {str(e)}", 500)


# ============================================
# 语音识别接口（ASR）
# ============================================

@v1_ninglawyer_enhanced_bp.route('/voice/recognize', methods=['POST'])
def voice_recognize():
    """
    语音识别接口（将语音转换为文本）
    
    请求体：
    {
        "audio_url": "音频URL（可选）",
        "audio_base64": "音频Base64数据（可选）",
        "user_id": "用户ID"
    }
    
    响应：
    {
        "success": true,
        "data": {
            "text": "识别的文本",
            "duration": 音频时长（毫秒）
        }
    }
    """
    try:
        data = request.get_json()
        
        # 1. 参数校验
        if not data:
            return error_response("缺少请求体", 400)
        
        audio_url = data.get('audio_url')
        audio_base64 = data.get('audio_base64')
        user_id = data.get('user_id', 'anonymous')
        
        if not audio_url and not audio_base64:
            return error_response("必须提供audio_url或audio_base64", 400)
        
        logger.info(f"🎤 语音识别 - 用户ID: {user_id}")
        
        # 2. 调用ASR
        ctx = new_context(method="asr.recognize")
        client = ASRClient(ctx=ctx)
        
        if audio_base64:
            # 使用Base64数据
            text, response_data = client.recognize(
                uid=user_id,
                base64_data=audio_base64
            )
        else:
            # 使用URL
            text, response_data = client.recognize(
                uid=user_id,
                url=audio_url
            )
        
        # 3. 获取音频时长
        duration = response_data.get("result", {}).get("duration", 0)
        
        logger.info(f"✅ 语音识别成功 - 文本: {text[:50]}..., 时长: {duration}ms")
        
        return success_response({
            "text": text,
            "duration": duration
        })
        
    except Exception as e:
        logger.error(f"❌ 语音识别失败: {str(e)}", exc_info=True)
        return error_response(f"语音识别失败: {str(e)}", 500)


# ============================================
# 语音合成接口（TTS）
# ============================================

@v1_ninglawyer_enhanced_bp.route('/voice/synthesize', methods=['POST'])
def voice_synthesize():
    """
    语音合成接口（将文本转换为语音）
    
    请求体：
    {
        "text": "要合成的文本",
        "user_id": "用户ID",
        "speaker": "音色ID（可选，默认女声）"
    }
    
    响应：
    {
        "success": true,
        "data": {
            "audio_url": "音频URL",
            "audio_size": 音频大小（字节）
        }
    }
    """
    try:
        data = request.get_json()
        
        # 1. 参数校验
        if not data or 'text' not in data:
            return error_response("缺少text参数", 400)
        
        text = data.get('text', '').strip()
        if not text:
            return error_response("text参数不能为空", 400)
        
        user_id = data.get('user_id', 'anonymous')
        speaker = data.get('speaker', DEFAULT_SPEAKER)
        
        logger.info(f"🔊 语音合成 - 用户ID: {user_id}, 文本: {text[:50]}...")
        
        # 2. 调用TTS
        ctx = new_context(method="tts.synthesize")
        client = TTSClient(ctx=ctx)
        
        audio_url, audio_size = client.synthesize(
            uid=user_id,
            text=text,
            speaker=speaker,
            audio_format=AUDIO_FORMAT,
            sample_rate=SAMPLE_RATE
        )
        
        logger.info(f"✅ 语音合成成功 - 音频URL: {audio_url}, 大小: {audio_size}字节")
        
        return success_response({
            "audio_url": audio_url,
            "audio_size": audio_size,
            "speaker": speaker
        })
        
    except Exception as e:
        logger.error(f"❌ 语音合成失败: {str(e)}", exc_info=True)
        return error_response(f"语音合成失败: {str(e)}", 500)


# ============================================
# 历史记录查询接口
# ============================================

@v1_ninglawyer_enhanced_bp.route('/history', methods=['GET'])
def get_history():
    """
    查询对话历史
    
    参数：
    - session_id: 会话ID（必需）
    
    响应：
    {
        "success": true,
        "data": {
            "history": [...]
        }
    }
    """
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return error_response("缺少session_id参数", 400)
        
        logger.info(f"📜 查询历史记录 - 会话ID: {session_id}")
        
        # 加载历史记录
        history = _load_conversation_history(session_id)
        
        return success_response({
            "session_id": session_id,
            "history": history,
            "count": len(history)
        })
        
    except Exception as e:
        logger.error(f"❌ 查询历史记录失败: {str(e)}")
        return error_response(f"查询失败: {str(e)}", 500)


# ============================================
# 会话管理接口
# ============================================

@v1_ninglawyer_enhanced_bp.route('/session', methods=['DELETE'])
def clear_session():
    """
    清除会话历史
    
    请求体：
    {
        "session_id": "会话ID"
    }
    
    响应：
    {
        "success": true
    }
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return error_response("缺少session_id参数", 400)
        
        logger.info(f"🗑️ 清除会话 - 会话ID: {session_id}")
        
        # 删除Redis缓存
        cache_key = f"conversation:{session_id}"
        cache_manager.delete(cache_key)
        
        return success_response({"message": "会话已清除"})
        
    except Exception as e:
        logger.error(f"❌ 清除会话失败: {str(e)}")
        return error_response(f"清除失败: {str(e)}", 500)


# ============================================
# 辅助函数
# ============================================

def _load_conversation_history(session_id: str, max_history: int = 20) -> list:
    """加载对话历史"""
    try:
        cache_key = f"conversation:{session_id}"
        history = cache_manager.get(cache_key)
        
        if not history:
            return []
        
        return history[-max_history:] if len(history) > max_history else history
        
    except Exception as e:
        logger.error(f"❌ 加载对话历史失败: {str(e)}")
        return []


def _save_conversation_history(session_id: str, query: str, answer: str):
    """保存对话历史"""
    try:
        cache_key = f"conversation:{session_id}"
        history_json = cache_manager.get(cache_key)
        
        if history_json:
            history = history_json
        else:
            history = []
        
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": answer})
        
        # 限制历史记录数量
        max_conversations = 40
        if len(history) > max_conversations:
            history = history[-max_conversations:]
        
        # 保存到Redis
        cache_manager.set(
            cache_key,
            history,
            ttl=CONVERSATION_TTL
        )
        
    except Exception as e:
        logger.error(f"❌ 保存对话历史失败: {str(e)}")


def _identify_scenario(query: str) -> str:
    """识别用户场景"""
    query_lower = query.lower()
    
    scenario_rules = [
        {'scenario': 'family_law', 'keywords': ['离婚', '抚养', '财产分割', '家暴', '婚姻', '夫妻', '孩子']},
        {'scenario': 'commercial', 'keywords': ['合同', '违约', '纠纷', '赔偿', '欠款', '债务', '企业']},
        {'scenario': 'general', 'keywords': ['咨询', '法律', '问']}
    ]
    
    for rule in scenario_rules:
        for keyword in rule['keywords']:
            if keyword in query_lower:
                return rule['scenario']
    
    return 'general'


def _identify_intent(query: str) -> dict:
    """识别用户意图"""
    query_lower = query.lower()
    
    intent_rules = [
        {'intent': 'contract_signing', 'description': '合同签署', 'keywords': ['签合同', '签署', '签约', '在线签署', '电子签名']},
        {'intent': 'contract_management', 'description': '合同管理', 'keywords': ['合同管理', '履行', '违约', '催款', '理约']},
        {'intent': 'judgment_query', 'description': '裁判观点查询', 'keywords': ['怎么判', '裁判', '判决', '判例', '胜诉率', '类案']},
        {'intent': 'lawyer_matching', 'description': '找律师', 'keywords': ['找律师', '法律教官', '委托律师', '律师服务']},
        {'intent': 'compliance_risk', 'description': '合规风险', 'keywords': ['合规', '风险防控', '防风险', '企业合规']},
        {'intent': 'general_consultation', 'description': '普通法律咨询', 'keywords': ['咨询', '法律问题', '问律师']}
    ]
    
    for rule in intent_rules:
        for keyword in rule['keywords']:
            if keyword in query_lower:
                return {'intent': rule['intent'], 'description': rule['description']}
    
    return {'intent': 'general_consultation', 'description': '普通法律咨询'}


def _identify_lead(query: str, intent_result: dict, user_id: str, session_id: str) -> dict:
    """案源识别"""
    query_lower = query.lower()
    
    lead_rules = [
        {'lead_type': 'divorce', 'description': '离婚咨询', 'keywords': ['离婚', '财产分割', '抚养权', '家暴'], 'priority': 'high'},
        {'lead_type': 'debt', 'description': '债务纠纷', 'keywords': ['债务', '欠款', '借钱', '还钱', '追债'], 'priority': 'medium'},
        {'lead_type': 'contract_dispute', 'description': '合同纠纷', 'keywords': ['合同', '违约', '纠纷', '赔偿'], 'priority': 'medium'},
        {'lead_type': 'injury', 'description': '人身损害', 'keywords': ['受伤', '赔偿', '医疗', '事故'], 'priority': 'high'},
        {'lead_type': 'company', 'description': '企业法务', 'keywords': ['公司', '企业', '合规', '劳动'], 'priority': 'medium'}
    ]
    
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


def _get_text_content(content: Union[str, List[str], List[Dict[str, Any]]]) -> str:
    """安全地从LLM响应中提取文本内容"""
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
