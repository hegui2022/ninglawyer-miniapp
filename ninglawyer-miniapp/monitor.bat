@echo off
REM 实时监控脚本 - Windows 版本
REM 功能：监控远程代码仓库变化，自动提醒更新

echo ========================================
echo 宁律师小程序实时监控工具
echo 每 30 秒检查一次更新
echo 按 Ctrl+C 停止监控
echo ========================================
echo.

:loop
cd C:\Users\Administrator\ninglawyer-miniapp

REM 拉取最新代码但不合并
git fetch origin >nul 2>&1

REM 比较本地和远程的差异
for /f %%i in ('git rev-list HEAD^..origin/main --count') do set commits=%%i

if %commits% gtr 0 (
    echo.
    echo ========================================
    echo [%time%] 发现 %commits% 个新提交！
    echo ========================================
    echo.
    echo 最新提交：
    git log origin/main -1 --pretty=format:"%%h - %%s (%%cr)"
    echo.
    echo 请手动运行 sync.bat 进行同步
    echo ========================================
    echo.
)

REM 等待 30 秒
timeout /t 30 /nobreak >nul

goto loop
