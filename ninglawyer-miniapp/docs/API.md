# 宁律师小程序 - API接口文档

## 📋 目录

1. [概述](#概述)
2. [认证方式](#认证方式)
3. [通用响应格式](#通用响应格式)
4. [基础接口](#基础接口)
5. [主脑接口](#主脑接口)
6. [业务接口](#业务接口)
7. [错误码说明](#错误码说明)

---

## 概述

**Base URL**：`http://your-domain.com/api`

**协议**：HTTPS（微信小程序必须）

**Content-Type**：`application/json`

**字符编码**：UTF-8

---

## 认证方式

当前版本不需要API Token，后续版本可能会添加。

**请求头**：

```http
Content-Type: application/json
Accept: application/json
```

---

## 通用响应格式

### 成功响应

```json
{
  "success": true,
  "data": {
    // 具体数据
  },
  "message": "操作成功"
}
```

### 失败响应

```json
{
  "success": false,
  "error": "错误信息",
  "code": "ERROR_CODE"
}
```

---

## 基础接口

### 1. 健康检查

检查服务是否正常运行。

**接口**：`GET /health`

**请求示例**：

```http
GET /health HTTP/1.1
Host: your-domain.com
```

**响应示例**：

```json
{
  "status": "ok",
  "service": "ninglawyer-miniapp",
  "version": "1.0.0-alpha"
}
```

### 2. API根路径

获取API基本信息。

**接口**：`GET /`

**请求示例**：

```http
GET / HTTP/1.1
Host: your-domain.com
```

**响应示例**：

```json
{
  "service": "宁律师法律咨询小程序矩阵",
  "version": "1.0.0-alpha",
  "endpoints": {
    "consultation": "/api/consultation",
    "contract": "/api/contract",
    "risk": "/api/risk"
  }
}
```

### 3. 测试接口

测试API是否正常工作。

**接口**：`GET /api/test`

**请求示例**：

```http
GET /api/test HTTP/1.1
Host: your-domain.com
```

**响应示例**：

```json
{
  "message": "宁律师 API 测试成功",
  "status": "ok"
}
```

---

## 主脑接口

### 1. 主脑路由

通过主脑自动路由到对应的Bot。

**接口**：`POST /api/master/route`

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_input | string | 是 | 用户输入的内容 |
| user_id | string | 否 | 用户ID，默认为"default" |
| context | object | 否 | 上下文信息 |

**请求示例**：

```json
{
  "user_input": "帮我脱敏一下，我叫张三",
  "user_id": "user123",
  "context": {
    "source": "miniprogram"
  }
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "answer": "脱敏结果：*三",
    "bot_type": "desensitize"
  }
}
```

### 2. 列出所有Bot

获取所有可用的Bot信息。

**接口**：`GET /api/master/list-bots`

**请求示例**：

```http
GET /api/master/list-bots HTTP/1.1
Host: your-domain.com
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "desensitize": {
      "bot_id": "7368002369864167438",
      "name": "宁律师脱敏助手",
      "description": "自动识别并脱敏证据中的敏感信息"
    },
    "civil_consult": {
      "bot_id": "7368000000000000000",
      "name": "民事咨询",
      "description": "提供民事法律咨询服务"
    }
  }
}
```

### 3. 主脑测试接口

测试主脑接口是否正常工作。

**接口**：`GET /api/master/test`

**请求示例**：

```http
GET /api/master/test HTTP/1.1
Host: your-domain.com
```

**响应示例**：

```json
{
  "message": "宁律师主脑调度接口测试成功",
  "status": "ok",
  "available_apis": [
    "POST /route - 主脑路由",
    "POST /desensitize - 脱敏",
    "POST /consult - 法律咨询",
    "POST /draft-contract - 合同起草",
    "POST /review-contract - 合同审查",
    "GET /list-bots - 列出Bot",
    "POST /register-bot - 注册Bot",
    "GET /health - 健康检查",
    "GET /test - 测试接口"
  ]
}
```

---

## 业务接口

### 1. 脱敏接口

对证据数据进行脱敏处理。

**接口**：`POST /api/master/desensitize`

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 否 | 姓名 |
| id_card | string | 否 | 身份证号 |
| phone | string | 否 | 手机号 |
| address | string | 否 | 地址 |
| 其他敏感字段 | string | 否 | 其他需要脱敏的信息 |

**请求示例**：

```json
{
  "name": "张三",
  "id_card": "123456789012345678",
  "phone": "13812345678",
  "address": "北京市朝阳区xxx街道xxx号"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "name": "*三",
    "id_card": "123***********678",
    "phone": "138****5678",
    "address": "北京市朝阳区xxx****"
  }
}
```

**脱敏规则**：
- 姓名：保留第一个字，其余用*替换
- 身份证号：保留前3位和后2位
- 手机号：保留前3位和后4位
- 地址：保留省市区，详细地址脱敏

### 2. 法律咨询接口

提供法律咨询服务。

**接口**：`POST /api/master/consult`

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| question | string | 是 | 用户的问题 |
| domain | string | 否 | 法律领域（民事、婚姻、劳动等） |
| user_id | string | 否 | 用户ID |

**请求示例**：

```json
{
  "question": "朋友借钱不还，我该怎么办",
  "domain": "民事",
  "user_id": "user123"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "answer": "根据《民法典》相关规定，朋友借钱不还属于债务纠纷...",
    "domain": "民事",
    "citations": [
      "《民法典》第六百六十七条",
      "《民法典》第六百七十五条"
    ],
    "suggestions": [
      "收集证据：借条、转账记录、聊天记录等",
      "友好协商：先尝试通过沟通解决",
      "法律途径：起诉至法院要求还款"
    ]
  }
}
```

### 3. 合同起草接口

起草各类合同。

**接口**：`POST /api/master/draft-contract`

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| contract_type | string | 是 | 合同类型（借款合同、租赁合同等） |
| details | string | 否 | 合同详细信息 |

**请求示例**：

```json
{
  "contract_type": "借款合同",
  "details": "借款方：张三，出借方：李四，金额：10000元，期限：6个月，利率：年化5%"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "contract": "借款合同\n\n甲方（出借方）：李四\n乙方（借款方）：张三\n\n...",
    "contract_type": "借款合同",
    "tips": [
      "建议双方当面签署合同",
      "保留转账记录作为凭证",
      "可约定还款方式：等额本息/到期一次性还款"
    ]
  }
}
```

**支持的合同类型**：
- 借款合同
- 租赁合同
- 劳动合同
- 买卖合同
- 服务合同
- 其他合同

### 4. 合同审查接口

审查合同的风险点。

**接口**：`POST /api/master/review-contract`

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| contract_content | string | 是 | 合同内容 |

**请求示例**：

```json
{
  "contract_content": "借款合同\n\n甲方：张三\n乙方：李四\n\n甲方向乙方借款10000元，乙方承诺6个月后归还。"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "risks": [
      "合同中未约定利息，可能产生纠纷",
      "未约定违约责任，借款方违约时难以追责",
      "未约定还款方式，可能导致还款争议"
    ],
    "suggestions": [
      "建议添加利息条款，明确利率和计算方式",
      "建议添加违约条款，明确违约责任",
      "建议约定还款时间和方式，如等额本息或到期一次性还款"
    ],
    "score": 60
  }
}
```

**风险评分说明**：
- 90-100分：合同完善，风险低
- 70-89分：合同基本完善，有少量风险
- 50-69分：合同存在明显风险，建议修改
- 0-49分：合同风险很高，不建议签署

---

## 错误码说明

### HTTP状态码

| 状态码 | 说明 |
|-------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（暂未使用） |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 业务错误码

| 错误码 | 说明 |
|-------|------|
| MISSING_PARAM | 缺少必需参数 |
| INVALID_PARAM | 参数格式错误 |
| BOT_ERROR | Bot调用失败 |
| NETWORK_ERROR | 网络错误 |
| TIMEOUT_ERROR | 请求超时 |

### 错误响应示例

```json
{
  "success": false,
  "error": "缺少user_input参数",
  "code": "MISSING_PARAM"
}
```

```json
{
  "success": false,
  "error": "Bot调用失败：未找到对应的Bot",
  "code": "BOT_ERROR"
}
```

---

## 使用示例

### Python示例

```python
import requests
import json

# Base URL
BASE_URL = "http://your-domain.com/api"

# 脱敏示例
def desensitize_data():
    url = f"{BASE_URL}/master/desensitize"
    data = {
        "name": "张三",
        "id_card": "123456789012345678",
        "phone": "13812345678"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if result['success']:
        print("脱敏结果：", result['data'])
    else:
        print("脱敏失败：", result['error'])

# 法律咨询示例
def legal_consultation():
    url = f"{BASE_URL}/master/consult"
    data = {
        "question": "朋友借钱不还怎么办",
        "domain": "民事"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if result['success']:
        print("咨询结果：", result['data']['answer'])
    else:
        print("咨询失败：", result['error'])

# 合同起草示例
def draft_contract():
    url = f"{BASE_URL}/master/draft-contract"
    data = {
        "contract_type": "借款合同",
        "details": "借款方：张三，出借方：李四，金额：10000元"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if result['success']:
        print("合同内容：", result['data']['contract'])
    else:
        print("起草失败：", result['error'])

if __name__ == '__main__':
    desensitize_data()
    legal_consultation()
    draft_contract()
```

### JavaScript（小程序）示例

```javascript
// 封装API请求
const BASE_URL = 'https://your-domain.com/api';

function request(url, data) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: BASE_URL + url,
      method: 'POST',
      data: data,
      header: {
        'content-type': 'application/json'
      },
      success: (res) => {
        if (res.data.success) {
          resolve(res.data.data);
        } else {
          reject(res.data.error);
        }
      },
      fail: (err) => {
        reject(err);
      }
    });
  });
}

// 脱敏
function desensitize(name, idCard, phone) {
  return request('/master/desensitize', {
    name: name,
    id_card: idCard,
    phone: phone
  });
}

// 法律咨询
function consult(question, domain) {
  return request('/master/consult', {
    question: question,
    domain: domain
  });
}

// 合同起草
function draftContract(contractType, details) {
  return request('/master/draft-contract', {
    contract_type: contractType,
    details: details
  });
}

// 使用示例
async function main() {
  try {
    // 脱敏
    const desensitizeResult = await desensitize('张三', '123456789012345678', '13812345678');
    console.log('脱敏结果：', desensitizeResult);
    
    // 咨询
    const consultResult = await consult('朋友借钱不还怎么办', '民事');
    console.log('咨询结果：', consultResult);
    
    // 起草合同
    const contractResult = await draftContract('借款合同', '借款方：张三，出借方：李四，金额：10000元');
    console.log('合同内容：', contractResult);
    
  } catch (error) {
    console.error('请求失败：', error);
  }
}
```

---

## 更新日志

### v1.0.0 (2025-01-21)

- ✅ 初始版本发布
- ✅ 支持证据脱敏
- ✅ 支持法律咨询
- ✅ 支持合同起草
- ✅ 支持合同审查

---

**文档版本**：1.0.0
**更新日期**：2025-01-21
