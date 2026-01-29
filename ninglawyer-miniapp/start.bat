@echo off
chcp 65001 >nul
REM 一键启动自动化工具

REM 读取配置文件
for /f "tokens=1,2 delims==" %%a in ('type sync-config.ini ^| find "="') do set %%a=%%b

:menu
cls
echo ========================================
echo 宁律师小程序 - 自动化工具
echo ========================================
echo.
echo 项目路径: %PROJECT_PATH%
echo 监控间隔: %MONITOR_INTERVAL% 秒
echo.
echo 请选择操作：
echo.
echo [1] 启动实时监控（每 %MONITOR_INTERVAL% 秒检查一次）
echo [2] 立即同步最新代码
echo [3] 查看最近提交记录
echo [4] 打开微信开发者工具
echo [5] 快速提交代码
echo [6] 配置路径
echo [0] 退出
echo.
set /p choice=请输入选项 (0-6):

if "%choice%"=="1" goto monitor
if "%choice%"=="2" goto sync
if "%choice%"=="3" goto log
if "%choice%"=="4" goto open_tools
if "%choice%"=="5" goto quick_commit
if "%choice%"=="6" goto config
if "%choice%"=="0" goto end
goto invalid

:monitor
cls
echo ========================================
echo 实时监控
echo ========================================
echo.
echo [提示] 启动实时监控...
echo [提示] 按 Ctrl+C 停止监控
echo.
if exist monitor.py (
    python monitor.py
) else (
    echo [错误] 找不到 monitor.py
    echo [提示] 请检查文件是否存在
    pause
)
goto menu

:sync
cls
echo ========================================
echo 立即同步
echo ========================================
echo.
call auto-sync.bat
pause
goto menu

:log
cls
echo ========================================
echo 最近 5 次提交记录
echo ========================================
echo.
if exist "%PROJECT_PATH%" (
    cd /d "%PROJECT_PATH%"
    git log -5 --pretty=format:"%%h - %%s (%%cr)"
    echo.
) else (
    echo [错误] 项目路径不存在: %PROJECT_PATH%
)
pause
goto menu

:open_tools
cls
echo ========================================
echo 打开微信开发者工具
echo ========================================
echo.
echo [提示] 正在打开微信开发者工具...
if exist "%WIN_PATH%" (
    "%WIN_PATH%" open --project "%PROJECT_PATH%\legal-instructor"
    echo [✓] 已打开法律教官小程序
) else (
    echo [错误] 微信开发者工具路径不存在
    echo [提示] 请运行 config-wizard.bat 配置路径
)
pause
goto menu

:quick_commit
cls
echo ========================================
echo 快速提交代码
echo ========================================
echo.
echo [提示] 正在提交代码...
echo.
if exist "%PROJECT_PATH%" (
    cd /d "%PROJECT_PATH%"
    call quick-commit.bat
) else (
    echo [错误] 项目路径不存在: %PROJECT_PATH%
)
pause
goto menu

:config
cls
echo ========================================
echo 配置路径
echo ========================================
echo.
if exist config-wizard.bat (
    call config-wizard.bat
) else (
    echo [错误] 找不到 config-wizard.bat
)
goto menu

:invalid
cls
echo.
echo ========================================
echo [错误] 无效的选项
echo ========================================
echo.
pause
goto menu

:end
cls
echo ========================================
echo 感谢使用！
echo ========================================
echo.
echo 提示：
echo - 下次运行 start.bat 快速访问自动化工具
echo - 运行 config-wizard.bat 重新配置路径
echo - 运行 auto-sync.bat 立即同步代码
echo.
pause
