# 宁律师智能法律服务系统 - 架构设计文档

## 📋 项目概述

**项目名称**：宁律师智能法律服务系统
**版本**：v1.0
**架构模式**：单一宁律师 + 主脑调度技能
**最后更新**：2025-01-09

### 项目愿景

构建一个基于微信小程序的智能法律服务生态系统，通过统一的"宁律师"人设，为用户提供专业、温暖、可靠的法律服务。

---

## 🏗️ 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      微信小程序矩阵                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │主程序    │  │防风险    │  │法律教官  │  │理约      │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│  ┌──────────┐  ┌──────────┐                 ┌──────────┐   │
│  │怎么判    │  │码上签约  │                 │更多...   │   │
│  └────┬─────┘  └────┬─────┘                 └────┬─────┘   │
└───────┼────────────┼───────────────────────────┼──────────┘
        │            │                           │
        └────────────┼───────────────────────────┘
                     │
        ┌────────────▼───────────────────────────┐
        │          后端服务（Flask）              │
        │  ┌──────────────────────────────────┐  │
        │  │        主脑智能体（Master Brain）  │  │
        │  │    - 意图识别                      │  │
        │  │    - 技能调度                      │  │
        │  │    - 对话管理                      │  │
        │  └────────────┬─────────────────────┘  │
        │               │                         │
        │  ┌────────────▼─────────────────────┐  │
        │  │    技能模块（Skills）             │  │
        │  │  - 合同审查 (contract_review)    │  │
        │  │  - 合同起草 (contract_draft)     │  │
        │  │  - 民事咨询 (civil_consult)      │  │
        │  │  - 脱敏处理 (desensitize)        │  │
        │  │  - 案件分析 (case_analysis)      │  │
        │  │  - 法律文书起草 (document_draft) │  │
        │  │  - 证据整理 (evidence_organize)  │  │
        │  │  - 更多...                       │  │
        │  └──────────────────────────────────┘  │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │      宁律师配置（Ning Lawyer）    │  │
        │  │  - 统一人设                       │  │
        │  │  - 服务理念                       │  │
        │  │  - 专业领域                       │  │
        │  │  - 语音配置                       │  │
        │  └──────────────────────────────────┘  │
        └─────────────────────────────────────────┘
                     │
        ┌────────────▼───────────────────────────┐
        │           数据层                        │
        │  ┌────────────┐  ┌────────────┐       │
        │  │ PostgreSQL │  │   Redis    │       │
        │  │  用户数据   │  │  对话缓存   │       │
        │  │  必要数据   │  │  会话管理   │       │
        │  └────────────┘  └────────────┘       │
        └─────────────────────────────────────────┘
                     │
        ┌────────────▼───────────────────────────┐
        │           外部服务                      │
        │  ┌────────────┐  ┌────────────┐       │
        │  │ 豆包模型   │  │ 微信API    │       │
        │  │  LLM       │  │  登录/授权 │       │
        │  └────────────┘  └────────────┘       │
        │  ┌────────────┐  ┌────────────┐       │
        │  │ 语音模型   │  │ 短信服务   │       │
        │  │  ASR/TTS   │  │  验证码    │       │
        │  └────────────┘  └────────────┘       │
        └─────────────────────────────────────────┘
```

### 核心设计理念

#### 1. 单一宁律师人设

**设计目标**：
- 提供一致的用户体验
- 避免用户在多个律师之间切换的困惑
- 增强品牌认知度和用户粘性

**实现方式**：
- 统一的宁律师配置（`src/config/ning_lawyer.py`）
- 统一的系统提示词（`src/prompts/ning_lawyer.py`）
- 所有技能调用都体现宁律师的人设和语气

**人设特点**：
- **专业严谨**：基于现行法律法规提供准确的法律建议
- **温暖共情**：理解用户处境，以温和语气表达关怀
- **清晰易懂**：避免晦涩法言法语，用通俗语言解释法律概念
- **风险预警**：及时提示法律风险和注意事项
- **客观中立**：基于事实和法律分析，不偏不倚

#### 2. 主脑调度技能

**设计目标**：
- 灵活扩展技能，无需修改核心逻辑
- 保持架构的解耦和可维护性
- 支持技能的动态注册和发现

**实现方式**：
- 主脑智能体（`Master Brain`）负责意图识别和技能路由
- 技能注册表（`Skill Registry`）管理所有可用技能
- 每个技能独立封装，通过标准接口调用

**路由流程**：
```
用户输入 
  → 意图识别（主脑）
  → 技能路由（匹配到对应技能）
  → 技能执行（调用具体技能）
  → 结果封装（以宁律师人设返回）
```

---

## 📁 项目目录结构

```
backend/
├── config/                    # 配置目录
│   ├── agent_llm_config.json  # Agent配置（包含宁律师系统提示词）
│   └── bot_config.json        # 扣子Bot配置
│
├── docs/                      # 文档目录
│   ├── architecture.md        # 架构设计文档（本文件）
│   └── api.md                 # API文档
│
├── src/                       # 源代码目录
│   ├── agents/                # 智能体目录
│   │   ├── master_brain.py    # 主脑智能体（意图识别 + 技能调度）
│   │   └── ning_lawyer.py     # 宁律师智能体（统一人设）
│   │
│   ├── config/                # 配置模块
│   │   └── ning_lawyer.py     # 宁律师配置（人设、领域、技能）
│   │
│   ├── prompts/               # 提示词目录
│   │   ├── ning_lawyer.py     # 宁律师系统提示词（统一）
│   │   ├── skills/            # 技能提示词目录
│   │   │   ├── contract_review.py
│   │   │   ├── contract_draft.py
│   │   │   ├── civil_consult.py
│   │   │   ├── desensitize.py
│   │   │   └── ...
│   │   └── manager.py         # 提示词管理器
│   │
│   ├── skills/                # 技能模块
│   │   ├── base_skill.py      # 技能基类
│   │   ├── contract_review.py # 合同审查技能
│   │   ├── contract_draft.py  # 合同起草技能
│   │   ├── civil_consult.py   # 民事咨询技能
│   │   ├── desensitize.py     # 脱敏处理技能
│   │   └── ...
│   │
│   ├── utils/                 # 工具模块
│   │   ├── skill_registry.py  # 技能注册表
│   │   ├── voice_handler.py   # 语音处理工具
│   │   └── logger.py          # 日志工具
│   │
│   ├── storage/               # 存储模块
│   │   ├── database.py        # PostgreSQL数据库
│   │   ├── redis_client.py    # Redis客户端
│   │   └── memory.py          # 短期记忆管理
│   │
│   └── api/                   # API模块
│       ├── routes/            # 路由
│       │   ├── chat.py        # 聊天接口
│       │   ├── voice.py       # 语音接口
│       │   └── auth.py        # 认证接口
│       │
│       └── main.py            # Flask应用入口
│
├── tests/                     # 测试目录
│   ├── test_new_architecture.py  # 新架构测试脚本
│   └── test_skills.py         # 技能测试
│
├── assets/                    # 资源目录
│   ├── data/                  # 测试数据
│   └── prompts/               # 提示词模板
│
├── requirements.txt           # Python依赖
├── README.md                  # 项目说明
└── .env                       # 环境变量
```

---

## 🔧 核心模块说明

### 1. 主脑智能体（Master Brain）

**文件位置**：`src/agents/master_brain.py`

**职责**：
- 意图识别：理解用户输入，识别用户意图
- 技能路由：根据意图路由到对应的技能
- 对话管理：管理多轮对话的上下文

**核心方法**：
```python
def route(user_input: str, user_id: int = None, context: Dict = None) -> Dict:
    """路由请求到对应技能"""
    
def _identify_intent(user_input: str, context: Dict = None) -> Dict:
    """识别用户意图"""
    
def _execute_skill(skill_name: str, user_input: str, user_id: int, context: Dict) -> Dict:
    """执行技能"""
```

### 2. 宁律师配置（Ning Lawyer Config）

**文件位置**：`src/config/ning_lawyer.py`

**职责**：
- 定义宁律师的人设、特点、服务理念
- 配置支持的法律领域
- 配置支持的技能列表
- 配置语音参数（ASR/TTS）

**核心配置**：
```python
class NingLawyerConfig:
    name = "宁律师"
    personality = ["专业严谨", "温暖共情", "清晰易懂", "风险预警", "客观中立"]
    domains = ["民事", "刑事", "合同", "劳动", "公司", "婚姻", "知识产权", ...]
    skills = ["contract_review", "contract_draft", "civil_consult", ...]
    voice_config = {...}
```

### 3. 技能模块（Skills）

**基类**：`src/skills/base_skill.py`

**技能列表**：
- `contract_review`：合同审查
- `contract_draft`：合同起草
- `civil_consult`：民事法律咨询
- `desensitize`：文档脱敏
- `case_analysis`：案件分析
- `document_draft`：法律文书起草
- `evidence_organize`：证据整理
- ... 更多技能持续扩展

**技能接口**：
```python
class BaseSkill:
    def execute(self, input_data: Dict, context: Dict = None) -> Dict:
        """执行技能"""
        raise NotImplementedError
```

### 4. 技能注册表（Skill Registry）

**文件位置**：`src/utils/skill_registry.py`

**职责**：
- 管理所有可用技能
- 支持技能的动态注册
- 提供技能查找功能

**使用方式**：
```python
from src.utils.skill_registry import skill_registry

# 注册技能
skill_registry.register("contract_review", ContractReviewSkill())

# 获取技能
skill = skill_registry.get("contract_review")

# 执行技能
result = skill.execute(input_data, context)
```

### 5. 提示词管理（Prompt Manager）

**文件位置**：`src/prompts/manager.py`

**职责**：
- 管理所有系统提示词
- 支持提示词的动态加载
- 提供提示词模板渲染功能

**提示词结构**：
```
prompts/
├── ning_lawyer.py      # 宁律师统一系统提示词
└── skills/             # 各技能的提示词
    ├── contract_review.py
    ├── contract_draft.py
    └── ...
```

---

## 🔄 数据流设计

### 用户交互流程

```
1. 用户输入
   ↓
2. 主脑意图识别
   ├─ 关键词匹配
   └─ LLM意图识别
   ↓
3. 技能路由
   ├─ 匹配到对应技能
   └─ 传递上下文参数
   ↓
4. 技能执行
   ├─ 调用特定技能
   └─ 调用LLM处理
   ↓
5. 结果封装
   ├─ 以宁律师人设返回
   └─ 保存对话记录（Redis）
   ↓
6. 返回给用户
```

### 对话管理

**存储策略**：
- **对话记录**：Redis缓存（不存数据库）
- **必要数据**：PostgreSQL（用户信息、订单等）

**对话窗口**：
- 默认保留最近 20 轮对话（40 条消息）
- 使用滑动窗口机制，避免上下文过长

**会话管理**：
- 每次对话生成唯一会话ID
- 支持多轮对话的上下文传递
- 支持用户切换场景的会话隔离

---

## 🛡️ 安全与权限

### 权限系统

**三态权限模型**：
1. **个人用户**：基础功能
2. **企业成员（未认证）**：受限功能
3. **企业成员（已认证）**：完整功能

### 安全措施

1. **数据加密**：敏感信息加密存储
2. **身份验证**：微信登录 + 电话验证码
3. **访问控制**：基于角色的权限管理
4. **日志审计**：记录所有操作日志
5. **免责声明**：在每次法律建议中提醒用户

---

## 🚀 技术栈

### 后端

- **框架**：Flask
- **ORM**：SQLAlchemy
- **数据库**：PostgreSQL（必要数据） + Redis（对话缓存）
- **AI模型**：豆包大模型（LLM、语音）
- **日志**：loguru
- **配置管理**：python-dotenv

### 前端

- **平台**：微信小程序
- **语言**：原生 JavaScript/WXML/WXSS

### 集成服务

- **扣子智能体API**：第一版全部使用扣子官方智能体
- **豆包语音大模型**：ASR（语音识别）+ TTS（语音合成）
- **微信API**：登录、授权、消息推送
- **短信服务**：验证码发送

---

## 📊 扩展性设计

### 添加新技能

**步骤**：
1. 在 `src/skills/` 创建新的技能类
2. 在 `src/prompts/skills/` 创建对应的提示词
3. 在技能注册表中注册新技能
4. 在主脑提示词中添加新技能的描述

**示例**：
```python
# 1. 创建技能
class NewSkill(BaseSkill):
    def execute(self, input_data: Dict, context: Dict = None) -> Dict:
        # 实现逻辑
        pass

# 2. 注册技能
skill_registry.register("new_skill", NewSkill())
```

### 添加新领域

**步骤**：
1. 在 `src/config/ning_lawyer.py` 中添加新领域
2. 更新宁律师系统提示词，包含新领域的内容
3. 创建对应领域的技能（如果需要）

---

## 🧪 测试策略

### 测试类型

1. **单元测试**：测试各个技能模块
2. **集成测试**：测试主脑与技能的集成
3. **端到端测试**：测试完整用户流程

### 测试脚本

**新架构测试**：`tests/test_new_architecture.py`
- 测试宁律师配置加载
- 测试主脑路由逻辑
- 测试提示词一致性
- 测试配置文件格式
- 测试旧文件清理

### 运行测试

```bash
# 运行所有测试
python backend/tests/test_new_architecture.py

# 运行特定测试
pytest backend/tests/test_skills.py
```

---

## 📝 开发规范

### 代码规范

- **Python**：遵循 PEP 8 规范
- **命名**：使用有意义的变量名和函数名
- **注释**：关键逻辑必须添加注释
- **日志**：使用 loguru 记录日志

### Git规范

- **分支策略**：
  - `main`：主分支
  - `develop`：开发分支
  - `feature/*`：功能分支
  - `fix/*`：修复分支

- **提交信息**：
  - `feat: 新功能`
  - `fix: 修复bug`
  - `docs: 文档更新`
  - `refactor: 重构`
  - `test: 测试`

---

## 🎯 第一版MVP目标

### 功能范围

**核心功能**：
- ✅ 统一宁律师人设
- ✅ 主脑意图识别
- ✅ 合同审查技能
- ✅ 合同起草技能
- ✅ 民事法律咨询
- ✅ 脱敏处理
- ✅ 微信登录
- ✅ 电话验证码验证
- ✅ 语音咨询（ASR/TTS）

**优先级**：
1. **成本**：优先级最高，使用扣子官方API降低开发成本
2. **体验**：确保用户交互流畅自然
3. **效果**：第一版优先保证核心功能可用

### 责任分工

- **用户**：负责主脑、小程序前后端
- **AI**：负责后端全部问题

---

## 🔮 未来规划

### 短期目标（3个月）

- [ ] 扩展更多法律领域技能
- [ ] 优化意图识别准确率
- [ ] 增强对话上下文理解
- [ ] 支持更多文档格式

### 中期目标（6个月）

- [ ] 企业版功能（团队协作）
- [ ] 法律知识库建设
- [ ] 案例库建设
- [ ] 多语言支持

### 长期目标（1年）

- [ ] AI驱动的法律分析
- [ ] 智能合同生成
- [ ] 法律风险预测
- [ ] 多端支持（Web、App）

---

## 📞 联系方式

**项目负责人**：[待补充]
**技术负责人**：[待补充]
**文档更新**：2025-01-09

---

## 📄 变更记录

| 版本 | 日期 | 变更内容 | 负责人 |
|------|------|----------|--------|
| v1.0 | 2025-01-09 | 架构调整：从"多律师"模式重构为"单一宁律师 + 主脑调度"模式 | AI |

---

## 附录

### A. 环境变量配置

```env
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost/ning_lawyer
REDIS_URL=redis://localhost:6379/0

# 扣子配置
COZE_API_KEY=your_coze_api_key
COZE_BOT_ID=your_coze_bot_id

# 微信配置
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret

# 短信服务配置
SMS_ACCESS_KEY=your_sms_access_key
SMS_SECRET_KEY=your_sms_secret_key

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=logs
```

### B. 数据库表结构

**用户表（users）**：
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    wechat_openid VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    nickname VARCHAR(100),
    avatar_url VARCHAR(500),
    permission_level INTEGER DEFAULT 0,  -- 0:个人, 1:企业未认证, 2:企业已认证
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**企业表（companies）**：
```sql
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    license VARCHAR(100),
    status INTEGER DEFAULT 0,  -- 0:未认证, 1:已认证
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### C. API端点

**聊天接口**：
```
POST /api/chat
请求体：
{
  "message": "用户消息",
  "user_id": 1,
  "session_id": "uuid"
}

响应：
{
  "success": true,
  "data": {
    "reply": "宁律师的回复",
    "skill_used": "contract_review",
    "confidence": 0.95
  }
}
```

**语音接口**：
```
POST /api/voice/asr
请求体：
{
  "audio_file": "base64编码的音频"
}

响应：
{
  "success": true,
  "data": {
    "text": "识别的文本"
  }
}

POST /api/voice/tts
请求体：
{
  "text": "要转换为语音的文本"
}

响应：
{
  "success": true,
  "data": {
    "audio_url": "音频文件URL"
  }
}
```

---

**文档结束**
