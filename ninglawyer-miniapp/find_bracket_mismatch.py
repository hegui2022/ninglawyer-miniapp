#!/usr/bin/env python3
"""
检查 JS 文件的括号匹配
"""

def find_bracket_mismatch(file_path):
    """找出括号不匹配的位置"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    brace_stack = []
    paren_stack = []
    
    for line_num, line in enumerate(lines, 1):
        for col_num, char in enumerate(line, 1):
            if char == '{':
                brace_stack.append((line_num, col_num))
            elif char == '}':
                if brace_stack:
                    brace_stack.pop()
                else:
                    print(f"多余的 }} 在第 {line_num} 行，第 {col_num} 列")
            elif char == '(':
                paren_stack.append((line_num, col_num))
            elif char == ')':
                if paren_stack:
                    paren_stack.pop()
                else:
                    print(f"多余的 ) 在第 {line_num} 行，第 {col_num} 列")
    
    if brace_stack:
        print(f"\n未闭合的 {len(brace_stack)} 个 {{ :")
        for line_num, col_num in brace_stack:
            print(f"  第 {line_num} 行，第 {col_num} 列")
            if line_num > 0 and line_num <= len(lines):
                print(f"  内容: {lines[line_num-1].strip()}")
    
    if paren_stack:
        print(f"\n未闭合的 {len(paren_stack)} 个 ( :")
        for line_num, col_num in paren_stack:
            print(f"  第 {line_num} 行，第 {col_num} 列")
            if line_num > 0 and line_num <= len(lines):
                print(f"  内容: {lines[line_num-1].strip()}")

if __name__ == "__main__":
    find_bracket_mismatch("legal-instructor/app.js")
