#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实时监控工具 - Python 版本
功能：监控 GitHub 代码仓库变化，自动提醒并支持一键同步
"""

import subprocess
import time
import json
import os
from datetime import datetime

# 配置
CONFIG = {
    'project_path': 'C:\\Users\\Administrator\\ninglawyer-miniapp',
    'monitor_interval': 30,  # 秒
    'auto_sync': False,  # 是否自动同步（建议设为 False）
}

def run_command(cmd, cwd=None):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), -1

def check_updates():
    """检查是否有更新"""
    output, code = run_command(
        'git fetch origin && git rev-list HEAD..origin/main --count',
        cwd=CONFIG['project_path']
    )

    if code != 0:
        return None

    try:
        return int(output)
    except ValueError:
        return None

def get_latest_commit():
    """获取最新提交信息"""
    output, code = run_command(
        'git log origin/main -1 --pretty=format:"%h|%s|%cr|%an"',
        cwd=CONFIG['project_path']
    )

    if code != 0:
        return None

    parts = output.split('|')
    if len(parts) == 4:
        return {
            'hash': parts[0],
            'message': parts[1],
            'time': parts[2],
            'author': parts[3]
        }
    return None

def sync_code():
    """同步代码"""
    output, code = run_command(
        'git reset --hard origin/main',
        cwd=CONFIG['project_path']
    )
    return code == 0

def show_banner():
    """显示横幅"""
    print("=" * 60)
    print("  宁律师小程序 - 实时监控工具")
    print("  监控间隔: {} 秒 | 自动同步: {}".format(
        CONFIG['monitor_interval'],
        "开启" if CONFIG['auto_sync'] else "关闭"
    ))
    print("=" * 60)
    print()

def main():
    """主函数"""
    show_banner()

    last_commit_hash = None

    print("[{}] 开始监控...".format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))

    try:
        while True:
            # 检查更新
            commit_count = check_updates()

            if commit_count is None:
                print("[警告] 无法连接到 Git 仓库，将在 {} 秒后重试...".format(
                    CONFIG['monitor_interval']
                ))
            elif commit_count > 0:
                # 获取最新提交信息
                commit_info = get_latest_commit()

                if commit_info and commit_info['hash'] != last_commit_hash:
                    print("\n" + "=" * 60)
                    print("[发现更新] {} 个新提交".format(commit_count))
                    print("=" * 60)
                    print()
                    print("最新提交:")
                    print("  - 提交哈希: {}".format(commit_info['hash']))
                    print("  - 提交信息: {}".format(commit_info['message']))
                    print("  - 提交时间: {}".format(commit_info['time']))
                    print("  - 提交作者: {}".format(commit_info['author']))
                    print()

                    # 自动同步
                    if CONFIG['auto_sync']:
                        print("[{}] 正在同步代码...".format(
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        ))

                        if sync_code():
                            print("[✓] 代码同步成功！")
                            print()
                            print("[提示] 请在微信开发者工具中刷新项目")
                            last_commit_hash = commit_info['hash']
                        else:
                            print("[✗] 代码同步失败，请手动运行 git pull")
                    else:
                        print()
                        print("[提示] 请在另一个终端运行 sync.bat 进行同步")
                        print("       或修改配置文件启用自动同步")
                        print()

                    last_commit_hash = commit_info['hash']
                    print("=" * 60 + "\n")
                else:
                    print("[{}] 检查中... 无更新".format(
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ))
            else:
                print("[{}] 检查中... 无更新".format(
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ))

            # 等待
            time.sleep(CONFIG['monitor_interval'])

    except KeyboardInterrupt:
        print("\n\n[{}] 监控已停止".format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))

if __name__ == '__main__':
    main()
