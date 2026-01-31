# 宁律师项目 - 第一版后端API文档

## 📋 项目概述

本项目是宁律师智能法律服务系统的第一版后端API，采用Flask框架，全部智能体使用扣子官方API实现。

## 🎯 第一版特性

- ✅ 微信小程序登录认证
- ✅ 电话验证码登录
- ✅ 刑事法律咨询
- ✅ 民事法律咨询
- ✅ 合同起草
- ✅ 合同审查
- ✅ 扣子智能体集成
- ✅ Redis对话缓存
- ✅ PostgreSQL数据存储

## 🗂️ 项目结构

```
.
├── scripts/                      # 部署脚本
│   └── setup.sh                  # 部署前设置脚本
├── backend/
│   ├── config/
│   │   └── agents_config.json    # 扣子智能体配置
│   ├── docs/
│   │   ├── DEPLOYMENT_FIX.md     # 部署问题修复记录
│   │   ├── DEPLOYMENT_GUIDE.md   # 部署指南（重要！）
│   │   ├── FRONTEND_ANALYSIS.md  # 前端分析报告
│   │   └── DECISIONS.md          # 项目决策记录
│   ├── scripts/
│   │   ├── init_db.py            # 数据库初始化脚本
│   │   ├── test_api.py           # API测试脚本
│   │   └── test_voice.py         # 语音功能测试脚本
│   ├── src/
│   │   ├── models/
│   │   │   └── v1_models.py      # 数据库模型
│   │   ├── routes/
│   │   │   ├── auth.py           # 认证路由
│   │   │   ├── consultation.py   # 咨询路由
│   │   │   └── contract.py       # 合同路由
│   │   ├── services/
│   │   │   ├── auth.py           # 认证服务
│   │   │   ├── voice.py          # 语音服务
│   │   │   └── coze_agent.py     # 扣子智能体服务
│   │   ├── utils/
│   │   │   ├── database.py       # 数据库配置
│   │   │   └── redis_client.py   # Redis客户端
│   │   └── app.py                # Flask应用主文件
│   ├── logs/                     # 日志目录
│   ├── assets/                   # 资源目录
│   │   ├── images/
│   │   ├── knowledge/
│   │   └── templates/
│   ├── .env                      # 环境变量配置
│   ├── .env.example              # 环境变量示例
│   ├── requirements.txt          # Python依赖
│   ├── Dockerfile                # Docker配置
│   └── README.md                 # 本文档
├── miniprograms/                 # 小程序代码
│   ├── ninglawyer-main/          # 宁律师主小程序
│   ├── fangfengxian/             # 防风险小程序
│   └── legal-instructor/         # 法律教官小程序
└── README.md                     # 项目总览
```

## 🚀 快速开始

### 1. 环境准备

确保已安装Python 3.8+和以下依赖：

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制`.env.example`为`.env`并配置：

```bash
cp .env.example .env
```

编辑`.env`文件，配置以下关键参数：

```env
# 数据库配置
DATABASE_URL=postgresql://username:password@localhost:5432/legal_assistant

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# 扣子API配置
COZE_API_KEY=your_coze_api_key_here
COZE_API_BASE_URL=https://api.coze.cn

# 微信小程序配置
WECHAT_APP_ID=your_wechat_app_id_here
WECHAT_APP_SECRET=your_wechat_app_secret_here

# JWT配置
JWT_SECRET_KEY=your_jwt_secret_key_here_change_this_in_production
```

### 3. 配置扣子智能体

编辑`config/agents_config.json`，将`请替换为实际的Bot ID`替换为实际的扣子智能体Bot ID。

### 4. 初始化数据库

```bash
cd backend
python scripts/init_db.py
```

### 5. 运行部署脚本（推荐）

在部署前运行以下脚本以确保环境配置正确：

```bash
# 从项目根目录运行
bash scripts/setup.sh
```

该脚本会：
- 设置 PYTHONPATH 环境变量
- 检查和创建 .env 配置文件
- 检查数据库状态
- 创建必要的目录（logs、assets等）

### 6. 启动服务

```bash
cd backend/src
python app.py
```

服务将在 `http://localhost:5000` 启动。

### 6. 测试API

```bash
cd backend
python scripts/test_api.py
```

## 📡 API接口文档

### 1. 认证接口

#### 1.1 微信登录

**接口：** `POST /api/auth/wechat/login`

**请求体：**
```json
{
  "code": "微信登录凭证"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "token": "JWT token",
    "user": {
      "id": 1,
      "name": "用户昵称",
      "avatar": "头像URL",
      "role": "individual",
      "has_phone": false
    }
  }
}
```

#### 1.2 发送验证码

**接口：** `POST /api/auth/verification-code/send`

**请求体：**
```json
{
  "phone": "手机号",
  "code_type": "验证码类型（login/register/bind_phone）"
}
```

#### 1.3 绑定手机号

**接口：** `POST /api/auth/bind-phone`

**请求头：** `Authorization: Bearer <token>`

**请求体：**
```json
{
  "phone": "手机号",
  "code": "验证码"
}
```

#### 1.4 获取用户信息

**接口：** `GET /api/auth/user-info`

**请求头：** `Authorization: Bearer <token>`

### 2. 咨询接口

#### 2.1 刑事咨询

**接口：** `POST /api/consultation/criminal`

**请求头：** `Authorization: Bearer <token>`

**请求体：**
```json
{
  "query": "用户咨询问题",
  "session_id": "会话ID（可选）",
  "stream": false
}
```

**响应（非流式）：**
```json
{
  "success": true,
  "data": {
    "session_id": "会话ID",
    "answer": "智能体回复",
    "bot_id": "Bot ID",
    "bot_name": "Bot名称",
    "conversation_type": "criminal_consultation"
  }
}
```

#### 2.2 民事咨询

**接口：** `POST /api/consultation/civil`

参数同刑事咨询。

#### 2.3 获取对话历史

**接口：** `GET /api/consultation/history/<session_id>`

**请求头：** `Authorization: Bearer <token>`

#### 2.4 清除对话

**接口：** `POST /api/consultation/clear`

**请求头：** `Authorization: Bearer <token>`

### 3. 合同接口

#### 3.1 合同起草

**接口：** `POST /api/contract/draft`

**请求头：** `Authorization: Bearer <token>`

**请求体：**
```json
{
  "query": "合同需求描述",
  "contract_type": "合同类型（采购合同/服务合同/租赁合同/劳动合同/合作协议/保密协议/借款合同）",
  "session_id": "会话ID（可选）",
  "stream": false,
  "save_to_db": false
}
```

#### 3.2 合同审查

**接口：** `POST /api/contract/review`

**请求头：** `Authorization: Bearer <token>`

**请求体：**
```json
{
  "contract_text": "合同内容",
  "contract_type": "合同类型（可选）",
  "session_id": "会话ID（可选）",
  "stream": false
}
```

#### 3.3 获取合同列表

**接口：** `GET /api/contract/list`

**请求头：** `Authorization: Bearer <token>`

**查询参数：**
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）
- `contract_type`: 合同类型（可选）
- `status`: 状态（可选）

#### 3.4 获取合同详情

**接口：** `GET /api/contract/detail/<contract_id>`

**请求头：** `Authorization: Bearer <token>`

#### 3.5 更新合同

**接口：** `PUT /api/contract/update/<contract_id>`

**请求头：** `Authorization: Bearer <token>`

#### 3.6 删除合同

**接口：** `DELETE /api/contract/delete/<contract_id>`

**请求头：** `Authorization: Bearer <token>`

### 4. 健康检查

**接口：** `GET /health`

**响应：**
```json
{
  "status": "ok",
  "service": "legal-assistant-backend",
  "version": "1.0.0"
}
```

## 🔧 数据库表结构

### users（用户表）
- `id`: 用户ID
- `wechat_openid`: 微信openid
- `wechat_unionid`: 微信unionid
- `phone`: 手机号
- `name`: 姓名
- `avatar`: 头像URL
- `role`: 角色（individual/enterprise_member/admin）
- `status`: 状态

### enterprises（企业表）
- `id`: 企业ID
- `name`: 企业名称
- `unified_code`: 统一社会信用代码
- `business_license`: 营业执照URL
- `verified`: 是否已认证
- `contact_name`: 联系人姓名
- `contact_phone`: 联系电话

### user_enterprise_relations（用户-企业关系表）
- `id`: 关系ID
- `user_id`: 用户ID
- `enterprise_id`: 企业ID
- `role_in_enterprise`: 在企业中的角色
- `department`: 部门
- `position`: 职位

### contracts（合同表）
- `id`: 合同ID
- `user_id`: 用户ID
- `contract_type`: 合同类型
- `contract_title`: 合同标题
- `contract_text`: 合同内容
- `status`: 状态（draft/signed/archived）
- `party_a`: 甲方
- `party_b`: 乙方
- `contract_amount`: 合同金额

### user_feedback（用户反馈表）
- `id`: 反馈ID
- `user_id`: 用户ID
- `feedback_text`: 反馈内容
- `feedback_type`: 反馈类型
- `rating`: 评分

### conversations（会话表）
- `id`: 会话ID
- `user_id`: 用户ID
- `session_id`: 会话ID
- `conversation_type`: 会话类型
- `user_message`: 用户消息
- `bot_response`: 智能体回复
- `bot_id`: Bot ID
- `bot_name`: Bot名称

### verification_codes（验证码表）
- `id`: 验证码ID
- `phone`: 手机号
- `code`: 验证码
- `code_type`: 验证码类型
- `expires_at`: 过期时间
- `used`: 是否已使用

## 🔐 安全注意事项

1. **环境变量**：`.env`文件包含敏感信息，不要提交到版本控制
2. **Bot ID**：扣子智能体Bot ID需要保密
3. **JWT密钥**：生产环境必须使用强密钥
4. **API密钥**：扣子API Key需要保密

## 📝 注意事项

1. **Redis依赖**：Redis服务需要启动，否则验证码和对话缓存功能将不可用
2. **微信API**：微信登录需要真实的微信小程序App ID和Secret
3. **扣子API**：需要配置真实的扣子Bot ID和API Key
4. **流式输出**：流式输出使用SSE格式，前端需要相应处理

## 🐛 故障排除

### 1. Redis连接失败

检查Redis服务是否启动：

```bash
# 检查Redis服务状态
redis-cli ping

# 启动Redis服务
redis-server
```

### 2. 数据库连接失败

检查DATABASE_URL配置是否正确，数据库服务是否启动。

### 3. 微信登录失败

检查微信小程序App ID和Secret是否正确，code是否有效。

### 4. 扣子智能体调用失败

检查Bot ID和API Key是否正确，网络是否通畅。

## 📧 联系方式

如有问题，请联系开发团队。

## 🚀 部署相关

### 部署文档

详细的部署指南请参考：

- **[部署指南](docs/DEPLOYMENT_GUIDE.md)** - 完整的部署流程和配置说明
- **[部署问题修复记录](docs/DEPLOYMENT_FIX.md)** - 常见部署问题及解决方案

### 快速部署

```bash
# 1. 运行部署脚本
bash scripts/setup.sh

# 2. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env 文件

# 3. 安装依赖
cd backend
pip install -r requirements.txt

# 4. 初始化数据库
python scripts/init_db.py

# 5. 启动服务
python src/main.py
```

### Docker 部署

```bash
cd backend
docker build -t ninglawyer-backend:latest .
docker run -d -p 5000:5000 --name ninglawyer-backend ninglawyer-backend:latest
```

### 云平台部署

确保项目根目录存在 `scripts/setup.sh` 脚本（已包含），部署系统会自动运行该脚本进行环境初始化。

---

**版本：** v1.0.0
**最后更新：** 2026-01-31
