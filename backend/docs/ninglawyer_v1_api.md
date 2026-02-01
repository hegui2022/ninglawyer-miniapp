# 宁律师 V1 API 使用文档

## 概述

宁律师 V1 API 提供简单、直接的宁律师咨询接口，让用户能够快速与宁律师进行交互。

**服务地址**：`http://localhost:5000`

**API 版本**：V1

---

## API 接口

### 1. 获取宁律师信息

**接口地址**：`GET /info`

**请求参数**：无

**响应示例**：

```json
{
  "code": 200,
  "data": {
    "name": "宁律师",
    "description": "你的智能法律助手，提供专业、高效的法律咨询服务",
    "version": "1.0",
    "bot_id": "7478766030654679080",
    "personalities": [
      {
        "id": "warm",
        "name": "温暖陪伴型",
        "description": "适合焦虑当事人，温柔体贴，提供情感支持"
      },
      {
        "id": "professional",
        "name": "专业严谨型",
        "description": "适合理性用户，专业严谨，逻辑清晰"
      },
      {
        "id": "business",
        "name": "企业商务型",
        "description": "适合企业用户，高效务实，注重商业价值"
      }
    ],
    "features": [
      "智能法律咨询",
      "人设动态选择",
      "意图识别",
      "多轮对话",
      "案源识别"
    ]
  },
  "message": "操作成功",
  "success": true
}
```

---

### 2. 聊天接口

**接口地址**：`POST /chat`

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 用户输入的问题 |
| user_id | string | 是 | 用户ID |
| session_id | string | 否 | 会话ID（可选，用于多轮对话） |
| user_type | string | 否 | 用户类型：individual（个人）或corporate（企业），默认individual |
| stream | boolean | 否 | 是否流式输出，默认false |

**请求示例**：

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "你好，我想咨询一下法律问题",
    "user_id": "test_user_1",
    "user_type": "individual"
  }'
```

**响应示例**：

```json
{
  "code": 200,
  "data": {
    "session_id": "temp_test_user_1_2629",
    "answer": "您好！我是宁律师，很高兴为您服务😊\n\n关于您提到的...",
    "bot_id": "7478766030654679080",
    "bot_name": "宁律师",
    "personality": {
      "id": "warm_personal",
      "name": "温暖陪伴型",
      "description": "婚姻家事、情感纠纷"
    },
    "intent": "general_consultation",
    "intent_desc": "普通法律咨询",
    "conversation_id": "mock_conv_6078536758646382629"
  },
  "message": "操作成功",
  "success": true
}
```

**响应字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| session_id | string | 会话ID |
| answer | string | 宁律师的回复内容 |
| bot_id | string | Bot ID |
| bot_name | string | Bot名称 |
| personality | object | 使用的人设信息 |
| personality.id | string | 人设ID |
| personality.name | string | 人设名称 |
| personality.description | string | 人设描述 |
| intent | string | 识别的意图ID |
| intent_desc | string | 意图描述 |
| conversation_id | string | 对话ID |

---

### 3. 获取人设列表

**接口地址**：`GET /personalities`

**请求参数**：无

**响应示例**：

```json
{
  "code": 200,
  "data": {
    "warm_personal": {
      "id": "warm_personal",
      "name": "温暖陪伴型",
      "target_user": "个人用户",
      "target_scenario": "婚姻家事、情感纠纷",
      "tone": "温柔、有同理心、会倾听、会共情"
    },
    "professional_personal": {
      "id": "professional_personal",
      "name": "专业严谨型",
      "target_user": "个人用户",
      "target_scenario": "商事场景",
      "tone": "专业严谨，逻辑清晰"
    },
    "business_corporate": {
      "id": "business_corporate",
      "name": "企业商务型",
      "target_user": "企业用户",
      "target_scenario": "企业商事、企业合规",
      "tone": "高效务实，注重商业价值"
    }
  },
  "message": "操作成功",
  "success": true
}
```

---

## 功能说明

### 1. 人设动态选择

宁律师会根据用户类型和场景自动选择合适的人设：

**用户类型**：
- `individual`（个人用户）
- `corporate`（企业用户）

**场景类型**：
- `family_law`（婚姻家事）
- `commercial`（商事场景）
- `compliance`（合规场景）
- `general`（通用场景）

**人设映射**：

| 用户类型 | 场景 | 人设 |
|---------|------|------|
| individual | family_law | 温暖陪伴型 |
| individual | commercial | 专业严谨型 |
| individual | compliance | 专业严谨型 |
| individual | general | 温暖陪伴型 |
| corporate | family_law | 专业严谨型 |
| corporate | commercial | 企业商务型 |
| corporate | compliance | 企业商务型 |
| corporate | general | 企业商务型 |

---

### 2. 意图识别

宁律师会根据用户输入自动识别意图，并导流到对应的小程序：

| 意图ID | 意图描述 | 触发关键词 |
|-------|---------|-----------|
| contract_signing | 合同签署 | 签合同、签署、签约、在线签署、电子签名 |
| contract_management | 合同管理 | 合同管理、履行、违约、催款、理约 |
| judgment_query | 裁判观点查询 | 怎么判、裁判、判决、判例、胜诉率、类案 |
| lawyer_matching | 找律师 | 找律师、法律教官、委托律师、律师服务 |
| compliance_risk | 合规风险 | 合规、风险防控、防风险、企业合规 |
| general_consultation | 普通法律咨询 | 咨询、法律问题、问律师 |

---

### 3. 测试用例

#### 测试用例1：普通法律咨询

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "你好，我想咨询一下法律问题",
    "user_id": "test_user_1",
    "user_type": "individual"
  }'
```

**预期结果**：
- 人设：温暖陪伴型
- 意图：普通法律咨询

---

#### 测试用例2：婚姻家事咨询

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "我和老公感情破裂，想离婚，孩子抚养权怎么判？",
    "user_id": "test_user_2",
    "user_type": "individual"
  }'
```

**预期结果**：
- 人设：温暖陪伴型
- 意图：裁判观点查询
- 回复风格：温暖、体贴、有同理心

---

#### 测试用例3：合同签署咨询

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "我需要在线签署一份租房合同，该怎么操作？",
    "user_id": "test_user_3",
    "user_type": "individual"
  }'
```

**预期结果**：
- 人设：专业严谨型
- 意图：合同签署

---

#### 测试用例4：企业用户咨询

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "我们公司需要做劳动合规，应该注意哪些方面？",
    "user_id": "test_company_1",
    "user_type": "corporate"
  }'
```

**预期结果**：
- 人设：企业商务型
- 意图：合规风险

---

## 注意事项

1. **当前使用模拟数据**：宁律师目前使用模拟数据生成回复，快速展示功能。待扣子API配置好后，将切换到真实调用。

2. **环境变量配置**：需要配置以下环境变量（在`.env`文件中）：
   - `COZE_WORKLOAD_IDENTITY_API_KEY`：扣子API Key
   - `NINGLAWYER_BOT_ID`：宁律师Bot ID

3. **服务端口**：默认端口为5000，可在`.env`文件中修改`API_PORT`配置。

4. **人设实现**：当前仅实现了"温暖陪伴型"人设，其他人设（专业严谨型、企业商务型）待后续补充。

---

## 下一步计划

1. ✅ 完成人设动态选择功能
2. ✅ 完成意图识别功能
3. ✅ 完成宁律师咨询API
4. ⏳ 配置扣子API，切换到真实调用
5. ⏳ 实现专业严谨型和企业商务型人设
6. ⏳ 实现多轮对话功能
7. ⏳ 实现案源识别功能

---

## 联系方式

如有问题，请联系开发团队。

---

*文档版本：V1.0*
*更新时间：2026-02-01*
