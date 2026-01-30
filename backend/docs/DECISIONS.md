# 宁律师项目决策记录

**文档版本：** v1.3（第一版决策完整版）
**最后更新：** 2025-01-30
**目的：** 记录所有沟通决策，避免遗忘

---

## 🚀 第一版策略（完整版）

### 核心原则

1. ✅ **尽量少功能** - MVP（最小可行性产品）
2. ✅ **全部智能体用扣子API实现** - 节省开发时间
3. ✅ **优先级：成本 > 体验 > 效果**
4. ✅ **责任分工：**
   - 用户负责：主脑、小程序前后端、后台PC端管理功能
   - AI负责：后端全部问题（API、数据库、扣子集成等）

---

## 🏗️ 第一版架构（简化版）

```
用户请求（微信小程序 / PC管理端）
  ↓
前端（用户负责）
  ├─ 微信小程序（用户负责）
  ├─ PC管理端（用户负责）
  └─ Master Brain（用户负责）
     ├─ 意图识别
     ├─ 权限检查
     └─ 路由到对应智能体
  ↓
后端API（AI负责）
  ├─ /api/consultation/*  咨询接口
  ├─ /api/contract/*      合同接口
  ├─ /api/compliance/*    合规接口
  ├─ /api/risk/*          风险接口
  ├─ /api/auth/*          认证接口
  ├─ /api/user/*          用户接口
  └─ /api/admin/*         管理接口
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
  ├─ 扣子提供的其他服务
  ├─ Redis（缓存对话记录）
  └─ PostgreSQL（存储必要数据）
```

---

## 📋 第一版功能清单

### 宁律师家族小程序

| 功能 | 智能体 | 实现 | 优先级 |
|-----|-------|------|-------|
| 用户登录 | - | 微信登录 + 电话验证码 | P0 |
| 刑事咨询 | 刑事宁律师 | 扣子智能体API | P0 |
| 民事咨询 | 民事宁律师 | 扣子智能体API | P0 |
| 劳动咨询 | 劳动宁律师 | 扣子智能体API | P1 |
| 合同起草 | 合同起草智能体 | 扣子智能体API | P0 |
| 合同审查 | 合同审查智能体 | 扣子智能体API | P1 |

### 防风险小程序

| 功能 | 智能体 | 实现 | 优先级 |
|-----|-------|------|-------|
| 用户登录 | - | 微信登录 + 电话验证码 | P0 |
| 企业认证 | - | 企业实名认证 | P0 |
| 企业合规检查 | 企业合规智能体 | 扣子智能体API | P0 |
| 风险评估 | 风险评估智能体 | 扣子智能体API | P1 |
| 合同起草 | 合同起草智能体 | 扣子智能体API（共享） | P0 |

### PC管理端

| 功能 | 实现 | 优先级 |
|-----|------|-------|
| 管理员登录 | - | P0 |
| 用户管理 | - | P1 |
| 对话记录查看 | - | P1 |
| 数据统计 | - | P2 |

---

## 🔧 AI负责的后端工作

### 1. API接口开发

```python
# 认证接口
POST /api/auth/wechat          # 微信登录
POST /api/auth/sms/send        # 发送验证码
POST /api/auth/sms/verify      # 验证码登录
POST /api/auth/logout          # 登出

# 咨询接口
POST /api/consultation/criminal    # 刑事咨询
POST /api/consultation/civil       # 民事咨询
POST /api/consultation/labor       # 劳动咨询

# 合同接口
POST /api/contract/draft           # 合同起草
POST /api/contract/review          # 合同审查
POST /api/contract/upload          # 上传合同
POST /api/contract/save            # 保存合同（数据库）

# 合规接口
POST /api/compliance/check         # 企业合规检查

# 风险接口
POST /api/risk/assess              # 风险评估

# 用户接口
GET  /api/user/profile             # 获取用户信息
POST /api/user/profile/update      # 更新用户信息
POST /api/user/enterprise/certify  # 企业认证

# 管理接口
GET  /api/admin/users              # 用户列表
GET  /api/admin/conversations      # 对话记录
GET  /api/admin/statistics         # 数据统计
```

### 2. 扣子智能体API调用

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

### 4. 对话记录缓存

```python
import redis

def save_conversation(user_id, message, response):
    """保存对话记录到缓存"""
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    # 使用 Redis List 存储对话
    conversation_key = f"conversation:{user_id}"
    redis_client.rpush(conversation_key, json.dumps({
        'message': message,
        'response': response,
        'timestamp': time.time()
    }))

    # 设置过期时间（7天）
    redis_client.expire(conversation_key, 7 * 24 * 60 * 60)

def get_conversation(user_id):
    """获取对话记录"""
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    conversation_key = f"conversation:{user_id}"

    messages = redis_client.lrange(conversation_key, 0, -1)
    return [json.loads(msg) for msg in messages]
```

### 5. Bot ID配置

```python
# config/agents_config.json
{
    "agents": {
        "criminal_lawyer": {
            "bot_id": "7382xxxx",
            "name": "刑事宁律师",
            "allowed_apps": ["ninglawyer"],
            "allowed_users": ["individual", "enterprise_member"]
        },
        "civil_lawyer": {
            "bot_id": "7383xxxx",
            "name": "民事宁律师",
            "allowed_apps": ["ninglawyer"],
            "allowed_users": ["individual", "enterprise_member"]
        },
        "contract_draft": {
            "bot_id": "7384xxxx",
            "name": "合同起草智能体",
            "allowed_apps": ["ninglawyer", "fangfengxian", "contract"],
            "allowed_users": ["individual", "enterprise_member"]
        },
        "compliance_check": {
            "bot_id": "7385xxxx",
            "name": "企业合规智能体",
            "allowed_apps": ["fangfengxian"],
            "allowed_users": ["enterprise_member"]
        }
    }
}
```

### 6. 数据库表

```sql
-- 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    wechat_openid VARCHAR(100) UNIQUE,
    phone VARCHAR(20) UNIQUE,
    name VARCHAR(50),
    role VARCHAR(20) DEFAULT 'individual',  -- individual | enterprise_member
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 企业表
CREATE TABLE enterprises (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    unified_code VARCHAR(50),  -- 统一社会信用代码
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户-企业关系表
CREATE TABLE user_enterprise_relations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    enterprise_id INTEGER REFERENCES enterprises(id),
    role_in_enterprise VARCHAR(50),  -- 法务 | 老总 | 负责人 | 员工
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 合同记录表
CREATE TABLE contracts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    contract_type VARCHAR(50),
    contract_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户反馈表
CREATE TABLE user_feedback (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    feedback_text TEXT,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

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

### 问题4：Bot ID配置

✅ **写在配置文件（.env或config.json）**
✅ 只有这个安全

### 问题5：对话记录存储

✅ **用缓存解决（Redis）**
✅ 不存数据库
✅ 除了必要需要上传的数据，才存数据库

### 问题6：用户认证

✅ **需要用户登录认证**
✅ **采用微信、电话验证码方式**
✅ **原因：需要收集用户信息，方便迭代用户反馈**
✅ **需要开发后台PC端的管理功能**

---

## 📊 第一版技术栈

### 后端（AI负责）

| 技术 | 用途 |
|-----|------|
| Flask | Web框架 |
| SQLAlchemy | 数据库ORM |
| PostgreSQL | 数据库（存储必要数据） |
| Redis | 缓存（对话记录） |
| 扣子智能体API | 智能体调用 |
| 扣子知识库API | 知识库检索 |
| 扣子大模型API | 大模型调用 |

### 前端（用户负责）

| 技术 | 用途 |
|-----|------|
| 微信小程序原生框架 | 小程序前端 |
| Master Brain（用户实现） | 主脑路由 |
| PC管理端（用户实现） | 后台管理功能 |

---

## 🎯 第一版开发优先级

### P0（必须有）

1. ✅ 后端API接口
2. ✅ 扣子智能体API调用
3. ✅ 权限检查
4. ✅ 数据库表设计
5. ✅ 用户认证（微信 + 电话验证码）
6. ✅ 对话记录缓存（Redis）
7. ✅ 刑事咨询、民事咨询、合同起草

### P1（重要）

8. ⚠️ 劳动咨询
9. ⚠️ 合同审查
10. ⚠️ 企业合规检查
11. ⚠️ 企业认证
12. ⚠️ PC管理端基本功能

### P2（可选）

13. ❌ 风险评估
14. ❌ PC管理端高级功能

---

## ⏭️ 待确认的问题（可能没有了）

| 问题编号 | 问题 | 状态 |
|---------|------|------|
| ✅ 问题1 | 主脑选择和用户权限系统 | 已完成 |
| ✅ 问题2 | 扣子API调用范围 | 已完成 |
| ✅ 问题3 | 开发框架和技术栈 | 已完成 |
| ✅ 问题4 | Bot ID配置 | 已完成 |
| ✅ 问题5 | 对话记录存储 | 已完成 |
| ✅ 问题6 | 用户认证方式 | 已完成 |

---

## ✅ 第一版决策完成！

所有关键问题都已明确，可以开始实施了！

---

**下一步：开始实施第一版后端开发**
