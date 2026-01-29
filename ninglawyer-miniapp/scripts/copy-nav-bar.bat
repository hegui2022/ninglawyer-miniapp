@echo off
chcp 65001 >nul
echo ========================================
echo 扣子平台小程序 nav-bar 组件修复工具
echo ========================================
echo.

set TARGET_DIR=%1

if "%TARGET_DIR%"=="" (
    echo 用法: copy-nav-bar.bat [扣子平台小程序目录]
    echo.
    echo 示例:
    echo   copy-nav-bar.bat C:\Users\YourName\Documents\coze-miniapp
    echo.
    pause
    exit /b 1
)

if not exist "%TARGET_DIR%" (
    echo 错误: 目标目录不存在
    echo %TARGET_DIR%
    pause
    exit /b 1
)

echo 目标目录: %TARGET_DIR%
echo.

:: 检查组件目录是否存在
if not exist "components\nav-bar" (
    echo 错误: 当前目录下找不到 components\nav-bar 目录
    echo 请在 ninglawyer-miniapp 目录下运行此脚本
    pause
    exit /b 1
)

echo 正在复制组件...
echo.

:: 创建目标目录
if not exist "%TARGET_DIR%\components" (
    echo 创建目录: %TARGET_DIR%\components
    mkdir "%TARGET_DIR%\components"
)

:: 复制组件
if exist "%TARGET_DIR%\components\nav-bar" (
    echo 删除旧组件...
    rmdir /s /q "%TARGET_DIR%\components\nav-bar"
)

echo 复制 nav-bar 组件...
xcopy /E /I /Y "components\nav-bar" "%TARGET_DIR%\components\nav-bar"

echo.
echo ========================================
echo ✅ 组件复制成功！
echo ========================================
echo.
echo 组件已复制到: %TARGET_DIR%\components\nav-bar
echo.
echo 下一步:
echo 1. 在微信开发者工具中打开扣子平台小程序
echo 2. 保存所有文件
echo 3. 等待自动编译
echo.
echo 如果还有其他组件缺失错误，请使用同样的方法复制其他组件。
echo.
pause
