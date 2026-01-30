# 数据适配器（Data Adapters）

## 概述

数据适配器负责将第三方API（如扣子知识库）返回的原始数据转换为前端（如微信小程序）需要的格式。

## 设计理念

### 核心原则

1. **关注点分离**：数据适配逻辑与业务逻辑分离
2. **性能优先**：优先使用正则表达式，仅在需要时使用LLM
3. **可扩展性**：支持多种前端格式（微信小程序、H5等）
4. **容错性强**：对错误数据进行优雅降级

### 三阶段处理架构

```
原始数据 → 数据清洗 → 格式转换 → 智能增强 → 前端格式
         ↓          ↓          ↓          ↓
      去噪补全    结构化     LLM摘要    微信小程序
```

1. **数据清洗阶段**：
   - 去除噪点信息
   - 补全缺失字段
   - 数据归一化

2. **格式转换阶段**：
   - 使用正则表达式提取关键信息
   - 转换为目标格式结构
   - 字段映射和重命名

3. **智能增强阶段**（可选）：
   - 使用LLM生成内容摘要
   - 提取关键要点
   - 语义理解增强

## 目录结构

```
backend/src/adapters/
├── __init__.py                        # 模块导出
├── base_adapter.py                    # 数据适配器基类
└── legal_knowledge_adapter.py         # 法律知识库适配器

backend/examples/
└── data_adapter_example.py            # 使用示例

backend/tests/
└── test_data_adapter.py               # 单元测试
```

## 使用方法

### 基础用法

```python
from backend.src.services import get_coze_knowledge_service
from backend.src.adapters import get_legal_knowledge_adapter

# 1. 调用扣子知识库API
kb_service = get_coze_knowledge_service(
    access_token="YOUR_ACCESS_TOKEN",
    dataset_id="YOUR_DATASET_ID"
)

raw_result = kb_service.search(
    query="刑法第二百六十四条",
    top_k=3
)

# 2. 使用数据适配器转换格式
adapter = get_legal_knowledge_adapter(enable_llm_enhance=False)
adapted_result = adapter.adapt(raw_result)

# 3. 使用适配后的数据
for item in adapted_result["data"]:
    print(f"法条编号: {item['article_number']}")
    print(f"法条名称: {item['law_name']}")
    print(f"罪名: {item['crime_name']}")
    print(f"刑期: {item['penalties']}")
    print(f"金额: {item['amounts']}")
    print(f"情节: {item['circumstances']}")
```

### 启用LLM增强

```python
# 启用LLM增强（生成摘要和关键点）
adapter = get_legal_knowledge_adapter(enable_llm_enhance=True)
adapted_result = adapter.adapt(raw_result)

# 查看增强后的数据
for item in adapted_result["data"]:
    print(f"摘要: {item['summary']}")
    print(f"关键点: {item['key_points']}")
```

### 转换为微信小程序格式

```python
def convert_to_wechat_format(data: dict) -> dict:
    """转换为微信小程序专用格式"""
    wechat_data = {
        "success": True,
        "data": {
            "law_articles": [],
            "total": data.get("total", 0)
        }
    }
    
    for item in data.get("data", []):
        wechat_data["data"]["law_articles"].append({
            "article_id": item.get("document_id", ""),
            "article_number": item.get("article_number", ""),
            "law_name": item.get("law_name", ""),
            "crime_name": item.get("crime_name", ""),
            "content": item.get("content", ""),
            "content_sections": item.get("content_sections", []),
            "penalties": item.get("penalties", []),
            "amounts": item.get("amounts", []),
            "circumstances": item.get("circumstances", []),
            "keywords": item.get("keywords", []),
            "summary": item.get("summary", ""),
            "key_points": item.get("key_points", []),
            "score": item.get("score", 0)
        })
    
    return wechat_data
```

## 适配器字段说明

### 原始字段

来自扣子知识库API的原始字段：

- `document_id`: 文档ID
- `content`: 文档内容
- `score`: 相似度分数

### 适配后字段

适配器添加/转换的字段：

#### 基础信息
- `article_number`: 法条编号（如：第二百六十四条）
- `law_name`: 法条名称（如：中华人民共和国刑法）
- `crime_name`: 罪名（如：盗窃罪）
- `content`: 原始内容

#### 结构化信息
- `penalties`: 刑期信息列表
  - `term`: 期限（如：三年）
  - `type`: 类型（如：有期徒刑、拘役、管制）
- `amounts`: 金额信息列表（如：三千元以上、三万元以下）
- `circumstances`: 情节列表（如：数额较大、多次盗窃、入户盗窃）

#### 辅助信息
- `content_sections`: 内容分段（便于前端显示）
- `keywords`: 关键词列表
- `summary`: 内容摘要（仅启用LLM增强时）
- `key_points`: 关键点列表（仅启用LLM增强时）

#### 原始字段保留
- `document_id`: 文档ID
- `score`: 相似度分数

## 性能对比

| 方式 | 处理时间 | 信息丰富度 | 适用场景 |
|------|---------|----------|---------|
| 仅正则表达式 | ~0.1秒 | 基础结构化信息 | 实时性要求高 |
| 正则 + LLM | ~2-3秒 | 摘要 + 关键点 | 需要智能摘要 |

## 扩展新的适配器

### 步骤1：继承基类

```python
from backend.src.adapters.base_adapter import DataAdapterBase

class YourCustomAdapter(DataAdapterBase):
    """自定义数据适配器"""
    
    def __init__(self, enable_llm_enhance: bool = True):
        super().__init__(enable_llm_enhance)
        
        # 初始化正则表达式
        self.patterns.update({
            "your_pattern": r"your_regex_here"
        })
    
    def get_target_format(self) -> str:
        """指定目标格式"""
        return "your_format"
    
    def _format_single_item(self, item: Dict) -> Dict:
        """格式化单个数据项"""
        formatted_item = super()._format_single_item(item)
        
        # 添加自定义格式化逻辑
        
        return formatted_item
```

### 步骤2：注册适配器

```python
# backend/src/adapters/__init__.py

from .your_custom_adapter import YourCustomAdapter, get_your_custom_adapter

__all__ = [
    "DataAdapterBase",
    "YourCustomAdapter",
    "get_your_custom_adapter"
]
```

### 步骤3：使用适配器

```python
from backend.src.adapters import get_your_custom_adapter

adapter = get_your_custom_adapter(enable_llm_enhance=False)
adapted_result = adapter.adapt(raw_data)
```

## 测试

### 运行单元测试

```bash
cd backend
python -m pytest tests/test_data_adapter.py -v
```

### 运行示例代码

```bash
cd backend
python examples/data_adapter_example.py
```

## 注意事项

1. **性能优化**：生产环境建议使用 `enable_llm_enhance=False`，仅在需要摘要时启用
2. **错误处理**：适配器会对错误数据进行优雅降级，不会抛出异常
3. **单例模式**：使用 `get_legal_knowledge_adapter()` 获取单例实例，避免重复初始化
4. **正则表达式**：根据实际数据格式优化正则表达式模式
5. **LLM配置**：启用LLM增强时，确保已配置有效的LLM客户端

## 故障排查

### 问题1：适配后的数据缺少某些字段

**原因**：正则表达式未匹配到对应内容

**解决**：
- 检查原始数据格式
- 优化正则表达式模式
- 参考 `_init_legal_patterns()` 方法

### 问题2：LLM增强失败

**原因**：LLM客户端未配置或网络问题

**解决**：
- 检查 LLMClient 配置
- 使用 `enable_llm_enhance=False` 降级到仅正则模式
- 查看日志获取详细错误信息

### 问题3：性能较慢

**原因**：启用了LLM增强或数据量大

**解决**：
- 使用 `enable_llm_enhance=False`
- 减少 `top_k` 参数
- 考虑批量处理和缓存

## 最佳实践

1. **单例模式**：使用 `get_legal_knowledge_adapter()` 获取实例，避免重复初始化
2. **容错处理**：对适配后的数据进行空值检查
3. **性能优化**：生产环境默认禁用LLM增强，按需启用
4. **日志记录**：记录适配过程中的关键信息，便于问题排查
5. **单元测试**：为新的适配器编写完整的单元测试

## 相关文档

- [扣子知识库服务文档](./coze_knowledge_service.md)
- [扣子智能体服务文档](./coze_agent_service.md)
- [扣子工作流服务文档](./coze_workflow_service.md)

## 更新日志

### v1.0.0 (2025-01-15)

- 初始版本
- 实现法律知识库适配器
- 支持正则表达式和LLM增强
- 完整的单元测试和示例代码
