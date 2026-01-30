# 小程序矩阵集成开发指南

## 📋 目录

1. [架构概述](#架构概述)
2. [组件库](#组件库)
3. [小程序跳转](#小程序跳转)
4. [数据交互](#数据交互)
5. [大模型对接](#大模型对接)
6. [MCP 协议](#mcp-协议)
7. [完整示例](#完整示例)

---

## 🏗️ 架构概述

宁律师小程序矩阵采用以下架构：

```
┌─────────────────────────────────────────────────────────────┐
│                        小程序矩阵                              │
├──────────────┬──────────────┬──────────────┬───────────────┤
│ 法律教官     │  码上签约     │    理约      │    怎么判     │
│ (主小程序)   │  (合同签署)   │  (履约管理)  │  (违约维权)   │
└──────┬───────┴──────┬───────┴──────┬───────┴───────┬───────┘
       │              │              │               │
       └──────────────┼──────────────┼───────────────┘
                      │              │
              ┌───────▼──────────────▼───────┐
              │      后端 API 服务           │
              │  (Flask + LangChain)         │
              ├──────────────────────────────┤
              │ • 咨询 API                   │
              │ • 合同 API                   │
              │ • 共享数据 API               │
              │ • MCP API                    │
              └──────────────────────────────┘
                      │
              ┌───────▼──────────────────────┐
              │      大模型服务               │
              │  (豆包 doubao-seed)          │
              └──────────────────────────────┘
```

---

## 🧩 组件库

### 1. 消息列表组件 (message-list)

显示聊天消息的组件，支持用户消息、律师消息、系统消息等多种类型。

#### 使用方法

在页面的 JSON 文件中引入：

```json
{
  "usingComponents": {
    "message-list": "/components/message-list/message-list"
  }
}
```

在 WXML 中使用：

```xml
<message-list
  messages="{{messages}}"
  userInfo="{{userInfo}}"
  lawyerInfo="{{lawyerInfo}}"
  showWelcome="{{true}}"
  loading="{{loading}}"
  bind:action="onActionClick"
  bind:cardAction="onCardActionClick">
</message-list>
```

#### 属性说明

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| messages | Array | [] | 消息列表 |
| userInfo | Object | {} | 用户信息 |
| lawyerInfo | Object | {} | 律师信息 |
| showWelcome | Boolean | true | 是否显示欢迎消息 |
| welcomeMessage | Object | {} | 欢迎消息内容 |
| loading | Boolean | false | 是否加载中 |

#### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| action | 快捷操作点击 | { action } |
| cardAction | 卡片操作点击 | { action } |

---

### 2. 聊天输入组件 (chat-input)

提供文本和图片输入的聊天输入框。

#### 使用方法

在页面的 JSON 文件中引入：

```json
{
  "usingComponents": {
    "chat-input": "/components/chat-input/chat-input"
  }
}
```

在 WXML 中使用：

```xml
<chat-input
  placeholder="请输入您的问题..."
  maxlength="1000"
  bind:send="onSendMessage">
</chat-input>
```

#### 属性说明

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| placeholder | String | '' | 占位符 |
| maxlength | Number | 1000 | 最大长度 |
| disabled | Boolean | false | 是否禁用 |

#### 事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| send | 发送消息 | { text, image } |
| focus | 聚焦 | e |
| blur | 失焦 | e |

---

### 3. 加载组件 (loading)

显示加载状态。

#### 使用方法

在页面的 JSON 文件中引入：

```json
{
  "usingComponents": {
    "loading": "/components/loading/loading"
  }
}
```

在 WXML 中使用：

```xml
<loading type="circular" size="medium" text="加载中..."></loading>
<loading type="dots" size="large" text="正在处理..."></loading>
<loading type="bar" size="small" text="上传中..."></loading>
```

#### 属性说明

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| type | String | 'circular' | 加载类型 |
| size | String | 'medium' | 尺寸 |
| text | String | '' | 加载文本 |
| mask | Boolean | false | 是否显示遮罩层 |

---

## 🔀 小程序跳转

使用 `mini-program-navigator` 模块实现小程序之间的跳转。

### 导入模块

```javascript
const {
  navigateToCodeSigning,
  navigateToLyue,
  navigateToZenmePan,
  navigateToPreventRisk
} = require('../../utils/mini-program-navigator');
```

### 跳转示例

```javascript
// 跳转到码上签约
async function jumpToContractDraft(contractData) {
  try {
    await navigateToCodeSigning({
      contractType: '采购合同',
      partyA: '甲方公司',
      partyB: '乙方公司'
    });
  } catch (err) {
    console.error('跳转失败', err);
  }
}

// 跳转到理约
async function jumpToPerformance(contractData) {
  try {
    await navigateToLyue({
      contractId: 'contract_123',
      contractName: '采购合同'
    });
  } catch (err) {
    console.error('跳转失败', err);
  }
}

// 跳转到怎么判
async function jumpToJudgment(disputeData) {
  try {
    await navigateToZenmePan({
      contractId: 'contract_123',
      disputeType: '违约'
    });
  } catch (err) {
    console.error('跳转失败', err);
  }
}
```

---

## 🔄 数据交互

使用 `data-interaction` 模块实现小程序之间的数据交互。

### 导入模块

```javascript
const {
  saveConsultationData,
  getConsultationData,
  saveContractData,
  getContractData,
  setSceneData,
  getDataByScene
} = require('../../utils/data-interaction');
```

### 数据交互示例

```javascript
// 保存咨询数据
async function saveConsultation(question, answer) {
  try {
    await saveConsultationData({
      domain: 'civil',
      question,
      answer,
      timestamp: Date.now()
    });
  } catch (err) {
    console.error('保存失败', err);
  }
}

// 设置场景数据（用于小程序跳转）
async function prepareJump() {
  try {
    await setSceneData('contract_draft', {
      contractInfo: {
        contractType: '采购合同',
        partyA: '甲方公司',
        partyB: '乙方公司'
      },
      from: 'consultation'
    });
  } catch (err) {
    console.error('设置场景数据失败', err);
  }
}

// 获取场景数据
async function handleSceneLoad() {
  try {
    const res = await getDataByScene('contract_draft');
    if (res.code === 200) {
      const contractInfo = res.data.contractInfo;
      // 处理数据...
    }
  } catch (err) {
    console.error('获取场景数据失败', err);
  }
}
```

---

## 🤖 大模型对接

使用 `ai-interaction` 模块与大模型交互。

### 导入模块

```javascript
const {
  aiChat,
  aiRouteConsult,
  aiDraftContract,
  aiReviewContract
} = require('../../utils/ai-interaction');
```

### 大模型调用示例

```javascript
// AI 聊天
async function chatWithAI(question) {
  try {
    const res = await aiChat({
      domain: 'civil',
      question: question,
      chat_history: this.getChatHistory()
    });
    
    const answer = res.data.answer;
    console.log('AI 回复:', answer);
    return answer;
  } catch (err) {
    console.error('AI 聊天失败', err);
    throw err;
  }
}

// AI 路由咨询
async function routeConsult(input) {
  try {
    const res = await aiRouteConsult({
      input: input,
      context: {
        user_id: 'user_123',
        history: this.getChatHistory()
      }
    });
    
    console.log('路由结果:', res.data);
    return res.data;
  } catch (err) {
    console.error('路由失败', err);
    throw err;
  }
}

// AI 起草合同
async function draftContract(contractInfo) {
  try {
    const res = await aiDraftContract({
      contract_type: contractInfo.type,
      partyA: contractInfo.partyA,
      partyB: contractInfo.partyB,
      terms: contractInfo.terms
    });
    
    console.log('合同草稿:', res.data);
    return res.data;
  } catch (err) {
    console.error('起草合同失败', err);
    throw err;
  }
}
```

---

## 🔌 MCP 协议

使用 `mcp-client` 模块管理模型上下文和工具调用。

### 导入模块

```javascript
const { createMCPClient } = require('../../utils/mcp-client');
```

### MCP 使用示例

```javascript
// 初始化 MCP 客户端
async function initMCP() {
  const mcpClient = createMCPClient({
    sessionId: 'session_' + Date.now(),
    context: {
      domain: 'civil',
      platform: 'wechat-miniapp'
    }
  });
  
  await mcpClient.init();
  
  return mcpClient;
}

// 发送消息
async function sendMessage(mcpClient, message) {
  try {
    const response = await mcpClient.sendMessage(message);
    
    console.log('AI 回复:', response.response);
    
    // 处理工具调用
    if (response.toolCalls && response.toolCalls.length > 0) {
      await handleToolCalls(response.toolCalls);
    }
    
    return response;
  } catch (err) {
    console.error('发送消息失败', err);
    throw err;
  }
}

// 处理工具调用
async function handleToolCalls(toolCalls) {
  for (const toolCall of toolCalls) {
    if (toolCall.name === 'draft_contract') {
      // 调用合同起草工具
      await executeContractDraft(toolCall.parameters);
    } else if (toolCall.name === 'check_performance') {
      // 调用履约检查工具
      await executePerformanceCheck(toolCall.parameters);
    }
  }
}

// 更新上下文
async function updateContext(mcpClient, context) {
  try {
    await mcpClient.updateContext(context);
    console.log('上下文更新成功');
  } catch (err) {
    console.error('更新上下文失败', err);
  }
}

// 结束会话
async function endSession(mcpClient) {
  try {
    await mcpClient.endSession();
    console.log('会话已结束');
  } catch (err) {
    console.error('结束会话失败', err);
  }
}
```

---

## 📝 完整示例

### 咨询页面完整示例

参考：`examples/consult-page-example.js`

```javascript
const { aiChat } = require('../../utils/ai-interaction');
const { createMCPClient } = require('../../utils/mcp-client');
const { navigateToCodeSigning } = require('../../utils/mini-program-navigator');
const { saveConsultationData, setSceneData } = require('../../utils/data-interaction');

Page({
  data: {
    messages: [],
    userInfo: { avatar: '/assets/images/user-avatar-default.png' },
    lawyerInfo: { avatar: '/assets/images/lawyer-avatar-default.png' },
    loading: false,
    mcpClient: null
  },

  onLoad(options) {
    this.initMCP();
    
    // 处理场景参数
    if (options.scene) {
      this.handleScene(options.scene);
    }
  },

  async initMCP() {
    const mcpClient = createMCPClient({
      sessionId: 'session_' + Date.now(),
      context: { domain: 'civil' }
    });
    
    await mcpClient.init();
    this.setData({ mcpClient });
  },

  async onSendMessage(e) {
    const { text, image } = e.detail;
    
    // 添加用户消息
    this.addMessage({ role: 'user', content: text, image });
    
    this.setData({ loading: true });
    
    try {
      const response = await this.data.mcpClient.sendMessage(text);
      
      // 添加助手消息
      this.addMessage({ role: 'assistant', content: response.response });
      
      // 处理工具调用
      if (response.toolCalls) {
        await this.handleToolCalls(response.toolCalls);
      }
      
      // 保存咨询数据
      await saveConsultationData({
        domain: 'civil',
        question: text,
        answer: response.response
      });
      
    } catch (err) {
      console.error('发送消息失败', err);
    } finally {
      this.setData({ loading: false });
    }
  },

  async handleToolCalls(toolCalls) {
    for (const toolCall of toolCalls) {
      if (toolCall.name === 'draft_contract') {
        await setSceneData('contract_draft', toolCall.parameters);
        await navigateToCodeSigning(toolCall.parameters);
      }
    }
  },

  addMessage(message) {
    const messages = [...this.data.messages, {
      id: Date.now(),
      timestamp: Date.now(),
      ...message
    }];
    this.setData({ messages });
  }
});
```

---

## 🎯 最佳实践

### 1. 组件化开发

- 所有页面都应该使用组件化开发
- 共享组件放在 `components/` 目录
- 页面特定的组件放在 `pages/xxx/components/` 目录

### 2. 错误处理

```javascript
try {
  await someAsyncFunction();
} catch (err) {
  console.error('操作失败', err);
  wx.showToast({
    title: '操作失败，请重试',
    icon: 'none'
  });
}
```

### 3. 数据保存

```javascript
// 保存到后端
await saveConsultationData(data);

// 保存到本地存储
wx.setStorageSync('key', value);

// 场景数据（用于跳转）
await setSceneData('scene_name', data);
```

### 4. 性能优化

- 使用节流和防抖
- 图片压缩
- 分页加载
- 缓存数据

---

## 📞 技术支持

如有问题，请联系开发团队或查看：
- [GitHub Issues](https://github.com/hegui2022/ninglawyer-miniapp/issues)
- [项目文档](https://github.com/hegui2022/ninglawyer-miniapp)

---

**宁律师·让法律服务触手可及**
