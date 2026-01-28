#!/bin/bash
#
# 宁律师法律咨询小程序矩阵 - 停止脚本
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW} 宁律师法律咨询小程序矩阵 - 停止 ${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# 停止服务
echo -e "${YELLOW}停止服务...${NC}"
docker-compose down

echo ""
echo -e "${GREEN}服务已停止${NC}"
echo ""
