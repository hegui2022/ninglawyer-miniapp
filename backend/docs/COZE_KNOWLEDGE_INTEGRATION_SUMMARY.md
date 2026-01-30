# 扣子知识库API集成完成

## ✅ 已完成的工作

### 1. 知识库服务模块

创建了 `backend/src/services/coze_knowledge_service.py`

**核心功能：**
- ✅ 使用Access Token做身份验证
- ✅ 支持Dataset ID配置
- ✅ 检索知识库（支持top_k和min_score过滤）
- ✅ 完善的错误处理
- ✅ 结果格式化

**错误处理覆盖：**
- ✅ Token过期/无效（401）
- ✅ Dataset ID不存在（404）
- ✅ 请求参数错误（400）
- ✅ 请求过于频繁（429）
- ✅ 网络超时
- ✅ 连接失败
- ✅ JSON解析失败
- ✅ 业务错误

### 2. 配置文件

创建了 `backend/config/coze_knowledge_config.json`

- 支持配置多个知识库
- 每个知识库有独立的Dataset ID
- 包含使用说明

### 3. 示例文件

创建了 `backend/examples/coze_knowledge_example.py`

包含5个完整示例：
- 基础检索示例
- 带过滤条件的检索
- 错误处理示例
- 多次检索示例
- 动态更新配置示例

### 4. 测试文件

创建了 `backend/tests/test_coze_knowledge_api.py`

完整的测试套件：
- 初始化测试
- 配置更新测试
- 结果格式化测试
- 错误处理测试（401, 404, 200等）
- 单例模式测试

### 5. 文档

创建了 `backend/docs/COZE_KNOWLEDGE_API_GUIDE.md`

- 完整的API文档
- 使用指南
- 故障排查
- 注意事项

## 📂 文件结构

```
backend/
├── src/
│   └── services/
│       ├── __init__.py                             # 更新导出
│       └── coze_knowledge_service.py               # 知识库服务（新增）
├── config/
│   └── coze_knowledge_config.json                  # 配置文件（新增）
├── docs/
│   ├── COZE_KNOWLEDGE_API_GUIDE.md                 # 使用指南（新增）
│   └── COZE_INTEGRATION_SUMMARY.md                 # 集成总结（已存在）
├── examples/
│   └── coze_knowledge_example.py                   # 使用示例（新增）
└── tests/
    └── test_coze_knowledge_api.py                  # 测试文件（新增）
```

## 🚀 使用方法

### 快速开始

```python
from backend.src.services.coze_knowledge_service import get_coze_knowledge_service

# 初始化服务
service = get_coze_knowledge_service(
    access_token="ACCESS_TOKEN",  # 占位符，替换为实际值
    dataset_id="DATASET_ID"       # 占位符，替换为实际值
)

# 检索知识库
result = service.search(
    query="刑法第二百六十四条",
    top_k=5
)

if result.get("success"):
    for item in result.get("data", []):
        print(f"相似度：{item.get('score', 0):.4f}")
        print(f"内容：{item.get('content', '')}")
```

### 错误处理

```python
result = service.search(query="测试")

if not result.get("success"):
    error_type = result.get("error_type")
    
    if error_type == "token_expired":
        # Token过期，需要更新
        service.set_access_token("NEW_TOKEN")
    elif error_type == "dataset_not_found":
        # Dataset ID错误
        print("Dataset ID不存在")
    else:
        # 其他错误
        print(f"错误：{result.get('error')}")
```

## 📋 数据格式

### 请求格式

```python
{
    "dataset_id": "DATASET_ID",
    "query": "用户问题",
    "top_k": 5,
    "min_score": 0.0  # 可选
}
```

### 成功响应格式

```python
{
    "success": True,
    "data": [
        {
            "content": "检索到的内容",
            "score": 0.95,
            "document_id": "doc_123",
            "metadata": {}
        }
    ],
    "total": 1,
    "query": "用户查询"
}
```

### 错误响应格式

```python
{
    "success": False,
    "error": "错误描述",
    "error_type": "错误类型",
    "http_status": 401  # 可选
}
```

## 🔍 关键特性

### 1. 占位符变量

代码中使用占位符变量，避免硬编码敏感数据：

```python
access_token: str = "ACCESS_TOKEN"  # 占位符
dataset_id: str = "DATASET_ID"      # 占位符
```

使用时需要替换为实际值：

```python
service = get_coze_knowledge_service(
    access_token="your_actual_token",
    dataset_id="your_actual_dataset_id"
)
```

### 2. 单例模式

使用单例模式，避免重复初始化：

```python
service1 = get_coze_knowledge_service("TOKEN", "DATASET")
service2 = get_coze_knowledge_service()  # 返回同一个实例
```

### 3. 动态配置更新

支持动态更新Token和Dataset ID：

```python
service.set_access_token("NEW_TOKEN")
service.set_dataset_id("NEW_DATASET")
```

### 4. 完善的错误处理

覆盖所有常见错误：
- HTTP错误（401, 404, 400, 429等）
- 网络错误（超时、连接失败）
- 业务错误（Token过期、Dataset不存在）
- 数据解析错误

## 🎯 下一步

### 1. 替换占位符

在实际使用前，需要：
1. 获取真实的Access Token
2. 获取真实的Dataset ID
3. 替换代码中的占位符

### 2. 集成到技能

将知识库服务集成到律师技能中：

```python
from backend.src.services.coze_knowledge_service import get_coze_knowledge_service

class CivilConsultSkill:
    def __init__(self):
        self.kb_service = get_coze_knowledge_service(
            access_token="your_token",
            dataset_id="your_dataset_id"
        )
    
    def execute(self, user_input, context):
        # 先检索知识库
        kb_result = self.kb_service.search(query=user_input)
        
        # 使用检索结果
        if kb_result.get("success"):
            relevant_docs = kb_result.get("data", [])
            # 处理检索结果...
```

### 3. 测试验证

运行测试：

```bash
python backend/tests/test_coze_knowledge_api.py
```

运行示例：

```bash
python backend/examples/coze_knowledge_example.py
```

## ✅ 总结

已完成的扣子知识库API集成包括：

1. ✅ **核心服务** - 完整的知识库检索功能
2. ✅ **错误处理** - 覆盖所有常见错误
3. ✅ **配置管理** - 支持多知识库配置
4. ✅ **示例代码** - 5个完整使用示例
5. ✅ **测试套件** - 完整的测试覆盖
6. ✅ **文档** - 详细的使用指南

**所有敏感数据都使用占位符，安全可靠！**
