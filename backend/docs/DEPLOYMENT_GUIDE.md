# 部署指南

## 前置要求

- Python 3.9+
- PostgreSQL（生产环境）
- Redis（用于会话缓存）
- Git

## 本地开发部署

### 1. 克隆项目

```bash
git clone <repository-url>
cd ninglawyer
```

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入实际配置
nano .env
```

### 4. 初始化数据库

```bash
# 使用初始化脚本
python scripts/init_db.py
```

或手动创建表：

```bash
python -c "
from src.models.v1_models import Base
from sqlalchemy import create_engine
import os

engine = create_engine(os.getenv('DATABASE_URL'))
Base.metadata.create_all(bind=engine)
print('Database tables created successfully!')
"
```

### 5. 启动服务

```bash
# 开发模式（自动重载）
python src/main.py

# 或使用 uvicorn
uvicorn src.app:app --reload --host 0.0.0.0 --port 5000
```

### 6. 验证服务

```bash
# 健康检查
curl http://localhost:5000/health

# 测试API
curl http://localhost:5000/api/
```

## Docker 部署

### 1. 构建镜像

```bash
cd backend
docker build -t ninglawyer-backend:latest .
```

### 2. 运行容器

```bash
docker run -d \
  --name ninglawyer-backend \
  -p 5000:5000 \
  -e DATABASE_URL=postgresql://user:password@db:5432/ninglawyer \
  -e REDIS_HOST=redis \
  -e REDIS_PORT=6379 \
  -e COZE_BOT_ID=your-bot-id \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/uploads:/app/uploads \
  ninglawyer-backend:latest
```

### 3. 使用 Docker Compose

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/ninglawyer
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - COZE_BOT_ID=${COZE_BOT_ID}
    volumes:
      - ./backend/logs:/app/logs
      - ./backend/uploads:/app/uploads
    depends_on:
      - db
      - redis

  db:
    image: postgres:14
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=ninglawyer
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

启动服务：

```bash
docker-compose up -d
```

## 云平台部署

### 部署流程

1. **运行部署脚本**
   ```bash
   bash scripts/setup.sh
   ```

2. **配置环境变量**
   - 在云平台配置界面添加环境变量
   - 或上传 .env 文件

3. **部署**
   - 提交代码
   - 触发自动部署
   - 等待部署完成

### 环境变量配置

| 变量名 | 说明 | 默认值 | 必填 |
|-------|------|-------|------|
| DATABASE_URL | 数据库连接字符串 | sqlite:///ninglawyer.db | 是 |
| API_HOST | API服务地址 | 0.0.0.0 | 否 |
| API_PORT | API服务端口 | 5000 | 否 |
| JWT_SECRET_KEY | JWT密钥 | - | 是 |
| COZE_BOT_ID | 扣子机器人ID | - | 是 |
| COZE_API_KEY | 扣子API密钥 | - | 是 |
| REDIS_HOST | Redis主机地址 | localhost | 否 |
| REDIS_PORT | Redis端口 | 6379 | 否 |

## 生产环境配置

### 1. 使用 PostgreSQL

```env
DATABASE_URL=postgresql://user:password@localhost:5432/ninglawyer
```

### 2. 使用 Redis

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### 3. 配置 CORS

```env
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
```

### 4. 文件上传

```env
UPLOAD_MAX_SIZE=10485760  # 10MB
UPLOAD_PATH=/app/uploads
```

### 5. 日志配置

```env
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log
```

## 监控与日志

### 查看日志

```bash
# 实时日志
tail -f backend/logs/app.log

# 错误日志
tail -f backend/logs/error.log

# Docker容器日志
docker logs -f ninglawyer-backend
```

### 健康检查

```bash
curl http://localhost:5000/health
```

响应示例：

```json
{
  "status": "healthy",
  "timestamp": "2026-01-31T12:00:00Z",
  "database": "connected",
  "redis": "connected"
}
```

## 常见问题

### 1. 数据库连接失败

**错误信息**: `OperationalError: unable to open database file`

**解决方案**:
- 检查数据库路径是否正确
- 确保目录有写入权限
- 检查数据库服务是否运行

### 2. Redis连接失败

**错误信息**: `Error connecting to Redis`

**解决方案**:
- 检查Redis是否运行
- 确认Redis主机和端口配置
- 检查防火墙设置

### 3. 扣子API调用失败

**错误信息**: `401 Unauthorized`

**解决方案**:
- 检查COZE_BOT_ID是否正确
- 检查COZE_API_KEY是否有效
- 确认API配额是否充足

### 4. 文件上传失败

**错误信息**: `File too large`

**解决方案**:
- 检查UPLOAD_MAX_SIZE配置
- 确保上传目录有写入权限
- 检查磁盘空间是否充足

## 性能优化

### 1. 数据库优化

- 使用连接池
- 添加索引
- 定期清理日志

### 2. 缓存优化

- 启用Redis缓存
- 缓存热点数据
- 设置合理的过期时间

### 3. 并发优化

- 使用异步处理
- 增加Worker数量
- 负载均衡

## 安全建议

1. **定期更新依赖**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **使用HTTPS**
   - 配置SSL证书
   - 强制HTTPS重定向

3. **敏感信息保护**
   - 不在代码中硬编码密钥
   - 使用环境变量存储密钥
   - 定期轮换密钥

4. **访问控制**
   - 启用JWT认证
   - 实施IP白名单
   - 限制API调用频率

## 备份与恢复

### 数据库备份

```bash
# SQLite
cp backend/ninglawyer.db backup/ninglawyer-$(date +%Y%m%d).db

# PostgreSQL
pg_dump -h localhost -U postgres ninglawyer > backup/ninglawyer-$(date +%Y%m%d).sql
```

### 数据恢复

```bash
# SQLite
cp backup/ninglawyer-20260131.db backend/ninglawyer.db

# PostgreSQL
psql -h localhost -U postgres ninglawyer < backup/ninglawyer-20260131.sql
```

## 更新部署

### 1. 拉取最新代码

```bash
git pull origin main
```

### 2. 更新依赖

```bash
cd backend
pip install -r requirements.txt --upgrade
```

### 3. 运行数据库迁移（如需要）

```bash
python scripts/init_db.py
```

### 4. 重启服务

```bash
# 手动重启
pkill -f "python src/main.py"
python src/main.py

# Docker重启
docker-compose restart backend
```

---

**文档版本**: v1.0
**更新时间**: 2026-01-31
**维护人员**: Coze Coding
