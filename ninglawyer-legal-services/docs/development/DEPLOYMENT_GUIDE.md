# 宁律师法律咨询小程序 - 独立部署指南

## 📋 部署概述

本指南提供宁律师法律咨询小程序的完整独立部署方案，包括后端 API、数据库、缓存、向量数据库和反向代理的部署。

### 架构图

```
┌─────────────┐
│  Nginx      │ ← 80/443 (HTTPS)
│  (反向代理)  │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  后端 API   │ ← 5000 (内部)
│  (Flask)    │
└──────┬──────┘
       │
       ├──────────────────┐
       ↓                  ↓
┌─────────────┐   ┌─────────────┐
│ PostgreSQL  │   │  Redis     │
│ (关系型DB)  │   │  (缓存)     │
└─────────────┘   └─────────────┘
       │                  │
       ↓                  ↓
┌─────────────┐   ┌─────────────┐
│   Milvus    │   │    S3       │
│ (向量DB)    │   │  (对象存储)  │
└─────────────┘   └─────────────┘
```

---

## 🚀 快速部署（3 步）

### 第一步：准备服务器

1. **购买服务器**
   - 推荐配置：4核8G，40G SSD
   - 操作系统：Ubuntu 22.04 LTS 或 CentOS 7+
   - 推荐：阿里云、腾讯云、华为云

2. **安装 Docker**
   ```bash
   # Ubuntu
   curl -fsSL https://get.docker.com | bash
   sudo usermod -aG docker $USER

   # 启动 Docker
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **安装 Docker Compose**
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

### 第二步：部署后端

```bash
# 1. 克隆项目
git clone https://github.com/hegui2022/ninglawyer-miniapp.git
cd ninglawyer-miniapp

# 2. 配置环境变量
cp .env.example .env
vi .env  # 编辑配置文件

# 3. 配置 SSL 证书
mkdir -p nginx/ssl
# 将 SSL 证书文件放到 nginx/ssl 目录
# 需要：cert.pem 和 key.pem

# 4. 一键部署
chmod +x scripts/deploy-prod.sh
./scripts/deploy-prod.sh
```

### 第三步：配置前端

1. 修改前端配置
   ```javascript
   // legal-instructor/utils/config.js
   const CONFIG = {
     production: {
       apiUrl: 'https://api.ninglawyer.com/api',  // 替换为你的域名
       baseUrl: 'https://api.ninglawyer.com'
     }
   };
   ```

2. 在微信公众平台配置服务器域名
   - 登录微信公众平台
   - 进入"开发" -> "开发设置"
   - 配置 request 合法域名：`https://api.ninglawyer.com`

---

## 📝 详细配置

### 1. 环境配置文件（.env）

```bash
# API 配置
API_HOST=0.0.0.0
API_PORT=5000
API_PREFIX=/api
DEBUG=False

# 数据库配置
DB_HOST=postgres
DB_PORT=5432
DB_NAME=ninglawyer
DB_USER=postgres
DB_PASSWORD=your_secure_password  # 请修改为强密码

# Redis 配置
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Milvus 配置
MILVUS_HOST=milvus-standalone
MILVUS_PORT=19530
MILVUS_COLLECTION=law_knowledge

# Neo4j 配置（可选）
NEO4J_HOST=localhost
NEO4J_PORT=7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# 对象存储 (S3)
S3_ENDPOINT=your_endpoint
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
S3_BUCKET=ninglawyer

# JWT 配置
JWT_SECRET_KEY=your_jwt_secret_key  # 请修改为随机字符串
JWT_ACCESS_TOKEN_EXPIRES=3600

# 豆包 AI 配置（必须配置）
DOUBAO_API_KEY=your_doubao_api_key  # 必须配置
DOUBAO_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# 知识库配置
KNOWLEDGE_BASE_ENDPOINT=your_kb_endpoint

# 语音服务配置（可选）
VOICE_ACCESS_KEY=your_voice_access_key
VOICE_SECRET_KEY=your_voice_secret_key

# 微信小程序配置
WECHAT_APPID=your_appid
WECHAT_SECRET=your_secret

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=/app/work/logs/bypass

# MinIO 配置（用于 Milvus）
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

### 2. Nginx 配置

编辑 `nginx/nginx.conf`，修改以下配置：

```nginx
server {
    listen 443 ssl http2;
    server_name api.ninglawyer.com;  # 替换为你的域名

    # SSL 证书配置
    ssl_certificate /etc/nginx/ssl/cert.pem;  # 替换为你的证书路径
    ssl_certificate_key /etc/nginx/ssl/key.pem;  # 替换为你的私钥路径
    ...
}
```

### 3. SSL 证书配置

**方式一：使用 Let's Encrypt（免费）**

```bash
# 安装 certbot
sudo apt-get install certbot

# 获取证书
sudo certbot certonly --standalone -d api.ninglawyer.com

# 证书位置
# /etc/letsencrypt/live/api.ninglawyer.com/fullchain.pem
# /etc/letsencrypt/live/api.ninglawyer.com/privkey.pem

# 复制到项目目录
sudo cp /etc/letsencrypt/live/api.ninglawyer.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/api.ninglawyer.com/privkey.pem nginx/ssl/key.pem
```

**方式二：使用已有证书**

将你的 SSL 证书文件放到 `nginx/ssl` 目录：
- `cert.pem` - 证书文件
- `key.pem` - 私钥文件

---

## 🔧 管理命令

### 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 启动特定服务
docker-compose up -d backend postgres redis

# 查看服务状态
docker-compose ps
```

### 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f postgres

# 查看最近 100 行日志
docker-compose logs --tail=100 backend
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

### 更新代码

```bash
# 拉取最新代码
git pull origin main

# 重新构建镜像
docker-compose build backend

# 重启服务
docker-compose up -d backend
```

---

## 📊 性能优化

### 1. 数据库优化

```sql
-- 创建索引（已在 init-db.sql 中定义）
CREATE INDEX idx_consultations_user_id ON consultations(user_id);
CREATE INDEX idx_consultations_created_at ON consultations(created_at DESC);
```

### 2. Redis 缓存

已在 `.env` 中配置 Redis，后端会自动使用缓存。

### 3. Nginx 缓存

已在 `nginx.conf` 中配置 Gzip 压缩和静态文件缓存。

### 4. 负载均衡

如果需要高可用，可以部署多个后端实例，使用 Nginx 负载均衡：

```nginx
upstream backend {
    server backend1:5000;
    server backend2:5000;
    server backend3:5000;
    least_conn;
}
```

---

## 🔒 安全配置

### 1. 防火墙配置

```bash
# Ubuntu UFW
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 2. 数据库安全

- 修改默认密码（在 .env 文件中）
- 限制数据库访问（只允许容器内部访问）
- 定期备份数据

### 3. API 安全

- 使用 JWT Token 认证
- 配置 CORS 白名单
- 限制请求频率（待实现）

---

## 📈 监控和日志

### 1. 日志查看

```bash
# 后端日志
docker-compose logs -f backend

# 数据库日志
docker-compose logs -f postgres

# Nginx 日志
docker-compose logs -f nginx
tail -f nginx/logs/access.log
tail -f nginx/logs/error.log
```

### 2. 健康检查

```bash
# 检查后端 API
curl http://localhost:5000/health

# 检查数据库
docker-compose exec postgres pg_isready -U postgres

# 检查 Redis
docker-compose exec redis redis-cli ping
```

### 3. 性能监控

可以使用以下工具：
- Prometheus + Grafana
- Datadog
- 阿里云云监控

---

## 🔄 数据备份

### 1. 数据库备份

```bash
# 备份 PostgreSQL
docker-compose exec postgres pg_dump -U postgres ninglawyer > backup_$(date +%Y%m%d).sql

# 恢复数据库
docker-compose exec -T postgres psql -U postgres ninglawyer < backup_20250109.sql
```

### 2. Redis 备份

```bash
# Redis 自动持久化（AOF）
# 数据会自动保存到 redis_data 卷
```

### 3. 定期备份脚本

创建 `scripts/backup.sh`：

```bash
#!/bin/bash
# 数据库备份
docker-compose exec postgres pg_dump -U postgres ninglawyer > /backup/ninglawyer_$(date +%Y%m%d).sql

# 删除 7 天前的备份
find /backup -name "ninglawyer_*.sql" -mtime +7 -delete
```

---

## ❓ 常见问题

### Q1: Docker 容器无法启动

**A**: 检查端口是否被占用：
```bash
sudo netstat -tulpn | grep -E ':(80|443|5000|5432|6379|19530)'
```

### Q2: 数据库连接失败

**A**: 检查数据库密码是否正确，确保 `.env` 中的 `DB_PASSWORD` 与实际一致。

### Q3: SSL 证书错误

**A**: 确保 SSL 证书路径正确，证书文件有效。

### Q4: 后端 API 响应慢

**A**:
- 检查大语言模型 API Key 是否正确
- 检查网络连接
- 考虑增加缓存

---

## 📞 技术支持

如果遇到问题，请：

1. 查看日志：`docker-compose logs -f`
2. 检查配置：`.env` 和 `nginx/nginx.conf`
3. 查看文档：本指南

---

## 📚 相关文档

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 官方文档](https://docs.docker.com/compose/)
- [Nginx 官方文档](https://nginx.org/en/docs/)
- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)

---

**部署完成后，请测试所有功能，确保正常运行！** 🎉
