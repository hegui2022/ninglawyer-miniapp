#!/usr/bin/env python3
"""
宁律师项目快速生成脚本
生成所有必要的基础文件和目录结构
"""

import os
import json

# 项目根目录
PROJECT_ROOT = '/workspace/projects/ninglawyer-miniapp'

# 必要的目录结构
DIRECTORIES = [
    'legal-instructor/pages/services',
    'legal-instructor/pages/profile',
    'legal-instructor/pages/lawyer-detail',
    'legal-instructor/components',
    'legal-instructor/images/tabbar',
    'legal-instructor/images/banners',
    'legal-instructor/images/lawyers',
    'ning-lawyer/template',
    'ning-lawyer/civil/pages',
    'ning-lawyer/criminal/pages',
    'ning-lawyer/contract/pages',
    'ning-lawyer/labor/pages',
    'ning-lawyer/company/pages',
    'ning-lawyer/ip/pages',
    'ning-lawyer/marriage/pages',
    'mashangqianyue/pages',
    'mashangqianyue/components',
    'liyue/pages',
    'liyue/components',
    'zenmepan/pages',
    'zenmepan/components',
    'fangfengxian',  # 已存在
    'assets/templates',
    'assets/knowledge',
    'assets/images',
    'components',
    'docs'
]

# 创建目录
for directory in DIRECTORIES:
    full_path = os.path.join(PROJECT_ROOT, directory)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f"创建目录: {directory}")
    else:
        print(f"目录已存在: {directory}")

print("\n目录结构创建完成！")
print(f"项目根目录: {PROJECT_ROOT}")
