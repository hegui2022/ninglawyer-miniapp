@echo off
REM 快速提交工具 - 自动添加、提交并推送

echo ========================================
echo 快速提交工具
echo ========================================
echo.

REM 检查是否在 Git 仓库中
if not exist ".git" (
    echo [错误] 当前目录不是 Git 仓库
    pause
    exit /b 1
)

REM 显示当前状态
echo [1/5] 检查当前状态...
git status
echo.

REM 获取提交信息
set /p commit_msg=请输入提交信息（或按回车使用默认信息）:

if "%commit_msg%"=="" (
    set commit_msg=update: 自动更新
)

REM 添加所有更改
echo [2/5] 添加更改...
git add .
echo.

REM 提交更改
echo [3/5] 提交更改...
git commit -m "%commit_msg%"
echo.

REM 推送到远程
echo [4/5] 推送到远程仓库...
git push
echo.

echo [5/5] 完成！
echo.
echo ========================================
echo 提交信息: %commit_msg%
echo ========================================
echo.
pause
