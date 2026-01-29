#!/usr/bin/env python3
"""
检查小程序 JS 文件的语法错误
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
        if not re.search(r'^(Page|App|Component)\s*\(\s*\{', content, re.MULTILINE):
            errors.append("文件未以 Page/App/Component({ 开头")
        
        # 检查是否以 }) 结尾
        if not content.rstrip().endswith('})'):
            errors.append("文件未以 }) 结尾")
        
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
        
        # 检查常见的语法错误
        if 'async ' in content and 'await ' not in content:
            errors.append("使用了 async 但没有 await")
        
        if 'await ' in content and 'async ' not in content:
            errors.append("使用了 await 但没有 async")
        
        # 检查是否有未闭合的字符串
        single_quotes = content.count("'")
        if single_quotes % 2 != 0:
            errors.append("单引号不匹配")
        
        double_quotes = content.count('"')
        if double_quotes % 2 != 0:
            errors.append("双引号不匹配")
        
        # 检查是否有未闭合的注释
        if content.count('/*') != content.count('*/'):
            errors.append("多行注释不匹配")
        
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

def main():
    """主函数"""
    print("=" * 60)
    print("  检查小程序 JS 文件语法")
    print("=" * 60)
    
    miniprogram_dir = Path("miniprogram")
    
    if not miniprogram_dir.exists():
        print("❌ miniprogram 目录不存在")
        return
    
    # 查找所有 JS 文件
    js_files = list(miniprogram_dir.rglob("*.js"))
    
    if not js_files:
        print("❌ 未找到 JS 文件")
        return
    
    print(f"\n找到 {len(js_files)} 个 JS 文件\n")
    
    # 检查每个文件
    total_files = len(js_files)
    passed_files = 0
    
    for js_file in js_files:
        if check_js_syntax(js_file):
            passed_files += 1
    
    # 汇总结果
    print("\n" + "=" * 60)
    print(f"  检查完成")
    print("=" * 60)
    print(f"总文件数: {total_files}")
    print(f"通过: {passed_files}")
    print(f"失败: {total_files - passed_files}")
    
    if passed_files == total_files:
        print("\n✅ 所有文件语法正确！")
        return 0
    else:
        print(f"\n❌ {total_files - passed_files} 个文件有语法错误")
        return 1

if __name__ == "__main__":
    exit(main())
