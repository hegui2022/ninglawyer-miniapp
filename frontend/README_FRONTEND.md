# 宁律师微信小程序前端

## 📱 功能特性

### 1. 宁律师聊天页面
- ✅ 类似豆包的聊天界面设计
- ✅ 文本输入和发送
- ✅ 流式输出显示（实时显示AI回复）
- ✅ 语音输入功能（录音）
- ✅ 语音播放功能（TTS）
- ✅ 语音识别功能（ASR）
- ✅ 多轮对话支持
- ✅ 历史记录查询
- ✅ 会话清除功能
- ✅ 自动滚动到底部
- ✅ 正在输入提示

### 2. 首页
- ✅ 小程序入口展示
- ✅ 卡片式布局
- ✅ 渐变背景
- ✅ 宁律师入口（可点击）

## 🎨 设计特点

1. **现代化UI**
   - 渐变色设计（紫蓝色调）
   - 圆角卡片
   - 流畅动画

2. **类似豆包的聊天界面**
   - 气泡消息
   - 用户/助手头像
   - 语音波形动画
   - 打字动画

3. **响应式布局**
   - 适配不同屏幕尺寸
   - 自动调整消息显示

## 📁 文件结构

```
frontend/
├── pages/
│   ├── ninglawyer/              # 宁律师聊天页面
│   │   ├── ninglawyer.wxml      # 页面结构
│   │   ├── ninglawyer.wxss      # 页面样式
│   │   ├── ninglawyer.js        # 页面逻辑
│   │   └── ninglawyer.json      # 页面配置
│   └── index/                   # 首页
│       ├── index.wxml
│       ├── index.wxss
│       ├── index.js
│       └── index.json
├── assets/                      # 资源文件（需要自行添加）
│   ├── avatar-ninglawyer.png    # 宁律师头像
│   ├── avatar-user.png          # 用户头像
│   ├── logo.png                 # Logo
│   ├── icon-ninglawyer.png      # 宁律师图标
│   ├── icon-risk.png            # 防风险图标
│   ├── icon-contract.png        # 合同图标
│   ├── icon-teacher.png         # 法律教官图标
│   ├── icon-arrow.png           # 箭头图标
│   ├── icon-history.png         # 历史记录图标
│   ├── icon-clear.png           # 清除图标
│   ├── icon-close.png           # 关闭图标
│   ├── icon-mic.png             # 麦克风图标
│   ├── icon-voice.png           # 语音图标
│   └── ...
├── app.json                     # 小程序配置
└── sitemap.json                 # 站点地图
```

## 🔧 使用方法

### 1. 配置后端API地址

在 `frontend/pages/ninglawyer/ninglawyer.js` 中修改API_BASE：

```javascript
const API_BASE = 'http://your-backend-url/api/v1/ninglawyer'
```

### 2. 添加资源文件

在 `frontend/assets/` 目录下添加所需的图片资源：
- 宁律师头像
- 用户头像
- 各种图标

### 3. 配置小程序权限

在 `frontend/app.json` 中配置录音权限：

```json
{
  "permission": {
    "scope.record": {
      "desc": "用于语音输入功能"
    }
  }
}
```

### 4. 运行小程序

使用微信开发者工具打开 `frontend` 目录，点击编译运行。

## 🎯 核心功能说明

### 流式聊天
使用 `wx.request` 的 `responseType: 'text'` 接收流式响应，实时更新UI。

### 语音识别（ASR）
1. 调用录音API录制音频
2. 读取音频文件并转换为Base64
3. 调用后端ASR API进行语音识别
4. 将识别的文本发送到聊天API

### 语音合成（TTS）
1. 调用后端TTS API合成语音
2. 获取音频URL
3. 使用 `wx.createInnerAudioContext()` 播放音频

### 多轮对话
使用 `sessionId` 维护会话上下文，后端自动保存和加载历史记录。

## 🚀 后续优化

1. **性能优化**
   - 消息列表虚拟滚动
   - 图片懒加载
   - 音频预加载

2. **功能增强**
   - 消息复制功能
   - 消息分享功能
   - 表情支持
   - 图片上传

3. **用户体验**
   - 加载动画优化
   - 错误提示优化
   - 网络状态检测
   - 离线模式

## 📝 注意事项

1. **网络请求**
   - 需要在微信小程序后台配置服务器域名白名单
   - 开发环境可以使用 `project.config.json` 的 `setting` 配置跳过域名校验

2. **录音功能**
   - 需要用户授权录音权限
   - 注意录音时长限制（默认最长60秒）

3. **音频播放**
   - 注意音频格式兼容性
   - 需要处理播放失败的情况

4. **内存管理**
   - 注意及时清理录音器和播放器
   - 避免内存泄漏

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License
