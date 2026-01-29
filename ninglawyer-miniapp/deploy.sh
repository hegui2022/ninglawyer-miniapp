#!/bin/bash

# 部署脚本

set -e

echo "开始部署宁律师法律咨询小程序..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 创建必要的目录
mkdir -p logs uploads ssl

# 复制环境配置
if [ ! -f .env ]; then
    echo "创建 .env 文件..."
    cp .env.production .env
    echo "警告: 请修改 .env 文件中的配置，特别是密码和密钥"
fi

# 检查 SSL 证书
if [ ! -f ssl/cert.pem ] || [ ! -f ssl/key.pem ]; then
    echo "警告: SSL 证书未找到，将使用自签名证书用于测试"
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/C=CN/ST=Beijing/L=Beijing/O=NingLawyer/OU=IT/CN=localhost"
fi

# 停止现有容器
echo "停止现有容器..."
docker-compose down

# 构建镜像
echo "构建 Docker 镜像..."
docker-compose build

# 启动服务
echo "启动服务..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "检查服务状态..."
docker-compose ps

# 初始化数据库
echo "初始化数据库..."
docker-compose exec app python -c "
from src.database import init_db
init_db()
print('数据库初始化完成')
"

echo ""
echo "======================================"
echo "部署完成！"
echo "======================================"
echo "服务地址："
echo "  - API: http://localhost:5000"
echo "  - 健康检查: http://localhost:5000/health"
echo "  - 健康检查: http://localhost/health"
echo ""
echo "查看日志："
echo "  docker-compose logs -f app"
echo ""
echo "停止服务："
echo "  docker-compose down"
echo "======================================"
