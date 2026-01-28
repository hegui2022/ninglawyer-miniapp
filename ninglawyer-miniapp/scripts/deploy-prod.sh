#!/bin/bash

# 宁律师法律咨询小程序 - 生产环境部署脚本

set -e

echo "========================================="
echo "  宁律师法律咨询小程序 - 生产环境部署"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查必要的命令
echo -e "${YELLOW}[1/8] 检查必要的命令...${NC}"
commands=("docker" "docker-compose" "git")
for cmd in "${commands[@]}"; do
    if ! command -v $cmd &> /dev/null; then
        echo -e "${RED}$cmd 未安装，请先安装${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ $cmd 已安装${NC}"
done
echo ""

# 检查环境配置文件
echo -e "${YELLOW}[2/8] 检查环境配置文件...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}.env 文件不存在，请先创建 .env 文件${NC}"
    echo "复制 .env.example 到 .env，并填写实际的配置信息"
    exit 1
else
    echo -e "${GREEN}✓ .env 文件已存在${NC}"
fi
echo ""

# 检查 SSL 证书
echo -e "${YELLOW}[3/8] 检查 SSL 证书...${NC}"
if [ ! -d "nginx/ssl" ]; then
    echo "创建 SSL 证书目录..."
    mkdir -p nginx/ssl
    echo -e "${GREEN}✓ SSL 证书目录已创建${NC}"
    echo -e "${YELLOW}请将 SSL 证书文件放到 nginx/ssl 目录${NC}"
    echo "需要的文件："
    echo "  - cert.pem (证书文件)"
    echo "  - key.pem (私钥文件)"
    echo ""
    read -p "SSL 证书是否已准备好？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}请先准备好 SSL 证书${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ SSL 证书目录已存在${NC}"
fi
echo ""

# 拉取最新代码
echo -e "${YELLOW}[4/8] 拉取最新代码...${NC}"
git pull origin main
echo -e "${GREEN}✓ 代码已更新${NC}"
echo ""

# 构建镜像
echo -e "${YELLOW}[5/8] 构建 Docker 镜像...${NC}"
docker-compose build
echo -e "${GREEN}✓ 镜像构建完成${NC}"
echo ""

# 停止旧服务
echo -e "${YELLOW}[6/8] 停止旧服务...${NC}"
docker-compose down
echo -e "${GREEN}✓ 旧服务已停止${NC}"
echo ""

# 启动服务
echo -e "${YELLOW}[7/8] 启动服务...${NC}"
docker-compose up -d
echo -e "${GREEN}✓ 服务已启动${NC}"
echo ""

# 等待服务启动
echo -e "${YELLOW}[8/8] 等待服务启动...${NC}"
echo "等待 30 秒..."
sleep 30
echo ""

# 健康检查
echo "========================================="
echo "  健康检查"
echo "========================================="
echo ""

# 检查 PostgreSQL
echo "检查 PostgreSQL..."
if docker-compose exec -T postgres pg_isready -U postgres &> /dev/null; then
    echo -e "${GREEN}✓ PostgreSQL 运行正常${NC}"
else
    echo -e "${RED}✗ PostgreSQL 运行异常${NC}"
fi

# 检查 Redis
echo "检查 Redis..."
if docker-compose exec -T redis redis-cli ping &> /dev/null; then
    echo -e "${GREEN}✓ Redis 运行正常${NC}"
else
    echo -e "${RED}✗ Redis 运行异常${NC}"
fi

# 检查后端 API
echo "检查后端 API..."
if curl -f http://localhost:5000/health &> /dev/null; then
    echo -e "${GREEN}✓ 后端 API 运行正常${NC}"
else
    echo -e "${RED}✗ 后端 API 运行异常${NC}"
fi

# 检查 Nginx
echo "检查 Nginx..."
if docker-compose exec -T nginx nginx -t &> /dev/null; then
    echo -e "${GREEN}✓ Nginx 配置正常${NC}"
else
    echo -e "${RED}✗ Nginx 配置异常${NC}"
fi

echo ""
echo "========================================="
echo "  部署完成"
echo "========================================="
echo ""
echo "服务地址："
echo "  - 后端 API: http://localhost:5000"
echo "  - Nginx: http://localhost"
echo ""
echo "查看日志："
echo "  - 查看所有服务日志: docker-compose logs -f"
echo "  - 查看后端日志: docker-compose logs -f backend"
echo "  - 查看数据库日志: docker-compose logs -f postgres"
echo ""
echo "停止服务："
echo "  - docker-compose down"
echo ""
echo "重启服务："
echo "  - docker-compose restart"
echo ""
