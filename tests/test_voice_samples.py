"""
语音音色样音生成工具
生成不同音色的样音，让用户选择最接近自己声音的
"""

import os
import requests
from coze_coding_dev_sdk import TTSClient
from coze_coding_utils.runtime_ctx.context import new_context


# 豆包语音可用音色列表（适合律师人设的）
VOICE_SAMPLES = {
    # 男性音色
    "zh_male_m191_uranus_bigtts": {
        "name": "云州",
        "description": "成熟稳重的男声（当前使用）",
        "category": "通用"
    },
    "zh_male_taocheng_uranus_bigtts": {
        "name": "小天",
        "description": "年轻活力的男声",
        "category": "通用"
    },
    "zh_male_dayi_saturn_bigtts": {
        "name": "大一",
        "description": "深沉有力的男声，适合视频配音",
        "category": "视频配音"
    },
    "saturn_zh_male_shuanglangshaonian_tob": {
        "name": "爽朗少年",
        "description": "开朗爽快的年轻男声",
        "category": "角色扮演"
    },
    "saturn_zh_male_tiancaitongzhuo_tob": {
        "name": "天才同桌",
        "description": "聪明理性的男声",
        "category": "角色扮演"
    },
    "saturn_zh_male_ruyayichen_saturn_bigtts": {
        "name": "优雅男士",
        "description": "温文尔雅的成熟男声",
        "category": "角色扮演"
    },

    # 女性音色（如果需要）
    "zh_female_xiaohe_uranus_bigtts": {
        "name": "小河",
        "description": "温柔自然的女声（默认）",
        "category": "通用"
    },
    "zh_female_vv_uranus_bigtts": {
        "name": "Vivi",
        "description": "中英双语女声",
        "category": "通用"
    },
}


# 测试文字（宁律师的自我介绍）
SAMPLE_TEXT = "你好，我是宁律师，有20年执业经验，主攻民商法、劳动法、婚姻家庭法、合同纠纷。有什么法律问题尽管问，我会用大白话给你讲清楚。"


def generate_voice_sample(voice_id: str, voice_info: dict, output_dir: str = "assets/voice_samples"):
    """生成单个音色的样音"""
    try:
        ctx = new_context(method="tts.synthesize")
        client = TTSClient(ctx=ctx)
        
        print(f"正在生成 {voice_info['name']} 的样音...")
        
        audio_url, _ = client.synthesize(
            uid="voice_sample",
            text=SAMPLE_TEXT,
            speaker=voice_id,
            audio_format="mp3",
            sample_rate=24000,
            speech_rate=0,
            loudness_rate=0
        )
        
        # 下载音频
        response = requests.get(audio_url)
        audio_content = response.content
        
        # 保存文件
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{voice_info['name']}_{voice_id}.mp3"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(audio_content)
        
        print(f"  ✓ 已保存: {filepath} ({len(audio_content)} 字节)")
        return filepath
        
    except Exception as e:
        print(f"  ✗ 生成失败: {str(e)}")
        return None


def generate_all_samples():
    """生成所有音色的样音"""
    print("=" * 70)
    print("🎙️  生成所有音色样音")
    print("=" * 70)
    
    output_dir = "assets/voice_samples"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n样音文字内容：\n{SAMPLE_TEXT}\n")
    print(f"输出目录：{output_dir}\n")
    
    results = []
    
    # 男性音色
    print("\n【男性音色】")
    print("-" * 70)
    for voice_id, voice_info in VOICE_SAMPLES.items():
        if voice_info['category'] in ['通用', '视频配音', '角色扮演']:
            result = generate_voice_sample(voice_id, voice_info, output_dir)
            if result:
                results.append({
                    'voice_id': voice_id,
                    'name': voice_info['name'],
                    'description': voice_info['description'],
                    'file': result
                })
    
    print("\n" + "=" * 70)
    print("✅ 样音生成完成！")
    print("=" * 70)
    
    print(f"\n共生成 {len(results)} 个样音文件")
    print("\n你可以：")
    print("1. 打开 assets/voice_samples/ 目录，逐个试听")
    print("2. 选择最接近你声音的音色")
    print("3. 告诉我音色名称或 voice_id，我来更新配置")
    
    print("\n📋 音色列表：")
    print("-" * 70)
    for item in results:
        print(f"• {item['name']}: {item['description']}")
    
    print("\n💡 提示：")
    print("- 律师人设推荐：云州（成熟稳重）、大一（深沉有力）、优雅男士")
    print("- 年轻律师推荐：小天（年轻活力）、天才同桌（聪明理性）")
    
    return results


def main():
    """主函数"""
    print("\n" + "🎤 " * 15)
    print("音色样音生成工具")
    print("🎤 " * 15 + "\n")
    
    results = generate_all_samples()
    
    print("\n需要更换音色吗？")
    print("告诉我你想用的音色名称（如：云州、小天、大一），我来帮你更新配置！")


if __name__ == "__main__":
    main()
