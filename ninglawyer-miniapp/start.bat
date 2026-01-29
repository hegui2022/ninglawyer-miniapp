@echo off
chcp 65001 >nul
REM 宁律师小程序矩阵 - 快速启动脚本（Windows）

echo ======================================
echo 宁律师小程序矩阵 - 快速启动
echo ======================================
echo.

REM 检查 Python
echo [1/8] 检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [×] Python 未安装
    echo 请先安装 Python 3.8 或更高版本
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [√] Python %PYTHON_VERSION% 已安装

REM 检查 pip
echo [2/8] 检查 pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [!] pip 未安装
) else (
    echo [√] pip 已安装
)

REM 检查虚拟环境
echo [3/8] 检查虚拟环境...
if exist venv (
    echo [√] 虚拟环境已存在
) else (
    echo [!] 创建虚拟环境...
    python -m venv venv
    echo [√] 虚拟环境已创建
)

REM 激活虚拟环境
echo [4/8] 激活虚拟环境...
call venv\Scripts\activate.bat

REM 检查依赖
echo [5/8] 检查依赖...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [!] 安装依赖...
    pip install -r requirements.txt
    echo [√] 依赖已安装
) else (
    echo [√] 依赖已安装
)

REM 检查环境配置
echo [6/8] 检查环境配置...
if exist .env (
    echo [√] 环境配置已存在
) else (
    echo [!] 创建环境配置...
    copy .env.example .env
    echo [√] 环境配置已创建（请编辑 .env 文件配置必要参数）
)

REM 检查数据库
echo [7/8] 检查数据库...
where psql >nul 2>&1
if errorlevel 1 (
    echo [!] PostgreSQL 未安装
) else (
    echo [√] PostgreSQL 已安装
)

REM 检查 Redis
echo [8/8] 检查 Redis...
where redis-cli >nul 2>&1
if errorlevel 1 (
    echo [!] Redis 未安装
) else (
    redis-cli ping >nul 2>&1
    if errorlevel 1 (
        echo [!] Redis 未运行
    ) else (
        echo [√] Redis 运行正常
    )
)

echo.
echo ======================================
echo 启动后端服务...
echo ======================================
echo.

REM 启动后端服务
python src\main.py

pause
