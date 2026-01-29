#!/bin/bash

echo "========================================"
echo "扣子平台小程序 nav-bar 组件修复工具"
echo "========================================"
echo ""

TARGET_DIR=$1

if [ -z "$TARGET_DIR" ]; then
    echo "用法: ./copy-nav-bar.sh [扣子平台小程序目录]"
    echo ""
    echo "示例:"
    echo "  ./copy-nav-bar.sh /Users/yourname/Documents/coze-miniapp"
    echo ""
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "错误: 目标目录不存在"
    echo "$TARGET_DIR"
    exit 1
fi

echo "目标目录: $TARGET_DIR"
echo ""

# 检查组件目录是否存在
if [ ! -d "components/nav-bar" ]; then
    echo "错误: 当前目录下找不到 components/nav-bar 目录"
    echo "请在 ninglawyer-miniapp 目录下运行此脚本"
    exit 1
fi

echo "正在复制组件..."
echo ""

# 创建目标目录
mkdir -p "$TARGET_DIR/components"

# 复制组件
if [ -d "$TARGET_DIR/components/nav-bar" ]; then
    echo "删除旧组件..."
    rm -rf "$TARGET_DIR/components/nav-bar"
fi

echo "复制 nav-bar 组件..."
cp -r components/nav-bar "$TARGET_DIR/components/"

echo ""
echo "========================================"
echo "✅ 组件复制成功！"
echo "========================================"
echo ""
echo "组件已复制到: $TARGET_DIR/components/nav-bar"
echo ""
echo "下一步:"
echo "1. 在微信开发者工具中打开扣子平台小程序"
echo "2. 保存所有文件"
echo "3. 等待自动编译"
echo ""
echo "如果还有其他组件缺失错误，请使用同样的方法复制其他组件。"
echo ""
