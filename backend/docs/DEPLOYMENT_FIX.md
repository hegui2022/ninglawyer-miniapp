# 部署问题修复记录

## 问题描述

部署时出现以下错误：

```
2026-01-31T12:45:42+08:00 error: [build] [runtime] bash: scripts/setup.sh: No such file or directory
2026-01-31T12:45:52+08:00 error: [build] [runtime] Pipeline run failed
2026-01-31T12:45:52+08:00 error: [launch] Deployment failed
```

### 根本原因

部署系统在构建 runtime 阶段尝试执行 `scripts/setup.sh` 脚本，但项目中不存在该文件。

## 解决方案

### 1. 创建 scripts/setup.sh 脚本

在项目根目录创建了 `scripts/setup.sh` 脚本，该脚本负责：

- 设置 PYTHONPATH 环境变量
- 检查和创建 .env 文件
- 检查数据库状态
- 创建必要的目录（logs、assets等）

### 2. 脚本内容

```bash
#!/bin/bash

# Setup script for deployment
# This script prepares the environment before deployment

set -e  # Exit on error

echo "======================================"
echo "Starting deployment setup..."
echo "======================================"

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend/src"
echo "PYTHONPATH set to: ${PYTHONPATH}"

# Navigate to backend directory
cd backend

echo "Current directory: $(pwd)"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found"
    echo "Creating .env from .env.example..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo ".env file created from .env.example"
    else
        echo "Error: .env.example not found"
        exit 1
    fi
fi

echo "Environment configuration: OK"

# Initialize database if needed (optional)
echo "Checking database..."
if [ -f "ninglawyer.db" ]; then
    echo "Database file exists: ninglawyer.db"
else
    echo "Database file not found. Will be created automatically on first run."
fi

# Create logs directory if it doesn't exist
if [ ! -d "logs" ]; then
    echo "Creating logs directory..."
    mkdir -p logs
    echo "Logs directory created"
fi

# Create assets directory if it doesn't exist
if [ ! -d "assets" ]; then
    echo "Creating assets directory..."
    mkdir -p assets/images
    mkdir -p assets/knowledge
    mkdir -p assets/templates
    echo "Assets directories created"
fi

echo "======================================"
echo "Deployment setup completed successfully!"
echo "======================================"

exit 0
```

### 3. 执行权限

运行以下命令给脚本添加执行权限：

```bash
chmod +x scripts/setup.sh
```

## 验证结果

运行脚本测试：

```bash
bash scripts/setup.sh
```

输出：

```
======================================
Starting deployment setup...
======================================
PYTHONPATH set to: :/workspace/projects/backend/src
Current directory: /workspace/projects/backend
Environment configuration: OK
Checking database...
Database file exists: ninglawyer.db
Creating assets directory...
Assets directories created
======================================
Deployment setup completed successfully!
======================================
```

## 项目目录结构

```
.
├── scripts/              # 部署脚本目录（新增）
│   └── setup.sh          # 部署前设置脚本（新增）
├── backend/
│   ├── scripts/          # 后端脚本
│   │   ├── init_db.py
│   │   ├── test_api.py
│   │   ├── test_voice.py
│   │   └── verify_coze_config.py
│   ├── src/
│   ├── config/
│   ├── logs/
│   ├── assets/
│   └── ...
└── ...
```

## 其他部署相关文件

### Dockerfile

位于 `backend/Dockerfile`，用于构建 Docker 镜像。

### .env 配置

部署前需要配置以下环境变量：

```env
# 数据库配置
DATABASE_URL=sqlite:///ninglawyer.db

# API配置
API_HOST=0.0.0.0
API_PORT=5000
API_PREFIX=/api

# JWT配置
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# 扣子配置
COZE_API_BASE=https://api.coze.com
COZE_BOT_ID=your-bot-id

# 其他配置
CORS_ORIGINS=["*"]
UPLOAD_MAX_SIZE=10485760
```

## 后续部署步骤

1. 确保所有环境变量已配置
2. 运行 `scripts/setup.sh` 进行初始化
3. 启动后端服务
4. 验证 API 接口

## 故障排查

如果部署仍然失败，请检查：

1. ✅ `scripts/setup.sh` 文件是否存在
2. ✅ 文件是否有执行权限（`chmod +x scripts/setup.sh`）
3. ✅ .env 文件是否配置正确
4. ✅ 网络连接是否正常（如果需要下载依赖）
5. ✅ 数据库连接配置是否正确

---

**修复时间**: 2026-01-31
**修复人员**: Coze Coding
**状态**: ✅ 已解决
