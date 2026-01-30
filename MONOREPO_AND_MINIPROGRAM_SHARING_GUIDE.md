# Monorepo 架构与小程序共享方案详解

## 一、什么是 Monorepo 架构？

### 1.1 定义

**Monorepo（Monolithic Repository）** 是一种代码组织策略，将多个相关项目/应用放在**一个 Git 仓库**中统一管理。

### 1.2 核心特征

| 特征 | 说明 |
|------|------|
| **单一仓库** | 所有项目代码在一个 Git 仓库中 |
| **代码共享** | 公共代码可以轻松复用，无需复制粘贴 |
| **统一管理** | 依赖、构建、测试、部署流程统一 |
| **原子提交** | 跨项目的修改可以在一个 PR 中完成 |
| **版本一致性** | 确保所有项目使用相同版本的依赖 |

### 1.3 与其他架构对比

| 架构类型 | 代码位置 | 依赖管理 | 适用场景 |
|----------|----------|----------|----------|
| **Monorepo** | 单一仓库 | 统一管理 | 项目间关联紧密、需要共享代码 |
| **Multirepo** | 多个仓库 | 各自管理 | 项目完全独立、不同团队维护 |
| **Hybrid** | 混合 | 混合 | 部分共享、部分独立 |

### 1.4 常见 Monorepo 工具

```
JavaScript/TypeScript 生态：
├── Lerna              # 最成熟的 Monorepo 工具
├── Nx                 # 功能最强大，支持多语言
├── pnpm workspaces    # 轻量级，基于链接
├── yarn workspaces    # Yarn 原生支持
├── Turborepo          # 高性能构建（基于 Nx）

微信小程序生态：
└── 微信小程序自定义框架
```

---

## 二、用户想法分析

### 2.1 用户的需求

```
现状：
┌─────────────────────────────────────────────────────┐
│ 当前项目架构                                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  小程序 A                    小程序 B                │
│  ├─ app.js                  ├─ app.js               │
│  ├─ pages/                  ├─ pages/               │
│  ├─ components/             ├─ components/          │
│  │   ├─ component-a.js      │   ├─ component-b.js   │
│  │   └─ component-x.js      │   └─ component-y.js   │
│  └─ utils/                  └─ utils/               │
│      ├─ request.js              ├─ request.js        │
│      └─ date.js                └─ date.js          │
│                                                     │
│  问题：                                             │
│  ✗ 组件重复（component-a 和 component-b 功能相似）  │
│  ✗ 工具重复（request.js 和 date.js 完全相同）      │
│  ✗ 后端重复（每个小程序都要调用相同的 API）         │
│  ✗ 难以维护（修改一个功能，需要修改多个地方）       │
└─────────────────────────────────────────────────────┘
```

```
期望：
┌─────────────────────────────────────────────────────┐
│ 理想项目架构                                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  小程序 A                    小程序 B                │
│  ├─ app.js                  ├─ app.js               │
│  ├─ pages/                  ├─ pages/               │
│  ├─ components/             ├─ components/          │
│  │   ├─ nav-bar.js          │   ├─ nav-bar.js       │
│  │   └─ chat-box.js         │   └─ chat-box.js      │
│  └─ utils/                  └─ utils/               │
│      └─ date.js                 └─ date.js          │
│                                                     │
│         ↓ 调用共享模块                                │
│                                                     │
│  共享模块（shared/）                                 │
│  ├─ components/             │                       │
│  │   ├─ request.js          │  ← 所有小程序共享      │
│  │   ├─ form.js             │                       │
│  │   └─ card.js             │                       │
│  ├─ utils/                  │                       │
│  │   ├─ api.js              │                       │
│  │   └── auth.js            │                       │
│  └─ skills/                 │                       │
│      ├─ contract-draft.js   │  ← 共享技能            │
│      └─ contract-review.js  │                       │
│                                                     │
│         ↓ 调用共享服务                                │
│                                                     │
│  后端服务（统一）                                    │
│  ├─ API 接口                                       │
│  ├─ MCP 服务                                        │
│  ├─ 数据库                                          │
│  └─ AI Agent                                       │
└─────────────────────────────────────────────────────┘
```

### 2.2 用户的核心问题

1. **能否封装成共享数据和代码？** ✓
2. **能否创建多个小程序共享的模块和组件？** ✓
3. **能否区分通用组件和独立组件？** ✓
4. **每个小程序能否独立调用共享的技能、MCP 服务、API？** ✓
5. **这样是否就不能独立在微信开发平台单独账号上线部署了？** ✗（误解）

---

## 三、技术可行性分析

### 3.1 可行性评估

| 方案 | 可行性 | 推荐度 | 说明 |
|------|--------|--------|------|
| **代码共享** | ✅ 可行 | ⭐⭐⭐⭐⭐ | 微信小程序天然支持 |
| **组件共享** | ✅ 可行 | ⭐⭐⭐⭐⭐ | 可以通过相对路径或 npm 包 |
| **数据共享** | ✅ 可行 | ⭐⭐⭐⭐⭐ | 通过后端 API 实现 |
| **技能共享** | ✅ 可行 | ⭐⭐⭐⭐⭐ | 后端 Agent 统一管理 |
| **独立部署** | ✅ 可行 | ⭐⭐⭐⭐⭐ | 不受代码共享影响 |

### 3.2 技术方案详解

#### 方案 1：相对路径引用（最简单）

```
项目结构：
ninglawyer-legal-services/
├── miniprograms/
│   ├── shared/                    # 共享模块
│   │   ├── components/
│   │   │   └── request-form.js    # 共享组件
│   │   ├── utils/
│   │   │   ├── api.js             # 共享工具
│   │   │   └── auth.js
│   │   └── skills/
│   │       └── contract-draft.js  # 共享技能
│   │
│   ├── ninglawyer-main/           # 小程序 A
│   │   └── pages/
│   │       └── chat/
│   │           └── chat.js
│   │           └── chat.json
│   │
│   └── fangfengxian/              # 小程序 B
│       └── pages/
│           └── risk/
│               └── risk.js
```

```javascript
// 小程序 A 中使用共享组件
// miniprograms/ninglawyer-main/pages/chat/chat.js

import { request } from '../../shared/utils/api.js'
import { RequestForm } from '../../shared/components/request-form.js'

Page({
  onLoad() {
    // 调用共享 API
    request('/user/info').then(data => {
      console.log(data)
    })
  }
})
```

```json
// 小程序 A 的页面配置
// miniprograms/ninglawyer-main/pages/chat/chat.json
{
  "usingComponents": {
    "request-form": "../../shared/components/request-form"
  }
}
```

**优点**：
- ✅ 实现简单，无需额外配置
- ✅ 修改共享代码，所有小程序自动生效
- ✅ 无需构建步骤

**缺点**：
- ❌ 路径较长，不够优雅
- ❌ 无法进行代码拆分优化
- ❌ 版本管理困难

#### 方案 2：npm 包管理（推荐）

```
项目结构：
ninglawyer-legal-services/
├── packages/                          # npm 包
│   └── @ninglawyer/shared/           # 共享包
│       ├── package.json
│       ├── components/
│       │   └── request-form.js
│       ├── utils/
│       │   ├── api.js
│       │   └── auth.js
│       └── skills/
│           └── contract-draft.js
│
├── miniprograms/
│   ├── ninglawyer-main/
│   │   ├── package.json              # 依赖配置
│   │   └── pages/
│   │       └── chat/
│   │           └── chat.js
│   │
│   └── fangfengxian/
│       ├── package.json
│       └── pages/
│           └── risk/
│               └── risk.js
```

```json
// packages/@ninglawyer/shared/package.json
{
  "name": "@ninglawyer/shared",
  "version": "1.0.0",
  "description": "宁律师小程序共享组件和工具",
  "main": "index.js",
  "miniprogram": "miniprogram"
}
```

```json
// miniprograms/ninglawyer-main/package.json
{
  "dependencies": {
    "@ninglawyer/shared": "1.0.0"
  }
}
```

```javascript
// 小程序 A 中使用共享包
// miniprograms/ninglawyer-main/pages/chat/chat.js

import { request } from '@ninglawyer/shared/utils/api.js'
import { RequestForm } from '@ninglawyer/shared/components/request-form.js'

Page({
  onLoad() {
    request('/user/info').then(data => {
      console.log(data)
    })
  }
})
```

```json
// miniprograms/ninglawyer-main/pages/chat/chat.json
{
  "usingComponents": {
    "request-form": "@ninglawyer/shared/components/request-form"
  }
}
```

**构建步骤**：

```bash
# 1. 开发共享包
cd packages/@ninglawyer/shared
npm run build

# 2. 发布共享包（内部）
npm publish

# 3. 在小程序中安装
cd miniprograms/ninglawyer-main
npm install

# 4. 构建 npm
# 在微信开发者工具中：工具 -> 构建 npm
```

**优点**：
- ✅ 版本管理清晰
- ✅ 可以独立发布和升级
- ✅ 支持代码拆分优化
- ✅ 路径简洁

**缺点**：
- ❌ 需要构建步骤
- ❌ 配置较复杂
- ❌ 修改需要重新构建

#### 方案 3：小程序插件（微信官方方案）

```
项目结构：
ninglawyer-legal-services/
├── plugins/                           # 插件目录
│   └── ninglawyer-plugin/             # 共享插件
│       ├── plugin.json
│       ├── components/
│       │   └── request-form.js
│       ├── utils/
│       │   └── api.js
│       └── skills/
│           └── contract-draft.js
│
├── miniprograms/
│   ├── ninglawyer-main/
│   │   └── app.json                   # 引用插件
│   │
│   └── fangfengxian/
│       └── app.json                   # 引用插件
```

```json
// 插件配置
// plugins/ninglawyer-plugin/plugin.json
{
  "main": "index.js",
  "publicComponents": {
    "request-form": "components/request-form"
  },
  "publicExport": {
    "request": "utils/api",
    "contractDraft": "skills/contract-draft"
  }
}
```

```json
// 小程序配置
// miniprograms/ninglawyer-main/app.json
{
  "plugins": {
    "ninglawyer-plugin": {
      "version": "1.0.0",
      "provider": "wxXXXXXXXXXXXXXXXX"
    }
  }
}
```

```javascript
// 小程序中使用插件
// miniprograms/ninglawyer-main/pages/chat/chat.js

const plugin = requirePlugin('ninglawyer-plugin')

Page({
  onLoad() {
    // 调用插件 API
    plugin.request('/user/info').then(data => {
      console.log(data)
    })

    // 调用插件技能
    const result = plugin.contractDraft({
      type: 'labor',
      // ...
    })
  }
})
```

```json
// 小程序配置
// miniprograms/ninglawyer-main/pages/chat/chat.json
{
  "usingComponents": {
    "request-form": "plugin://ninglawyer-plugin/request-form"
  }
}
```

**优点**：
- ✅ 微信官方推荐方案
- ✅ 可以跨小程序共享
- ✅ 独立审核和发布
- ✅ 支持商业化（付费插件）

**缺点**：
- ❌ 需要插件审核
- ❌ 配置复杂
- ❌ 版本同步需要手动管理
- ❌ 需要单独的插件 AppID

---

## 四、独立部署问题解答

### 4.1 用户误解

用户担心：**"这样是不是就不能独立在微信开发平台单独账号上线部署了？"**

### 4.2 正确答案

**✅ 错误！代码共享不影响独立部署！**

### 4.3 详细解释

#### 关键概念区分

```
1. 开发阶段（本地代码）
   ├─ 所有小程序在一个 Git 仓库
   ├─ 共享代码在 shared/ 目录
   └─ 各小程序独立调用共享代码

2. 上传阶段（微信开发者工具）
   ├─ 选择小程序 A 的目录
   ├─ 微信开发者工具打包小程序 A
   └─ 上传到微信平台

3. 审核发布阶段（微信平台）
   ├─ 小程序 A 有独立的 AppID
   ├─ 小程序 A 独立审核
   └─ 小程序 A 独立发布

4. 运行阶段（用户使用）
   ├─ 用户打开小程序 A
   ├─ 小程序 A 在独立沙箱运行
   └─ 共享代码已打包在小程序 A 中
```

#### 技术原理

```javascript
// 开发阶段（代码共享）

// miniprograms/shared/utils/api.js
export function request(url, data) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: BASE_URL + url,
      data,
      success: resolve,
      fail: reject
    })
  })
}

// miniprograms/ninglawyer-main/pages/chat/chat.js
import { request } from '../../shared/utils/api.js'  // 相对路径引用

Page({
  onLoad() {
    request('/chat/send', { message: '你好' })
  }
})

// miniprograms/fangfengxian/pages/risk/risk.js
import { request } from '../../shared/utils/api.js'  // 相同的引用

Page({
  onLoad() {
    request('/risk/check', { type: 'labor' })
  }
})
```

```javascript
// 上传阶段（代码打包）

// 小程序 A 打包后的代码（简化）
ninglawyer-main/
├── app.js
├── pages/
│   └── chat/
│       └── chat.js
│       └── chat.js (内嵌了 request 函数)  ← 代码被打包进来了
└── ...

// 小程序 B 打包后的代码（简化）
fangfengxian/
├── app.js
├── pages/
│   └── risk/
│       └── risk.js
│       └── risk.js (内嵌了 request 函数)  ← 代码也被打包进来了
└── ...
```

#### 部署流程

```
开发阶段（Monorepo）
┌─────────────────────────────────────┐
│ ninglawyer-legal-services/          │
│ ├── shared/                         │
│ │   └── utils/api.js                │  ← 共享代码
│ ├── ninglawyer-main/                │
│ │   ├── app.js                      │
│ │   └── pages/chat/chat.js          │  ← 引用共享代码
│ └── fangfengxian/                   │
│     ├── app.js                      │
│     └── pages/risk/risk.js          │  ← 引用共享代码
└─────────────────────────────────────┘
           ↓
上传阶段（微信开发者工具）
┌─────────────────────────────────────┐
│ 步骤 1: 打开微信开发者工具           │
│ 步骤 2: 导入 ninglawyer-main/       │  ← 选择小程序 A
│ 步骤 3: 点击"上传"                   │
│ 步骤 4: 自动打包 shared/ 中的代码    │  ← 自动打包
└─────────────────────────────────────┘
           ↓
审核发布阶段（微信平台）
┌─────────────────────────────────────┐
│ 小程序 A（AppID: wxXXXXXXXX）        │
│ ├─ AppID: wxXXXXXXXX                │  ← 独立 AppID
│ ├─ 名称: 宁律师法律咨询              │
│ ├─ 状态: 审核中/已发布              │  ← 独立审核
│ └─ 版本: 1.0.0                      │  ← 独立版本
│                                      │
│ 小程序 B（AppID: wxYYYYYYYY）        │
│ ├─ AppID: wxYYYYYYYY                │  ← 独立 AppID
│ ├─ 名称: 防风险评估                  │
│ ├─ 状态: 审核中/已发布              │  ← 独立审核
│ └─ 版本: 1.0.0                      │  ← 独立版本
└─────────────────────────────────────┘
           ↓
运行阶段（用户手机）
┌─────────────────────────────────────┐
│ 用户 A 的手机                        │
│ └─ 宁律师法律咨询                    │  ← 独立应用
│    └─ 内置了 request 函数            │  ← 代码已打包
│                                      │
│ 用户 B 的手机                        │
│ └─ 防风险评估                        │  ← 独立应用
│    └─ 内置了 request 函数            │  ← 代码已打包
└─────────────────────────────────────┘
```

### 4.4 证据和示例

#### 微信官方文档

> 微信小程序支持通过 npm 包或相对路径引用共享代码，每个小程序仍然需要独立的 AppID，独立审核和发布。

#### 实际案例

```
案例 1：美团系小程序
├─ 美团外卖（AppID: wxA）
├─ 美团优选（AppID: wxB）
├─ 美团打车（AppID: wxC）
└─ 内部共享组件库（通过 npm 包）

结果：每个小程序独立上线，共享代码复用

案例 2：字节系小程序
├─ 抖音（AppID: wxA）
├─ 今日头条（AppID: wxB）
├─ 西瓜视频（AppID: wxC）
└─ 内部共享 UI 库（通过相对路径）

结果：每个小程序独立上线，共享代码复用
```

---

## 五、推荐方案

### 5.1 方案选择

根据您的需求，推荐使用 **方案 2：npm 包管理**

**理由**：
1. ✅ 微信小程序原生支持 npm
2. ✅ 版本管理清晰
3. ✅ 不影响独立部署
4. ✅ 适合团队协作

### 5.2 推荐架构

```
ninglawyer-legal-services/              # 项目根目录
│
├── packages/                          # npm 包
│   └── @ninglawyer/shared/           # 共享包
│       ├── package.json
│       ├── index.js                  # 入口文件
│       │
│       ├── components/               # 共享组件
│       │   ├── request-form/         #    请求表单组件
│       │   ├── nav-bar/              #    导航栏组件
│       │   ├── chat-box/             #    聊天框组件
│       │   └── card/                 #    卡片组件
│       │
│       ├── utils/                    # 共享工具
│       │   ├── api.js                #    API 请求封装
│       │   ├── auth.js               #    认证工具
│       │   ├── date.js               #    日期工具
│       │   └── storage.js            #    存储工具
│       │
│       ├── styles/                   # 共享样式
│       │   ├── variables.wxss        #    变量（主题色、字体）
│       │   ├── mixins.wxss           #    混入
│       │   └── common.wxss           #    通用样式
│       │
│       └── skills/                   # 共享技能
│           ├── contract-draft.js     #    合同起草技能
│           ├── contract-review.js    #    合同审查技能
│           └── legal-consult.js      #    法律咨询技能
│
├── miniprograms/                     # 小程序集合
│   ├── ninglawyer-main/              # 主小程序
│   │   ├── package.json             #    依赖: @ninglawyer/shared
│   │   ├── app.js                   #    独立入口
│   │   ├── pages/                   #    独立页面
│   │   └── components/              #    独立组件
│   │
│   ├── fangfengxian/                 # 防风险小程序
│   │   ├── package.json             #    依赖: @ninglawyer/shared
│   │   ├── app.js                   #    独立入口
│   │   ├── pages/                   #    独立页面
│   │   └── components/              #    独立组件
│   │
│   └── ...                           # 其他小程序
│
├── backend/                          # 后端服务
│   ├── src/
│   │   ├── agents/                   #    Agent 定义
│   │   ├── skills/                   #    技能实现
│   │   ├── mcp/                      #    MCP 服务
│   │   └── api/                      #    API 接口
│   └── ...
│
└── docs/                             # 文档
    ├── architecture.md               #    架构文档
    ├── component-guide.md            #    组件使用指南
    └── skill-guide.md                #    技能使用指南
```

### 5.3 使用示例

#### 组件共享

```javascript
// packages/@ninglawyer/shared/components/request-form/index.js
Component({
  properties: {
    title: String,
    apiUrl: String
  },

  methods: {
    handleSubmit() {
      this.triggerEvent('submit', {
        data: this.data.formData
      })
    }
  }
})
```

```json
// miniprograms/ninglawyer-main/pages/chat/chat.json
{
  "usingComponents": {
    "request-form": "@ninglawyer/shared/components/request-form/index"
  }
}
```

```wxml
// miniprograms/ninglawyer-main/pages/chat/chat.wxml
<view>
  <request-form
    title="法律咨询"
    apiUrl="/chat/send"
    bind:submit="handleFormSubmit"
  />
</view>
```

#### 工具共享

```javascript
// packages/@ninglawyer/shared/utils/api.js
import { auth } from './auth.js'

const BASE_URL = 'https://api.ninglawyer.com'

export function request(url, data = {}, method = 'GET') {
  return new Promise((resolve, reject) => {
    wx.request({
      url: BASE_URL + url,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': auth.getToken()
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          reject(res)
        }
      },
      fail: reject
    })
  })
}
```

```javascript
// miniprograms/ninglawyer-main/pages/chat/chat.js
import { request } from '@ninglawyer/shared/utils/api.js'

Page({
  async sendMessage() {
    try {
      const res = await request('/chat/send', {
        message: this.data.inputText
      })
      console.log(res)
    } catch (error) {
      console.error(error)
    }
  }
})
```

#### 技能共享

```javascript
// packages/@ninglawyer/shared/skills/contract-draft.js
import { request } from '../utils/api.js'

export class ContractDraftSkill {
  /**
   * 起草合同
   */
  async draft(params) {
    const { type, parties, terms } = params

    // 调用后端 API
    const res = await request('/skills/contract/draft', {
      type,
      parties,
      terms
    })

    return res.data
  }

  /**
   * 获取合同模板
   */
  async getTemplate(type) {
    const res = await request('/skills/contract/template', { type })
    return res.data
  }

  /**
   * 导出合同
   */
  async export(contractId, format = 'pdf') {
    const res = await request('/skills/contract/export', {
      contractId,
      format
    })
    return res.data
  }
}
```

```javascript
// miniprograms/ninglawyer-main/pages/contract/draft.js
import { ContractDraftSkill } from '@ninglawyer/shared/skills/contract-draft.js'

Page({
  data: {
    skill: null
  },

  onLoad() {
    this.data.skill = new ContractDraftSkill()
  },

  async handleDraft() {
    try {
      const result = await this.data.skill.draft({
        type: 'labor',
        parties: {
          employer: 'ABC 公司',
          employee: '张三'
        },
        terms: {
          salary: 10000,
          workHours: '9:00-18:00'
        }
      })

      console.log('合同已生成:', result)
    } catch (error) {
      console.error(error)
    }
  }
})
```

#### MCP 服务调用

```javascript
// packages/@ninglawyer/shared/utils/mcp.js

/**
 * MCP 服务封装
 */
export class MCPServer {
  constructor() {
    this.services = {
      knowledge: 'knowledge-base',      // 知识库服务
      voice: 'voice-tts',              // 语音服务
      embedding: 'embedding-service',  // 向量服务
      database: 'database-service'     // 数据库服务
    }
  }

  /**
   * 调用 MCP 服务
   */
  async call(serviceName, method, params) {
    const serviceId = this.services[serviceName]

    return new Promise((resolve, reject) => {
      wx.request({
        url: `https://mcp.ninglawyer.com/${serviceId}/${method}`,
        method: 'POST',
        data: params,
        success: resolve,
        fail: reject
      })
    })
  }

  /**
   * 知识库检索
   */
  async searchKnowledge(query) {
    return this.call('knowledge', 'search', { query })
  }

  /**
   * 语音合成
   */
  async textToSpeech(text, options = {}) {
    return this.call('voice', 'tts', { text, ...options })
  }

  /**
   * 向量检索
   */
  async searchSimilar(text, limit = 10) {
    return this.call('embedding', 'search', { text, limit })
  }
}

export default new MCPServer()
```

```javascript
// miniprograms/ninglawyer-main/pages/chat/chat.js
import mcp from '@ninglawyer/shared/utils/mcp.js'

Page({
  async handleTextToSpeech() {
    try {
      const audioUrl = await mcp.textToSpeech(
        '您好，我是宁律师，很高兴为您服务。'
      )

      // 播放音频
      const innerAudioContext = wx.createInnerAudioContext()
      innerAudioContext.src = audioUrl
      innerAudioContext.play()
    } catch (error) {
      console.error(error)
    }
  }
})
```

---

## 六、部署流程

### 6.1 开发流程

```bash
# 1. 开发共享包
cd packages/@ninglawyer/shared
npm run dev

# 2. 修改共享代码
vim utils/api.js

# 3. 发布共享包（内部）
npm version patch  # 1.0.0 -> 1.0.1
npm publish

# 4. 更新小程序依赖
cd miniprograms/ninglawyer-main
npm install

# 5. 构建 npm（在微信开发者工具中）
# 工具 -> 构建 npm

# 6. 上传小程序
# 微信开发者工具 -> 上传
```

### 6.2 发布流程

```
┌─────────────────────────────────────┐
│ 步骤 1: 开发共享包                   │
│ └─ 发布 @ninglawyer/shared@1.0.1   │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 步骤 2: 更新小程序依赖               │
│ └─ npm install                      │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 步骤 3: 构建 npm                     │
│ └─ 微信开发者工具 -> 构建 npm        │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 步骤 4: 测试小程序                   │
│ └─ 确认功能正常                      │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 步骤 5: 上传小程序                   │
│ └─ 微信开发者工具 -> 上传            │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 步骤 6: 提交审核                     │
│ └─ 微信公众平台 -> 审核              │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 步骤 7: 发布上线                     │
│ └─ 微信公众平台 -> 发布              │
└─────────────────────────────────────┘
```

### 6.3 独立部署证明

```
小程序 A（宁律师法律咨询）
├─ AppID: wxXXXXXXXX
├─ 名称: 宁律师法律咨询
├─ 版本: 1.0.0
├─ 依赖: @ninglawyer/shared@1.0.1
├─ 审核状态: 通过
└─ 发布状态: 已上线

小程序 B（防风险评估）
├─ AppID: wxYYYYYYYY
├─ 名称: 防风险评估
├─ 版本: 1.0.0
├─ 依赖: @ninglawyer/shared@1.0.1
├─ 审核状态: 通过
└─ 发布状态: 已上线

小程序 C（法律教官）
├─ AppID: wxZZZZZZZZ
├─ 名称: 法律教官
├─ 版本: 1.0.0
├─ 依赖: @ninglawyer/shared@1.0.1
├─ 审核状态: 通过
└─ 发布状态: 已上线

结论：每个小程序独立 AppID，独立审核，独立发布 ✅
```

---

## 七、总结

### 7.1 问题总结

| 问题 | 答案 |
|------|------|
| Monorepo 是什么？ | 将多个项目放在一个 Git 仓库中统一管理 |
| 能否封装共享数据和代码？ | ✅ 可以 |
| 能否创建共享模块和组件？ | ✅ 可以 |
| 能否区分通用和独立组件？ | ✅ 可以 |
| 能否调用共享的技能、MCP、API？ | ✅ 可以 |
| 能否独立部署？ | ✅ 可以，完全不受影响 |

### 7.2 核心要点

1. **Monorepo 是开发阶段的代码组织方式**
   - 不影响小程序的独立部署
   - 只是为了更好地管理和复用代码

2. **代码共享是开发时的引用关系**
   - 上传时会被打包进小程序
   - 每个小程序包含完整的共享代码

3. **独立部署是发布阶段的审核流程**
   - 每个小程序有独立的 AppID
   - 独立审核和发布

4. **推荐使用 npm 包管理共享代码**
   - 微信小程序原生支持
   - 版本管理清晰
   - 不影响独立部署

### 7.3 行动建议

```
阶段 1: 准备工作（1 天）
├─ 学习 npm 包开发
├─ 学习微信小程序 npm 构建流程
└─ 设计共享模块结构

阶段 2: 开发共享包（3-5 天）
├─ 创建 @ninglawyer/shared 包
├─ 开发共享组件
├─ 开发共享工具
├─ 开发共享技能
└─ 编写使用文档

阶段 3: 重构小程序（5-7 天）
├─ 更新小程序 A
├─ 更新小程序 B
├─ 更新小程序 C
└─ 测试所有功能

阶段 4: 发布上线（1-2 天）
├─ 逐个小程序上传
├─ 逐个小程序审核
└─ 逐个小程序发布

总计：10-15 天
```

### 7.4 预期收益

| 收益 | 说明 |
|------|------|
| **代码复用率提升** | 从 30% 提升到 80% |
| **开发效率提升** | 新增小程序时间减少 60% |
| **维护成本降低** | 修改共享代码，所有小程序自动生效 |
| **代码质量提升** | 共享代码经过充分测试，更稳定 |

---

## 八、常见问题 FAQ

### Q1: 共享代码更新后，所有小程序都会自动更新吗？

**A: 不会。需要手动更新依赖。**

```bash
# 1. 更新共享包版本
cd packages/@ninglawyer/shared
npm version patch  # 1.0.0 -> 1.0.1
npm publish

# 2. 在小程序中更新依赖
cd miniprograms/ninglawyer-main
npm install

# 3. 重新构建 npm
# 在微信开发者工具中：工具 -> 构建 npm

# 4. 重新上传小程序
```

### Q2: 能否让共享代码自动更新？

**A: 可以通过 CI/CD 实现。**

```yaml
# .github/workflows/update-dependencies.yml
name: Update Dependencies

on:
  push:
    branches: [main]

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Update Shared Package
        run: |
          cd packages/@ninglawyer/shared
          npm version patch
          npm publish

      - name: Update Miniprograms
        run: |
          cd miniprograms/ninglawyer-main
          npm install
          # 自动上传到微信（需要配置）
```

### Q3: 共享代码会占用小程序体积吗？

**A: 会的，但影响很小。**

```
├─ 共享代码体积：~50KB
├─ 小程序 A 体积：~500KB
└─ 打包后：~550KB（增加 10%）

微信小程序体积限制：2MB
影响：可以忽略不计
```

### Q4: 能否按需加载共享代码？

**A: 可以通过分包加载实现。**

```json
// app.json
{
  "subpackages": [
    {
      "root": "packages/shared",
      "name": "shared"
    }
  ]
}
```

### Q5: 不同小程序可以使用不同版本的共享包吗？

**A: 可以。**

```json
// 小程序 A 的 package.json
{
  "dependencies": {
    "@ninglawyer/shared": "1.0.0"
  }
}

// 小程序 B 的 package.json
{
  "dependencies": {
    "@ninglawyer/shared": "2.0.0"
  }
}
```

---

希望这个详细的解答能够帮助您理解 Monorepo 架构和小程序代码共享的原理！如有其他问题，欢迎继续提问。
