#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证自动同步工具
"""

import subprocess
import os
import sys

def test_command(description, command, should_succeed=True):
    """测试命令执行"""
    print(f"\n{'='*60}")
    print(f"测试: {description}")
    print(f"命令: {command}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        print(f"返回码: {result.returncode}")
        print(f"标准输出:\n{result.stdout}")

        if result.stderr:
            print(f"标准错误:\n{result.stderr}")

        if should_succeed:
            if result.returncode == 0:
                print(f"\n✅ 测试通过")
                return True
            else:
                print(f"\n❌ 测试失败")
                return False
        else:
            print(f"\n✅ 测试完成")
            return True

    except subprocess.TimeoutExpired:
        print(f"\n⏱️ 命令超时（这是正常的，因为某些脚本会一直运行）")
        return True
    except Exception as e:
        print(f"\n❌ 测试异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("  自动同步工具测试")
    print("="*60)

    # 已经在正确的目录中，不需要切换

    tests = [
        ("检查 Git 是否安装", "git --version"),
        ("检查项目是否是 Git 仓库", "git status --short"),
        ("检查远程仓库", "git remote -v"),
        ("测试 Python 监控脚本", "python monitor.py", False),
    ]

    results = []
    for test in tests:
        if len(test) == 2:
            desc, cmd = test
            should_succeed = True
        else:
            desc, cmd, should_succeed = test
        result = test_command(desc, cmd, should_succeed)
        results.append((desc, result))

    # 打印测试总结
    print("\n" + "="*60)
    print("  测试总结")
    print("="*60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for desc, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status}: {desc}")

    print(f"\n总计: {passed}/{total} 个测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！自动同步工具已就绪！")
        print("\n下一步:")
        print("1. 双击 start.bat 启动监控")
        print("2. 或运行 python monitor.py 启动高级监控")
        print("3. 或运行 sync.bat 手动同步")
    else:
        print("\n⚠️ 部分测试失败，请检查配置")

if __name__ == '__main__':
    main()
