"""
宁律师语音功能本地测试脚本
使用方法：
1. 语音合成测试：运行脚本，会自动生成语音文件到 assets 目录
2. 语音识别测试：准备本地音频文件，按照提示上传测试
"""

import os
import requests
from coze_coding_dev_sdk import TTSClient, ASRClient
from coze_coding_dev_sdk.s3 import S3SyncStorage
from coze_coding_utils.runtime_ctx.context import new_context


def test_text_to_speech_local():
    """测试语音合成：将文字转换为语音并保存到本地"""
    print("=" * 60)
    print("【语音合成测试】")
    print("=" * 60)
    
    # 测试文字内容（宁律师的建议）
    text = """先收集好能证明你在这家公司上班的证据，比如劳动合同、工牌、考勤记录、工资条或者和领导的聊天记录，然后去公司所在地的劳动监察大队投诉，他们会帮你去跟公司协调要工资。要是协调不成，就拿着这些证据去劳动仲裁委员会申请仲裁，这个过程是免费的。另外，公司拖欠工资超过三个月，你还可以主动跟公司解除劳动合同，要求公司支付拖欠的工资和经济补偿金。对了，你有没有跟公司签劳动合同，之前的工资是通过什么方式发的？"""
    
    print(f"\n要合成的文字：\n{text}\n")
    
    try:
        # 步骤 1: 使用 TTS 合成语音
        ctx = new_context(method="tts.synthesize")
        tts_client = TTSClient(ctx=ctx)
        
        print("正在合成语音...")
        audio_url, audio_size = tts_client.synthesize(
            uid="test_user",
            text=text,
            speaker="zh_male_m191_uranus_bigtts",  # 男性声音，适合律师
            audio_format="mp3",
            sample_rate=24000,
            speech_rate=0,  # 正常语速
            loudness_rate=0  # 正常音量
        )
        
        print(f"✓ 语音合成成功")
        print(f"  音频 URL: {audio_url}")
        print(f"  文件大小: {audio_size} 字节")
        
        # 步骤 2: 下载音频到本地 assets 目录
        print("\n正在下载语音文件...")
        response = requests.get(audio_url)
        audio_content = response.content
        
        # 确保目录存在
        output_dir = "assets"
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存到本地
        output_file = os.path.join(output_dir, "ning_lawyer_reply.mp3")
        with open(output_file, 'wb') as f:
            f.write(audio_content)
        
        print(f"✓ 语音文件已保存到: {output_file}")
        print(f"✓ 文件大小: {len(audio_content)} 字节")
        
        # 步骤 3: 上传到对象存储（可选）
        print("\n正在上传到对象存储...")
        storage = S3SyncStorage(
            endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
            access_key="",
            secret_key="",
            bucket_name=os.getenv("COZE_BUCKET_NAME"),
            region="cn-beijing",
        )
        
        file_key = f"legal_agent_audio/test_reply.mp3"
        storage.upload_file(
            file_content=audio_content,
            file_name=file_key,
            content_type="audio/mpeg"
        )
        
        print(f"✓ 已上传到对象存储: {file_key}")
        
        # 生成签名 URL
        signed_url = storage.generate_presigned_url(
            key=file_key,
            expire_time=3600
        )
        
        print(f"✓ 签名 URL（有效期1小时）: {signed_url}")
        
        print("\n" + "=" * 60)
        print("✅ 语音合成测试完成！")
        print("=" * 60)
        print(f"\n你可以用以下方式播放语音：")
        print(f"1. 直接打开本地文件: {output_file}")
        print(f"2. 访问在线链接: {signed_url}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 语音合成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_speech_recognition_example():
    """语音识别测试示例（需要用户提供音频文件）"""
    print("\n" + "=" * 60)
    print("【语音识别测试示例】")
    print("=" * 60)
    
    print("\n要测试语音识别功能，请按照以下步骤：")
    print("\n1. 准备一个音频文件（支持 MP3/WAV/OGG OPUS 格式）")
    print("2. 将音频文件上传到可访问的 URL（或者使用对象存储）")
    print("3. 调用 recognize_speech 函数进行识别")
    
    print("\n示例代码：")
    print("""
from coze_coding_dev_sdk import ASRClient
from coze_coding_utils.runtime_ctx.context import new_context

ctx = new_context(method="asr.recognize")
client = ASRClient(ctx=ctx)

# 方式一：使用 URL
text, data = client.recognize(
    uid="test_user",
    url="https://your-audio-url.com/audio.mp3"
)

# 方式二：使用 Base64
import base64
with open("audio.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode("utf-8")

text, data = client.recognize(
    uid="test_user",
    base64_data=audio_base64
)

print(f"识别结果: {text}")
    """)
    
    print("\n如果你有音频文件的 URL，我可以帮你测试识别功能！")


def main():
    """主函数"""
    print("\n" + "🎤 " * 20)
    print("宁律师语音功能本地测试工具")
    print("🎤 " * 20)
    
    # 测试语音合成
    success = test_text_to_speech_local()
    
    if success:
        print("\n✅ 语音合成功能正常！")
        print("\n现在你可以：")
        print("1. 打开 assets/ning_lawyer_reply.mp3 文件播放语音")
        print("2. 如果你有音频文件 URL，我可以帮你测试语音识别")
    else:
        print("\n❌ 语音合成测试失败，请检查配置和网络连接")
    
    # 显示语音识别示例
    test_speech_recognition_example()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
