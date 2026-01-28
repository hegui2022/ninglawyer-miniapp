# 小程序图片资源说明

## 必需的图标文件

### Tab Bar 图标 (48x48px)
- `tab/chat.png` - 咨询图标（未选中）
- `tab/chat-active.png` - 咨询图标（选中）
- `tab/history.png` - 历史图标（未选中）
- `tab/history-active.png` - 历史图标（选中）
- `tab/mine.png` - 我的图标（未选中）
- `tab/mine-active.png` - 我的图标（选中）

### 音频图标
- `audio-static.png` - 音频静态图标（未播放）
- `audio-playing.gif` - 音频播放动画（播放中）

### 分享图片
- `share.jpg` - 分享封面图（建议 5:4 比例）

## 临时解决方案

在正式图标准备好之前，可以使用以下方案：

### 方案1：使用 emoji（无需修改代码）
Tab Bar 已经配置好了，但需要图标文件。可以：
1. 从 iconfont 下载图标
2. 使用在线图标生成工具
3. 使用纯色块代替

### 方案2：修改代码使用 emoji
将 `app.json` 中的 `iconPath` 和 `selectedIconPath` 改为使用 emoji
（需要修改 TabBar 配置，改用自定义 TabBar）

### 推荐图标资源
- iconfont（阿里巴巴矢量图标库）：https://www.iconfont.cn/
- IconPark：https://iconpark.oceanengine.com/
- Iconify：https://iconify.design/

## 图标设计规范

### Tab Bar 图标
- 尺寸：48x48px（实际显示 81x81px）
- 格式：PNG，透明背景
- 风格：线性图标，2px 描边
- 颜色：
  - 未选中：#999999
  - 选中：#07C160（微信绿）

### 音频图标
- 尺寸：32x32px
- 格式：PNG（静态）/ GIF（动画）
- 风格：简洁线条

### 分享图片
- 尺寸：建议 400x320px 或更大
- 格式：JPG/PNG
- 内容：宁律师 Logo + Slogan

## 快速获取图标

### 使用 iconfont
1. 访问 https://www.iconfont.cn/
2. 搜索图标：聊天、历史、用户
3. 添加到项目，下载 PNG 格式
4. 放到对应目录

### 使用 IconPark
1. 访问 https://iconpark.oceanengine.com/
2. 搜索图标，选择样式
3. 下载 SVG 或 PNG
4. 转换为 PNG（如果是 SVG）
