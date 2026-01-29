#!/usr/bin/env python3
"""
检查文件中的双引号匹配问题
"""

def check_quotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    total_double_quotes = content.count('"')
    
    if total_double_quotes % 2 != 0:
        print(f"文件: {file_path}")
        print(f"总双引号数: {total_double_quotes}")
        print(f"❌ 双引号数量不匹配（必须是偶数）")
        print("\n查找未闭合的双引号...")
        
        # 逐行检查，跟踪引号状态
        in_string = False
        escape_next = False
        
        for line_num, line in enumerate(lines, 1):
            for col_num, char in enumerate(line):
                if escape_next:
                    escape_next = False
                    continue
                
                if char == '\\':
                    escape_next = True
                    continue
                
                if char == '"':
                    in_string = not in_string
                    if not in_string:
                        print(f"  闭合双引号在第 {line_num} 行第 {col_num} 列")
                    else:
                        print(f"  开启双引号在第 {line_num} 行第 {col_num} 列")
        
        if in_string:
            print("\n❌ 找到未闭合的双引号（最后一个字符串没有闭合）")
        
        return False
    else:
        print(f"文件: {file_path}")
        print(f"总双引号数: {total_double_quotes}")
        print(f"✅ 双引号匹配")
        return True

if __name__ == "__main__":
    import sys
    
    files = [
        "miniprogram/pages/chat/chat.js",
        "ninglawyer-miniapp-local/miniprogram/pages/chat/chat.js"
    ]
    
    for file in files:
        print("=" * 60)
        check_quotes(file)
