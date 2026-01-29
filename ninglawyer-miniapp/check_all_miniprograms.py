#!/usr/bin/env python3
"""
检查所有小程序的 JS 文件语法
"""

import os
import re
from pathlib import Path

def check_js_syntax(file_path):
    """检查 JS 文件的语法"""
    print(f"\n检查: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        errors = []
        
        # 检查是否以 Page({ 或 App({ 或 Component({ 开头
        if not re.search(r'^(Page|App|Component|const|let|var|function|export)', content, re.MULTILINE):
            # 如果是配置文件，可能以 { 开头
            if not content.strip().startswith('{'):
                errors.append("文件开头不符合小程序规范")
        
        # 统计括号数量
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces != close_braces:
            errors.append(f"括号不匹配: {{ 有 {open_braces} 个, }} 有 {close_braces} 个")
        
        open_parens = content.count('(')
        close_parens = content.count(')')
        if open_parens != close_parens:
            errors.append(f"圆括号不匹配: ( 有 {open_parens} 个, ) 有 {close_parens} 个")
        
        open_brackets = content.count('[')
        close_brackets = content.count(']')
        if open_brackets != close_brackets:
            errors.append(f"方括号不匹配: [ 有 {open_brackets} 个, ] 有 {close_brackets} 个")
        
        # 检查未闭合的字符串
        single_quotes = content.count("'")
        if single_quotes % 2 != 0:
            errors.append("单引号不匹配")
        
        double_quotes = content.count('"')
        if double_quotes % 2 != 0:
            errors.append("双引号不匹配")
        
        if errors:
            print(f"  ❌ 发现 {len(errors)} 个错误:")
            for error in errors:
                print(f"     - {error}")
            return False
        else:
            print(f"  ✅ 语法正确")
            return True
            
    except Exception as e:
        print(f"  ❌ 读取文件失败: {e}")
        return False

def check_json_syntax(file_path):
    """检查 JSON 文件语法"""
    print(f"\n检查: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有注释（JSON 不支持注释）
        # 只检查行首的注释，不包括字符串中的 //
        lines = content.split('\n')
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('//'):
                print(f"  ❌ JSON 文件包含注释（不支持）")
                return False
        
        import json
        json.loads(content)
        print(f"  ✅ JSON 语法正确")
        return True
            
    except Exception as e:
        print(f"  ❌ JSON 语法错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("  检查所有小程序的代码")
    print("=" * 60)
    
    # 检查的小程序列表
    miniprogram_dirs = [
        "miniprogram",
        "lyue",
        "prevent-risk",
        "zenme-pan",
        "legal-instructor",
        "code-signing"
    ]
    
    all_js_ok = True
    all_json_ok = True
    total_js = 0
    passed_js = 0
    total_json = 0
    passed_json = 0
    
    for miniprogram_dir in miniprogram_dirs:
        if not Path(miniprogram_dir).exists():
            print(f"\n❌ {miniprogram_dir} 目录不存在")
            continue
        
        print(f"\n{'='*60}")
        print(f"  检查小程序: {miniprogram_dir}")
        print(f"{'='*60}")
        
        # 检查 JS 文件
        js_files = list(Path(miniprogram_dir).rglob("*.js"))
        for js_file in js_files:
            total_js += 1
            if check_js_syntax(js_file):
                passed_js += 1
            else:
                all_js_ok = False
        
        # 检查 JSON 文件
        json_files = list(Path(miniprogram_dir).rglob("*.json"))
        for json_file in json_files:
            total_json += 1
            if check_json_syntax(json_file):
                passed_json += 1
            else:
                all_json_ok = False
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("  检查完成")
    print("=" * 60)
    print(f"\nJS 文件:")
    print(f"  总数: {total_js}")
    print(f"  通过: {passed_js}")
    print(f"  失败: {total_js - passed_js}")
    
    print(f"\nJSON 文件:")
    print(f"  总数: {total_json}")
    print(f"  通过: {passed_json}")
    print(f"  失败: {total_json - passed_json}")
    
    if all_js_ok and all_json_ok:
        print("\n✅ 所有文件语法正确！")
        return 0
    else:
        print(f"\n❌ 存在语法错误")
        return 1

if __name__ == "__main__":
    exit(main())
