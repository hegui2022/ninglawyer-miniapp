# 前后端对接完成 - 使用说明

## ✅ 已完成的工作

### 1. 修改前端代码，连接真实后端 API

#### 文件修改：
- ✅ `legal-instructor/pages/consult/consult.js` - 咨询页面
- ✅ `legal-instructor/utils/config.js` - 统一配置文件
- ✅ `legal-instructor/app.js` - 小程序入口

#### 主要改动：

**1. 创建统一配置文件 (`utils/config.js`)**
```javascript
// 支持开发和生产环境
const CONFIG = {
  development: {
    apiUrl: 'http://localhost:5000/api',
    baseUrl: 'http://localhost:5000'
  },
  production: {
    apiUrl: 'https://api.ninglawyer.com/api',
    baseUrl: 'https://api.ninglawyer.com'
  },
  coze: {
    apiUrl: 'https://api.coze.cn/v1',
    botId: '',
    apiKey: ''
  }
};
```

**2. 修改咨询页面 (`pages/consult/consult.js`)**
- ✅ 将模拟回复改为真实 API 调用
- ✅ 添加错误处理
- ✅ 支持对话历史保存
- ✅ 支持图片上传和分析
- ✅ 添加加载提示

**3. 修改小程序入口 (`app.js`)**
- ✅ 使用统一配置文件
- ✅ 添加统一的请求方法
- ✅ 添加文件上传方法

---

## 🚀 快速开始（3 步）

### 第一步：启动后端

```bash
cd ninglawyer-miniapp

# 创建环境配置文件
cp .env.example .env

# 编辑 .env 文件，填写实际的配置
# 必须配置：
# MODEL_API_KEY=your_doubao_api_key
# MODEL_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
python src/main.py
```

后端服务将在 `http://localhost:5000` 启动。

### 第二步：配置前端 API 地址

修改 `legal-instructor/utils/config.js`：

```javascript
const CONFIG = {
  development: {
    apiUrl: 'http://localhost:5000/api',  // 确保地址正确
    baseUrl: 'http://localhost:5000'
  }
};
```

### 第三步：启动微信开发者工具

1. 打开微信开发者工具
2. 导入 `legal-instructor` 目录
3. 点击"编译"按钮
4. 测试咨询功能

---

## 🎯 测试咨询功能

1. **打开咨询页面**
   - 首页 → 点击"宁律师·民事"
   - 进入咨询对话页面

2. **发送问题**
   - 在输入框输入问题，如："离婚需要什么手续？"
   - 点击"发送"按钮

3. **查看结果**
   - 如果后端正常运行，会收到 AI 的真实回复
   - 如果后端未启动，会显示错误提示

---

## ❓ 常见问题

### Q1: 提示"网络连接失败"
**A**：检查后端服务是否启动，API 地址是否正确。

### Q2: 提示"咨询失败"
**A**：检查后端日志，可能是：
- 大语言模型 API Key 未配置
- 数据库连接失败
- 后端代码错误

### Q3: 回复很慢
**A**：这是正常的，因为：
- 大语言模型调用需要时间（通常 3-10 秒）
- 可以在后端添加缓存优化

---

## 🔄 Coze 平台一键部署

关于您提到的"在扣子平台就能一键部署"，我已经创建了详细的部署方案：

**查看文档**：`COZE_DEPLOYMENT_GUIDE.md`

**两种方案**：

### 方案一：Coze Bot + 微信小程序插件（推荐）
- ✅ 免服务器部署
- ✅ 快速上线（1-2天）
- ✅ 自动运维

### 方案二：Coze API + 独立后端
- ✅ 完全控制前端 UI
- ✅ 可以添加自定义功能
- ✅ 使用自己的数据库

---

## 📊 部署方式对比

| 方式 | 优点 | 缺点 | 部署时间 |
|------|------|------|----------|
| **Coze 一键部署** | 免服务器、快速发布 | 受限于 Coze 平台能力 | 1-2天 |
| **独立部署** | 完全控制、可定制性强 | 需要服务器运维、成本高 | 3-5天 |

---

## 🎬 推荐方案

### 如果您希望：
- ✅ **快速上线**（1-2天）
- ✅ **免服务器部署**
- ✅ **快速验证业务模式**

**选择 Coze 一键部署**

### 如果您希望：
- ✅ **完全控制前端 UI**
- ✅ **可以添加自定义功能**
- ✅ **使用自己的数据库**

**选择独立部署**

---

## 📞 下一步

**请告诉我您希望使用哪种部署方式？**

我将帮您：
1. **Coze 一键部署**：创建 Coze Bot 配置，指导您在 Coze 平台部署
2. **独立部署**：创建部署脚本，提供完整的部署文档

或者，如果您已经启动了后端，现在就可以测试咨询功能了！😊
