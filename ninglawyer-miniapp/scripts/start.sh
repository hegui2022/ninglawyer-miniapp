#!/bin/bash
#
# 宁律师法律咨询小程序矩阵 - 启动脚本
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN} 宁律师法律咨询小程序矩阵 - 启动 ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查 .env 文件
if [ ! -f .env ]; then
    echo -e "${RED}错误: .env 文件不存在${NC}"
    echo -e "${YELLOW}请先运行: cp .env.example .env${NC}"
    exit 1
fi

# 启动服务
echo -e "${YELLOW}启动服务...${NC}"
docker-compose up -d

# 等待服务启动
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 10

# 检查服务状态
echo -e "${GREEN}服务状态:${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}启动成功！${NC}"
echo ""
echo -e "查看日志: docker-compose logs -f"
echo -e "停止服务: ./scripts/stop.sh"
echo ""
