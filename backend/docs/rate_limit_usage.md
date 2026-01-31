# API限流使用文档

## 概述

系统实现了灵活的API限流机制，支持基于用户ID和IP地址的限流，可以通过环境变量配置不同的限流规则。

## 配置

### 环境变量

在 `.env` 文件中配置以下环境变量：

```bash
# 是否启用限流（true/false）
RATE_LIMIT_ENABLED=true

# 限流存储方式：memory（内存）或 redis（分布式）
RATE_LIMIT_STORAGE=memory

# 默认规则：每分钟最多60次请求
RATE_LIMIT_DEFAULT_MAX=60
RATE_LIMIT_DEFAULT_WINDOW=60

# 登录接口：每分钟最多5次请求
RATE_LIMIT_LOGIN_MAX=5
RATE_LIMIT_LOGIN_WINDOW=60

# 注册接口：每分钟最多3次请求
RATE_LIMIT_REGISTER_MAX=3
RATE_LIMIT_REGISTER_WINDOW=60

# 发送验证码：每分钟最多1次请求
RATE_LIMIT_SEND_CODE_MAX=1
RATE_LIMIT_SEND_CODE_WINDOW=60

# 文件上传：每分钟最多10次请求
RATE_LIMIT_UPLOAD_MAX=10
RATE_LIMIT_UPLOAD_WINDOW=60

# 查询接口：每分钟最多120次请求
RATE_LIMIT_QUERY_MAX=120
RATE_LIMIT_QUERY_WINDOW=60

# 聊天接口：每分钟最多30次请求
RATE_LIMIT_CHAT_MAX=30
RATE_LIMIT_CHAT_WINDOW=60

# Redis配置（用于分布式限流）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

## 使用方法

### 1. 导入装饰器

```python
from src.middleware.rate_limit import rate_limit
```

### 2. 应用到API路由

```python
from flask import Blueprint
from src.middleware.rate_limit import rate_limit

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
@rate_limit('login')
def login():
    """登录接口 - 每分钟最多5次请求"""
    # 处理登录逻辑
    pass

@user_bp.route('/register', methods=['POST'])
@rate_limit('register')
def register():
    """注册接口 - 每分钟最多3次请求"""
    # 处理注册逻辑
    pass

@user_bp.route('/upload', methods=['POST'])
@rate_limit('upload')
def upload_file():
    """文件上传接口 - 每分钟最多10次请求"""
    # 处理上传逻辑
    pass
```

### 3. 自定义规则

如果需要自定义限流规则，可以在 `src/config/rate_limit_config.py` 中添加：

```python
DEFAULT_RULES = {
    # ... 现有规则 ...
    'custom_rule': {
        'max_requests': 100,
        'window': 300  # 5分钟
    }
}
```

## 响应头

启用限流的API会返回以下响应头：

- `X-RateLimit-Limit`: 请求上限
- `X-RateLimit-Remaining`: 剩余请求次数
- `X-RateLimit-Reset`: 重置时间（秒）

## 超限响应

当请求超过限制时，返回以下JSON响应：

```json
{
  "success": false,
  "error": "请求过于频繁，请稍后再试",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 60
}
```

HTTP状态码：429

## 限流策略

### 基于用户ID（推荐）

如果用户已登录（有JWT token），限流基于用户ID，不同用户有独立的限流计数。

### 基于IP地址（备选）

如果用户未登录，限流基于IP地址，同一IP的所有请求共享限流计数。

## 测试

运行限流测试：

```bash
cd backend
python -m pytest tests/test_rate_limit.py -v
```

## 注意事项

1. **内存限流**：当前使用内存存储限流计数，重启服务后会清空
2. **分布式限流**：生产环境建议使用Redis存储，支持多实例部署
3. **限流键**：优先使用用户ID，未认证用户使用IP地址
4. **时间窗口**：基于滑动窗口，超时的请求记录会被自动清理

## 未来改进

- [ ] 实现Redis分布式限流
- [ ] 支持按天、按小时的限流周期
- [ ] 支持VIP用户更高限流额度
- [ ] 实现限流统计和监控
