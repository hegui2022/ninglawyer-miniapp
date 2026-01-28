#!/usr/bin/env python3
"""
生成公共组件脚本
"""

import os

PROJECT_ROOT = '/workspace/projects/ninglawyer-miniapp'

# 公共组件列表
COMPONENTS = [
    {
        'name': 'nav-bar',
        'description': '导航栏组件'
    },
    {
        'name': 'service-card',
        'description': '服务卡片组件'
    },
    {
        'name': 'lawyer-avatar',
        'description': '律师头像组件'
    },
    {
        'name': 'message-item',
        'description': '消息项组件'
    },
    {
        'name': 'loading',
        'description': '加载中组件'
    },
    {
        'name': 'empty',
        'description': '空状态组件'
    }
]

# 模板文件
COMPONENT_JS_TEMPLATE = """/**
 * {name} 组件
 */
Component({{
  properties: {{
    // 组件属性
  }},

  data: {{
    // 组件内部数据
  }},

  methods: {{
    // 组件方法
  }}
}});
"""

COMPONENT_WXML_TEMPLATE = """<!-- {name} 组件 -->
<view class="component-{name}">
  <!-- 组件内容 -->
</view>
"""

COMPONENT_WXSS_TEMPLATE = """/* {name} 组件样式 */
.component-{name} {{
  
}}
"""

COMPONENT_JSON_TEMPLATE = """{{
  "component": true,
  "usingComponents": {{}}
}}
"""

# 创建组件
for comp in COMPONENTS:
    component_dir = os.path.join(PROJECT_ROOT, 'components', comp['name'])
    
    if not os.path.exists(component_dir):
        os.makedirs(component_dir)
        print(f"创建组件目录: {comp['name']}")
    
    # 创建 JS 文件
    js_file = os.path.join(component_dir, f"{comp['name']}.js")
    if not os.path.exists(js_file):
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(COMPONENT_JS_TEMPLATE.format(name=comp['name']))
        print(f"  创建: {comp['name']}.js")
    
    # 创建 WXML 文件
    wxml_file = os.path.join(component_dir, f"{comp['name']}.wxml")
    if not os.path.exists(wxml_file):
        with open(wxml_file, 'w', encoding='utf-8') as f:
            f.write(COMPONENT_WXML_TEMPLATE.format(name=comp['name']))
        print(f"  创建: {comp['name']}.wxml")
    
    # 创建 WXSS 文件
    wxss_file = os.path.join(component_dir, f"{comp['name']}.wxss")
    if not os.path.exists(wxss_file):
        with open(wxss_file, 'w', encoding='utf-8') as f:
            f.write(COMPONENT_WXSS_TEMPLATE.format(name=comp['name']))
        print(f"  创建: {comp['name']}.wxss")
    
    # 创建 JSON 文件
    json_file = os.path.join(component_dir, f"{comp['name']}.json")
    if not os.path.exists(json_file):
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(COMPONENT_JSON_TEMPLATE)
        print(f"  创建: {comp['name']}.json")

print("\n公共组件创建完成！")
