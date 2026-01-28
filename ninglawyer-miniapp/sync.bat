@echo off
REM 自动同步脚本 - Windows 版本
REM 功能：自动拉取 GitHub 最新代码并通知

echo ========================================
echo 宁律师小程序自动同步工具
echo ========================================
echo.

REM 检查是否在正确的目录
if not exist "ninglawyer-miniapp\.git" (
    echo [错误] 请先克隆项目到当前目录
    echo 执行命令：git clone https://github.com/hegui2022/ninglawyer-miniapp.git
    pause
    exit /b 1
)

cd ninglawyer-miniapp

REM 拉取最新代码
echo [1/3] 拉取最新代码...
git fetch origin
git reset --hard origin/main

REM 检查是否有更新
for /f %%i in ('git rev-list HEAD^..origin/main --count') do set commits=%%i

if %commits% gtr 0 (
    echo.
    echo ========================================
    echo [✓] 发现 %commits% 个新提交，已同步到本地！
    echo ========================================
    echo.
    echo 最新提交：
    git log -1 --pretty=format:"%h - %s (%cr)"
    echo.
    echo [提示] 请在微信开发者工具中刷新项目
    echo.
    choice /C YN /M "是否立即打开微信开发者工具"
    if errorlevel 2 goto end
    if errorlevel 1 open_wechat_tools
) else (
    echo.
    echo [✓] 已是最新版本，无需更新
    echo.
)

:end
pause
