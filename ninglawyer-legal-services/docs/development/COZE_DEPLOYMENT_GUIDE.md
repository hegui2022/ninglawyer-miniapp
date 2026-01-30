# 宁律师法律咨询小程序 - Coze 平台一键部署方案

## 📋 方案概述

本方案介绍如何通过 **Coze（扣子）平台** 实现宁律师法律咨询小程序的一键部署。

### 为什么选择 Coze 平台？

1. **免服务器部署**：无需购买和管理云服务器
2. **一键发布**：通过 Coze 平台快速发布到多个渠道
3. **内置 AI 能力**：直接使用 Coze 平台的 AI 能力
4. **多渠道支持**：支持微信小程序、企业微信、飞书等多个平台
5. **自动化运维**：Coze 平台负责运维和扩容

---

## 🚀 部署方式对比

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Coze 一键部署** | 免服务器、快速发布、多渠道 | 受限于 Coze 平台能力 | 快速上线、MVP 验证 |
| **独立部署** | 完全控制、可定制性强 | 需要服务器运维、成本高 | 生产环境、大规模应用 |

---

## 📱 Coze 一键部署方案

### 方案一：使用 Coze Bot + 微信小程序插件（推荐）

#### 优势
- ✅ 免服务器部署
- ✅ 快速上线（1-2天）
- ✅ 自动运维
- ✅ 支持多平台（微信小程序、企业微信、飞书）

#### 步骤

##### 第一步：在 Coze 平台创建 Bot

1. 登录 Coze 平台：https://www.coze.cn/
2. 点击"创建 Bot"
3. 填写 Bot 信息：
   - Bot 名称：宁律师法律咨询
   - Bot 描述：专业的法律咨询 AI 助手
   - Bot 头像：上传宁律师头像
4. 点击"创建"

##### 第二步：配置 Bot 能力

1. **配置人设与回复逻辑**
   ```
   角色：你是宁律师，专业的法律咨询 AI 助手。
   能力：你可以提供民事、刑事、合同、劳动、公司、知识产权、婚姻等领域的法律咨询服务。
   风格：专业、严谨、友好。
   ```

2. **添加技能**

   在 Coze Bot 中添加以下技能：
   - **法律咨询**：用户提问，AI 回答
   - **合同分析**：用户上传合同，AI 分析
   - **风险扫描**：AI 扫描法律风险
   - **合规检查**：AI 检查合规性

3. **配置知识库**

   上传法律知识库到 Coze 平台：
   - 法律条文
   - 判例库
   - 合同模板
   - 合规指南

##### 第三步：发布到微信小程序

1. 在 Coze 平台点击"发布"
2. 选择"微信小程序"
3. 填写小程序信息：
   - 小程序名称：宁律师法律咨询
   - 小程序 AppID：填入你的小程序 AppID
   - 服务器域名：Coze 会自动配置
4. 点击"发布"

##### 第四步：在微信开发者工具中配置

1. 打开微信开发者工具
2. 导入 `legal-instructor` 项目
3. 修改 `app.js`，使用 Coze API：

```javascript
// app.js
App({
  globalData: {
    config: {
      // 使用 Coze Bot URL
      apiUrl: 'https://api.coze.cn/v1',
      botId: '你的 Coze Bot ID',
      apiKey: '你的 Coze API Key'
    }
  },

  onLaunch() {
    console.log('宁律师小程序启动');
  }
});
```

4. 修改 `pages/consult/consult.js`，调用 Coze API：

```javascript
// pages/consult/consult.js
async sendToBackend(question) {
  const { botId, apiKey, apiUrl } = getApp().globalData.config;

  const response = await new Promise((resolve, reject) => {
    wx.request({
      url: `${apiUrl}/bot/chat`,
      method: 'POST',
      data: {
        bot_id: botId,
        user_id: wx.getStorageSync('userId') || 'default_user',
        query: question,
        stream: false
      },
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      success: (res) => {
        resolve(res.data);
      },
      fail: (err) => {
        reject(err);
      }
    });
  });

  // 处理回复
  const aiMessage = {
    id: Date.now(),
    type: 'ai',
    content: response.messages[0].content,
    time: this.formatTime(new Date())
  };

  this.setData({
    messages: [...this.data.messages, aiMessage],
    isTyping: false
  });
}
```

##### 第五步：提交审核

1. 在微信开发者工具中点击"上传"
2. 在微信公众平台提交审核
3. 审核通过后，小程序即可上线

---

### 方案二：使用 Coze API + 独立部署后端

#### 优势
- ✅ 完全控制前端 UI
- ✅ 可以添加自定义功能
- ✅ 可以使用自己的数据库

#### 步骤

##### 第一步：在 Coze 平台创建 Bot（同上）

##### 第二步：获取 Coze API Key

1. 在 Coze 平台进入 Bot 设置
2. 复制 Bot ID 和 API Key

##### 第三步：配置后端环境

创建 `.env` 文件：

```bash
# 使用 Coze API
COZE_BOT_ID=你的 Coze Bot ID
COZE_API_KEY=你的 Coze API Key
COZE_API_URL=https://api.coze.cn/v1

# 其他配置
API_HOST=0.0.0.0
API_PORT=5000
```

##### 第四步：修改后端代码

修改 `src/agents/master_agent.py`，使用 Coze API：

```python
"""
Master Agent - 使用 Coze API
"""

import requests
from typing import Dict, Any, Optional
from loguru import logger

from src.utils.config import get_config

config = get_config()


class MasterAgent:
    """主脑 AGENT - 使用 Coze API"""

    def __init__(self):
        """初始化 Master Agent"""
        self.bot_id = config['COZE_BOT_ID']
        self.api_key = config['COZE_API_KEY']
        self.api_url = config['COZE_API_URL']

    def consult(self, question: str, domain: str = 'civil') -> Dict[str, Any]:
        """
        咨询 - 调用 Coze API

        Args:
            question: 问题
            domain: 法律领域

        Returns:
            咨询结果
        """
        try:
            url = f"{self.api_url}/bot/chat"

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }

            data = {
                'bot_id': self.bot_id,
                'user_id': 'user_123',
                'query': question,
                'stream': False
            }

            response = requests.post(url, json=data, headers=headers, timeout=30)
            result = response.json()

            if 'messages' in result:
                answer = result['messages'][0]['content']
                return {
                    'success': True,
                    'answer': answer,
                    'domain': domain
                }
            else:
                return {
                    'success': False,
                    'error': 'No response from Coze'
                }

        except Exception as e:
            logger.error(f"Coze API 调用失败：{str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
```

##### 第五步：部署后端

```bash
# 安装依赖
pip install -r requirements.txt

# 启动后端
python src/main.py
```

---

## 🔑 Coze API 使用说明

### 1. 获取 API Key

1. 登录 Coze 平台
2. 进入 Bot 设置
3. 复制 Bot ID 和 API Key

### 2. 调用 Coze API

```javascript
// 前端调用示例
wx.request({
  url: 'https://api.coze.cn/v1/bot/chat',
  method: 'POST',
  data: {
    bot_id: '你的 Bot ID',
    user_id: 'user_123',
    query: '请问离婚需要什么手续？',
    stream: false
  },
  header: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 你的 API Key'
  },
  success: (res) => {
    console.log('AI 回复:', res.data.messages[0].content);
  }
});
```

---

## 📊 两种方案对比总结

| 特性 | 方案一：Coze Bot + 小程序插件 | 方案二：Coze API + 独立后端 |
|------|------------------------------|---------------------------|
| **部署难度** | ⭐ 简单 | ⭐⭐ 中等 |
| **部署时间** | 1-2 天 | 3-5 天 |
| **服务器成本** | 免费 | 需要购买服务器 |
| **自定义能力** | 受限 | 完全自定义 |
| **数据控制** | 在 Coze 平台 | 完全控制 |
| **扩展性** | 受限 | 高度可扩展 |
| **推荐场景** | MVP、快速验证 | 生产环境、大规模应用 |

---

## 🎯 推荐方案

### 如果您希望：
- ✅ **快速上线**（1-2天）
- ✅ **免服务器部署**
- ✅ **快速验证业务模式**

**选择方案一：Coze Bot + 微信小程序插件**

### 如果您希望：
- ✅ **完全控制前端 UI**
- ✅ **可以添加自定义功能**
- ✅ **使用自己的数据库**
- ✅ **后续扩展性强**

**选择方案二：Coze API + 独立后端**

---

## 📞 下一步

**请告诉我您希望使用哪种方案？**

我将帮您：
1. **方案一**：创建 Coze Bot 配置文件，指导您在 Coze 平台创建 Bot
2. **方案二**：修改后端代码，使用 Coze API，提供完整的部署脚本

或者，如果您有其他想法，也请告诉我！😊
