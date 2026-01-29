#!/usr/bin/env python3
"""
检查并修复括号不匹配的问题
"""

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 检查文件中是否有 });
    for i, line in enumerate(lines):
        if '});,' in line:
            print(f"发现问题: 第 {i+1} 行包含 '}});,'")
            # 删除逗号
            new_line = line.replace('});,', '});')
            lines[i] = new_line
            print(f"修复后: {new_line}")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"已修复文件: {file_path}")

if __name__ == "__main__":
    fix_file("ninglawyer-miniapp-local/ninglawyer-miniapp/legal-instructor/app.js")
