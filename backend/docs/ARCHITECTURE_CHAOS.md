# 当前架构混乱情况可视化

```
┌─────────────────────────────────────────────────────────────┐
│                    前端（微信小程序）                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      API 层 (Flask)                           │
│  - /api/consultation/route  → master_agent.route()           │
│  - /api/contract/draft      → lawyer_factory.get_lawyer()    │
│  - /api/session/*           → session_service                │
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ↓                 ↓                 ↓
┌─────────────────┐  ┌──────────┐  ┌──────────────┐
│ Master Agent    │  │ Master   │  │ Lawyer       │
│ (master_agent)  │  │ Brain    │  │ Factory      │
│  ⚠️ 不知道      │  │ (master_ │  │              │
│   用哪一个     │  │  brain)  │  │              │
└────────┬────────┘  └────┬─────┘  └──────┬───────┘
         │                │                │
         ↓                ↓                ↓
┌─────────────────────────────────────────────────────────────┐
│                 三种不同的调用方式！                          │
│                                                              │
│  方式1: bot_registry.py                                      │
│    requests.post(bot['api_url'], ...)  ← 调用扣子Bot        │
│                                                              │
│  方式2: coze_agent_service.py (我刚实现的，可能不需要)       │
│    BaseThirdPartyAPIService._request(...) ← 调用扣子智能体  │
│                                                              │
│  方式3: LLMClient 直接调用                                   │
│    LLMClient().invoke(...) ← 直接调用大模型                  │
└─────────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ↓                 ↓                 ↓
┌─────────────────┐  ┌──────────┐  ┌──────────────┐
│ Skills (本地)   │  │ Agents   │  │ 扣子API      │
│  - civil_consult│  │ (Lang    │  │              │
│  - contract     │  │  Chain)  │  │  ⚠️ 到底调    │
│  - desensitize  │  │          │  │   用哪些？   │
│  ⚠️ 只有LLM，   │  │          │  │              │
│    没有知识库    │  │          │  │              │
└─────────────────┘  └──────────┘  └──────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ↓                 ↓                 ↓
┌─────────────────┐  ┌──────────┐  ┌──────────────┐
│ Knowledge?      │  │ LLM?     │  │ Adapter?     │
│  ⚠️ coze_       │  │  ⚠️ 3种   │  │  ⚠️ 我实现   │
│    knowledge_   │  │     方式  │  │    的可能    │
│    service.py   │  │          │  │    不需要    │
│  (我刚实现的)   │  │          │  │              │
└─────────────────┘  └──────────┘  └──────────────┘
```

---

## 核心矛盾总结

### 1. 两个主脑
```
master_agent.py  ← LangChain 实现，可能调用扣子Bot
master_brain.py  ← LLMClient 实现，调用本地Skills
```

### 2. 三种LLM调用方式
```
方式1: LangChain ChatOpenAI (ning_lawyer_template.py)
方式2: LLMClient (master_brain.py, skills/*.py)
方式3: 扣子智能体API (coze_agent_service.py - 我刚实现的)
```

### 3. 扣子API调用混乱
```
bot_registry.py          → 直接 requests 调用扣子Bot
coze_agent_service.py    → 调用扣子智能体（我刚实现的，可能不需要）
coze_knowledge_service.py → 调用扣子知识库（我刚实现的，可能需要）
coze_skill_service.py    → 调用扣子技能（我刚实现的，可能不需要）
coze_workflow_service.py → 调用扣子工作流（我刚实现的，可能不需要）
```

### 4. 技能不完整且不调用知识库
```
现有技能：
✅ civil_consult_skill.py  ← 只有LLM，无知识库
✅ contract_skill.py       ← 只有LLM，无知识库
✅ desensitize_skill.py    ← 正则表达式

缺失技能：
❌ 刑事咨询
❌ 劳动咨询
❌ 公司咨询
❌ 知识产权咨询
❌ 婚姻咨询
```

### 5. LangGraph 未使用
```
requirements.txt:
  langgraph>=0.1.0  ✅ 已安装

实际代码:
  grep "from langgraph" → 空结果！❌
```

---

## 期望架构（等待确认）

```
前端请求
  ↓
本地 LangGraph Agent (用 LangGraph 实现，支持多轮对话)
  ↓
本地 Skills (用 LangChain 实现，调用知识库)
  ↓
本地 Tools (用 LangChain Tools 实现)
  ↓
扣子知识库API ← 唯一调用的扣子API？
扣子大模型API  ← 唯一调用的扣子API？
```

---

## 下一步行动

⏸️ **停止所有代码实现**
📋 **等待用户明确需求**
🎯 **根据需求重构架构**
