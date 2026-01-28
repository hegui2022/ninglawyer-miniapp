@echo off
REM 宁律师法律咨询小程序 - 开发环境启动脚本（Windows）

setlocal enabledelayedexpansion

echo =========================================
echo   宁律师法律咨询小程序 - 开发环境启动
echo =========================================
echo.

REM 检查 Python 版本
echo [1/6] 检查 Python 版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装，请先安装 Python 3.11+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [成功] Python 版本: !PYTHON_VERSION!
echo.

REM 检查虚拟环境
echo [2/6] 检查虚拟环境...
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    echo [成功] 虚拟环境创建完成
) else (
    echo [成功] 虚拟环境已存在
)
echo.

REM 激活虚拟环境
echo [3/6] 激活虚拟环境...
call venv\Scripts\activate.bat
echo [成功] 虚拟环境已激活
echo.

REM 安装依赖
echo [4/6] 安装依赖...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo [成功] 依赖安装完成
echo.

REM 检查环境配置文件
echo [5/6] 检查环境配置文件...
if not exist ".env" (
    echo 创建环境配置文件...
    copy .env.example .env
    echo [成功] 环境配置文件已创建: .env
    echo [提示] 请编辑 .env 文件，填写实际的配置信息
    echo.
    echo 必须配置的项：
    echo   - MODEL_API_KEY: 豆包大模型 API Key
    echo   - MODEL_BASE_URL: 豆包大模型 API 地址
    echo.
    echo 可选配置的项：
    echo   - DB_*: 数据库配置（如果不配置，使用默认配置）
    echo   - REDIS_*: Redis 配置（如果不配置，使用默认配置）
    echo.
    set /p EDIT_ENV="是否现在编辑 .env 文件？(y/n): "
    if /i "!EDIT_ENV!"=="y" (
        notepad .env
    )
) else (
    echo [成功] 环境配置文件已存在
)
echo.

REM 创建必要的目录
echo [6/6] 创建必要的目录...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
echo [成功] 目录创建完成
echo.

REM 启动服务
echo =========================================
echo   启动开发环境服务
echo =========================================
echo.

REM 检查是否需要启动数据库
set /p START_DB="是否启动 Docker 数据库服务？(y/n): "
if /i "!START_DB!"=="y" (
    docker --version >nul 2>&1
    if not errorlevel 1 (
        echo 启动 Docker 数据库服务...
        docker-compose up -d postgres redis
        echo [成功] Docker 数据库服务已启动
        echo.
        echo 等待数据库启动...
        timeout /t 5 /nobreak >nul
    ) else (
        echo [提示] Docker 未安装，跳过数据库启动
        echo [提示] 请确保数据库服务已启动，或者使用外部数据库
    )
)
echo.

REM 启动后端服务
echo 启动后端 API 服务...
python src\main.py

pause
