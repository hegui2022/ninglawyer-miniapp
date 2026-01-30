# 宁律师民事智能体语音咨询功能文档

**文档版本**: v1.0
**创建时间**: 2025-01-31
**功能状态**: ✅ 已完成

---

## 📋 功能概述

宁律师民事智能体语音咨询功能允许用户通过语音进行法律咨询，系统会自动完成以下流程：

1. **语音识别（ASR）**：将用户的语音转换为文字
2. **智能体咨询**：调用民事咨询智能体获取法律建议
3. **语音合成（TTS）**：将智能体的回复转换为语音文件

整个流程对用户透明，用户只需发送语音文件，即可获得语音回复。

---

## 🎯 核心功能

### 1. 语音识别（ASR）

将语音文件转换为文字，支持：
- **音频格式**: WAV、MP3、OGG OPUS
- **文件大小**: 最大100MB
- **音频时长**: 最大2小时

### 2. 语音合成（TTS）

将文字转换为语音，支持：
- **音频格式**: MP3、PCM、OGG Opus
- **采样率**: 8000-48000 Hz
- **语速调整**: -50到+100
- **音量调整**: -50到+100
- **语音类型**: 15+种不同语音

### 3. 民事语音咨询

完整的语音咨询流程，集成：
- 语音识别
- 民事咨询智能体
- 语音合成

---

## 📡 API接口文档

### 1. 民事语音咨询（完整流程）

**接口**: `POST /api/consultation/civil/voice`

**认证**: 需要JWT token

**请求格式**: `multipart/form-data`

**请求参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| audio | File | 是 | 语音文件（WAV/MP3/OGG） |
| session_id | String | 否 | 会话ID（用于多轮对话） |
| speaker | String | 否 | 语音ID（默认女声） |

**响应**:
- **Content-Type**: `audio/mpeg`
- **Body**: MP3音频文件
- **Headers**:
  - `X-Session-Id`: 会话ID
  - `X-Recognized-Text`: 识别出的文字（前100字符）
  - `X-Answer-Text`: 智能体回复的文字（前100字符）
  - `X-Bot-Id`: 智能体ID
  - `X-Bot-Name`: 智能体名称

**示例**:
```bash
curl -X POST http://localhost:5000/api/consultation/civil/voice \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "audio=@/path/to/audio.wav" \
  -F "speaker=zh_female_xiaohe_uranus_bigtts" \
  -o response.mp3
```

### 2. 语音识别（单独使用）

**接口**: `POST /api/consultation/voice/recognize`

**认证**: 需要JWT token

**请求格式**: `multipart/form-data`

**请求参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| audio | File | 是 | 语音文件 |

**响应**:
```json
{
  "success": true,
  "data": {
    "text": "识别出的文字",
    "duration": 5000,
    "utterances": [...]
  }
}
```

### 3. 语音合成（单独使用）

**接口**: `POST /api/consultation/voice/synthesize`

**认证**: 需要JWT token

**请求格式**: `application/json`

**请求参数**:
```json
{
  "text": "要合成的文字",
  "speaker": "zh_female_xiaohe_uranus_bigtts",
  "audio_format": "mp3",
  "sample_rate": 24000
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "audio_url": "音频文件URL",
    "audio_size": 12345,
    "audio_format": "mp3"
  }
}
```

### 4. 获取可用语音列表

**接口**: `GET /api/consultation/voice/speakers`

**认证**: 不需要

**响应**:
```json
{
  "success": true,
  "data": {
    "通用语音": {
      "zh_female_xiaohe_uranus_bigtts": {
        "name": "小禾（女声）",
        "description": "通用女声，适合日常对话",
        "gender": "female",
        "recommended": true
      },
      ...
    },
    ...
  }
}
```

---

## 🎤 可用语音列表

### 通用语音

| 语音ID | 名称 | 描述 | 性别 | 推荐 |
|--------|------|------|------|------|
| zh_female_xiaohe_uranus_bigtts | 小禾 | 通用女声，适合日常对话 | 女 | ✅ |
| zh_female_vv_uranus_bigtts | Vivi | 中英文女声，专业感强 | 女 | ✅ |
| zh_male_m191_uranus_bigtts | 韵舟 | 通用男声，专业稳重 | 男 | ❌ |
| zh_male_taocheng_uranus_bigtts | 晓天 | 年轻男声，亲切自然 | 男 | ❌ |

### 有声读物

| 语音ID | 名称 | 描述 | 性别 | 推荐 |
|--------|------|------|------|------|
| zh_female_xueayi_saturn_bigtts | 雪阿姨 | 儿童读物女声，亲切温暖 | 女 | ❌ |

### 视频配音

| 语音ID | 名称 | 描述 | 性别 | 推荐 |
|--------|------|------|------|------|
| zh_male_dayi_saturn_bigtts | 大义 | 视频配音男声，专业有力 | 男 | ❌ |
| zh_female_mizai_saturn_bigtts | 米在 | 温柔女声，适合情感类内容 | 女 | ❌ |
| zh_female_jitangnv_saturn_bigtts | 鸡汤女声 | 励志女声，充满正能量 | 女 | ❌ |
| zh_female_meilinvyou_saturn_bigtts | 美腻女友 | 女友音，甜蜜温柔 | 女 | ❌ |

### 角色扮演

| 语音ID | 名称 | 描述 | 性别 | 推荐 |
|--------|------|------|------|------|
| saturn_zh_female_keainvsheng_tob | 可爱女生 | 甜美可爱，活泼开朗 | 女 | ❌ |
| saturn_zh_male_shuanglangshaonian_tob | 爽朗少年 | 阳光开朗，充满活力 | 男 | ❌ |
| saturn_zh_male_tiancaitongzhuo_tob | 天才同桌 | 聪明伶俐，学霸气质 | 男 | ❌ |

---

## 💡 使用场景

### 场景1：快速咨询

用户遇到法律问题，录制一段语音发送给系统，系统立即返回语音回复。

**流程**:
1. 用户录制语音： "请问如何追讨债务？"
2. 系统识别语音
3. 系统调用民事咨询智能体
4. 系统合成语音回复
5. 用户播放语音回复

### 场景2：多轮对话

用户进行连续的语音咨询，系统保持对话上下文。

**流程**:
1. 第一轮：用户发送语音，获得回复（获得session_id）
2. 第二轮：用户发送语音 + session_id，获得回复
3. 第三轮：用户发送语音 + session_id，获得回复

### 场景3：个性化语音

用户可以选择自己喜欢的语音风格。

**流程**:
1. 用户查看可用语音列表
2. 用户选择语音（如：zh_female_xiaohe_uranus_bigtts）
3. 用户发送语音，系统使用选择的语音回复

---

## 🧪 测试指南

### 1. 准备测试音频

准备一个测试音频文件（WAV/MP3格式），内容可以是：
- "请问如何追讨债务？"
- "劳动合同违约怎么办？"
- "邻居噪音扰民如何维权？"

### 2. 获取Token

使用微信登录或测试模式获取JWT token。

### 3. 测试语音识别

```bash
curl -X POST http://localhost:5000/api/consultation/voice/recognize \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "audio=@test.wav"
```

### 4. 测试语音合成

```bash
curl -X POST http://localhost:5000/api/consultation/voice/synthesize \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "您好，我是宁律师民事咨询助手。"}'
```

### 5. 测试语音咨询（完整流程）

```bash
curl -X POST http://localhost:5000/api/consultation/civil/voice \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "audio=@test.wav" \
  -F "speaker=zh_female_xiaohe_uranus_bigtts" \
  -o response.mp3
```

### 6. 使用测试脚本

```bash
cd backend
python scripts/test_voice.py
```

---

## 🔧 技术实现

### 技术栈

- **语音识别（ASR）**: 豆包语音大模型
- **语音合成（TTS）**: 豆包语音大模型
- **民事咨询智能体**: 扣子官方API
- **SDK**: coze-coding-dev-sdk

### 文件结构

```
backend/src/
├── services/
│   └── voice.py              # 语音服务
├── routes/
│   └── consultation.py       # 咨询路由（包含语音接口）
└── scripts/
    └── test_voice.py         # 测试脚本
```

### 核心流程

```python
# 语音服务
class VoiceService:
    def recognize_audio()  # 语音识别
    def synthesize_speech()  # 语音合成
    
# 民事语音咨询接口
def civil_voice_consultation():
    1. 接收语音文件
    2. 语音识别 → 文字
    3. 调用民事咨询智能体 → 回复文字
    4. 语音合成 → 语音文件
    5. 返回语音文件
```

---

## ⚠️ 注意事项

### 音频文件要求

1. **格式**: WAV、MP3、OGG OPUS
2. **大小**: 最大100MB
3. **时长**: 最大2小时
4. **质量**: 建议使用清晰的音频，噪音会影响识别准确率

### 性能考虑

1. **响应时间**: 完整流程约需5-10秒
2. **并发限制**: 建议控制并发请求数量
3. **临时文件**: 系统会自动清理临时文件

### 错误处理

1. **音频格式错误**: 返回400错误
2. **识别失败**: 返回识别失败信息
3. **咨询失败**: 返回咨询失败信息
4. **合成失败**: 返回合成失败信息

---

## 🚀 后续优化

### 短期优化

1. **实时语音流**: 支持实时语音流输入输出
2. **语音降噪**: 提高识别准确率
3. **语音情感分析**: 识别用户情绪

### 中期优化

4. **多语言支持**: 支持英文等外语咨询
5. **方言识别**: 支持常见方言识别
6. **语音克隆**: 用户可以自定义语音

### 长期规划

7. **智能打断**: 支持用户打断智能体
8. **多轮对话优化**: 提高对话连贯性
9. **个性化推荐**: 根据用户习惯推荐语音

---

## 📞 技术支持

如有问题，请联系开发团队。

---

**文档版本**: v1.0
**最后更新**: 2025-01-31
**作者**: AI开发助手
