#!/usr/bin/env python
"""
列出Flask应用的所有路由
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.app import create_app

app = create_app()

print("=" * 80)
print("Flask应用的所有路由")
print("=" * 80)

for rule in app.url_map.iter_rules():
    print(f"{rule.rule:50s} {rule.methods} -> {rule.endpoint}")

print("=" * 80)
