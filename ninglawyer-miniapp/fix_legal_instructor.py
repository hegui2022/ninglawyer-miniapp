#!/usr/bin/env python3
"""
修复 legal-instructor/app.js 的括号问题
"""

def fix_file():
    file_path = "legal-instructor/app.js"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 检查末尾是否有重复的 }); 
    if len(lines) >= 2:
        last_two = lines[-2:]
        if ''.join(last_two).strip() == '});':
            print("发现末尾有重复的 });")
            # 删除最后一行
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines[:-1])
            print("已删除最后一行")
        else:
            print(f"末尾两行内容: {last_two}")
    else:
        print("文件太短")

if __name__ == "__main__":
    fix_file()
