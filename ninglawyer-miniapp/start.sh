#!/bin/bash
# 宁律师法律咨询小程序 - 启动脚本

set -e

echo "========================================"
echo "  宁律师法律咨询小程序"
echo "========================================"
echo ""

# 检查 Python 版本
echo "📋 检查 Python 版本..."
python3 --version

# 检查是否在项目根目录
if [ ! -f "src/main.py" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ 错误：.env 文件不存在"
    echo "💡 请复制 .env.example 为 .env 并配置"
    exit 1
fi

# 检查虚拟环境（可选）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖..."
pip install -q -r requirements.txt

# 初始化数据库
echo "🗄️  初始化数据库..."
python3 scripts/migrate_subscription.py

# 创建日志目录
mkdir -p logs

# 启动服务
echo ""
echo "========================================"
echo "  启动服务"
echo "========================================"
echo ""

python3 src/main.py
