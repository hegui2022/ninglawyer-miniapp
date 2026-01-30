# 宁律师项目决策记录

**文档版本：** v1.2（第一版决策）
**最后更新：** 2025-01-30
**目的：** 记录所有沟通决策，避免遗忘

---

## 🚀 第一版策略（重要！）

### 核心原则

1. ✅ **尽量少功能** - MVP（最小可行性产品）
2. ✅ **全部智能体用扣子API实现** - 节省开发时间
3. ✅ **优先级：成本 > 体验 > 效果**
4. ✅ **责任分工：**
   - 用户负责：主脑、小程序前后端
   - AI负责：后端全部问题

---

## 🏗️ 第一版架构（简化版）

```
用户请求（微信小程序）
  ↓
小程序前端（用户负责）
  ↓
Master Brain（用户负责）
  ├─ 意图识别
  ├─ 权限检查
  └─ 路由到对应智能体
  ↓
后端API（AI负责）
  ├─ /api/consultation/*  咨询接口
  ├─ /api/contract/*      合同接口
  ├─ /api/compliance/*    合规接口
  └─ /api/risk/*          风险接口
  ↓
扣子智能体API（全部智能体都用这个）
  ├─ 刑事宁律师
  ├─ 民事宁律师
  ├─ 劳动宁律师
  ├─ 合同起草智能体
  ├─ 合同审查智能体
  ├─ 企业合规智能体
  └─ 风险评估智能体
  ↓
底层服务
  ├─ 扣子知识库API（必须使用）
  ├─ 扣子大模型API（必须使用）
  └─ 扣子提供的其他服务
```

---

## 📋 第一版功能清单

### 宁律师家族小程序

| 功能 | 智能体 | 实现 | 优先级 |
|-----|-------|------|-------|
| 刑事咨询 | 刑事宁律师 | 扣子智能体API | P0 |
| 民事咨询 | 民事宁律师 | 扣子智能体API | P0 |
| 劳动咨询 | 劳动宁律师 | 扣子智能体API | P1 |
| 合同起草 | 合同起草智能体 | 扣子智能体API | P0 |
| 合同审查 | 合同审查智能体 | 扣子智能体API | P1 |

### 防风险小程序

| 功能 | 智能体 | 实现 | 优先级 |
|-----|-------|------|-------|
| 企业合规检查 | 企业合规智能体 | 扣子智能体API | P0 |
| 风险评估 | 风险评估智能体 | 扣子智能体API | P1 |
| 合同起草 | 合同起草智能体 | 扣子智能体API（共享） | P0 |

---

## 🔧 AI负责的后端工作

### 1. API接口开发

```python
# 咨询接口
POST /api/consultation/criminal    # 刑事咨询
POST /api/consultation/civil       # 民事咨询
POST /api/consultation/labor       # 劳动咨询

# 合同接口
POST /api/contract/draft           # 合同起草
POST /api/contract/review          # 合同审查

# 合规接口
POST /api/compliance/check         # 企业合规检查

# 风险接口
POST /api/risk/assess              # 风险评估
```

### 2. 调用扣子智能体API

```python
from src.services.coze_agent_service import CozeAgentService

def call_coze_bot(bot_id, message, user_id):
    service = CozeAgentService(access_token="...")
    result = service.chat(
        bot_id=bot_id,
        message=message,
        user_id=user_id
    )
    return result
```

### 3. 权限检查

```python
def check_permission(user_id, app_type, skill_name):
    # 检查用户身份
    user = get_user(user_id)

    # 检查小程序类型
    if app_type not in skill.allowed_apps:
        return False

    # 检查用户权限
    if user.role not in skill.allowed_users:
        return False

    return True
```

### 4. 数据库表

- `users` - 用户表
- `enterprises` - 企业表
- `user_enterprise_relations` - 用户企业关系表
- `conversations` - 对话记录表
- `contracts` - 合同记录表

---

## ✅ 已确认的决策

### 问题1：主脑选择和用户权限系统

✅ 使用 `master_brain.py`（用户负责）
✅ 三态权限系统（个人 / 企业成员（未认证） / 企业成员（已认证））

### 问题2：扣子API调用范围

✅ 知识库API：必须使用
✅ 大模型API：使用扣子的（第一版不调用其他模型）
⚠️ 智能体API：全部使用（第一版策略）
⚠️ 技能API：按需使用（第一版优先用扣子）
⚠️ 工作流API：按需使用（第一版优先用扣子）

### 问题3：开发框架和技术栈

✅ 第一版：全部智能体用扣子API
✅ 第二版：考虑用LangGraph（现在不考虑）
✅ 开发原则：成本 > 体验 > 效果

---

## ⏸️ 暂不需要考虑的问题

以下问题第二版再考虑：

- ❌ LangChain自开发智能体
- ❌ LangGraph工作流
- ❌ MCP服务
- ❌ 其他大模型（DeepSeek、智谱、腾讯）
- ❌ 数据适配器（第一版直接用扣子返回的数据）

---

## 📊 第一版技术栈

### 后端（AI负责）

| 技术 | 用途 |
|-----|------|
| Flask | Web框架 |
| SQLAlchemy | 数据库ORM |
| PostgreSQL | 数据库 |
| 扣子智能体API | 智能体调用 |
| 扣子知识库API | 知识库检索 |
| 扣子大模型API | 大模型调用 |

### 前端（用户负责）

| 技术 | 用途 |
|-----|------|
| 微信小程序原生框架 | 小程序前端 |
| Master Brain（用户实现） | 主脑路由 |

---

## 🎯 第一版开发优先级

### P0（必须有）

1. ✅ 后端API接口
2. ✅ 扣子智能体API调用
3. ✅ 权限检查
4. ✅ 数据库表设计
5. ✅ 刑事咨询、民事咨询、合同起草

### P1（重要）

6. ⚠️ 劳动咨询
7. ⚠️ 合同审查
8. ⚠️ 企业合规检查

### P2（可选）

9. ❌ 风险评估

---

## ⏭️ 待确认的问题

虽然决定第一版全部用扣子API，但还有一些细节需要确认：

| 问题编号 | 问题 | 状态 |
|---------|------|------|
| ✅ 问题1-3 | 主脑、用户权限、扣子API | 已完成 |
| ❓ 问题4 | 扣子智能体的Bot ID如何获取和配置 | 等待回答 |
| ❓ 问题5 | 第一版是否需要数据库存储对话记录 | 等待回答 |
| ❓ 问题6 | 第一版是否需要用户认证（登录） | 等待回答 |

---

**下一问题：问题4 - 扣子智能体的Bot ID配置**
