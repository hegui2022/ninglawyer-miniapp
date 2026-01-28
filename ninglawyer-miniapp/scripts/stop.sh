#!/bin/bash

# 宁律师小程序矩阵 - 停止服务脚本

echo "=================================================="
echo "宁律师小程序矩阵 - 停止服务"
echo "=================================================="

# 查找并停止服务
echo "查找运行中的服务..."
PIDS=$(ps aux | grep "python.*main.py" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "未找到运行中的服务"
else
    echo "找到以下进程："
    ps aux | grep "python.*main.py" | grep -v grep
    
    echo ""
    read -p "确认停止以上进程？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for PID in $PIDS; do
            echo "停止进程 ${PID}..."
            kill ${PID}
        done
        
        sleep 2
        
        # 检查是否还有残留进程
        REMAINING=$(ps aux | grep "python.*main.py" | grep -v grep | awk '{print $2}')
        if [ -n "$REMAINING" ]; then
            echo "强制停止残留进程..."
            pkill -9 -f "python.*main.py"
        fi
        
        echo "✓ 服务已停止"
    else
        echo "取消操作"
    fi
fi

echo ""
echo "=================================================="
