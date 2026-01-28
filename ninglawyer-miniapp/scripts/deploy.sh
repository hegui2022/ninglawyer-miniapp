#!/bin/bash
#
# 宁律师法律咨询小程序矩阵 - 部署脚本
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
ENV=${1:-dev}
COMPOSE_FILE="docker-compose.yml"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN} 宁律师法律咨询小程序矩阵 - 部署 ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装${NC}"
    exit 1
fi

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: Docker Compose 未安装${NC}"
    exit 1
fi

# 创建必要的目录
echo -e "${YELLOW}创建必要的目录...${NC}"
mkdir -p logs

# 复制环境配置文件
if [ ! -f .env ]; then
    echo -e "${YELLOW}创建环境配置文件...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}请编辑 .env 文件，填写实际配置${NC}"
fi

# 停止旧容器
echo -e "${YELLOW}停止旧容器...${NC}"
docker-compose down

# 拉取最新镜像
echo -e "${YELLOW}拉取最新镜像...${NC}"
docker-compose pull

# 构建镜像
echo -e "${YELLOW}构建镜像...${NC}"
docker-compose build

# 启动服务
echo -e "${YELLOW}启动服务...${NC}"
docker-compose up -d

# 等待服务启动
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 10

# 检查服务状态
echo -e "${GREEN}检查服务状态...${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN} 部署完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "服务地址:"
echo -e "  - API: http://localhost:5000"
echo -e "  - PostgreSQL: localhost:5432"
echo -e "  - Redis: localhost:6379"
echo -e "  - Milvus: localhost:19530"
echo -e "  - Neo4j: http://localhost:7474"
echo ""
echo -e "查看日志: docker-compose logs -f"
echo -e "停止服务: ./scripts/stop.sh"
echo ""
