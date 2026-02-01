# 宁律师小程序前端

类似豆包的聊天界面设计。

## 目录结构

```
frontend/
├── pages/
│   ├── ninglawyer/
│   │   ├── ninglawyer.wxml      # 宁律师聊天页面
│   │   ├── ninglawyer.wxss      # 宁律师样式
│   │   ├── ninglawyer.js        # 宁律师逻辑
│   │   └── ninglawyer.json      # 宁律师配置
├── components/
│   ├── chat-message/            # 消息组件
│   ├── voice-button/            # 语音按钮组件
│   └── audio-player/            # 音频播放器组件
├── utils/
│   ├── request.js               # 网络请求
│   ├── audio-recorder.js        # 录音工具
│   └── storage.js               # 本地存储
└── app.json
```

## 功能特性

1. **聊天界面**
   - 类似豆包的聊天界面
   - 消息气泡（用户/助手）
   - 流式输出显示
   - 自动滚动到底部

2. **语音功能**
   - 语音输入（录音按钮）
   - 语音播放（TTS）
   - 语音识别（ASR）

3. **多轮对话**
   - 会话管理
   - 历史记录
   - 上下文保持

## API接口

- POST /api/v1/ninglawyer/chat/stream - 流式聊天
- POST /api/v1/ninglawyer/voice/recognize - 语音识别
- POST /api/v1/ninglawyer/voice/synthesize - 语音合成
- GET /api/v1/ninglawyer/history - 历史记录
- DELETE /api/v1/ninglawyer/session - 清除会话
