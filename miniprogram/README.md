# 宁律师 - 智能法律咨询小程序

## 项目简介

宁律师是一款智能法律咨询小程序，采用豆包风格的移动端 UI，支持文本和语音双模式交互，提供专业的法律咨询服务。

## 功能特性

### ✨ 核心功能
- 📝 **文本咨询**：输入法律问题，获得专业解答
- 🎤 **语音输入**：长按说话，更自然的交互方式
- 🔊 **语音播放**：宁律师的回复可以语音播放
- 📚 **知识库支持**：基于真实法律条文回答
- 💬 **对话历史**：查看和管理咨询记录

### 🎨 界面特点
- 📱 **豆包风格 UI**：完全克隆豆包移动端界面
- 🏷️ **快捷标签**：可滑动的快捷问题标签
- 📊 **底部 TAB**：咨询、历史、我的三个主页面
- 🎯 **流畅动画**：消息滑入、打字动画等

## 项目结构

```
miniprogram/
├── app.js              # 小程序入口
├── app.json            # 小程序配置
├── app.wxss            # 全局样式
├── sitemap.json        # 站点地图配置
├── images/             # 图片资源
│   ├── README.md       # 图片说明
│   ├── tab/            # Tab Bar 图标
│   ├── audio-*.png     # 音频图标
│   └── share.jpg       # 分享图片
└── pages/              # 页面
    ├── chat/           # 咨询页面
    │   ├── chat.wxml   # 页面结构
    │   ├── chat.wxss   # 页面样式
    │   ├── chat.js     # 页面逻辑
    │   └── chat.json   # 页面配置
    ├── history/        # 历史记录页面
    │   ├── history.wxml
    │   ├── history.wxss
    │   ├── history.js
    │   └── history.json
    └── mine/           # 我的页面
        ├── mine.wxml
        ├── mine.wxss
        ├── mine.js
        └── mine.json
```

## 快速开始

### 1. 安装微信开发者工具

下载并安装微信开发者工具：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html

### 2. 导入项目

1. 打开微信开发者工具
2. 选择"导入项目"
3. 项目目录选择 `miniprogram` 文件夹
4. AppID 可以选择"测试号"或使用自己的 AppID
5. 项目名称：宁律师

### 3. 配置服务器地址

打开 `app.js`，修改 `baseUrl`：

```javascript
globalData: {
  // 开发环境
  baseUrl: 'http://localhost:8000',
  
  // 生产环境（需要部署到公网）
  // baseUrl: 'https://your-domain.com',
}
```

### 4. 启动后端服务

```bash
cd /workspace/projects
python scripts/chat_server.py
```

### 5. 运行小程序

1. 在微信开发者工具中点击"编译"
2. 预览小程序

## 配置说明

### 开发环境

开发环境需要：
- 后端服务运行在 `localhost:8000`
- 微信开发者工具开启"不校验合法域名"

#### 如何开启不校验合法域名：

1. 点击微信开发者工具右上角的"详情"
2. 选择"本地设置"
3. 勾选"不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书"

### 生产环境

生产环境需要：
1. 后端服务部署到公网
2. 配置 HTTPS 证书
3. 在微信小程序后台配置服务器域名

#### 配置步骤：

1. 登录微信公众平台：https://mp.weixin.qq.com/
2. 选择你的小程序
3. 进入"开发" -> "开发管理" -> "开发设置"
4. 在"服务器域名"中添加：
   - request 合法域名：`https://your-domain.com`
   - uploadFile 合法域名：`https://your-domain.com`
   - downloadFile 合法域名：`https://your-domain.com`

## 页面说明

### 咨询页面（pages/chat）

主要功能：
- 文本输入和发送
- 语音录制和发送
- 消息列表显示
- 语音播放
- 快捷标签

### 历史记录页面（pages/history）

主要功能：
- 查看历史对话
- 语音播放
- 清空历史
- 导出记录

### 我的页面（pages/mine）

主要功能：
- 用户信息展示
- 统计数据
- 功能列表
- 关于和帮助

## API 接口

### 1. 发送消息

```
POST /chat
Content-Type: application/json

{
  "message": "用户输入的文本",
  "voice_url": "语音文件URL（可选）",
  "session_id": "会话ID"
}

Response:
{
  "success": true,
  "text": "宁律师的回复",
  "audio_url": "语音URL"
}
```

### 2. 上传语音（可选）

```
POST /upload
Content-Type: multipart/form-data

file: 语音文件

Response:
{
  "success": true,
  "url": "语音文件URL"
}
```

## 注意事项

### 1. 图标资源

小程序需要以下图标文件（详见 `images/README.md`）：

**必需的 Tab Bar 图标：**
- `tab/chat.png` / `tab/chat-active.png`
- `tab/history.png` / `tab/history-active.png`
- `tab/mine.png` / `tab/mine-active.png`

**音频图标：**
- `audio-static.png`
- `audio-playing.gif`

**分享图片：**
- `share.jpg`

临时解决方案：可以暂时不添加图标，Tab Bar 会显示文字。

### 2. 录音权限

小程序使用录音功能需要用户授权，首次使用时会弹出授权提示。

### 3. 音频播放

音频播放需要网络连接，音频文件存储在对象存储中。

### 4. 消息历史

消息历史存储在本地，清除缓存会丢失所有历史记录。

## 开发建议

### 1. 调试技巧

- 使用微信开发者工具的 Console 查看日志
- 使用 Network 面板查看网络请求
- 使用 Storage 面板查看本地存储

### 2. 性能优化

- 消息列表使用虚拟列表（如果消息很多）
- 图片懒加载
- 防抖和节流

### 3. 用户体验

- 加载状态提示
- 错误处理
- 网络异常提示

## 常见问题

### Q1: 小程序无法连接服务器？

**A:** 检查以下几点：
1. 后端服务是否启动
2. `app.js` 中的 `baseUrl` 是否正确
3. 是否开启了"不校验合法域名"

### Q2: 录音功能不能用？

**A:** 检查以下几点：
1. 是否授权了录音权限
2. 手机是否支持录音
3. 是否在真机上测试（部分模拟器不支持）

### Q3: Tab Bar 图标不显示？

**A:** 图标文件需要手动添加：
1. 从 iconfont 下载图标
2. 放到 `images/tab/` 目录
3. 确保文件名与 `app.json` 中配置一致

## 技术栈

- 微信小程序原生框架
- Flask（后端服务）
- LangChain（Agent 框架）
- 豆包大模型（AI 回复）
- 豆包语音（TTS）

## 版本历史

### v1.0.0（当前版本）
- 初始版本
- 文本咨询功能
- 语音输入和播放
- 历史记录
- 我的页面

## 联系方式

- 反馈：feedback@ninglawyer.com
- 官网：https://ninglawyer.com

## 免责声明

宁律师提供的法律建议仅供参考，不构成正式法律意见。如遇复杂法律问题，建议咨询专业律师。
