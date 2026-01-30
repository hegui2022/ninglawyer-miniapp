# 宁律师法律咨询小程序 - 部署文档

## 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 2GB 内存
- 至少 10GB 可用磁盘空间

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd ninglawyer-miniapp
```

### 2. 配置环境变量

```bash
# 复制环境配置文件
cp .env.production .env

# 编辑配置文件，修改以下重要配置：
# - POSTGRES_PASSWORD: 数据库密码
# - SECRET_KEY: 应用密钥
# - JWT_SECRET_KEY: JWT 密钥
# - WECHAT_APP_ID: 微信小程序 AppID
# - WECHAT_APP_SECRET: 微信小程序 AppSecret
```

### 3. 部署服务

```bash
# 赋予部署脚本执行权限
chmod +x deploy.sh

# 执行部署脚本
./deploy.sh
```

或手动部署：

```bash
# 停止现有容器
docker-compose down

# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 4. 验证部署

```bash
# 检查服务状态
docker-compose ps

# 健康检查
curl http://localhost:5000/health
```

## 服务说明

### 核心服务

1. **app**: 主应用服务
   - 端口: 5000
   - 提供所有 API 接口

2. **postgres**: PostgreSQL 数据库
   - 端口: 5432
   - 存储用户、会话、消息等数据

3. **redis**: Redis 缓存
   - 端口: 6379
   - 用于缓存和 Celery 消息队列

4. **celery-worker**: Celery 异步任务处理器
   - 处理异步任务（通知、备份等）

5. **celery-beat**: Celery 定时任务调度器
   - 执行定时任务（清理过期会话等）

6. **nginx**: 反向代理（生产环境）
   - 端口: 80, 443
   - 提供 HTTPS 支持

## 目录结构

```
ninglawyer-miniapp/
├── src/                    # 源代码
│   ├── agents/            # 智能体
│   ├── api/               # API 接口
│   ├── skills/            # 技能模块
│   ├── services/          # 业务服务
│   ├── models/            # 数据模型
│   ├── crud/              # 数据库操作
│   ├── middleware/        # 中间件
│   ├── tasks/             # 异步任务
│   ├── storage/           # 存储模块
│   └── utils/             # 工具类
├── miniprogram/           # 微信小程序前端
├── logs/                  # 日志文件
├── uploads/               # 上传文件
├── ssl/                   # SSL 证书
├── docker-compose.yml     # Docker Compose 配置
├── Dockerfile             # Docker 镜像配置
└── nginx.conf             # Nginx 配置
```

## 常用命令

### 服务管理

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f [service_name]

# 进入容器
docker-compose exec app bash
```

### 数据库操作

```bash
# 初始化数据库
docker-compose exec app python -c "from src.database import init_db; init_db()"

# 备份数据库
docker-compose exec postgres pg_dump -U ninglawyer ninglawyer_db > backup.sql

# 恢复数据库
docker-compose exec -T postgres psql -U ninglawyer ninglawyer_db < backup.sql
```

### 日志查看

```bash
# 查看应用日志
docker-compose logs -f app

# 查看错误日志
docker-compose logs app | grep ERROR

# 查看所有日志
docker-compose logs --tail=100 -f
```

## 生产环境配置

### SSL 证书

1. 获取 SSL 证书（推荐使用 Let's Encrypt）

```bash
# 安装 certbot
sudo apt-get install certbot

# 获取证书
sudo certbot certonly --standalone -d your-domain.com

# 复制证书
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
```

2. 修改 `nginx.conf` 中的域名配置

### 性能优化

1. **数据库连接池**

```python
# 在 database.py 中配置
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

2. **Redis 缓存**

```python
# 在 cache.py 中配置
# 默认配置已优化
```

3. **Nginx 配置**

```nginx
# 在 nginx.conf 中配置
# 已包含 Gzip 压缩和缓存设置
```

### 监控和告警

1. **应用监控**

```bash
# 健康检查
curl http://localhost:5000/health

# 查看日志
docker-compose logs -f app
```

2. **系统监控**

```bash
# 查看资源使用
docker stats

# 查看磁盘使用
df -h
```

## 故障排查

### 常见问题

1. **服务启动失败**

```bash
# 查看详细日志
docker-compose logs app

# 检查端口占用
netstat -tlnp | grep 5000
```

2. **数据库连接失败**

```bash
# 检查数据库状态
docker-compose ps postgres

# 查看数据库日志
docker-compose logs postgres
```

3. **Redis 连接失败**

```bash
# 检查 Redis 状态
docker-compose ps redis

# 测试 Redis 连接
docker-compose exec redis redis-cli ping
```

### 日志位置

- 应用日志: `logs/app.log`
- 错误日志: `logs/error.log`
- Nginx 日志: `/var/log/nginx/`

## 安全建议

1. **定期更新密钥**

```bash
# 生成新的 SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. **配置防火墙**

```bash
# 只允许必要的端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

3. **定期备份**

```bash
# 创建备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U ninglawyer ninglawyer_db > backup_$DATE.sql
EOF

# 设置定时任务
crontab -e
# 添加: 0 2 * * * /path/to/backup.sh
```

## 扩展部署

### 多实例部署

```bash
# 修改 docker-compose.yml 中的 app 服务
app:
  deploy:
    replicas: 3
  ...
```

### 负载均衡

使用 Nginx 或其他负载均衡器分发请求到多个实例。

## 技术支持

- 项目文档: [项目地址]
- 问题反馈: [Issue Tracker]
- 联系方式: support@ninglawyer.com
