#!/usr/bin/env python3
"""
分析括号不匹配的问题
"""

def analyze_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计括号
    open_braces = content.count('{')
    close_braces = content.count('}')
    open_parens = content.count('(')
    close_parens = content.count(')')
    
    print(f"文件: {file_path}")
    print(f"{{: {open_braces}, }}: {close_braces}")
    print(f"(: {open_parens}, ): {close_parens}")
    
    # 查找末尾是否有多余的括号
    lines = content.split('\n')
    print(f"\n文件末尾:")
    for line in lines[-10:]:
        print(line)

if __name__ == "__main__":
    analyze_file("ninglawyer-miniapp-local/ninglawyer-miniapp/legal-instructor/app.js")
