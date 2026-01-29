@echo off
chcp 65001 >nul
REM 同步脚本 - 简化版同步工具

echo ========================================
echo 同步工具
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

echo [1/3] 拉取最新代码...
git pull origin main

echo [2/3] 显示更改文件...
git diff --stat HEAD~1 HEAD

echo [3/3] 刷新微信开发者工具...

REM 检查微信开发者工具路径
if exist "%WIN_PATH%" (
    REM 刷新所有小程序项目
    for %%p in (%PROJECTS%) do (
        echo   刷新: %%p
        "%WIN_PATH%" open --project "%PROJECT_PATH%\%%p" >nul 2>&1
    )
    echo [✓] 已刷新所有小程序项目
) else (
    echo [提示] 微信开发者工具路径未配置
    echo [提示] 请在微信开发者工具中手动刷新项目
)

echo.
echo [✓] 同步完成！
echo.

timeout /t 3 >nul
