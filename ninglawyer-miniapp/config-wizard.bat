@echo off
chcp 65001 >nul
echo ========================================
echo 宁律师小程序 - 自动化工具配置向导
echo ========================================
echo.
echo 本向导将帮助您配置自动化开发工具
echo.

REM 检查配置文件是否存在
if not exist "sync-config.ini" (
    echo [错误] 找不到配置文件 sync-config.ini
    pause
    exit /b 1
)

REM 读取配置文件
for /f "tokens=1,2 delims==" %%a in ('type sync-config.ini ^| find "="') do set %%a=%%b

echo 当前配置：
echo.
echo 项目路径: %PROJECT_PATH%
echo 微信开发者工具路径: %WIN_PATH%
echo.

echo 是否需要修改配置？
echo [Y] 是，修改配置
echo [N] 否，使用当前配置
echo.

set /p modify=请输入选项 (Y/N):

if /i "%modify%"=="Y" (
    echo.
    echo ========================================
    echo 配置项目路径
    echo ========================================
    echo.
    echo 当前项目路径: %PROJECT_PATH%
    echo.
    set /p new_project_path=请输入项目路径（留空保持原值）:

    if not "%new_project_path%"=="" (
        set PROJECT_PATH=%new_project_path%
    )

    echo.
    echo ========================================
    echo 配置微信开发者工具路径
    echo ========================================
    echo.
    echo 当前路径: %WIN_PATH%
    echo.
    echo 常见安装路径：
    echo 1. C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat
    echo 2. C:\Program Files\Tencent\微信web开发者工具\cli.bat
    echo 3. D:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat
    echo.
    set /p new_wechat_path=请输入微信开发者工具 cli.bat 路径（留空保持原值）:

    if not "%new_wechat_path%"=="" (
        set WIN_PATH=%new_wechat_path%
    )

    echo.
    echo ========================================
    echo 配置监控间隔
    echo ========================================
    echo.
    echo 当前监控间隔: %MONITOR_INTERVAL% 秒
    echo.
    set /p new_interval=请输入监控间隔（秒，留空保持原值）:

    if not "%new_interval%"=="" (
        set MONITOR_INTERVAL=%new_interval%
    )

    echo.
    echo ========================================
    echo 保存配置
    echo ========================================
    echo.
    echo 正在更新配置文件...

    REM 更新配置文件
    powershell -Command "(Get-Content sync-config.ini) -replace '^PROJECT_PATH=.*$', 'PROJECT_PATH=%PROJECT_PATH%' | Set-Content sync-config.ini"
    powershell -Command "(Get-Content sync-config.ini) -replace '^WIN_PATH=.*$', 'WIN_PATH=%WIN_PATH%' | Set-Content sync-config.ini"
    powershell -Command "(Get-Content sync-config.ini) -replace '^MONITOR_INTERVAL=.*$', 'MONITOR_INTERVAL=%MONITOR_INTERVAL%' | Set-Content sync-config.ini"

    echo [✓] 配置已保存
    echo.
)

echo ========================================
echo 验证配置
echo ========================================
echo.

REM 验证项目路径
if exist "%PROJECT_PATH%" (
    echo [✓] 项目路径存在: %PROJECT_PATH%
) else (
    echo [✗] 项目路径不存在: %PROJECT_PATH%
    echo [提示] 请检查项目路径是否正确
)

REM 验证微信开发者工具路径
if exist "%WIN_PATH%" (
    echo [✓] 微信开发者工具路径存在
) else (
    echo [✗] 微信开发者工具路径不存在
    echo [提示] 请检查微信开发者工具安装路径是否正确
)

echo.
echo ========================================
echo 配置完成
echo ========================================
echo.

echo 配置摘要：
echo 项目路径: %PROJECT_PATH%
echo 微信开发者工具路径: %WIN_PATH%
echo 监控间隔: %MONITOR_INTERVAL% 秒
echo.

echo 下一步操作：
echo.
echo [1] 启动实时监控（每 %MONITOR_INTERVAL% 秒检查一次）
echo [2] 立即同步最新代码
echo [3] 打开微信开发者工具
echo [4] 查看使用指南
echo [0] 退出
echo.

set /p next_step=请输入选项 (0-4):

if "%next_step%"=="1" (
    echo.
    echo 正在启动实时监控...
    echo [提示] 按 Ctrl+C 停止监控
    echo.
    python monitor.py
    goto end
)

if "%next_step%"=="2" (
    echo.
    call sync.bat
    goto end
)

if "%next_step%"=="3" (
    echo.
    echo 正在打开微信开发者工具...
    "%WIN_PATH%" open --project "%PROJECT_PATH%\legal-instructor"
    goto end
)

if "%next_step%"=="4" (
    echo.
    echo ========================================
    echo 自动化工具使用指南
    echo ========================================
    echo.
    echo 1. 实时监控
    echo    - 运行 start.bat，选择 [1]
    echo    - 自动监控代码更新，每 %MONITOR_INTERVAL% 秒检查一次
    echo    - 发现新代码后自动拉取并刷新微信开发者工具
    echo.
    echo 2. 立即同步
    echo    - 运行 start.bat，选择 [2]
    echo    - 立即拉取最新代码并刷新微信开发者工具
    echo.
    echo 3. 快速提交
    echo    - 修改代码后，运行 quick-commit.bat
    echo    - 自动添加、提交并推送代码
    echo.
    echo 4. 查看日志
    echo    - 运行 start.bat，选择 [3]
    echo    - 查看最近 5 次提交记录
    echo.
    echo 5. 打开开发者工具
    echo    - 运行 start.bat，选择 [4]
    echo    - 快速打开微信开发者工具
    echo.
    pause
    goto end
)

:end
echo.
echo 感谢使用！
pause
