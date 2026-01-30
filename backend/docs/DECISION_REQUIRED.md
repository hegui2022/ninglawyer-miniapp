# 项目关键问题清单

**生成时间：** 2025-01-30
**目的：** 等待用户决策，明确下一步行动

---

## 🚨 最关键的问题（需要立即确认）

### 问题1：扣子API调用范围

根据你之前说的："不能全部功能都调用扣子的API，也不使用BOT"

**请明确：**
- ✅ 只调用扣子知识库API
- ✅ 只调用扣子大模型API
- ❌ 不调用扣子智能体API
- ❌ 不调用扣子Bot
- ❌ 不调用扣子技能API
- ❌ 不调用扣子工作流API

**我实现的扣子服务（需要你决定保留/删除）：**

| 服务 | 用途 | 是否需要 |
|-----|------|---------|
| `coze_agent_service.py` | 调用扣子智能体 | ❓ |
| `coze_knowledge_service.py` | 调用扣子知识库 | ❓ |
| `coze_skill_service.py` | 调用扣子技能 | ❓ |
| `coze_workflow_service.py` | 调用扣子工作流 | ❓ |
| `base_service.py` | 统一基类 | ❓ |

---

### 问题2：大模型如何调用？

**当前代码有3种调用方式：**

| 方式 | 文件 | 是否使用 |
|-----|------|---------|
| LangChain ChatOpenAI | `ning_lawyer_template.py`, `master_agent.py` | ✅ |
| LLMClient 直接调用 | `master_brain.py`, `skills/*.py` | ✅ |
| 扣子智能体API | `coze_agent_service.py` | ⚠️ 我实现的 |

**请明确：**
- 应该用哪种方式？
- 还是我理解错了？

---

### 问题3：主脑应该用哪一个？

| 选项 | 文件 | 特点 | 是否使用 |
|-----|------|------|---------|
| A | `master_agent.py` | LangChain + 可能调用扣子Bot | ❓ |
| B | `master_brain.py` | LLMClient + 本地Skills | ❓ |
| C | 都不要，重新实现 | 使用 LangGraph | ❓ |

**请明确：**
- 用哪一个？
- 还是两个都不对？

---

### 问题4：知识库服务需要吗？

我实现了：
- ✅ `coze_knowledge_service.py` - 扣子知识库服务
- ✅ `legal_knowledge_adapter.py` - 法律数据适配器

**请明确：**
- 这两个需要保留吗？
- 如果需要，技能层应该如何使用？

---

### 问题5：技能层应该如何实现？

**当前技能：**
- `civil_consult_skill.py` - 只有LLM，无知识库
- `contract_skill.py` - 只有LLM，无知识库
- `desensitize_skill.py` - 正则表达式

**缺失技能：**
- 刑事咨询
- 劳动咨询
- 公司咨询
- 知识产权咨询
- 婚姻咨询

**请明确：**
1. 现有技能是否需要修改？
2. 是否需要补充缺失的技能？
3. 技能应该调用知识库吗？
4. 技能应该使用数据适配器吗？

---

### 问题6：LangGraph 需要使用吗？

**现状：**
- requirements.txt 中有 `langgraph>=0.1.0`
- 但代码中没有使用

**请明确：**
- 需要使用 LangGraph 吗？
- 如果需要，应该如何设计？

---

## 📋 我需要你回答的问题

请直接告诉我：

### 1. 扣子API
```
✅ 知识库API：需要 / 不需要
✅ 大模型API：需要 / 不需要
❌ 智能体API：需要 / 不需要
❌ Bot API：需要 / 不需要
❌ 技能API：需要 / 不需要
❌ 工作流API：需要 / 不需要
```

### 2. 主脑
```
请选择：
□ master_agent.py
□ master_brain.py
□ 都不要，重新实现
□ 两个都保留
```

### 3. 大模型调用方式
```
请选择：
□ LangChain ChatOpenAI
□ LLMClient
□ 其他（请说明）
```

### 4. 知识库服务
```
□ 保留 coze_knowledge_service.py
□ 保留 legal_knowledge_adapter.py
□ 都删除
□ 重新设计
```

### 5. 技能层
```
□ 现有技能需要修改
□ 现有技能不需要修改
□ 需要补充缺失的技能
□ 技能应该调用知识库
□ 技能应该使用数据适配器
```

### 6. LangGraph
```
□ 需要使用 LangGraph
□ 不需要使用 LangGraph
```

---

## 🎯 你的期望架构是什么样的？

请直接描述你期望的系统架构，例如：

```
前端请求
  ↓
本地 LangGraph Agent (用 LangGraph 实现)
  ↓
本地 Skills (用 LangChain 实现)
  ↓
本地 Tools (用 LangChain Tools 实现)
  ↓
扣子知识库API (唯一调用的扣子API)
扣子大模型API (唯一调用的扣子API)
```

**请直接告诉我你期望的架构是什么样的，不要再让我猜了！**

---

## ⏸️ 我现在停止所有代码实现

**等待你明确回答以上问题后再继续！**
