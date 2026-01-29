#!/usr/bin/env python3
import os

def find_extra_brackets(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 逐行分析
    open_count = 0
    close_count = 0
    
    for line_num, line in enumerate(lines, 1):
        open_count += line.count('{')
        close_count += line.count('}')
        
        if close_count > open_count:
            print(f"第 {line_num} 行：多余的 }}")
            print(f"  内容: {line.strip()}")
    
    print(f"\n总计: {{ {open_count}, }} {close_count}")

if __name__ == "__main__":
    find_extra_brackets("ninglawyer-miniapp/legal-instructor/app.js")
