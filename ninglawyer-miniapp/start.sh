#!/bin/bash
# 宁律师小程序矩阵 - 快速启动脚本

set -e

echo "======================================"
echo "宁律师小程序矩阵 - 快速启动"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Python
echo -n "检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 未安装"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

# 检查 pip
echo -n "检查 pip..."
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} pip 已安装"
else
    echo -e "${YELLOW}⚠${NC} pip 未安装，尝试安装..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# 检查虚拟环境
echo -n "检查虚拟环境..."
if [ -d "venv" ]; then
    echo -e "${GREEN}✓${NC} 虚拟环境已存在"
else
    echo -e "${YELLOW}⚠${NC} 创建虚拟环境..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} 虚拟环境已创建"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 检查依赖
echo "检查依赖..."
if pip list | grep -q "fastapi"; then
    echo -e "${GREEN}✓${NC} 依赖已安装"
else
    echo -e "${YELLOW}⚠${NC} 安装依赖..."
    pip install -r requirements.txt
    echo -e "${GREEN}✓${NC} 依赖已安装"
fi

# 检查环境配置
echo -n "检查环境配置..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} 环境配置已存在"
else
    echo -e "${YELLOW}⚠${NC} 创建环境配置..."
    cp .env.example .env
    echo -e "${GREEN}✓${NC} 环境配置已创建（请编辑 .env 文件配置必要参数）"
fi

# 检查数据库
echo -n "检查数据库连接..."
if command -v psql &> /dev/null; then
    if psql -h localhost -U postgres -d ninglawyer -c '\q' 2>/dev/null; then
        echo -e "${GREEN}✓${NC} 数据库连接正常"
    else
        echo -e "${YELLOW}⚠${NC} 数据库连接失败，请检查配置"
    fi
else
    echo -e "${YELLOW}⚠${NC} PostgreSQL 未安装"
fi

# 检查 Redis
echo -n "检查 Redis..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Redis 运行正常"
    else
        echo -e "${YELLOW}⚠${NC} Redis 未运行"
    fi
else
    echo -e "${YELLOW}⚠${NC} Redis 未安装"
fi

echo ""
echo "======================================"
echo "启动后端服务..."
echo "======================================"
echo ""

# 启动后端服务
python src/main.py
