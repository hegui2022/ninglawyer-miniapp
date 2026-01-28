@echo off
REM 一键启动监控工具

echo ========================================
echo 宁律师小程序 - 自动同步工具
echo ========================================
echo.
echo 请选择操作：
echo.
echo [1] 启动实时监控（每 30 秒检查一次）
echo [2] 立即同步最新代码
echo [3] 查看最近提交记录
echo [4] 启动微信开发者工具
echo [0] 退出
echo.
set /p choice=请输入选项 (0-4):

if "%choice%"=="1" goto monitor
if "%choice%"=="2" goto sync
if "%choice%"=="3" goto log
if "%choice%"=="4" goto open_tools
if "%choice%"=="0" goto end
goto invalid

:monitor
echo.
echo [提示] 启动实时监控...
echo [提示] 按 Ctrl+C 停止监控
echo.
if exist monitor.py (
    python monitor.py
) else (
    monitor.bat
)
goto end

:sync
echo.
call sync.bat
goto end

:log
echo.
echo ========================================
echo 最近 5 次提交记录
echo ========================================
cd C:\Users\Administrator\ninglawyer-miniapp
git log -5 --pretty=format:"%h - %s (%cr)"
echo.
pause
goto end

:open_tools
echo.
echo [提示] 正在启动微信开发者工具...
"C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat" open --project C:\Users\Administrator\ninglawyer-miniapp\legal-instructor
goto end

:invalid
echo.
echo [错误] 无效的选项
pause

:end
