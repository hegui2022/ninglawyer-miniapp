#!/bin/bash

# 宁律师小程序矩阵 - 启动脚本

echo "=================================================="
echo "宁律师小程序矩阵 - 启动服务"
echo "=================================================="

# 检查环境
echo "检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误：Python3 未安装"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
if [ ! -f "requirements.txt" ]; then
    echo "警告：未找到 requirements.txt"
fi

# 创建日志目录
echo "创建日志目录..."
mkdir -p /app/work/logs/bypass

# 启动后端服务
echo "启动后端服务..."
cd "$(dirname "$0")/.."

# 检查端口占用
PORT=${API_PORT:-5000}
lsof -i :${PORT} > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "端口 ${PORT} 已被占用，尝试停止旧进程..."
    pkill -f "python.*main.py"
    sleep 2
fi

# 启动服务
echo "后端服务启动中..."
nohup python3 src/main.py > /app/work/logs/bypass/app.log 2>&1 &
PID=$!

sleep 3

# 检查服务状态
if ps -p $PID > /dev/null; then
    echo "✓ 后端服务启动成功 (PID: ${PID})"
    echo "✓ 服务地址: http://localhost:${PORT}"
    echo "✓ 日志文件: /app/work/logs/bypass/app.log"
else
    echo "✗ 后端服务启动失败"
    echo "查看日志: tail -f /app/work/logs/bypass/app.log"
    exit 1
fi

echo ""
echo "=================================================="
echo "启动完成！"
echo "=================================================="
echo "后端 API: http://localhost:${PORT}"
echo "API 文档: http://localhost:${PORT}/docs"
echo "健康检查: http://localhost:${PORT}/health"
echo ""
echo "小程序开发："
echo "- 法律教官: legal-instructor/"
echo "- 码上签约: code-signing/"
echo "- 理约: manage-contract/"
echo "- 怎么判: how-to-judge/"
echo "=================================================="

# 显示实时日志
read -p "是否查看实时日志？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    tail -f /app/work/logs/bypass/app.log
fi
