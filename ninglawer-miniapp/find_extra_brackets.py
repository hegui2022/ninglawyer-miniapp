#!/usr/bin/env python3
"""
找出多余的括号
"""

def find_extra_brackets(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找出所有 { 和 } 的位置
    open_braces = []
    close_braces = []
    
    for i, char in enumerate(content):
        if char == '{':
            open_braces.append(i)
        elif char == '}':
            close_braces.append(i)
    
    # 打印最后几个 }
    print(f"文件共 {len(content)} 个字符")
    print(f"{{ 共 {len(open_braces)} 个")
    print(f"}} 共 {len(close_braces)} 个")
    print(f"\n最后 5 个 }} 的位置:")
    for pos in close_braces[-5:]:
        line_num = content[:pos].count('\n') + 1
        print(f"  位置 {pos} (第 {line_num} 行): ...{content[max(0,pos-20):pos+20]}...")

if __name__ == "__main__":
    find_extra_brackets("legal-instructor/app.js")
