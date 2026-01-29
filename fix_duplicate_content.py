#!/usr/bin/env python3
"""
删除文件中重复的内容
"""

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到第一个 });
    end_idx = None
    for i, line in enumerate(lines):
        if line.strip() == '});':
            end_idx = i
            break
    
    if end_idx is not None:
        # 只保留到 end_idx+1 行
        new_lines = lines[:end_idx+1]
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f"已修复文件: {file_path}")
        print(f"原行数: {len(lines)}")
        print(f"新行数: {len(new_lines)}")
    else:
        print("未找到结束标记 });")

if __name__ == "__main__":
    fix_file("ninglawyer-miniapp-local/ninglawyer-miniapp/legal-instructor/app.js")
