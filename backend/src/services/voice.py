"""
语音服务
提供语音识别（ASR）和语音合成（TTS）功能
"""

import os
import base64
import requests
import logging
import uuid
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session

from coze_coding_dev_sdk import TTSClient, ASRClient
from coze_coding_utils.runtime_ctx.context import new_context

logger = logging.getLogger(__name__)


class VoiceService:
    """语音服务"""
    
    def __init__(self, db: Session):
        """初始化"""
        self.db = db
        
        # 初始化TTS客户端
        self.tts_client = TTSClient(ctx=new_context(method="tts.synthesize"))
        
        # 初始化ASR客户端
        self.asr_client = ASRClient(ctx=new_context(method="asr.recognize"))
    
    # ============================================
    # 语音识别（ASR）
    # ============================================
    
    def recognize_audio(
        self,
        user_id: int,
        audio_url: Optional[str] = None,
        audio_base64: Optional[str] = None,
        audio_file_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        语音识别（语音转文字）
        
        Args:
            user_id: 用户ID
            audio_url: 音频文件URL
            audio_base64: 音频文件Base64编码
            audio_file_path: 音频文件路径（如果提供，会转换为Base64）
        
        Returns:
            识别结果
        """
        try:
            uid = f"user_{user_id}"
            
            # 如果提供了文件路径，读取并转换为Base64
            if audio_file_path:
                audio_base64 = self._audio_to_base64(audio_file_path)
            
            # 调用ASR识别
            if audio_url:
                # 使用URL识别
                text, data = self.asr_client.recognize(
                    uid=uid,
                    url=audio_url
                )
            elif audio_base64:
                # 使用Base64识别
                text, data = self.asr_client.recognize(
                    uid=uid,
                    base64_data=audio_base64
                )
            else:
                return {
                    "success": False,
                    "message": "必须提供audio_url或audio_base64"
                }
            
            logger.info(f"语音识别成功: user_id={user_id}, text={text[:50]}...")
            
            return {
                "success": True,
                "data": {
                    "text": text,
                    "duration": data.get("result", {}).get("duration"),
                    "utterances": data.get("result", {}).get("utterances", [])
                }
            }
            
        except Exception as e:
            logger.error(f"语音识别失败: {str(e)}")
            return {
                "success": False,
                "message": f"识别失败: {str(e)}"
            }
    
    def _audio_to_base64(self, file_path: str) -> str:
        """
        将音频文件转换为Base64
        
        Args:
            file_path: 文件路径
        
        Returns:
            Base64编码字符串
        """
        with open(file_path, 'rb') as f:
            audio_data = f.read()
            return base64.b64encode(audio_data).decode('utf-8')
    
    # ============================================
    # 语音合成（TTS）
    # ============================================
    
    def synthesize_speech(
        self,
        user_id: int,
        text: str,
        speaker: Optional[str] = None,
        audio_format: str = "mp3",
        sample_rate: int = 24000,
        speech_rate: int = 0,
        loudness_rate: int = 0
    ) -> Dict[str, Any]:
        """
        语音合成（文字转语音）
        
        Args:
            user_id: 用户ID
            text: 要合成的文字
            speaker: 语音ID（默认：zh_female_xiaohe_uranus_bigtts）
            audio_format: 音频格式（mp3/pcm/ogg_opus）
            sample_rate: 采样率（8000-48000）
            speech_rate: 语速调整（-50到100）
            loudness_rate: 音量调整（-50到100）
        
        Returns:
            合成结果（包含音频URL）
        """
        try:
            uid = f"user_{user_id}"
            
            # 默认使用女声（适合法律咨询）
            if not speaker:
                speaker = "zh_female_xiaohe_uranus_bigtts"
            
            # 调用TTS合成
            audio_url, audio_size = self.tts_client.synthesize(
                uid=uid,
                text=text,
                speaker=speaker,
                audio_format=audio_format,
                sample_rate=sample_rate,
                speech_rate=speech_rate,
                loudness_rate=loudness_rate
            )
            
            logger.info(f"语音合成成功: user_id={user_id}, size={audio_size}")
            
            return {
                "success": True,
                "data": {
                    "audio_url": audio_url,
                    "audio_size": audio_size,
                    "audio_format": audio_format
                }
            }
            
        except Exception as e:
            logger.error(f"语音合成失败: {str(e)}")
            return {
                "success": False,
                "message": f"合成失败: {str(e)}"
            }
    
    def synthesize_and_download(
        self,
        user_id: int,
        text: str,
        output_dir: Optional[str] = None,
        speaker: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        语音合成并下载到本地
        
        Args:
            user_id: 用户ID
            text: 要合成的文字
            output_dir: 输出目录（默认：/tmp）
            speaker: 语音ID
        
        Returns:
            合成结果（包含文件路径）
        """
        try:
            # 先合成
            result = self.synthesize_speech(
                user_id=user_id,
                text=text,
                speaker=speaker
            )
            
            if not result.get('success'):
                return result
            
            # 下载音频
            audio_url = result['data']['audio_url']
            response = requests.get(audio_url, timeout=30)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"下载音频失败: {response.status_code}"
                }
            
            # 保存文件
            if not output_dir:
                output_dir = "/tmp"
            
            # 确保目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 生成文件名
            filename = f"voice_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
            file_path = os.path.join(output_dir, filename)
            
            # 保存文件
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"语音合成并下载成功: user_id={user_id}, file={file_path}")
            
            return {
                "success": True,
                "data": {
                    "file_path": file_path,
                    "filename": filename,
                    "audio_url": audio_url,
                    "audio_size": os.path.getsize(file_path)
                }
            }
            
        except Exception as e:
            logger.error(f"语音合成并下载失败: {str(e)}")
            return {
                "success": False,
                "message": f"失败: {str(e)}"
            }
    
    # ============================================
    # 可用的语音列表
    # ============================================
    
    @staticmethod
    def get_available_speakers() -> Dict[str, Dict[str, str]]:
        """
        获取可用的语音列表
        
        Returns:
            语音列表
        """
        return {
            "通用语音": {
                "zh_female_xiaohe_uranus_bigtts": {
                    "name": "小禾（女声）",
                    "description": "通用女声，适合日常对话",
                    "gender": "female",
                    "recommended": True
                },
                "zh_female_vv_uranus_bigtts": {
                    "name": "Vivi（女声）",
                    "description": "中英文女声，专业感强",
                    "gender": "female",
                    "recommended": True
                },
                "zh_male_m191_uranus_bigtts": {
                    "name": "韵舟（男声）",
                    "description": "通用男声，专业稳重",
                    "gender": "male",
                    "recommended": False
                },
                "zh_male_taocheng_uranus_bigtts": {
                    "name": "晓天（男声）",
                    "description": "年轻男声，亲切自然",
                    "gender": "male",
                    "recommended": False
                }
            },
            "有声读物": {
                "zh_female_xueayi_saturn_bigtts": {
                    "name": "雪阿姨",
                    "description": "儿童读物女声，亲切温暖",
                    "gender": "female",
                    "recommended": False
                }
            },
            "视频配音": {
                "zh_male_dayi_saturn_bigtts": {
                    "name": "大义（男声）",
                    "description": "视频配音男声，专业有力",
                    "gender": "male",
                    "recommended": False
                },
                "zh_female_mizai_saturn_bigtts": {
                    "name": "米在（女声）",
                    "description": "温柔女声，适合情感类内容",
                    "gender": "female",
                    "recommended": False
                },
                "zh_female_jitangnv_saturn_bigtts": {
                    "name": "鸡汤女声",
                    "description": "励志女声，充满正能量",
                    "gender": "female",
                    "recommended": False
                },
                "zh_female_meilinvyou_saturn_bigtts": {
                    "name": "美腻女友",
                    "description": "女友音，甜蜜温柔",
                    "gender": "female",
                    "recommended": False
                }
            },
            "角色扮演": {
                "saturn_zh_female_keainvsheng_tob": {
                    "name": "可爱女生",
                    "description": "甜美可爱，活泼开朗",
                    "gender": "female",
                    "recommended": False
                },
                "saturn_zh_male_shuanglangshaonian_tob": {
                    "name": "爽朗少年",
                    "description": "阳光开朗，充满活力",
                    "gender": "male",
                    "recommended": False
                },
                "saturn_zh_male_tiancaitongzhuo_tob": {
                    "name": "天才同桌",
                    "description": "聪明伶俐，学霸气质",
                    "gender": "male",
                    "recommended": False
                }
            }
        }
    
    @staticmethod
    def get_default_speaker() -> str:
        """
        获取默认语音ID
        
        Returns:
            语音ID
        """
        return "zh_female_xiaohe_uranus_bigtts"
