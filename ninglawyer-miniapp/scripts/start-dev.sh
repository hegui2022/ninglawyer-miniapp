#!/bin/bash

# 宁律师法律咨询小程序 - 开发环境启动脚本

set -e

echo "========================================="
echo "  宁律师法律咨询小程序 - 开发环境启动"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Python 版本
echo -e "${YELLOW}[1/6] 检查 Python 版本...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 未安装，请先安装 Python 3.11+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓ Python 版本: $PYTHON_VERSION${NC}"
echo ""

# 检查虚拟环境
echo -e "${YELLOW}[2/6] 检查虚拟环境...${NC}"
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    echo -e "${GREEN}✓ 虚拟环境创建完成${NC}"
else
    echo -e "${GREEN}✓ 虚拟环境已存在${NC}"
fi
echo ""

# 激活虚拟环境
echo -e "${YELLOW}[3/6] 激活虚拟环境...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ 虚拟环境已激活${NC}"
echo ""

# 安装依赖
echo -e "${YELLOW}[4/6] 安装依赖...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ 依赖安装完成${NC}"
echo ""

# 检查环境配置文件
echo -e "${YELLOW}[5/6] 检查环境配置文件...${NC}"
if [ ! -f ".env" ]; then
    echo "创建环境配置文件..."
    cp .env.example .env
    echo -e "${GREEN}✓ 环境配置文件已创建: .env${NC}"
    echo -e "${YELLOW}请编辑 .env 文件，填写实际的配置信息${NC}"
    echo ""
    echo "必须配置的项："
    echo "  - MODEL_API_KEY: 豆包大模型 API Key"
    echo "  - MODEL_BASE_URL: 豆包大模型 API 地址"
    echo ""
    echo "可选配置的项："
    echo "  - DB_*: 数据库配置（如果不配置，使用默认配置）"
    echo "  - REDIS_*: Redis 配置（如果不配置，使用默认配置）"
    echo ""
    read -p "是否现在编辑 .env 文件？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-vi} .env
    fi
else
    echo -e "${GREEN}✓ 环境配置文件已存在${NC}"
fi
echo ""

# 创建必要的目录
echo -e "${YELLOW}[6/6] 创建必要的目录...${NC}"
mkdir -p logs uploads
echo -e "${GREEN}✓ 目录创建完成${NC}"
echo ""

# 启动服务
echo "========================================="
echo "  启动开发环境服务"
echo "========================================="
echo ""

# 检查是否需要启动数据库
read -p "是否启动 Docker 数据库服务？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v docker &> /dev/null; then
        echo "启动 Docker 数据库服务..."
        docker-compose up -d postgres redis
        echo -e "${GREEN}✓ Docker 数据库服务已启动${NC}"
        echo ""
        echo "等待数据库启动..."
        sleep 5
    else
        echo -e "${YELLOW}Docker 未安装，跳过数据库启动${NC}"
        echo -e "${YELLOW}请确保数据库服务已启动，或者使用外部数据库${NC}"
    fi
fi
echo ""

# 启动后端服务
echo "启动后端 API 服务..."
python src/main.py
