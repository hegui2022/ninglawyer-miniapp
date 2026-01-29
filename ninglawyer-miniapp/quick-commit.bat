@echo off
chcp 65001 >nul
REM 快速提交脚本 - 自动添加、提交并推送代码

echo ========================================
echo 快速提交工具
echo ========================================
echo.

REM 读取配置文件
for /f "tokens=1,2 delims==" %%a in ('type sync-config.ini ^| find "="') do set %%a=%%b

REM 检查项目路径
if not exist "%PROJECT_PATH%" (
    echo [错误] 项目路径不存在: %PROJECT_PATH%
    echo [提示] 请运行 config-wizard.bat 配置正确的路径
    pause
    exit /b 1
)

cd /d "%PROJECT_PATH%"

REM 检查是否有更改
git diff --quiet >nul 2>&1
if %errorlevel% equ 0 (
    git diff --cached --quiet >nul 2>&1
    if %errorlevel% equ 0 (
        echo [提示] 没有需要提交的更改
        goto end
    )
)

echo [1/4] 添加更改...
git add -A

echo [2/4] 查看更改文件...
git status --short
echo.

set /p commit_msg=请输入提交信息（留空使用默认）:

if "%commit_msg%"=="" (
    set commit_msg=Update code
)

echo [3/4] 提交更改...
git commit -m "%commit_msg%"

echo [4/4] 推送到远程仓库...
git push origin main

echo.
echo [✓] 提交完成！
echo.

:end
timeout /t 3 >nul
