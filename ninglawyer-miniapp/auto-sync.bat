@echo off
chcp 65001 >nul
REM 智能同步脚本 - 自动刷新微信开发者工具

echo ========================================
echo 智能同步工具
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

REM 拉取最新代码
echo [1/4] 检查更新...
git fetch origin >nul 2>&1

for /f %%i in ('git rev-list HEAD^..origin/main --count') do set commits=%%i

if %commits% equ 0 (
    echo [✓] 已是最新版本
    goto end
)

echo [2/4] 发现 %commits% 个新提交
echo 最新提交：
git log origin/main -1 --pretty=format:"%%h - %%s"
echo.

echo [3/4] 拉取代码...
git reset --hard origin/main

echo [4/4] 刷新微信开发者工具...

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
    echo [提示] 或按 Ctrl+S 触发重新编译
    echo [提示] 运行 config-wizard.bat 配置路径
)

echo.
echo [✓] 同步完成！
echo.

:end
timeout /t 3 >nul
