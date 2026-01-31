#!/bin/bash

# HTTP服务启动脚本
# 用于部署时启动Flask应用

set -e  # Exit on error

# 默认端口
DEFAULT_PORT=5000

# 解析参数
PORT=5000
while getopts "p:" opt; do
  case $opt in
    p)
      PORT=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

echo "======================================"
echo "Starting HTTP service..."
echo "======================================"
echo "Port: ${PORT}"
echo "Working Directory: $(pwd)"

# 切换到backend目录
cd backend

# 检查环境变量
if [ -z "$DATABASE_URL" ]; then
    echo "Warning: DATABASE_URL not set, using default SQLite database"
    export DATABASE_URL="sqlite:///ninglawyer.db"
fi

if [ -z "$JWT_SECRET_KEY" ]; then
    echo "Warning: JWT_SECRET_KEY not set, using default (not recommended for production)"
    export JWT_SECRET_KEY="change-this-secret-key-in-production"
fi

# 设置Flask配置
export FLASK_HOST=0.0.0.0
export FLASK_PORT=${PORT}
export FLASK_DEBUG=false

# 确保必要的目录存在
mkdir -p logs
mkdir -p uploads
mkdir -p assets

echo ""
echo "Starting Flask application..."
echo "Host: ${FLASK_HOST}"
echo "Port: ${FLASK_PORT}"
echo "Debug: ${FLASK_DEBUG}"
echo "Database: ${DATABASE_URL}"
echo "======================================"

# 启动Flask应用
exec python src/app.py
