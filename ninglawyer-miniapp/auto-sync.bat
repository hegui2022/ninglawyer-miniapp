@echo off
REM 智能同步脚本 - 自动刷新微信开发者工具

set PROJECT_DIR=C:\Users\Administrator\ninglawyer-miniapp
set WECHAT_TOOLS_EXE="C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat"

echo ========================================
echo 智能同步工具
echo ========================================
echo.

cd %PROJECT_DIR%

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

REM 尝试刷新微信开发者工具（如果支持命令行）
if exist %WECHAT_TOOLS_EXE% (
    %WECHAT_TOOLS_EXE% open --project %PROJECT_DIR%\legal-instructor
    %WECHAT_TOOLS_EXE% open --project %PROJECT_DIR%\code-signing
    %WECHAT_TOOLS_EXE% open --project %PROJECT_DIR%\lyue
    %WECHAT_TOOLS_EXE% open --project %PROJECT_DIR%\zenme-pan
) else (
    echo [提示] 请在微信开发者工具中手动刷新项目
    echo 或按 Ctrl+S 触发重新编译
)

echo.
echo [✓] 同步完成！
echo.

:end
timeout /t 3 >nul
