# @ninglawyer/shared

宁律师小程序共享组件和工具库

## 版本

1.0.0

## 功能模块

### 组件 (Components)
- `request-form` - 请求表单组件
- `nav-bar` - 导航栏组件
- `chat-box` - 聊天框组件
- `card` - 卡片组件

### 工具 (Utils)
- `api.js` - API 请求封装
- `auth.js` - 认证工具
- `date.js` - 日期工具
- `storage.js` - 存储工具

### 技能 (Skills)
- `contract-draft.js` - 合同起草技能
- `contract-review.js` - 合同审查技能
- `legal-consult.js` - 法律咨询技能

### MCP 服务 (MCP)
- `index.js` - MCP 服务封装

## 安装

```bash
npm install @ninglawyer/shared
```

## 使用

### 工具函数

```javascript
import { request, auth } from '@ninglawyer/shared'

// API 请求
const data = await request('/user/info')

// 认证
const token = auth.getToken()
```

### 组件

```json
{
  "usingComponents": {
    "request-form": "@ninglawyer/shared/components/request-form/index"
  }
}
```

```wxml
<request-form bind:submit="handleSubmit" />
```

### 技能

```javascript
import { ContractDraftSkill } from '@ninglawyer/shared/skills/contract-draft.js'

const skill = new ContractDraftSkill()
const result = await skill.draft({ type: 'labor' })
```

### MCP 服务

```javascript
import mcp from '@ninglawyer/shared/mcp/index.js'

const audio = await mcp.textToSpeech('您好，我是宁律师')
```

## 开发

```bash
# 安装依赖
npm install

# 构建
npm run build
```

## 文档

详细文档请查看项目根目录的 `docs/` 目录。

## License

MIT
