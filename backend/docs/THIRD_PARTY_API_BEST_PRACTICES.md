# 第三方API封装最佳实践指南

## 📖 概述

本项目遵循统一的生产级代码开发规范，所有第三方API都基于 `BaseThirdPartyAPIService` 基类进行封装。

## 🎯 核心原则

### 1. 统一封装
所有第三方API（扣子、微信、支付宝、阿里云等）都按统一模板封装，便于管理和维护。

### 2. 异常统一处理
网络超时、Token过期、权限不足等通用错误，在基类中一次性处理。

### 3. 降低耦合
业务逻辑和API调用逻辑分离，便于理解和维护。

### 4. 便于扩展
后续加缓存、重试、日志、监控，都可以在封装类里加，不影响业务代码。

## 📦 架构设计

```
BaseThirdPartyAPIService（基类）
    ├── CozeAgentService（扣子智能体）
    ├── CozeKnowledgeService（扣子知识库）
    ├── CozeWorkflowService（扣子工作流）
    ├── CozeSkillService（扣子技能）
    ├── WeChatService（微信，待开发）
    ├── AlipayService（支付宝，待开发）
    └── ...（其他第三方服务）
```

## 🔧 基础类：BaseThirdPartyAPIService

### 核心功能

```python
class BaseThirdPartyAPIService(ABC):
    """第三方API基础封装类"""
    
    def __init__(self, api_key: str, base_url: str, timeout: int = 30):
        """初始化"""
    
    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """通用请求方法"""
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """通用响应处理"""
```

### 错误处理

基类已经处理了以下错误：

| 错误类型 | HTTP状态码 | 处理方式 |
|---------|-----------|---------|
| Token过期/无效 | 401 | 返回 `token_expired` |
| 资源不存在 | 404 | 返回 `not_found` |
| 请求参数错误 | 400 | 返回 `bad_request` |
| 请求过于频繁 | 429 | 返回 `rate_limit` |
| 网络超时 | - | 返回 `timeout` |
| 连接失败 | - | 返回 `connection_error` |

## 📋 不同场景的封装

### 1. 简单API（如知识库检索）

**适用场景：** 参数简单、调用频率适中

**实现方式：** 继承基类，实现具体的API调用方法

```python
class CozeKnowledgeService(BaseThirdPartyAPIService):
    """扣子知识库服务"""
    
    def __init__(self, access_token: str = None):
        super().__init__(
            api_key=access_token or "ACCESS_TOKEN",
            base_url="https://api.coze.cn",
            timeout=30
        )
    
    def search(self, query: str, dataset_id: str, top_k: int = 5):
        """检索知识库"""
        return self._request(
            method="POST",
            path="/v1/dataset/retrieve",
            json={"dataset_id": dataset_id, "query": query, "top_k": top_k}
        )
```

### 2. 扣子工作流API

**适用场景：** 复杂的工作流执行

**实现方式：** 继承基类，实现 `run_workflow()` 方法

```python
class CozeWorkflowService(BaseThirdPartyAPIService):
    """扣子工作流服务"""
    
    def run_workflow(self, workflow_id: str, params: dict):
        """运行工作流"""
        return self._request(
            method="POST",
            path="/v1/workflow/run",
            json={"workflow_id": workflow_id, "parameters": params}
        )
```

### 3. 扣子技能API

**适用场景：** 调用特定技能

**实现方式：** 继承基类，实现 `call_skill()` 方法

```python
class CozeSkillService(BaseThirdPartyAPIService):
    """扣子技能服务"""
    
    def call_skill(self, skill_id: str, skill_params: dict):
        """调用技能"""
        return self._request(
            method="POST",
            path="/v1/skill/call",
            json={"skill_id": skill_id, "parameters": skill_params}
        )
```

### 4. 高频调用的API

**适用场景：** 调用频率很高，需要缓存

**实现方式：** 添加缓存逻辑

```python
from functools import lru_cache

class HighFrequencyService(BaseThirdPartyAPIService):
    """高频调用服务"""
    
    @lru_cache(maxsize=100)
    def search(self, query: str):
        """带缓存的检索"""
        return self._request("POST", "/search", json={"query": query})
```

### 5. 需要重试的API

**适用场景：** 容易失败，需要自动重试

**实现方式：** 添加重试装饰器

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class RetryService(BaseThirdPartyAPIService):
    """需要重试的服务"""
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def call_api(self, params):
        """带重试的调用"""
        return self._request("POST", "/api", json=params)
```

## 🚀 如何开发新的第三方API服务

### 步骤1：创建服务类

```python
from backend.src.services.base_service import BaseThirdPartyAPIService
from loguru import logger

class NewPlatformService(BaseThirdPartyAPIService):
    """新平台服务"""
    
    def __init__(self, api_key: str = None):
        super().__init__(
            api_key=api_key or "API_KEY",
            base_url="https://api.newplatform.com",
            timeout=30
        )
        
        logger.info("✅ 新平台服务初始化完成")
    
    def call_specific_api(self, param1: str, param2: int):
        """调用特定API"""
        return self._request(
            method="POST",
            path="/v1/specific",
            json={"param1": param1, "param2": param2}
        )
```

### 步骤2：注册到服务模块

```python
# backend/src/services/__init__.py
from .new_platform_service import NewPlatformService, get_new_platform_service

__all__ = [
    # ... 其他服务
    "NewPlatformService",
    "get_new_platform_service"
]
```

### 步骤3：实现单例模式（可选）

```python
# 全局实例
_new_platform_service = None

def get_new_platform_service(api_key: str = None):
    """获取服务实例（单例模式）"""
    global _new_platform_service
    
    if _new_platform_service is None:
        _new_platform_service = NewPlatformService(api_key)
    elif api_key:
        _new_platform_service.set_api_key(api_key)
    
    return _new_platform_service
```

### 步骤4：使用服务

```python
from backend.src.services import get_new_platform_service

# 初始化服务
service = get_new_platform_service(api_key="your_api_key")

# 调用API
result = service.call_specific_api(param1="value1", param2=123)

if result.get("success"):
    print("成功：", result.get("data"))
else:
    print("失败：", result.get("error"))
```

## 📝 返回格式规范

### 成功响应

```python
{
    "success": True,
    "data": {  # 业务数据
        # ... 具体数据
    },
    "raw": {  # 原始响应（可选）
        # ...
    }
}
```

### 错误响应

```python
{
    "success": False,
    "error": "错误描述",
    "error_type": "错误类型",
    "code": 123,  # 业务错误码（可选）
    "http_status": 401  # HTTP状态码（可选）
}
```

## 🔍 可重写的方法

基类提供了以下方法，子类可以根据需要重写：

```python
def _is_business_success(self, result: Dict) -> bool:
    """判断业务是否成功（默认：code==0 或 success==True）"""

def _extract_business_data(self, result: Dict) -> Any:
    """提取业务数据（默认：返回 result.get("data")）"""

def _extract_business_error(self, result: Dict) -> str:
    """提取业务错误信息（默认：返回 result.get("msg")）"""

def _extract_business_code(self, result: Dict) -> Optional[str]:
    """提取业务错误码（默认：返回 result.get("code")）"""
```

## ⚠️ 例外情况

不是所有API都需要完整封装，以下情况可以简化：

### 1. 一次性调用的测试代码

```python
# 直接写简单请求，不用封装类
import requests

response = requests.get("https://api.example.com/once", params={"key": "value"})
```

### 2. 超简单的API

```python
# 只有一个GET请求，无复杂参数，封装成单个函数即可
def get_simple_data():
    response = requests.get("https://api.example.com/data")
    return response.json()
```

### 3. 已有成熟SDK的API

```python
# 直接使用官方SDK
import wechatpy

wechat = wechatpy.WeChatClient(appid, secret, token)
```

## ✅ 检查清单

开发新的第三方API服务时，请确保：

- [ ] 继承 `BaseThirdPartyAPIService` 基类
- [ ] 调用 `super().__init__()` 初始化
- [ ] 使用 `_request()` 方法发送请求
- [ ] 实现结果格式化方法
- [ ] 添加日志记录
- [ ] 实现单例模式（如需要）
- [ ] 更新 `__init__.py` 导出
- [ ] 编写使用示例
- [ ] 编写测试用例

## 📚 相关文档

- [扣子智能体API文档](./COZE_AGENT_API_GUIDE.md)
- [扣子知识库API文档](./COZE_KNOWLEDGE_API_GUIDE.md)
- [扣子工作流API文档](./COZE_WORKFLOW_API_GUIDE.md)（待补充）
- [扣子技能API文档](./COZE_SKILL_API_GUIDE.md)（待补充）

## 🤝 贡献

遵循此规范开发新的第三方API服务，保持代码一致性。
