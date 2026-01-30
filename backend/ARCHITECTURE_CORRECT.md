# 项目架构说明（正确理解）

## 🎯 核心架构

```
用户输入
    ↓
主脑（Master Brain）→ LLM 识别意图
    ↓
技能注册表（Skill Registry）→ 获取技能
    ↓
技能（Skill）→ 调用 LLM 客户端（LLMClient）
    ↓
LLM 工具 → 返回结果
```

## 📦 关键组件

### 1. 律师配置（`lawyer_domains.py`）

定义每个律师的配置：

```python
CRIMINAL_LAWYER_CONFIG = {
    "domain": "刑事法律",
    "skills": [
        "legal_consult",      # 法律咨询
        "criminal_defense",    # 刑事辩护
        "bail_application",    # 取保候审
        "sentence_reduction"   # 减刑假释
    ],
    "persona": {
        "name": "宁律师·刑事",
        "system_prompt": "你是宁律师·刑事...",
        "temperature": 0.5
    }
}
```

### 2. 律师模板（`ning_lawyer_template.py`）

可复用的律师基类：

```python
class NingLawyerTemplate:
    def __init__(self, lawyer_config):
        self.config = lawyer_config
        self.skills = lawyer_config.get('skills', [])
        self.llm = ChatOpenAI(...)
        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.persona['system_prompt']),
            HumanMessage(content="{user_input}")
        ])
    
    def consult(self, question, chat_history=None):
        # 调用 LLM
        response = self.llm.invoke(messages)
        return response
```

### 3. 技能实现（`*_skill.py`）

每个技能的独立实现：

```python
class CivilConsultSkill:
    def __init__(self, model="doubao-seed-1-8-251228"):
        self.model = model
        # 使用 LLM 客户端（不是 ChatOpenAI）
        self.client = LLMClient(ctx=new_context(method="invoke"))
    
    def execute(self, user_input, context):
        # 调用 LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        response = self.client.invoke(
            messages=messages,
            model=self.model,
            temperature=0.5
        )
        return result

# 全局实例 + 执行函数（用于注册）
_civil_consult_skill = CivilConsultSkill()

def execute_civil_consult(user_input, context):
    return _civil_consult_skill.execute(user_input, context)
```

### 4. 技能注册（`skill_registry.py`）

注册技能到注册表：

```python
skill_registry.register(
    skill_name="civil_consult",
    description="民事法律咨询",
    execute_func=execute_civil_consult,  # 全局函数
    category="legal"
)
```

### 5. 主脑路由（`master_brain.py`）

路由请求到技能：

```python
class MasterBrain:
    def route(self, user_input, user_id=None, context=None):
        # 1. 识别意图
        routing_decision = self._identify_intent(user_input)
        skill_name = routing_decision["data"]["skill"]
        
        # 2. 执行技能
        skill = skill_registry.get_skill(skill_name)
        result = skill.execute(user_input, context)
        
        return result
    
    def _identify_intent(self, user_input):
        # 使用 LLM 识别意图
        response = self.client.invoke(messages=messages, model=self.model)
        return decision
```

## 🔑 关键理解

### 技能调用工具

技能通过 `LLMClient` 调用大模型：

```python
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context

client = LLMClient(ctx=new_context(method="invoke"))
response = client.invoke(messages=messages, model="...")
```

### Bot 调用（可选）

也可以调用扣子 Bot：

```python
from src.utils.bot_registry import get_bot_registry

bot_registry = get_bot_registry()
result = bot_registry.call_bot(bot_type, query, user_id)
```

## ❌ 错误的做法

1. ❌ **直接导入案例和法条**
   - 错误：把案例和法条当成静态数据导入
   - 正确：通过技能调用 LLM 动态检索

2. ❌ **创建独立的知识库工具**
   - 错误：不基于 SKILL 框架
   - 正确：创建技能，使用 LLM 客户端

3. ❌ **在律师类中硬编码数据**
   - 错误：违反框架设计
   - 正确：在技能中调用工具

4. ❌ **使用 LangChain Agent**
   - 错误：项目使用主脑路由
   - 正确：使用 MasterBrain 路由到技能

## ✅ 正确的技能实现

### 示例：法律检索技能

```python
# src/skills/legal_search_skill.py
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context

class LegalSearchSkill:
    def __init__(self):
        self.client = LLMClient(ctx=new_context(method="invoke"))
        self.system_prompt = "你是法律检索专家..."
    
    def execute(self, query, context):
        # 通过 LLM 调用检索能力
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"搜索相关法条：{query}")
        ]
        response = self.client.invoke(
            messages=messages,
            model="doubao-seed-1-8-251228",
            temperature=0.5
        )
        return response

# 注册
skill_registry.register(
    skill_name="legal_search",
    description="法律检索技能",
    execute_func=execute_legal_search,
    category="legal"
)
```

## 📋 案例和法条的正确使用方式

案例和法条不是静态数据，而是通过以下方式动态获取：

### 方式1：通过 LLM 检索
- 在技能中调用 LLM
- 让 LLM 根据知识库检索相关法条和案例

### 方式2：通过 Bot 调用
- 调用扣子平台的法律咨询 Bot
- Bot 内部处理检索逻辑

### 方式3：通过集成工具
- 使用扣子平台的集成服务（如知识库集成）
- 在技能中调用集成工具

## 🎓 总结

项目的核心设计是：
1. **Agent（律师）**：提供专业能力
2. **Skill（技能）**：可复用的功能模块
3. **Tool（工具）**：LLM、语音、检索等底层能力
4. **Registry（注册表）**：统一管理技能和 Bot

关键点：
- ✅ 技能通过 `LLMClient` 调用大模型
- ✅ 主脑通过 LLM 识别意图，路由到技能
- ✅ 数据动态获取，不硬编码
- ✅ 使用项目框架，不自己发明轮子
