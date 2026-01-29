#!/usr/bin/env python3
"""
详细定位括号位置和匹配情况
"""

def analyze_brackets():
    file_path = "ninglawyer-miniapp/legal-instructor/app.js"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    stack = []
    brace_map = {'{': '}', '[': ']', '(': ')'}
    bracket_types = {'{': '}', '}': '{', '[': ']', ']': '[', '(': ')', ')': '('}
    
    # 记录每个括号的位置
    open_positions = {}  # { 行号: 列表 of (列号, 类型) }
    close_positions = {}  # { 行号: 列表 of (列号, 类型) }
    
    for line_num, line in enumerate(lines, 1):
        for col_num, char in enumerate(line):
            if char in brace_map:
                if line_num not in open_positions:
                    open_positions[line_num] = []
                open_positions[line_num].append((col_num, char))
                stack.append((line_num, col_num, char))
            elif char in bracket_types and char not in brace_map:
                if line_num not in close_positions:
                    close_positions[line_num] = []
                close_positions[line_num].append((col_num, char))
                
                if stack:
                    last = stack[-1]
                    expected = brace_map.get(last[2], '')
                    if char == expected:
                        stack.pop()
                    else:
                        print(f"第 {line_num} 行第 {col_num} 列: 找到 '{char}'，但栈顶期望 '{expected}'")
                        print(f"  栈顶: 第 {last[0]} 行第 {last[1]} 列 '{last[2]}'")
                        return
                else:
                    print(f"第 {line_num} 行第 {col_num} 列: 多余的 '{char}'")
                    return
    
    if stack:
        print(f"未闭合的括号:")
        for pos in stack:
            print(f"  第 {pos[0]} 行第 {pos[1]} 列 '{pos[2]}'")
    
    # 统计总括号数
    total_open = sum(len(v) for v in open_positions.values())
    total_close = sum(len(v) for v in close_positions.values())
    
    print(f"\n开括号总数: {total_open}")
    print(f"闭括号总数: {total_close}")
    
    if total_open == total_close:
        print("✅ 括号匹配！")
    else:
        print(f"❌ 不匹配！相差 {total_close - total_open} 个闭括号")
    
    # 显示每个括号的位置
    print("\n开括号位置:")
    for line_num in sorted(open_positions.keys()):
        for col_num, char in open_positions[line_num]:
            print(f"  第 {line_num} 行第 {col_num} 列: '{char}'")
    
    print("\n闭括号位置:")
    for line_num in sorted(close_positions.keys()):
        for col_num, char in close_positions[line_num]:
            print(f"  第 {line_num} 行第 {col_num} 列: '{char}'")

if __name__ == "__main__":
    analyze_brackets()
