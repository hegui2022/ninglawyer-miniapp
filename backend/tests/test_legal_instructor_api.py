"""
测试法律教官API
"""

import pytest
import json
from datetime import datetime


def test_create_legal_case(client):
    """测试创建案例"""
    test_data = {
        "title": "测试案例：张某盗窃案",
        "subtitle": "盗窃罪数额认定标准",
        "keywords": [
            {"type": "裁判类型", "value": "判决"},
            {"type": "案由", "value": "盗窃"},
            {"value": "数额认定"},
            {"value": "刑事责任"}
        ],
        "basic_facts": "<p>2023年1月，张某在北京市朝阳区某商场盗窃...</p>",
        "judgment_essence": "<p>盗窃罪的数额认定应当以实际盗窃金额为准...</p>",
        "judgment_result": "<p>北京市朝阳区人民法院于2023年3月15日作出判决...</p>",
        "dispute_foci": [
            "盗窃数额如何认定",
            "是否构成犯罪"
        ],
        "related_index": {
            "laws": [
                {
                    "law_name": "中华人民共和国刑法",
                    "article_numbers": "第264条、第265条"
                }
            ],
            "proceedings": [
                {
                    "procedure_type": "一审",
                    "court": "北京市朝阳区人民法院",
                    "case_number": "(2023)京0105刑初123号",
                    "judgment_type": "判决",
                    "judgment_date": "2023-03-15"
                }
            ]
        },
        "status": "published",
        "created_by": "test_user"
    }

    response = client.post('/api/v1/legal_instructor/cases', 
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'case_id' in data.get('data', {}) or 'id' in data.get('data', {})
    print(f"✓ 创建案例成功: {data.get('data', {}).get('title', 'N/A')}")


def test_get_cases(client):
    """测试获取案例列表"""
    response = client.get('/api/v1/legal_instructor/cases')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'cases' in data.get('data', {})
    print(f"✓ 获取案例列表成功: 共{len(data.get('data', {}).get('cases', []))}条案例")


def test_search_cases(client):
    """测试搜索案例"""
    search_data = {
        "keywords": "盗窃",
        "filters": {
            "case_type": "盗窃"
        }
    }
    
    response = client.post('/api/v1/legal_instructor/cases/search',
                          data=json.dumps(search_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'cases' in data.get('data', {})
    print(f"✓ 搜索案例成功: 找到{len(data.get('data', {}).get('cases', []))}条相关案例")


if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/workspace/projects/backend/src')
    
    from app import create_app
    app = create_app()
    client = app.test_client()
    
    print("=" * 60)
    print("开始测试法律教官API")
    print("=" * 60)
    
    try:
        print("\n1. 测试创建案例...")
        test_create_legal_case(client)
        
        print("\n2. 测试获取案例列表...")
        test_get_cases(client)
        
        print("\n3. 测试搜索案例...")
        test_search_cases(client)
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
