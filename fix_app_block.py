#!/usr/bin/env python3
"""
找到并删除重复的内容
"""

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到第一个完整的 App({...}) 块
    # 从 App({ 开始，到对应的 }); 结束
    in_app = False
    brace_count = 0
    end_idx = None
    
    for i, line in enumerate(lines):
        # 检查是否是 App({
        if 'App({' in line and not in_app:
            in_app = True
            brace_count = 1
            continue
        
        if in_app:
            brace_count += line.count('{') - line.count('}')
            
            if brace_count == 0 and '});' in line:
                end_idx = i + 1  # 保留这一行
                break
    
    if end_idx is not None:
        # 只保留到 end_idx 行
        new_lines = lines[:end_idx]
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f"已修复文件: {file_path}")
        print(f"原行数: {len(lines)}")
        print(f"新行数: {len(new_lines)}")
        print(f"结束行: {end_idx}")
    else:
        print("未找到完整的 App() 块")

if __name__ == "__main__":
    fix_file("ninglawyer-miniapp-local/ninglawyer-miniapp/legal-instructor/app.js")
