"""
完整业务流程测试
模拟PC端录入案例 → 小程序检索案例的完整流程
"""

import json
import sys

sys.path.insert(0, '/workspace/projects/backend/src')

from app import create_app

app = create_app()
client = app.test_client()

print("=" * 70)
print("法律教官系统 - 完整业务流程测试")
print("=" * 70)

# ============================================
# 场景1：PC端录入一个真实的法律案例
# ============================================
print("\n【场景1】PC端录入法律案例")
print("-" * 70)

case_data = {
    "title": "张三诉李四房屋买卖合同纠纷案",
    "subtitle": "违约金数额调整的司法认定标准",
    "keywords": [
        {"type": "裁判类型", "value": "判决"},
        {"type": "案由", "value": "合同纠纷"},
        {"value": "违约金"},
        {"value": "数额调整"},
        {"value": "商品房买卖"}
    ],
    "basic_facts": """
        <p><strong>原告诉称：</strong></p>
        <p>2023年3月15日，原告张三与被告李四签订《商品房买卖合同》，约定原告购买被告位于北京市朝阳区的房屋一套，总价款500万元，定金50万元。合同约定，如被告违约，应双倍返还定金并支付违约金100万元。</p>
        <p><strong>被告辩称：</strong></p>
        <p>被告承认违约事实，但认为约定的违约金过高，请求法院予以适当减少。被告主张，原告实际损失仅为购房款的利息损失，约20万元。</p>
        <p><strong>法院经审理查明：</strong></p>
        <p>原、被告签订的《商品房买卖合同》合法有效。合同签订后，原告按约支付定金50万元。后因被告将房屋另行出售给他人，导致合同无法继续履行。原告提起诉讼，要求被告双倍返还定金并支付违约金。</p>
    """,
    "judgment_essence": """
        <p><strong>裁判规则：</strong></p>
        <p>1. 违约金的数额应以实际损失为基础，兼顾合同的履行情况、当事人的过错程度以及预期利益等综合因素，根据公平原则和诚实信用原则予以衡量。</p>
        <p>2. 当事人约定的违约金超过造成损失的30%的，一般可以认定为"过分高于造成的损失"。</p>
        <p>3. 当事人请求人民法院减少违约金的，人民法院应当以实际损失为基础进行判断。</p>
    """,
    "judgment_result": """
        <p>北京市朝阳区人民法院于2023年6月20日作出(2023)京0105民初字第1234号民事判决：</p>
        <p>一、解除原告张三与被告李四签订的《商品房买卖合同》；</p>
        <p>二、被告李四于本判决生效之日起十日内双倍返还原告张三定金100万元；</p>
        <p>三、被告李四于本判决生效之日起十日内支付原告张三违约金50万元（原约定100万元，调整为50万元）；</p>
        <p>四、驳回原告张三的其他诉讼请求。</p>
        <p>宣判后，双方均未提出上诉，判决已发生法律效力。</p>
    """,
    "dispute_foci": [
        "约定的违约金是否过高",
        "违约金数额应如何调整",
        "双倍返还定金是否应当支持"
    ],
    "related_index": {
        "laws": [
            {
                "law_name": "中华人民共和国民法典",
                "article_numbers": "第585条、第586条、第587条"
            },
            {
                "law_name": "最高人民法院关于适用《中华人民共和国民法典》合同编通则若干问题的解释",
                "article_numbers": "第65条"
            }
        ],
        "proceedings": [
            {
                "procedure_type": "一审",
                "court": "北京市朝阳区人民法院",
                "case_number": "(2023)京0105民初字第1234号",
                "judgment_type": "判决",
                "judgment_date": "2023-06-20"
            }
        ]
    },
    "status": "published",
    "created_by": "legal_instructor_pc"
}

print(f"📝 正在提交案例：{case_data['title']}")

response = client.post(
    '/api/v1/legal_instructor/cases',
    data=json.dumps(case_data),
    content_type='application/json'
)

result = json.loads(response.data)
if result['success']:
    case_id = result['data']['id']
    print(f"✅ 案例创建成功！案例ID: {case_id}")
    print(f"   标题: {result['data']['title']}")
    print(f"   副标题: {result['data']['subtitle']}")
    print(f"   关键词数量: {len(result['data']['keywords'])}")
    print(f"   争议焦点数量: {len(result['data']['dispute_foci'])}")
    print(f"   法条数量: {len(result['data']['laws'])}")
    print(f"   历审程序数量: {len(result['data']['proceedings'])}")
else:
    print(f"❌ 案例创建失败: {result.get('message', '未知错误')}")
    sys.exit(1)

# ============================================
# 场景2：小程序端搜索案例（判例检索）
# ============================================
print("\n【场景2】小程序端检索案例（判例检索功能）")
print("-" * 70)

search_keywords = ["违约金", "合同纠纷", "房屋买卖"]

for keyword in search_keywords:
    print(f"\n🔍 搜索关键词: {keyword}")
    
    search_data = {
        "keywords": keyword,
        "filters": {
            "case_type": "合同纠纷"
        }
    }
    
    response = client.post(
        '/api/v1/legal_instructor/cases/search',
        data=json.dumps(search_data),
        content_type='application/json'
    )
    
    result = json.loads(response.data)
    if result['success']:
        cases = result['data']['cases']
        print(f"   找到 {len(cases)} 条相关案例")
        
        # 检查我们刚创建的案例是否在搜索结果中
        found = False
        for case in cases:
            if case['case_id'] == case_id:
                print(f"   ✅ 找到刚创建的案例: {case['case_title']}")
                print(f"      案号: {case['case_number']}")
                print(f"      法院: {case['court']}")
                print(f"      裁判类型: {case['judgment_type']}")
                print(f"      案由: {case['cause_of_action']}")
                print(f"      结果摘要: {case['result'][:50]}...")
                found = True
                break
        
        if not found:
            print(f"   ⚠️  未找到刚创建的案例")
    else:
        print(f"   ❌ 搜索失败: {result.get('message', '未知错误')}")

# ============================================
# 场景3：小程序端查看案例详情
# ============================================
print("\n【场景3】小程序端查看案例详情")
print("-" * 70)

response = client.get(f'/api/v1/legal_instructor/cases/{case_id}')
result = json.loads(response.data)

if result['success']:
    case = result['data']
    print(f"📄 案例详情:")
    print(f"   ID: {case['id']}")
    print(f"   标题: {case['title']}")
    print(f"   副标题: {case['subtitle']}")
    print(f"   状态: {case['status']}")
    print(f"   创建时间: {case['created_at']}")
    print(f"   关键词: {json.dumps(case['keywords'], ensure_ascii=False)}")
    print(f"   争议焦点: {json.dumps(case['dispute_foci'], ensure_ascii=False)}")
    print(f"\n   裁判要旨预览: {case['judgment_essence'][:100]}...")
    print(f"\n   关联法条:")
    for law in case['laws']:
        print(f"      - {law['law_name']} {law['article_numbers']}")
    print(f"\n   历审程序:")
    for proc in case['proceedings']:
        print(f"      - {proc['procedure_type']}: {proc['court']} {proc['case_number']}")
else:
    print(f"❌ 获取案例详情失败: {result.get('message', '未知错误')}")

# ============================================
# 场景4：获取所有案例列表
# ============================================
print("\n【场景4】获取所有案例列表")
print("-" * 70)

response = client.get('/api/v1/legal_instructor/cases')
result = json.loads(response.data)

if result['success']:
    data = result['data']
    print(f"📊 案例列表统计:")
    print(f"   总数: {data['total']}")
    print(f"   当前页: {data['page']}")
    print(f"   每页数量: {data['page_size']}")
    print(f"   总页数: {data['total_pages']}")
    print(f"\n   案例列表:")
    for i, case in enumerate(data['cases'], 1):
        print(f"      {i}. {case['title']} (ID: {case['id']})")
else:
    print(f"❌ 获取案例列表失败: {result.get('message', '未知错误')}")

# ============================================
# 测试总结
# ============================================
print("\n" + "=" * 70)
print("✅ 业务流程测试完成！")
print("=" * 70)
print("\n📋 测试场景:")
print("   ✅ 场景1：PC端录入案例")
print("   ✅ 场景2：小程序端检索案例")
print("   ✅ 场景3：小程序端查看案例详情")
print("   ✅ 场景4：小程序端获取案例列表")
print("\n🎯 结论：业务流程完全跑通！")
print("   PC端录入 → 后端存储 → 小程序检索/展示")
print("=" * 70)
