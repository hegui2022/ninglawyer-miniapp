# 宁律师小程序 - 快速开始指南

## 5 分钟快速启动

### Step 1: 启动后端服务

```bash
cd /workspace/projects
python scripts/chat_server.py
```

看到以下输出说明启动成功：
```
🎙️  宁律师聊天服务器启动成功！
访问地址：http://localhost:8000
```

### Step 2: 打开微信开发者工具

1. 下载微信开发者工具：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
2. 安装并打开

### Step 3: 导入项目

1. 点击"导入项目"
2. 项目目录选择 `miniprogram` 文件夹
3. AppID 选择"测试号"（首次使用）
4. 项目名称：宁律师
5. 点击"导入"

### Step 4: 配置开发环境

1. 点击右上角"详情"
2. 选择"本地设置"
3. 勾选"不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书"

### Step 5: 运行小程序

点击"编译"按钮，即可在模拟器中看到宁律师小程序！

---

## 功能测试

### 测试文本咨询

1. 在聊天页面输入："你好，宁律师"
2. 点击发送
3. 查看宁律师的回复

### 测试快捷标签

1. 在聊天页面底部，点击快捷标签："我被拖欠工资了怎么办？"
2. 自动发送并查看回复

### 测试语音输入（需要真机）

1. 长按麦克风按钮 🎤
2. 说话
3. 松开发送

---

## 图标配置（可选）

小程序需要 Tab Bar 图标才能完美显示。临时方案：

### 方案 A：暂不添加图标
小程序会显示 Tab Bar 文字，功能正常。

### 方案 B：添加图标

1. 访问 iconfont：https://www.iconfont.cn/
2. 搜索图标：聊天、历史、用户
3. 下载 PNG 格式（48x48px）
4. 放到 `miniprogram/images/tab/` 目录
5. 文件命名：
   - chat.png / chat-active.png
   - history.png / history-active.png
   - mine.png / mine-active.png

---

## 配置说明

### 修改服务器地址

编辑 `miniprogram/app.js`：

```javascript
globalData: {
  // 开发环境
  baseUrl: 'http://localhost:8000',
  
  // 生产环境（部署后修改）
  // baseUrl: 'https://your-domain.com',
}
```

### 修改快捷标签

编辑 `miniprogram/pages/chat/chat.js`：

```javascript
quickTags: [
  '我被拖欠工资了怎么办？',
  '离婚财产怎么分？',
  // 添加更多...
]
```

---

## 页面说明

### 📱 咨询页面
- 文本输入
- 语音录制
- 快捷标签
- 消息列表

### 📋 历史记录页面
- 查看历史对话
- 清空历史
- 导出记录

### 👤 我的页面
- 统计信息
- 功能列表
- 关于和帮助

---

## 常见问题

### Q: 点击"编译"报错？

A: 检查以下几点：
1. 后端服务是否启动
2. 项目目录是否正确
3. 是否勾选了"不校验合法域名"

### Q: Tab Bar 图标不显示？

A: 需要添加图标文件到 `miniprogram/images/tab/` 目录，详见上方"图标配置"部分。

### Q: 语音按钮没反应？

A: 语音功能需要在真机上测试，模拟器可能不支持。

### Q: 发送消息没反应？

A: 检查：
1. 后端服务是否运行
2. `app.js` 中的 `baseUrl` 是否正确
3. 网络是否正常

---

## 下一步

### 开发更多功能

参考 `README.md` 和 `DEPLOY.md`：
- 添加用户登录
- 收藏功能
- 分享功能
- 消息置顶

### 部署到生产环境

参考 `DEPLOY.md`：
- 云服务器部署
- HTTPS 配置
- 域名配置
- 小程序发布

---

## 技术支持

- 文档：`miniprogram/README.md`
- 部署指南：`miniprogram/DEPLOY.md`
- 反馈：feedback@ninglawyer.com

---

## 开始体验吧！🎉

现在你已经可以：
- ✅ 在模拟器中查看宁律师小程序
- ✅ 发送文本消息
- ✅ 查看快捷标签
- ✅ 查看历史记录
- ✅ 探索"我的"页面

祝使用愉快！
