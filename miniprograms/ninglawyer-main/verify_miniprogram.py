#!/usr/bin/env python3
"""
验证小程序配置和文件完整性
"""

import os
import json
from pathlib import Path

def check_file_exists(file_path):
    """检查文件是否存在"""
    if file_path.exists():
        return True
    return False

def check_json_syntax(file_path):
    """检查 JSON 文件语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except Exception as e:
        print(f"    JSON 语法错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("  验证小程序配置和文件完整性")
    print("=" * 60)
    
    miniprogram_dir = Path("miniprogram")
    
    if not miniprogram_dir.exists():
        print("❌ miniprogram 目录不存在")
        return
    
    # 1. 检查核心配置文件
    print("\n1️⃣  检查核心配置文件")
    core_files = [
        "app.js",
        "app.json",
        "app.wxss",
        "sitemap.json"
    ]
    
    all_core_files_ok = True
    for file_name in core_files:
        file_path = miniprogram_dir / file_name
        if check_file_exists(file_path):
            print(f"  ✅ {file_name}")
            if file_name.endswith('.json'):
                if not check_json_syntax(file_path):
                    all_core_files_ok = False
        else:
            print(f"  ❌ {file_name} 不存在")
            all_core_files_ok = False
    
    # 2. 检查页面文件
    print("\n2️⃣  检查页面文件")
    
    with open(miniprogram_dir / "app.json", 'r', encoding='utf-8') as f:
        app_config = json.load(f)
    
    pages = app_config.get('pages', [])
    print(f"  找到 {len(pages)} 个页面")
    
    all_pages_ok = True
    for page in pages:
        page_dir = miniprogram_dir / page
        page_name = page.split('/')[-1]
        
        required_files = [
            f"{page_name}.js",
            f"{page_name}.json",
            f"{page_name}.wxml",
            f"{page_name}.wxss"
        ]
        
        page_ok = True
        for file_name in required_files:
            file_path = page_dir / file_name
            if not check_file_exists(file_path):
                print(f"  ❌ {page}/{file_name} 不存在")
                page_ok = False
                all_pages_ok = False
        
        if page_ok:
            print(f"  ✅ {page}")
    
    # 3. 检查静态资源
    print("\n3️⃣  检查静态资源")
    static_dir = miniprogram_dir / "static"
    if static_dir.exists():
        print(f"  ✅ static 目录存在")
    else:
        print(f"  ⚠️  static 目录不存在（可选）")
    
    # 4. 检查 tabBar 配置
    print("\n4️⃣  检查 tabBar 配置")
    tabBar = app_config.get('tabBar', {})
    if tabBar:
        tabBar_pages = tabBar.get('list', [])
        print(f"  配置了 {len(tabBar_pages)} 个 tabBar 页面")
        
        for tab_page in tabBar_pages:
            page_path = tab_page.get('pagePath')
            if page_path in pages:
                print(f"  ✅ {page_path}")
            else:
                print(f"  ❌ {page_path} 未在 pages 中定义")
                all_pages_ok = False
    else:
        print(f"  ⚠️  未配置 tabBar")
    
    # 5. 汇总
    print("\n" + "=" * 60)
    print("  验证结果")
    print("=" * 60)
    
    if all_core_files_ok and all_pages_ok:
        print("✅ 所有必要文件都存在，配置正确！")
        print("\n可以启动小程序了！")
        return 0
    else:
        print("❌ 存在缺失的文件或配置错误")
        return 1

if __name__ == "__main__":
    exit(main())
