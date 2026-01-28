# 快速创建所有缺失页面文件的脚本
import os
import json

# 页面配置
pages_config = {
    'code-signing': {
        'sign': {
            'js': 'Page({ data: { currentTab: 0, pendingList: [], signingList: [] }, onTabChange(e) { this.setData({ currentTab: e.detail.index }); } });',
            'json': '{"navigationBarTitleText":"签署"}'
        },
        'record': {
            'js': 'Page({ data: { recordList: [] }, onLoad() { this.loadRecords(); } });',
            'json': '{"navigationBarTitleText":"签署记录"}'
        }
    },
    'manage-contract': {
        'list': {
            'js': 'Page({ data: { contractList: [] }, onLoad() { this.loadContracts(); } });',
            'json': '{"navigationBarTitleText":"合同列表"}'
        },
        'reminder': {
            'js': 'Page({ data: { reminders: [] }, onLoad() { this.loadReminders(); } });',
            'json': '{"navigationBarTitleText":"到期提醒"}'
        }
    },
    'how-to-judge': {
        'detail': {
            'js': 'Page({ data: { caseDetail: null }, onLoad(e) { this.loadDetail(e.detail.id); } });',
            'json': '{"navigationBarTitleText":"案例详情"}'
        },
        'lawyer': {
            'js': 'Page({ data: { lawyers: [] }, onLoad() { this.loadLawyers(); } });',
            'json': '{"navigationBarTitleText":"律师推荐"}'
        }
    }
}

# 创建文件
for miniapp, pages in pages_config.items():
    for page, files in pages.items():
        page_dir = f'{miniapp}/pages/{page}'
        os.makedirs(page_dir, exist_ok=True)
        
        # 创建 JS 文件
        with open(f'{page_dir}/{page}.js', 'w', encoding='utf-8') as f:
            f.write(files.get('js', '// Page({})'))
        
        # 创建 WXML 文件
        with open(f'{page_dir}/{page}.wxml', 'w', encoding='utf-8') as f:
            f.write(f'<view class="{page}-page"><text>{page}</text></view>')
        
        # 创建 WXSS 文件
        with open(f'{page_dir}/{page}.wxss', 'w', encoding='utf-8') as f:
            f.write(f'.{page}-page {{ min-height: 100vh; }}')
        
        # 创建 JSON 文件
        with open(f'{page_dir}/{page}.json', 'w', encoding='utf-8') as f:
            json.dump(json.loads(files.get('json', '{}')), f, ensure_ascii=False, indent=2)

print("所有页面文件创建完成！")
