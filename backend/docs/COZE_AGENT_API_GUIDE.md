# 扣子智能体API使用指南

## 📖 概述

本模块提供了调用扣子平台智能体/Bot的完整API接口，包括：
- 认证管理（Access Token自动刷新）
- 智能体调用（非流式/流式）
- Bot列表查询
- Bot信息获取
- 多轮对话支持

## 🔧 配置

### 1. 获取凭证

登录[扣子平台](https://www.coze.cn/)，进入「API & SDK」页面创建应用，获取：
- `Client ID`
- `Client Secret`

### 2. 配置环境变量

在 `.env` 文件中添加：

```bash
COZE_CLIENT_ID=your_coze_client_id_here
COZE_CLIENT_SECRET=your_coze_client_secret_here
COZE_API_BASE_URL=https://api.coze.cn
```

## 🚀 快速开始

### 基础使用

```python
from backend.src.services.coze_agent_service import get_coze_agent_service

# 获取服务实例
service = get_coze_agent_service()

# 运行智能体
result = service.run_bot(
    bot_id="your_bot_id",
    query="你好，请帮我检索刑法第二百六十四条",
    user_id="user_12345"
)

print(result.get("answer"))
```

### 流式输出

```python
for chunk in service.run_bot_stream(
    bot_id="your_bot_id",
    query="你好",
    user_id="user_12345"
):
    if chunk.get("event") == "message":
        print(chunk.get("data", {}).get("content", ""), end="")
```

### 多轮对话

```python
# 第一轮
result1 = service.run_bot(
    bot_id="your_bot_id",
    query="盗窃罪的定义是什么？",
    user_id="user_12345"
)
conversation_id = result1.get("conversation_id")

# 第二轮（使用会话ID）
result2 = service.run_bot(
    bot_id="your_bot_id",
    query="那量刑标准呢？",
    user_id="user_12345",
    conversation_id=conversation_id
)
```

## 📋 API文档

### CozeAgentService

#### run_bot()

运行智能体（非流式）

**参数：**
- `bot_id` (str): Bot ID，必填
- `query` (str): 用户输入，必填
- `user_id` (str): 用户ID，必填
- `conversation_id` (str, optional): 会话ID，用于多轮对话
- `stream` (bool): 是否流式返回，默认False
- `additional_messages` (list, optional): 额外的历史消息

**返回：**
```python
{
    "success": True,
    "bot_id": "xxx",
    "conversation_id": "xxx",
    "answer": "回答内容",
    "messages": [...],
    "status": "completed"
}
```

#### run_bot_stream()

流式运行智能体

**参数：**
- `bot_id` (str): Bot ID，必填
- `query` (str): 用户输入，必填
- `user_id` (str): 用户ID，必填
- `conversation_id` (str, optional): 会话ID

**返回：**
生成器，每次返回一个数据块

**数据块格式：**
```python
{
    "event": "message",
    "data": {
        "content": "部分内容"
    }
}
```

#### get_bot_list()

获取Bot列表

**参数：**
- `page_size` (int): 每页数量，默认20

**返回：**
```python
{
    "success": True,
    "bots": [...],
    "total": 10
}
```

#### get_bot_info()

获取Bot详细信息

**参数：**
- `bot_id` (str): Bot ID，必填

**返回：**
```python
{
    "success": True,
    "bot_info": {
        "bot_id": "xxx",
        "bot_name": "名称",
        "description": "描述"
    }
}
```

## 🧪 测试

运行测试：

```bash
# 确保配置了环境变量
export COZE_CLIENT_ID=your_client_id
export COZE_CLIENT_SECRET=your_client_secret

# 运行测试
python backend/tests/test_coze_agent_api.py
```

或使用pytest：

```bash
pytest backend/tests/test_coze_agent_api.py -v
```

## 📝 示例

查看完整示例：

```bash
python backend/examples/coze_agent_example.py
```

## 🔍 注意事项

### 1. Access Token管理

- Token自动缓存，有效期内重复使用
- 提前5分钟自动刷新
- 无需手动管理Token

### 2. 错误处理

所有API调用都会返回统一的格式：

```python
{
    "success": True/False,
    "data": ...,  # 成功时
    "error": "..."  # 失败时
}
```

### 3. 并发限制

- 单实例模式，避免重复初始化
- 自动管理Token缓存

### 4. 超时设置

- 认证请求：10秒
- Bot调用：60秒

## 📊 性能优化

### Token缓存

```python
# 自动缓存，无需手动处理
service = get_coze_agent_service()
```

### 批量调用

```python
# 多个Bot可以并行调用
results = []
for bot_id in bot_ids:
    result = service.run_bot(bot_id=bot_id, query="...", user_id="user_123")
    results.append(result)
```

## 🐛 故障排查

### 常见问题

**Q: 获取Token失败**
- 检查Client ID和Secret是否正确
- 检查网络连接

**Q: Bot调用失败**
- 检查Bot ID是否正确
- 检查Bot是否已发布
- 查看日志获取详细错误信息

**Q: 流式输出中断**
- 检查网络连接稳定性
- 增加超时时间

## 📚 相关文档

- [扣子平台官方文档](https://www.coze.cn/docs)
- [扣子API文档](https://www.coze.cn/docs/developer_guides/authentication)

## 🤝 贡献

如有问题或建议，请提交Issue。
