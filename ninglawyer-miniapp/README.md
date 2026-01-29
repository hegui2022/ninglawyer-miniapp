# 宁律师法律咨询小程序

一个基于 Flask 和微信小程序的智能法律服务平台，提供专业的法律咨询、合同审核、隐私脱敏等功能。

## 项目简介

宁律师法律咨询小程序是一个完全独立的法律服务平台，不依赖第三方 Bot 平台，数据私有化，成本可控。项目采用前后端分离架构，后端使用 Flask + PostgreSQL，前端使用微信小程序原生框架。

## 核心功能

### 智能体矩阵
- **主脑智能体**: 负责任务分发、上下文管理和全局协调
- **领域律师**: 民事律师、刑事律师、公司律师、劳动律师、婚姻律师、知识产权律师
- **技能模块**: 民事咨询技能、合同技能、脱敏技能

### 用户系统
- 微信一键登录
- 手机号登录
- 用户信息管理
- 用户档案管理

### 会话管理
- 多轮对话支持
- 上下文记忆
- 会话列表
- 历史消息

### 历史记录
- 咨询记录
- 合同记录
- 脱敏记录
- 数据统计

### 文件上传
- 证据文件上传
- 合同文件上传
- 文件管理
- 文件下载

## 技术栈

### 后端
- **框架**: Flask 3.0+
- **数据库**: PostgreSQL 14 + SQLAlchemy 2.0
- **缓存**: Redis 7
- **异步任务**: Celery 5.3
- **认证**: PyJWT
- **验证**: Pydantic 2.0
- **日志**: Loguru
- **加密**: Cryptography

### 前端
- **框架**: 微信小程序原生框架
- **状态管理**: 自定义实现
- **网络请求**: 原生 wx.request

### AI 能力
- **LLM**: 集成大语言模型服务
- **向量数据库**: Milvus
- **图数据库**: Neo4j（可选）

## 项目结构

```
ninglawyer-miniapp/
├── src/                      # 后端源码
│   ├── agents/              # 智能体模块
│   │   ├── master_agent.py  # 主脑智能体
│   │   ├── lawyer_factory.py # 律师工厂
│   │   └── ...              # 领域律师
│   ├── api/                 # API 接口
│   │   ├── user.py          # 用户 API
│   │   ├── session.py       # 会话 API
│   │   ├── records.py       # 历史记录 API
│   │   ├── files.py         # 文件 API
│   │   └── admin.py         # 管理后台 API
│   ├── skills/              # 技能模块
│   │   ├── civil_consult_skill.py
│   │   ├── contract_skill.py
│   │   └── desensitize_skill.py
│   ├── services/            # 业务服务
│   │   ├── user_service.py
│   │   ├── session_service.py
│   │   └── file_service.py
│   ├── models/              # 数据模型
│   │   ├── models.py        # ORM 模型
│   │   └── schemas.py       # Pydantic 模式
│   ├── crud/                # 数据库操作
│   │   └── crud.py
│   ├── middleware/          # 中间件
│   │   ├── error_handler.py # 错误处理
│   │   └── rate_limit.py    # 限流
│   ├── tasks/               # 异步任务
│   │   └── async_tasks.py
│   ├── storage/             # 存储模块
│   │   ├── cache.py         # Redis 缓存
│   │   ├── db.py            # 数据库连接
│   │   └── vector_store.py  # 向量存储
│   ├── utils/               # 工具类
│   │   ├── security.py      # 安全加密
│   │   ├── logger.py        # 日志工具
│   │   └── config.py        # 配置管理
│   ├── config/              # 配置文件
│   ├── main.py              # 应用入口
│   └── database.py          # 数据库初始化
├── miniprogram/             # 小程序前端
│   ├── pages/               # 页面
│   │   ├── index/           # 首页
│   │   ├── consultation/    # 咨询页面
│   │   ├── contract/        # 合同页面
│   │   ├── desensitize/     # 脱敏页面
│   │   ├── history/         # 历史记录
│   │   ├── profile/         # 个人中心
│   │   ├── login/           # 登录页面
│   │   └── session/         # 会话页面
│   ├── static/              # 静态资源
│   ├── app.js               # 应用逻辑
│   ├── app.json             # 应用配置
│   └── app.wxss             # 应用样式
├── scripts/                 # 脚本
├── tests/                   # 测试
├── logs/                    # 日志文件
├── uploads/                 # 上传文件
├── docker-compose.yml       # Docker Compose 配置
├── Dockerfile               # Docker 镜像配置
├── requirements.txt         # Python 依赖
├── .env.production          # 生产环境配置
├── nginx.conf               # Nginx 配置
├── deploy.sh                # 部署脚本
└── README.md                # 项目说明
```

## 快速开始

### 环境要求

- Python 3.9+
- Docker 20.10+
- Docker Compose 2.0+
- PostgreSQL 14+
- Redis 7+

### 安装部署

1. **克隆项目**

```bash
git clone <repository-url>
cd ninglawyer-miniapp
```

2. **配置环境**

```bash
cp .env.production .env
# 编辑 .env 文件，配置必要参数
```

3. **启动服务**

```bash
# 使用 Docker Compose
chmod +x deploy.sh
./deploy.sh

# 或手动启动
docker-compose up -d
```

4. **验证部署**

```bash
curl http://localhost:5000/health
```

### 开发模式

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.production .env
# 修改 .env 文件

# 初始化数据库
python -c "from src.database import init_db; init_db()"

# 启动应用
python src/main.py
```

## API 文档

### 用户接口

- `POST /api/user/wechat-login` - 微信登录
- `POST /api/user/phone-login` - 手机号登录
- `GET /api/user/profile` - 获取用户信息
- `PUT /api/user/profile` - 更新用户信息

### 会话接口

- `POST /api/session/create` - 创建会话
- `GET /api/session/list` - 获取会话列表
- `GET /api/session/<id>/messages` - 获取会话消息
- `DELETE /api/session/<id>` - 删除会话

### 历史记录接口

- `GET /api/records/consultations` - 获取咨询记录
- `GET /api/records/contracts` - 获取合同记录
- `GET /api/records/desensitizes` - 获取脱敏记录
- `GET /api/records/stats` - 获取记录统计

### 文件接口

- `POST /api/files/upload` - 上传文件
- `GET /api/files/<id>` - 获取文件信息
- `GET /api/files/<id>/download` - 下载文件
- `DELETE /api/files/<id>` - 删除文件

### 管理后台接口

- `GET /api/admin/dashboard` - 仪表板数据
- `GET /api/admin/users` - 用户列表
- `GET /api/admin/reports` - 报告数据

## 性能优化

### 缓存策略
- Redis 缓存用户信息、会话数据
- 缓存装饰器支持灵活配置
- 缓存过期自动清理

### 异步处理
- Celery 异步任务处理
- 定时任务自动执行
- 消息队列解耦

### 数据库优化
- 连接池管理
- 索引优化
- 查询优化

## 安全加固

### 数据加密
- 敏感数据加密存储
- 密码哈希存储
- JWT Token 认证

### 访问控制
- API 限流
- 权限验证
- CORS 配置

### 日志审计
- 操作日志记录
- 错误日志监控
- 安全事件追踪

## 部署文档

详细的部署文档请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

## 测试

```bash
# 运行测试
pytest tests/

# 运行集成测试
pytest tests/integration_test.py

# 测试覆盖率
pytest --cov=src tests/
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

[MIT License](LICENSE)

## 联系方式

- 项目地址: [GitHub]
- 问题反馈: [Issues]
- 技术支持: support@ninglawyer.com

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 完成核心功能开发
- 支持生产环境部署
