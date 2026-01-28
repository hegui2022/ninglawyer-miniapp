# 宁律师小程序项目结构

```
miniprogram/                          # 小程序根目录
│
├── app.js                            # 小程序入口文件
│   ├── globalData                    # 全局数据
│   │   ├── baseUrl                   # 服务器地址
│   │   ├── userInfo                  # 用户信息
│   │   ├── sessionId                 # 会话ID
│   │   └── messageHistory            # 消息历史
│   ├── onLaunch()                    # 小程序启动
│   ├── generateSessionId()           # 生成会话ID
│   ├── loadMessageHistory()          # 加载消息历史
│   ├── saveMessageHistory()          # 保存消息历史
│   ├── getUserInfo()                 # 获取用户信息
│   └── setUserInfo()                 # 设置用户信息
│
├── app.json                          # 小程序配置文件
│   ├── pages                         # 页面列表
│   ├── window                        # 窗口配置
│   ├── tabBar                        # 底部 TabBar 配置
│   ├── permission                    # 权限配置
│   ├── networkTimeout                # 网络超时配置
│   └── debug                         # 调试模式
│
├── app.wxss                          # 全局样式文件
│   ├── .chat-container               # 容器样式
│   ├── .message-bubble               # 消息气泡
│   ├── .avatar                       # 头像样式
│   ├── .quick-tag                    # 快捷标签
│   ├── .input-area                   # 输入区域
│   └── ...                           # 其他通用样式
│
├── sitemap.json                      # 站点地图配置
│
├── .gitignore                        # Git 忽略文件配置
│
├── README.md                         # 项目说明文档
│   ├── 项目简介
│   ├── 功能特性
│   ├── 项目结构
│   ├── 快速开始
│   ├── 页面说明
│   ├── API 接口
│   ├── 注意事项
│   └── 常见问题
│
├── DEPLOY.md                         # 部署指南
│   ├── 本地运行
│   ├── 生产部署
│   │   ├── 云服务器方案
│   │   ├── 云函数方案
│   │   └── 云开发方案
│   ├── 环境变量配置
│   ├── 性能优化
│   ├── 监控和日志
│   ├── 备份和恢复
│   ├── 安全建议
│   └── 成本估算
│
├── QUICKSTART.md                     # 快速开始指南
│   ├── 5 分钟快速启动
│   ├── 功能测试
│   ├── 图标配置
│   ├── 配置说明
│   ├── 页面说明
│   ├── 常见问题
│   └── 下一步
│
├── images/                           # 图片资源目录
│   ├── README.md                     # 图片说明文档
│   ├── tab/                          # TabBar 图标
│   │   ├── chat.png                  # 咨询图标（未选中）
│   │   ├── chat-active.png           # 咨询图标（选中）
│   │   ├── history.png               # 历史图标（未选中）
│   │   ├── history-active.png        # 历史图标（选中）
│   │   ├── mine.png                  # 我的图标（未选中）
│   │   └── mine-active.png           # 我的图标（选中）
│   ├── audio-static.png              # 音频静态图标
│   ├── audio-playing.gif             # 音频播放动画
│   └── share.jpg                     # 分享封面图
│
└── pages/                            # 页面目录
    │
    ├── chat/                         # 咨询页面
    │   ├── chat.wxml                 # 页面结构
    │   │   ├── .chat-container       # 聊天容器
    │   │   ├── .message-list        # 消息列表
    │   │   ├── .message              # 消息项
    │   │   ├── .quick-tags-scroll   # 快捷标签滚动
    │   │   ├── .input-area          # 输入区域
    │   │   └── .recording-tip       # 录音提示
    │   │
    │   ├── chat.wxss                 # 页面样式
    │   │   ├── .message-list        # 消息列表样式
    │   │   ├── .message-bubble      # 消息气泡样式
    │   │   ├── .audio-player        # 音频播放器样式
    │   │   ├── .input-area          # 输入区域样式
    │   │   └── .quick-tag           # 快捷标签样式
    │   │
    │   ├── chat.js                   # 页面逻辑
    │   │   ├── data                  # 页面数据
    │   │   │   ├── messages          # 消息列表
    │   │   │   ├── inputText         # 输入文本
    │   │   │   ├── isTyping          # 是否打字中
    │   │   │   ├── showRecorder      # 是否显示录音
    │   │   │   ├── quickTags         # 快捷标签
    │   │   │   └── ...               # 其他数据
    │   │   ├── onLoad()              # 页面加载
    │   │   ├── onShow()              # 页面显示
    │   │   ├── initRecorder()        # 初始化录音
    │   │   ├── initAudioPlayer()     # 初始化播放器
    │   │   ├── sendMessage()         # 发送消息
    │   │   ├── sendVoiceMessage()    # 发送语音
    │   │   ├── addMessage()          # 添加消息
    │   │   ├── playAudio()           # 播放音频
    │   │   └── ...                   # 其他方法
    │   │
    │   └── chat.json                 # 页面配置
    │       ├── navigationBarTitleText
    │       ├── enablePullDownRefresh
    │       └── backgroundColor
    │
    ├── history/                      # 历史记录页面
    │   ├── history.wxml             # 页面结构
    │   │   ├── .history-list        # 历史记录列表
    │   │   ├── .history-item        # 历史记录项
    │   │   ├── .empty-state         # 空状态
    │   │   └── .bottom-actions      # 底部操作
    │   │
    │   ├── history.wxss             # 页面样式
    │   │   ├── .history-list        # 历史列表样式
    │   │   ├── .message-row         # 消息行样式
    │   │   ├── .empty-state         # 空状态样式
    │   │   └── .action-btn          # 操作按钮样式
    │   │
    │   ├── history.js               # 页面逻辑
    │   │   ├── data                  # 页面数据
    │   │   │   ├── messages          # 消息列表
    │   │   │   └── isPlayingAudio    # 是否播放中
    │   │   ├── onLoad()              # 页面加载
    │   │   ├── loadMessages()        # 加载消息
    │   │   ├── playAudio()           # 播放音频
    │   │   ├── clearHistory()        # 清空历史
    │   │   └── exportHistory()       # 导出历史
    │   │
    │   └── history.json             # 页面配置
    │       ├── navigationBarTitleText
    │       ├── enablePullDownRefresh
    │       └── backgroundColor
    │
    └── mine/                         # 我的页面
        ├── mine.wxml                 # 页面结构
        │   ├── .user-card            # 用户信息卡片
        │   ├── .stats-card           # 统计卡片
        │   ├── .function-list        # 功能列表
        │   ├── .disclaimer           # 免责声明
        │   └── .version-info         # 版本信息
        │
        ├── mine.wxss                 # 页面样式
        │   ├── .user-card            # 用户卡片样式
        │   ├── .stats-card           # 统计卡片样式
        │   ├── .function-list        # 功能列表样式
        │   └── .disclaimer           # 免责声明样式
        │
        ├── mine.js                   # 页面逻辑
        │   ├── data                  # 页面数据
        │   │   ├── messageCount       # 对话次数
        │   │   ├── todayCount         # 今日咨询
        │   │   └── cacheSize          # 缓存大小
        │   ├── onLoad()              # 页面加载
        │   ├── loadStats()           # 加载统计
        │   ├── showAbout()           # 关于
        │   ├── showHelp()            # 帮助
        │   ├── showFAQ()             # 常见问题
        │   ├── clearCache()          # 清除缓存
        │   └── ...                   # 其他方法
        │
        └── mine.json                 # 页面配置
            ├── navigationBarTitleText
            ├── backgroundColor
            └── ...

后端服务（scripts/）
│
└── chat_server.py                    # Flask 聊天服务器
    ├── app                           # Flask 应用
    ├── HTML_TEMPLATE                 # HTML 模板
    ├── agent                         # LangChain Agent
    ├── /chat                         # 聊天接口
    └── /                             # 主页
```

## 核心文件说明

### 配置文件
- `app.json`: 小程序主配置，包含页面、TabBar、权限等
- `project.config.json`: 项目配置（由微信开发者工具生成）

### 入口文件
- `app.js`: 小程序入口，包含全局数据和方法
- `app.wxss`: 全局样式

### 页面文件
每个页面包含 4 个文件：
- `.wxml`: 页面结构（类似 HTML）
- `.wxss`: 页面样式（类似 CSS）
- `.js`: 页面逻辑（JavaScript）
- `.json`: 页面配置

### 数据流

```
用户输入 → 小程序页面 → API 请求 → 后端服务 → LangChain Agent → 豆包模型 → 返回结果 → 小程序显示
```

### 本地存储

```
小程序本地存储
├── sessionId           # 会话ID
├── userInfo            # 用户信息
└── messageHistory      # 消息历史
```

## 关键技术点

### 1. 豆包风格 UI
- 渐变色按钮和背景
- 圆角卡片
- 流畅动画
- 简洁图标

### 2. 语音功能
- 录音：`wx.getRecorderManager()`
- 播放：`wx.createInnerAudioContext()`
- 权限：`scope.record`

### 3. 消息管理
- 本地存储：`wx.getStorageSync()`
- 实时更新：`setData()`
- 滚动定位：`scroll-into-view`

### 4. 网络请求
- 文本消息：`wx.request()`
- 语音上传：`wx.uploadFile()`
- 超时处理：`timeout: 30000`

## 扩展建议

### 功能扩展
1. 用户登录和注册
2. 消息收藏功能
3. 分享功能
4. 消息搜索
5. 多语言支持

### 性能优化
1. 虚拟列表（长消息）
2. 图片懒加载
3. 分包加载
4. 缓存策略

### 体验优化
1. 骨架屏
2. 加载动画
3. 错误提示
4. 网络异常处理
