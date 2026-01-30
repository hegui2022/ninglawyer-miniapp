# Monorepo 迁移完成指南

## 概述

项目已成功迁移到 Monorepo 架构，新项目位于 `ninglawyer-legal-services/` 目录。

## 迁移后的目录结构

```
ninglawyer-legal-services/
├── packages/                      # npm 包
│   └── @ninglawyer/shared/       #    共享组件和工具
├── miniprograms/                 # 小程序集合
│   ├── ninglawyer-main/          #    主小程序
│   ├── fangfengxian/             #    防风险评估
│   ├── legal-instructor/         #    法律教官
│   ├── lyue/                     #    乐约
│   ├── zenme-pan/                #    怎么判
│   └── code-signing/             #    码上签约
├── backend/                      # 后端服务
├── docs/                         # 文档
├── scripts/                      # 脚本
└── infrastructure/               # 基础设施
```

## 快速开始

### 1. 启动后端服务

```bash
cd ninglawyer-legal-services/backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入配置信息

# 启动服务
python3 main.py
```

### 2. 开发小程序

#### 主小程序（ninglawyer-main）

```bash
cd ninglawyer-legal-services/miniprograms/ninglawyer-main

# 安装依赖（如果还没有）
npm install

# 构建共享包 npm（在微信开发者工具中）
# 工具 -> 构建 npm

# 使用微信开发者工具打开该目录
```

#### 其他小程序

类似地，进入对应的小程序目录，使用微信开发者工具打开。

### 3. 使用共享包

#### 安装共享包

```bash
cd ninglawyer-legal-services/packages/@ninglawyer/shared
npm install
```

#### 在小程序中使用

```javascript
// 导入工具
import { request, auth } from '@ninglawyer/shared'

// API 请求
const data = await request('/user/info')

// 认证
auth.setToken('your_token')
```

```json
// 页面配置
{
  "usingComponents": {
    "request-form": "@ninglawyer/shared/components/request-form/index"
  }
}
```

## 共享包使用指南

### 工具函数

#### api.js - API 请求封装

```javascript
import { request, get, post, put, delete, uploadFile } from '@ninglawyer/shared'

// GET 请求
const data = await get('/user/info')

// POST 请求
const result = await post('/chat/send', { message: '你好' })

// 上传文件
const fileUrl = await uploadFile(filePath, 'file')
```

#### auth.js - 认证工具

```javascript
import { setToken, getToken, setUserInfo, getUserInfo, isLoggedIn } from '@ninglawyer/shared'

// 设置 Token
setToken('your_token', 7 * 24 * 60 * 60 * 1000) // 7 天

// 获取 Token
const token = getToken()

// 检查是否已登录
if (isLoggedIn()) {
  // 已登录
}

// 设置用户信息
setUserInfo({ id: '1', name: '张三' })

// 获取用户信息
const userInfo = getUserInfo()
```

#### date.js - 日期工具

```javascript
import { formatDate, formatRelativeTime, getToday, getTomorrow } from '@ninglawyer/shared'

// 格式化日期
const formatted = formatDate(new Date(), 'YYYY-MM-DD HH:mm:ss')

// 相对时间
const relative = formatRelativeTime(new Date()) // "刚刚", "5分钟前", "2小时前"

// 获取今天
const today = getToday()
```

#### storage.js - 存储工具

```javascript
import { set, get, remove, clear, createNamespace } from '@ninglawyer/shared'

// 设置数据
set('key', { value: 'data' })

// 获取数据
const value = get('key', 'default_value')

// 删除数据
remove('key')

// 清空所有数据
clear()

// 创建命名空间
const userStorage = createNamespace('user')
userStorage.set('name', '张三')
const userName = userStorage.get('name')
```

### 技能类

#### contract-draft.js - 合同起草技能

```javascript
import { ContractDraftSkill } from '@ninglawyer/shared/skills/contract-draft.js'

const skill = new ContractDraftSkill()

// 起草合同
const result = await skill.draft({
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

// 获取模板
const template = await skill.getTemplate('labor')

// 导出合同
const url = await skill.export(contractId, 'pdf')
```

#### contract-review.js - 合同审查技能

```javascript
import { ContractReviewSkill } from '@ninglawyer/shared/skills/contract-review.js'

const skill = new ContractReviewSkill()

// 审查合同
const result = await skill.review({
  contractId: '123',
  content: '合同内容...'
})

// 快速检查
const quickResult = await skill.quickCheck({
  content: '合同内容...'
})
```

#### legal-consult.js - 法律咨询技能

```javascript
import { LegalConsultSkill } from '@ninglawyer/shared/skills/legal-consult.js'

const skill = new LegalConsultSkill()

// 法律咨询
const answer = await skill.consult({
  question: '我被拖欠工资了怎么办？',
  history: [...]
})
```

### MCP 服务

```javascript
import mcp from '@ninglawyer/shared/mcp/index.js'

// 语音合成
const audio = await mcp.textToSpeech('您好，我是宁律师')

// 知识库检索
const results = await mcp.searchKnowledge('劳动合同')

// 向量检索
const similar = await mcp.searchSimilar('合同条款', 10)
```

## 部署指南

### 后端部署

#### 本地部署

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
vim .env

# 启动服务
python3 main.py
```

#### Docker 部署

```bash
cd infrastructure/docker

# 构建镜像
docker build -t ninglawyer-backend .

# 运行容器
docker run -p 5001:5001 ninglawyer-backend

# 使用 docker-compose
docker-compose up -d
```

### 小程序部署

#### 上传小程序

1. 使用微信开发者工具打开小程序目录
2. 点击"上传"按钮
3. 填写版本号和项目备注
4. 等待上传完成

#### 提交审核

1. 登录微信公众平台
2. 进入"版本管理"
3. 选择上传的版本
4. 点击"提交审核"
5. 填写审核信息
6. 等待审核通过

#### 发布上线

1. 审核通过后，点击"发布"
2. 确认发布
3. 等待发布完成

## 常见问题

### Q1: 小程序中的引用路径需要更新吗？

A: 是的。需要将原来的相对路径改为使用共享包：

```javascript
// 旧代码
import { request } from '../../utils/request.js'

// 新代码
import { request } from '@ninglawyer/shared/utils/api.js'
```

### Q2: 如何更新共享包？

A:

```bash
# 1. 修改共享代码
vim packages/@ninglawyer/shared/utils/api.js

# 2. 更新版本
cd packages/@ninglawyer/shared
npm version patch

# 3. 在小程序中重新构建 npm
# 微信开发者工具 -> 工具 -> 构建 npm
```

### Q3: 每个小程序可以使用不同版本的共享包吗？

A: 可以。修改小程序的 `package.json`：

```json
{
  "dependencies": {
    "@ninglawyer/shared": "1.0.0"
  }
}
```

### Q4: 如何添加新的小程序？

A:

1. 在 `miniprograms/` 下创建新目录
2. 复制 `ninglawyer-main/package.json`
3. 修改 `app.json` 中的 `appid`
4. 使用微信开发者工具打开
5. 开发功能

### Q5: 共享代码会占用小程序体积吗？

A: 会，但影响很小。共享包体积约 50KB，对 2MB 限制影响可以忽略不计。

## 迁移待办事项

- [ ] 更新所有小程序中的引用路径
- [ ] 更新配置文件中的路径
- [ ] 更新部署脚本中的路径
- [ ] 测试后端服务启动
- [ ] 测试所有小程序功能
- [ ] 确认小程序审核和发布流程
- [ ] 清理旧目录（确认一切正常后）

## 联系支持

如有问题，请联系开发团队：
- 邮箱: support@ninglawyer.com
- 文档: https://docs.ninglawyer.com

## 更新日志

- 2025-01-30: 初始版本，完成 Monorepo 迁移
