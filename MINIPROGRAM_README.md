# 宁律师智能法律咨询 - 完整项目说明

## 📋 项目概述

宁律师智能法律咨询项目包含两个部分：
1. **后端服务**（Python + Flask + LangChain）
2. **微信小程序前端**（原生小程序开发）

整体采用豆包风格的移动端 UI，支持文本和语音双模式交互。

---

## 🏗️ 项目结构

```
/workspace/projects/                 # 项目根目录
│
├── miniprogram/                    # 微信小程序前端
│   ├── app.js                      # 小程序入口
│   ├── app.json                    # 小程序配置
│   ├── app.wxss                    # 全局样式
│   ├── pages/                      # 页面目录
│   │   ├── chat/                   # 咨询页面
│   │   ├── history/                # 历史记录页面
│   │   └── mine/                   # 我的页面
│   ├── images/                     # 图片资源
│   ├── README.md                   # 项目说明
│   ├── DEPLOY.md                   # 部署指南
│   ├── QUICKSTART.md               # 快速开始
│   ├── PROJECT_STRUCTURE.md        # 项目结构
│   └── dev.sh                      # 开发启动脚本
│
├── scripts/                        # 后端脚本
│   ├── chat_server.py              # Flask 聊天服务器
│   └── read_word_docs.py           # Word 文档读取脚本
│
├── src/                            # 源代码目录
│   ├── agents/                     # Agent 定义
│   │   └── agent.py                # 宁律师 Agent
│   ├── tools/                      # 工具定义
│   │   ├── speech_recognition_tool.py    # 语音识别
│   │   ├── text_to_speech_tool.py        # 语音合成
│   │   └── knowledge_base_tool.py        # 知识库查询
│   ├── storage/                    # 存储相关
│   │   └── memory/                 # 短期记忆
│   └── utils/                      # 工具函数
│
├── config/                         # 配置文件
│   └── agent_llm_config.json       # Agent 配置
│
├── assets/                         # 资源文件
│   ├── legal_knowledge_base.md     # 法律知识库
│   ├── 数据合规管理知识库.md       # 用户上传文档
│   └── voice_samples/              # 语音样本
│
├── docs/                           # 文档目录
│   └── knowledge_base_format_limits.md  # 知识库格式说明
│
├── tests/                          # 测试目录
│
├── AGENT.md                        # Agent 规范
├── README.md                       # 项目说明
├── requirements.txt                # Python 依赖
└── .coze                           # Coze 配置
```

---

## 🚀 快速开始

### 方式一：使用启动脚本（推荐）

```bash
cd /workspace/projects/miniprogram
./dev.sh
```

### 方式二：手动启动

1. **启动后端服务**
```bash
cd /workspace/projects
python scripts/chat_server.py
```

2. **打开微信开发者工具**
   - 下载：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
   - 导入项目：`miniprogram` 目录

3. **配置开发环境**
   - 勾选"不校验合法域名"

4. **点击编译**

---

## 📱 小程序功能

### 1. 咨询页面（pages/chat）

**核心功能：**
- ✅ 文本输入和发送
- ✅ 语音录制和发送（长按麦克风）
- ✅ 语音播放（宁律师回复自动播放）
- ✅ 消息列表（自动滚动到底部）
- ✅ 快捷标签（可滑动，点击快速提问）
- ✅ 打字动画（宁律师回复时）
- ✅ 消息气泡（豆包风格）

**快捷标签：**
- 我被拖欠工资了怎么办？
- 离婚财产怎么分？
- 借钱不还怎么维权？
- 签合同要注意什么？
- 公司不给交社保
- 工伤赔偿标准
- 租房纠纷怎么办
- 如何申请法律援助

### 2. 历史记录页面（pages/history）

**核心功能：**
- ✅ 查看所有历史对话
- ✅ 语音播放
- ✅ 清空历史记录
- ✅ 导出记录到剪贴板
- ✅ 空状态提示

### 3. 我的页面（pages/mine）

**核心功能：**
- ✅ 用户信息展示
- ✅ 统计数据（对话次数、今日咨询）
- ✅ 关于宁律师
- ✅ 使用帮助
- ✅ 常见问题
- ✅ 分享给好友
- ✅ 意见反馈
- ✅ 清除缓存

---

## 🎨 UI 风格

### 豆包风格特点

1. **颜色方案**
   - 主色调：`#07C160`（微信绿）
   - 辅助色：`#4A90E2`（蓝色）
   - 背景色：`#F7F7F7`（浅灰）
   - 消息气泡：用户（绿色渐变）、律师（白色）

2. **设计元素**
   - 圆角卡片（12px-16px）
   - 渐变色按钮
   - 流畅动画
   - 简洁图标
   - Emoji 头像

3. **交互体验**
   - 点击反馈（缩放效果）
   - 加载动画（打字点）
   - 滑动流畅
   - 自动播放

---

## 🔧 技术栈

### 前端
- 微信小程序原生框架
- WXML（页面结构）
- WXSS（页面样式）
- JavaScript（逻辑）

### 后端
- Python 3.7+
- Flask（Web 框架）
- LangChain（Agent 框架）
- LangGraph（图框架）

### AI 能力
- 豆包大模型（文本生成）
- 豆包语音（TTS/ASR）
- 知识库（RAG）

---

## 📡 API 接口

### 1. 发送消息

**请求：**
```http
POST /chat
Content-Type: application/json

{
  "message": "用户输入的文本",
  "voice_url": "语音文件URL（可选）",
  "session_id": "会话ID"
}
```

**响应：**
```json
{
  "success": true,
  "text": "宁律师的回复文本",
  "audio_url": "语音文件URL（可选）"
}
```

### 2. Web 主页

```http
GET /
```

返回包含聊天界面的 HTML 页面（用于 Web 测试）

---

## 📚 文档说明

### 小程序文档（miniprogram/）

1. **README.md** - 项目说明
   - 功能特性
   - 项目结构
   - 快速开始
   - API 接口
   - 注意事项
   - 常见问题

2. **DEPLOY.md** - 部署指南
   - 本地运行
   - 生产部署
   - 云服务器方案
   - 云函数方案
   - 云开发方案

3. **QUICKSTART.md** - 快速开始
   - 5 分钟快速启动
   - 功能测试
   - 图标配置
   - 常见问题

4. **PROJECT_STRUCTURE.md** - 项目结构
   - 完整的目录树
   - 文件说明
   - 数据流
   - 技术点
   - 扩展建议

### 项目文档（根目录）

1. **README.md** - 项目总览
2. **AGENT.md** - Agent 规范
3. **docs/knowledge_base_format_limits.md** - 知识库格式说明

---

## ⚙️ 配置说明

### 小程序配置（miniprogram/app.js）

```javascript
globalData: {
  // 服务器地址（根据环境修改）
  baseUrl: 'http://localhost:8000',  // 开发环境
  // baseUrl: 'https://your-domain.com',  // 生产环境
  
  // 用户信息
  userInfo: null,
  
  // 会话ID
  sessionId: '',
  
  // 消息历史
  messageHistory: []
}
```

### 后端配置（config/agent_llm_config.json）

```json
{
  "config": {
    "model": "doubao-seed-1-8-251228",
    "temperature": 0.8,
    "top_p": 0.9,
    "max_completion_tokens": 8000
  },
  "sp": "系统提示词...",
  "tools": ["工具列表"]
}
```

---

## 🎯 后续开发建议

### 功能扩展

1. **用户系统**
   - 微信登录
   - 用户信息管理
   - 收藏功能

2. **消息功能**
   - 消息搜索
   - 消息置顶
   - 消息标签
   - 消息导出

3. **分享功能**
   - 分享到好友
   - 分享到朋友圈
   - 分享卡片

4. **高级功能**
   - 多轮对话优化
   - 上下文理解增强
   - 智能推荐
   - 在线律师预约

### 性能优化

1. **前端优化**
   - 虚拟列表（长消息）
   - 图片懒加载
   - 分包加载
   - 代码压缩

2. **后端优化**
   - 使用 Gunicorn + Gevent
   - Redis 缓存
   - CDN 加速
   - 负载均衡

---

## 🐛 常见问题

### Q1: 小程序无法连接服务器？

**A:** 检查以下几点：
1. 后端服务是否启动：`ps aux | grep chat_server`
2. `app.js` 中的 `baseUrl` 是否正确
3. 是否勾选了"不校验合法域名"

### Q2: Tab Bar 图标不显示？

**A:** 需要手动添加图标文件到 `miniprogram/images/tab/` 目录，详见 `miniprogram/images/README.md`

### Q3: 语音功能不能用？

**A:** 
1. 语音功能需要在真机上测试
2. 首次使用需要授权录音权限
3. 检查手机是否支持录音

### Q4: 消息不显示？

**A:** 检查：
1. 是否正确调用了 `setData()`
2. 消息格式是否正确
3. 是否有 JS 错误

---

## 📞 技术支持

- 反馈：feedback@ninglawyer.com
- 文档：`miniprogram/README.md`
- 部署：`miniprogram/DEPLOY.md`
- 快速开始：`miniprogram/QUICKSTART.md`

---

## 📄 许可证

本项目仅供学习和研究使用。

---

## 🙏 致谢

- 豆包大模型 - 提供强大的 AI 能力
- LangChain - Agent 框架
- 微信小程序 - 平台支持

---

## 🎉 开始使用

现在你已经了解了整个项目，可以：

1. 运行 `./miniprogram/dev.sh` 启动开发环境
2. 阅读 `miniprogram/QUICKSTART.md` 快速上手
3. 查看 `miniprogram/DEPLOY.md` 了解部署

祝你开发愉快！
