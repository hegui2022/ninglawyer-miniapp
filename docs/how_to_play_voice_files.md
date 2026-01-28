# 宁律师语音文件播放指南

## 🎧 语音文件位置

所有语音文件都保存在项目的 `assets/` 目录下：

### 1. 宁律师回复语音

**文件**：`assets/ning_lawyer_reply.mp3`

**内容**：宁律师对"公司拖欠工资"问题的回复

### 2. 音色样音

**目录**：`assets/voice_samples/`

| 文件名 | 音色 | 说明 |
|--------|------|------|
| `天才同桌_saturn_zh_male_tiancaitongzhuo_tob.mp3` | 天才同桌 | 当前使用 ✅ |
| `云州_zh_male_m191_uranus_bigtts.mp3` | 云州 | 成熟稳重 |
| `小天_zh_male_taocheng_uranus_bigtts.mp3` | 小天 | 年轻活力 |
| `大一_zh_male_dayi_saturn_bigtts.mp3` | 大一 | 深沉有力 |
| `爽朗少年_saturn_zh_male_shuanglangshaonian_tob.mp3` | 爽朗少年 | 开朗爽快 |
| `小河_zh_female_xiaohe_uranus_bigtts.mp3` | 小河 | 温柔自然（女声） |
| `Vivi_zh_female_vv_uranus_bigtts.mp3` | Vivi | 中英双语（女声） |

---

## 🎯 如何播放语音

### 方法 1：直接双击（最简单）✅

1. 打开项目目录：`/workspace/projects`
2. 进入 `assets/` 目录
3. 双击任何 `.mp3` 文件即可播放

### 方法 2：使用文件管理器

**Windows**：
```
文件资源管理器 → 导航到项目目录 → assets → 双击 .mp3 文件
```

**macOS**：
```
访达 → 导航到项目目录 → assets → 双击 .mp3 文件
```

**Linux**：
```
文件管理器 → 导航到项目目录 → assets → 双击 .mp3 文件
```

### 方法 3：使用命令行（如果有播放器）

**Linux（使用 VLC）**：
```bash
vlc assets/ning_lawyer_reply.mp3
```

**Linux（使用 mpv）**：
```bash
mpv assets/ning_lawyer_reply.mp3
```

**Linux（使用 ffplay）**：
```bash
ffplay assets/ning_lawyer_reply.mp3
```

### 方法 4：使用网页播放器

1. 复制文件路径
2. 拖拽到浏览器中（如果浏览器支持）
3. 或使用在线播放器

---

## 🎵 推荐先听什么？

### 推荐顺序：

1. **先听音色样音**（选择最喜欢的声音）
   - 进入 `assets/voice_samples/` 目录
   - 逐个试听每个音色
   - 选择最像你声音的，或者最喜欢的

2. **再听宁律师回复**（体验实际效果）
   - 播放 `assets/ning_lawyer_reply.mp3`
   - 体验宁律师的对话风格

---

## 🔄 如何生成新的语音？

### 方法 1：运行测试脚本

```bash
python tests/test_voice_local.py
```

这会重新生成语音文件到 `assets/ning_lawyer_reply.mp3`

### 方法 2：生成所有音色样音

```bash
python tests/test_voice_samples.py
```

这会重新生成所有音色的样音到 `assets/voice_samples/` 目录

### 方法 3：使用 Agent 生成语音

```bash
python src/main.py
```

然后在对话中说："请用语音回答"，Agent 会生成新的语音链接。

---

## 📊 当前音色配置

**当前使用**：天才同桌（saturn_zh_male_tiancaitongzhuo_tob）

**特点**：聪明理性的男声

**如果想换音色**：
1. 试听 `assets/voice_samples/` 目录下的所有音色
2. 告诉我你想用的音色名称（如："小天"、"大一"、"云州"）
3. 我帮你更新配置

---

## 💡 常见问题

### Q1：为什么双击播放不了？
**A**：可能是你的系统没有默认的 mp3 播放器。安装一个播放器（如 VLC、Windows Media Player、QuickTime Player）即可。

### Q2：语音文件在哪里？
**A**：在项目目录的 `assets/` 文件夹下。

### Q3：可以下载到电脑上播放吗？
**A**：可以！直接复制 `assets/` 目录下的 `.mp3` 文件到你的电脑，然后用任何播放器播放。

### Q4：如何分享语音给别人？
**A**：复制 `.mp3` 文件，通过微信、邮件等方式发送即可。

### Q5：语音文件有多大？
**A**：通常 80-100 KB，很小，方便传输。

---

## 🎬 开始播放

### 快速开始：

1. **打开项目目录**
   ```
   /workspace/projects/assets/
   ```

2. **双击播放**
   - `ning_lawyer_reply.mp3` - 宁律师回复
   - `voice_samples/*.mp3` - 音色样音

---

## 🚀 需要帮助？

如果播放遇到问题：
1. 确认文件路径正确
2. 检查是否有 mp3 播放器
3. 尝试不同的播放器
4. 联系技术支持

---

**现在就去试试吧！双击这些文件就能听到宁律师的声音了！** 🎧
