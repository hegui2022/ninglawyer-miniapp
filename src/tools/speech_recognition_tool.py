import base64
import os
from langchain.tools import tool
from langchain.tools import ToolRuntime
from coze_coding_dev_sdk import ASRClient
from coze_coding_utils.runtime_ctx.context import new_context


@tool
def recognize_speech(audio_url: str, runtime: ToolRuntime) -> str:
    """
    语音识别工具：将语音文件转换为文字
    
    Args:
        audio_url: 语音文件的 URL 地址（支持 http/https）
    
    Returns:
        识别出的文字内容
    """
    try:
        ctx = new_context(method="asr.recognize")
        client = ASRClient(ctx=ctx)
        
        text, data = client.recognize(
            uid="legal_agent_user",
            url=audio_url
        )
        
        return f"语音识别结果：{text}"
        
    except Exception as e:
        return f"语音识别失败：{str(e)}"


@tool
def recognize_speech_from_base64(audio_base64: str, runtime: ToolRuntime) -> str:
    """
    语音识别工具（Base64 版本）：将 Base64 编码的语音数据转换为文字
    
    Args:
        audio_base64: Base64 编码的语音数据
    
    Returns:
        识别出的文字内容
    """
    try:
        ctx = new_context(method="asr.recognize")
        client = ASRClient(ctx=ctx)
        
        text, data = client.recognize(
            uid="legal_agent_user",
            base64_data=audio_base64
        )
        
        return f"语音识别结果：{text}"
        
    except Exception as e:
        return f"语音识别失败：{str(e)}"
