#!/usr/bin/env python3
"""
使用栈来检查括号匹配
"""

def check_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    stack = []
    brace_map = {'{': '}', '[': ']', '(': ')'}
    
    for line_num, line in enumerate(lines, 1):
        for col_num, char in enumerate(line):
            if char in brace_map:
                stack.append((line_num, col_num, char))
            elif char in brace_map.values():
                if stack:
                    expected = brace_map.get(stack[-1][2], '')
                    if char == expected:
                        stack.pop()
                    else:
                        print(f"错误: 第 {line_num} 行第 {col_num} 列")
                        print(f"  找到: '{char}'")
                        print(f"  期望: '{expected}'")
                        print(f"  栈顶: 第 {stack[-1][0]} 行第 {stack[-1][1]} 列 '{stack[-1][2]}'")
                        return False
                else:
                    print(f"错误: 第 {line_num} 行第 {col_num} 列有多余的 '{char}'")
                    return False
    
    if stack:
        print(f"未闭合的括号（共 {len(stack)} 个）:")
        for pos in stack[:10]:  # 只显示前10个
            print(f"  第 {pos[0]} 行第 {pos[1]} 列 '{pos[2]}'")
        return False
    
    print("✅ 所有括号都匹配")
    return True

if __name__ == "__main__":
    check_file("ninglawyer-miniapp-local/ninglawyer-miniapp/legal-instructor/app.js")
