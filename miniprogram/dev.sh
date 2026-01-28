#!/bin/bash

# 宁律师小程序开发启动脚本

echo "=========================================="
echo "   宁律师小程序 - 开发环境启动"
echo "=========================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装，请先安装 Python 3"
    exit 1
fi

echo "✓ Python 版本: $(python3 --version)"
echo ""

# 进入项目根目录
cd "$(dirname "$0")/.."

# 检查后端服务
if ! pgrep -f "chat_server.py" > /dev/null; then
    echo "🚀 启动后端服务..."
    python3 scripts/chat_server.py &
    BACKEND_PID=$!
    echo "✓ 后端服务已启动 (PID: $BACKEND_PID)"
    echo ""
else
    echo "✓ 后端服务已在运行"
    echo ""
fi

echo "=========================================="
echo "   接下来："
echo "=========================================="
echo ""
echo "1. 打开微信开发者工具"
echo "2. 导入项目: $(pwd)/miniprogram"
echo "3. 在'本地设置'中勾选'不校验合法域名'"
echo "4. 点击'编译'按钮"
echo ""
echo "=========================================="
echo "   访问地址"
echo "=========================================="
echo "• Web 界面: http://localhost:8000"
echo "• API 接口: http://localhost:8000/chat"
echo ""
echo "提示: 按 Ctrl+C 可停止后端服务"
echo ""

# 等待用户中断
trap "echo ''; echo '🛑 停止后端服务...'; kill $BACKEND_PID 2>/dev/null; exit 0" INT

# 保持脚本运行
wait
