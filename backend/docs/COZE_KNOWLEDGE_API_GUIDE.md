# 扣子知识库API使用指南

## 📖 概述

本模块提供了调用扣子平台知识库检索的完整API接口，支持：
- 知识库检索
- 相似度过滤
- 错误处理（Token过期、Dataset ID错误等）
- 结果格式化

## 🔧 配置

### 1. 获取凭证

**Access Token：**
- 通过扣子平台认证API获取
- 有效期通常为2小时
- 需要定期刷新

**Dataset ID：**
- 在扣子平台创建知识库后获取
- 每个知识库有唯一的Dataset ID

### 2. 环境变量配置

在 `.env` 文件中添加：

```bash
# 扣子知识库配置
COZE_ACCESS_TOKEN=your_access_token_here
COZE_DATASET_ID=your_dataset_id_here
```

### 3. 配置文件

在 `config/coze_knowledge_config.json` 中配置多个知识库：

```json
{
  "knowledge_bases": {
    "civil_law": {
      "name": "民事法律知识库",
      "dataset_id": "your_dataset_id",
      "description": "包含民事法律条文、案例等内容"
    }
  }
}
```

## 🚀 快速开始

### 基础使用

```python
from backend.src.services.coze_knowledge_service import get_coze_knowledge_service

# 初始化服务
service = get_coze_knowledge_service(
    access_token="ACCESS_TOKEN",  # 替换为实际值
    dataset_id="DATASET_ID"       # 替换为实际值
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
else:
    print(f"错误：{result.get('error')}")
```

### 使用不同的Dataset ID

```python
# 方法1：在search方法中指定
result = service.search(
    query="合同违约",
    dataset_id="ANOTHER_DATASET_ID"
)

# 方法2：动态更新
service.set_dataset_id("NEW_DATASET_ID")
result = service.search(query="合同违约")
```

## 📋 API文档

### search()

检索知识库

**参数：**
- `query` (str): 用户问题，必填
- `dataset_id` (str, optional): 知识库ID，默认使用初始化时的ID
- `top_k` (int): 返回结果数量，默认5
- `min_score` (float): 最小相似度分数，默认0.0

**返回：**
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

### 错误返回格式

```python
{
    "success": False,
    "error": "错误描述",
    "error_type": "错误类型"
}
```

**错误类型：**
- `token_expired`: Access Token过期或无效
- `dataset_not_found`: Dataset ID不存在
- `timeout`: 请求超时
- `connection_error`: 网络连接失败
- `rate_limit`: 请求过于频繁
- `business_error`: 业务错误
- `http_error`: HTTP错误

## 🧪 测试

运行测试：

```bash
python backend/tests/test_coze_knowledge_api.py
```

或使用pytest：

```bash
pytest backend/tests/test_coze_knowledge_api.py -v
```

## 📝 示例

查看完整示例：

```bash
python backend/examples/coze_knowledge_example.py
```

### 示例列表

1. **基础检索** - 最简单的检索用法
2. **带过滤条件的检索** - 使用相似度过滤
3. **错误处理** - 处理各种错误情况
4. **多次检索** - 连续检索多个问题
5. **动态更新配置** - 动态更新Token和Dataset ID

## 🔍 注意事项

### 1. Access Token管理

- Token会过期，建议定期刷新
- 可以使用 `set_access_token()` 方法更新Token
- 生产环境建议实现自动刷新机制

### 2. Dataset ID

- 每个知识库有唯一的Dataset ID
- 可以配置多个知识库，通过不同的Dataset ID调用
- Dataset ID错误会返回404错误

### 3. 相似度分数

- 分数范围：0.0 - 1.0
- 1.0表示完全匹配
- 建议设置合理的 `min_score` 过滤低质量结果

### 4. 性能优化

- 设置合理的 `top_k` 值（通常5-10）
- 使用 `min_score` 过滤低相似度结果
- 缓存常用的查询结果

## 🐛 故障排查

### 常见问题

**Q: Token过期错误**
- 错误类型：`token_expired`
- 解决方案：使用 `set_access_token()` 更新Token

**Q: Dataset ID不存在**
- 错误类型：`dataset_not_found`
- 解决方案：检查Dataset ID是否正确

**Q: 请求超时**
- 错误类型：`timeout`
- 解决方案：检查网络连接，或增加超时时间

**Q: 返回结果为空**
- 检查知识库中是否有相关内容
- 降低 `min_score` 阈值
- 增大 `top_k` 值

## 📚 相关文档

- [扣子平台官方文档](https://www.coze.cn/docs)
- [扣子知识库API文档](https://www.coze.cn/docs/developer_guides/knowledge_base)

## 🤝 贡献

如有问题或建议，请提交Issue。
