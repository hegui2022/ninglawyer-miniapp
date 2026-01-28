import os
import uuid
import requests
from langchain.tools import tool
from langchain.tools import ToolRuntime
from coze_coding_dev_sdk import TTSClient
from coze_coding_dev_sdk.s3 import S3SyncStorage
from coze_coding_utils.runtime_ctx.context import new_context


@tool
def text_to_speech(text: str, runtime: ToolRuntime) -> str:
    """
    语音合成工具：将文字转换为语音并上传到对象存储
    
    Args:
        text: 要合成的文字内容
    
    Returns:
        语音文件的访问 URL
    """
    try:
        # 步骤 1: 使用 TTS 合成语音
        ctx = new_context(method="tts.synthesize")
        tts_client = TTSClient(ctx=ctx)
        
        # 使用男性声音（天才同桌），适合律师人设
        audio_url, audio_size = tts_client.synthesize(
            uid="legal_agent_user",
            text=text,
            speaker="saturn_zh_male_tiancaitongzhuo_tob",  # 天才同桌：聪明理性的男声
            audio_format="mp3",
            sample_rate=24000,
            speech_rate=0,  # 正常语速
            loudness_rate=0  # 正常音量
        )
        
        # 步骤 2: 下载音频到临时目录
        response = requests.get(audio_url)
        audio_content = response.content
        
        # 生成临时文件名
        temp_filename = f"lawyer_reply_{uuid.uuid4().hex[:8]}.mp3"
        temp_filepath = os.path.join("/tmp", temp_filename)
        
        with open(temp_filepath, 'wb') as f:
            f.write(audio_content)
        
        # 步骤 3: 上传到对象存储
        storage = S3SyncStorage(
            endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
            access_key="",
            secret_key="",
            bucket_name=os.getenv("COZE_BUCKET_NAME"),
            region="cn-beijing",
        )
        
        # 生成对象存储的文件名（使用规范格式：filename_a_b.ext）
        file_key = f"legal_agent_audio/{temp_filename}"
        
        storage.upload_file(
            file_content=audio_content,
            file_name=file_key,
            content_type="audio/mpeg"
        )
        
        # 步骤 4: 生成签名 URL 并返回
        signed_url = storage.generate_presigned_url(
            key=file_key,
            expire_time=3600  # 1小时有效期
        )
        
        return f"语音已生成，访问地址：{signed_url}"
        
    except Exception as e:
        return f"语音合成失败：{str(e)}"
