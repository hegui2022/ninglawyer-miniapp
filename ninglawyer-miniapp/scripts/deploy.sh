#!/bin/bash

# 宁律师小程序矩阵 - 部署脚本

echo "=================================================="
echo "宁律师小程序矩阵 - 开始部署"
echo "=================================================="

# 1. 检查 Python 环境
echo "1. 检查 Python 环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误：Python3 未安装"
    exit 1
fi

# 2. 安装依赖
echo "2. 安装依赖..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误：依赖安装失败"
    exit 1
fi

# 3. 运行测试
echo "3. 运行测试..."
python3 tests/test_all_lawyers.py
if [ $? -ne 0 ]; then
    echo "错误：测试失败"
    exit 1
fi

# 4. 创建日志目录
echo "4. 创建日志目录..."
mkdir -p /app/work/logs/bypass

# 5. 启动服务
echo "5. 启动服务..."
echo "启动后端服务..."
nohup python3 src/main.py > /app/work/logs/bypass/app.log 2>&1 &

sleep 3

# 6. 检查服务状态
echo "6. 检查服务状态..."
ps aux | grep "python3 src/main.py" | grep -v grep
if [ $? -eq 0 ]; then
    echo "✓ 后端服务启动成功"
else
    echo "✗ 后端服务启动失败"
    exit 1
fi

echo "=================================================="
echo "部署完成！"
echo "=================================================="
echo "后端服务已启动"
echo "小程序请使用微信开发者工具打开对应目录"
echo "=================================================="
