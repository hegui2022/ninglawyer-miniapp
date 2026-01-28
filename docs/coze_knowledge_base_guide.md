# 扣子平台知识库对接指南

## 🎯 两种方案

### 方案一：使用当前的 knowledge-base 服务（推荐）⭐

**优势**：
- ✅ 已经集成好了，立即可用
- ✅ 支持通过 CLI 快速导入数据
- ✅ 支持通过 Python SDK 动态添加内容
- ✅ 向量化搜索，智能匹配

**如何管理知识库**：

#### 方法 1：使用 CLI 导入数据
```bash
# 导入文本内容
coze-coding-ai knowledge add \
  --dataset "legal_knowledge" \
  --content "这里写你的法律知识内容"

# 导入 URL
coze-coding-ai knowledge add \
  --dataset "legal_knowledge" \
  --url "https://example.com/legal-doc.html"
```

#### 方法 2：使用 Python SDK 动态添加
```python
from coze_coding_dev_sdk import KnowledgeClient, Config, KnowledgeDocument, DataSourceType

config = Config()
client = KnowledgeClient(config=config)

# 添加文档
documents = [
    KnowledgeDocument(
        source=DataSourceType.TEXT,
        raw_data="你的法律知识内容"
    )
]

response = client.add_documents(
    documents=documents,
    table_name="legal_knowledge"
)
```

---

### 方案二：使用扣子平台知识库（如果你有扣子平台账号）

**注意**：当前的 knowledge-base 集成是独立的向量数据库服务，不是扣子平台的知识库。

如果你想使用扣子平台的知识库，需要：

1. **在扣子平台创建知识库**：
   - 登录扣子平台
   - 进入"知识库"模块
   - 创建新知识库
   - 上传文档（PDF、Word、TXT等）

2. **对接方式**：
   - 需要扣子平台提供知识库的 API 接口
   - 当前环境可能需要额外配置

3. **可能遇到的问题**：
   - 扣子平台知识库 API 可能不对外开放
   - 需要额外的认证和配置

---

## 💡 推荐操作流程

### 使用当前的 knowledge-base 服务

#### 1. 准备你的法律知识文件

将你的法律知识整理成文本文件，例如：
```
assets/my_legal_knowledge.md
```

#### 2. 导入到知识库
```bash
coze-coding-ai knowledge add \
  --dataset "legal_knowledge" \
  --content "$(cat assets/my_legal_knowledge.md)"
```

#### 3. 测试查询
```bash
coze-coding-ai knowledge search \
  --query "劳动仲裁要多久" \
  --top-k 3
```

#### 4. Agent 自动使用
Agent 会自动调用 `search_legal_knowledge` 工具查询知识库，无需额外配置。

---

## 📝 知识库数据格式建议

### 推荐格式：Markdown

```markdown
# 标题

## 子标题

### 具体问题
这里写具体的问题内容

### 法律依据
- 《中华人民共和国民法典》第XXX条
- 《中华人民共和国劳动法》第XXX条

### 解答
这里用大白话解释，老百姓能听懂

### 证据要求
1. 证据1
2. 证据2

### 解决途径
1. 方法1
2. 方法2
```

### 实例

```markdown
# 工资拖欠问题

## 问：工资被拖欠了，去哪里投诉？

### 法律依据
《中华人民共和国劳动法》第50条：工资应当以货币形式按月支付给劳动者本人。不得克扣或者无故拖欠劳动者的工资。

### 解答
可以先向当地劳动监察大队投诉，劳动监察大队会责令用人单位支付工资。如果投诉后仍未解决，可以向劳动仲裁委员会申请劳动仲裁，这是免费的。

### 证据要求
1. 劳动合同
2. 工资条
3. 考勤记录
4. 转账记录
5. 与用人单位的沟通记录

### 解决途径
1. 向劳动监察大队投诉
2. 申请劳动仲裁（免费）
3. 向人民法院起诉
```

---

## 🔄 更新知识库内容

### 当你需要添加新内容时

#### 方法 1：重新导入全部内容
```bash
# 更新知识库文件
vim assets/legal_knowledge_base.md

# 重新导入
coze-coding-ai knowledge add \
  --dataset "legal_knowledge" \
  --content "$(cat assets/legal_knowledge_base.md)"
```

#### 方法 2：增量添加新内容
```bash
# 创建新文件
echo "新的法律知识内容" > assets/new_knowledge.md

# 导入新内容
coze-coding-ai knowledge add \
  --dataset "legal_knowledge" \
  --content "$(cat assets/new_knowledge.md)"
```

---

## 📊 知识库管理

### 查看已有数据集
```bash
coze-coding-ai knowledge list
```

### 查询知识库
```bash
coze-coding-ai knowledge search \
  --query "你的查询内容" \
  --top-k 5
```

---

## 🎯 总结

### 推荐方案：使用当前的 knowledge-base 服务

**理由**：
1. ✅ 已经集成，立即可用
2. ✅ 支持命令行快速导入
3. ✅ 支持 Python SDK 动态管理
4. ✅ Agent 自动使用，无需额外配置

**操作步骤**：
1. 准备你的法律知识文件（Markdown格式）
2. 使用 CLI 导入到知识库
3. Agent 自动查询和使用

---

## ❓ 你的选择

**选项 1：使用当前的 knowledge-base 服务**（推荐）
- 我帮你准备知识库文件模板
- 你补充你的法律知识内容
- 我帮你导入到知识库
- Agent 立即可用

**选项 2：坚持使用扣子平台知识库**
- 你告诉我扣子平台知识库的 API 信息
- 我帮你对接代码

**请告诉我你想用哪种方案？**

或者如果你已经准备好了法律知识内容，直接发给我，我帮你导入到知识库！
