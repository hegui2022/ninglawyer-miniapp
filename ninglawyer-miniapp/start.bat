@echo off
chcp 65001 >nul
REM 宁律师法律咨询小程序 - Windows 启动脚本

echo ========================================
echo   宁律师法律咨询小程序
echo ========================================
echo.

REM 检查 Python 版本
echo 📋 检查 Python 版本...
python --version

REM 检查是否在项目根目录
if not exist "src\main.py" (
    echo ❌ 错误：请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 检查 .env 文件
if not exist ".env" (
    echo ❌ 错误：.env 文件不存在
    echo 💡 请复制 .env.example 为 .env 并配置
    pause
    exit /b 1
)

REM 检查虚拟环境（可选）
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
    echo ✅ 虚拟环境创建完成
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 📦 安装依赖...
pip install -q -r requirements.txt

REM 初始化数据库
echo 🗄️  初始化数据库...
python scripts\migrate_subscription.py

REM 创建日志目录
if not exist "logs" mkdir logs

REM 启动服务
echo.
echo ========================================
echo   启动服务
echo ========================================
echo.

python src\main.py

pause
