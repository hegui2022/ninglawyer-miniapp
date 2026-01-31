"""
测试统一API网关
验证后端API统一功能
"""

import sys
import os
import json
import requests

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from loguru import logger

# 配置日志
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")

# API基础URL
API_BASE_URL = 'http://localhost:5000'

# 测试用例
test_cases = [
    {
        "name": "健康检查",
        "url": f"{API_BASE_URL}/health",
        "method": "GET",
        "description": "测试健康检查接口"
    },
    {
        "name": "获取技能列表",
        "url": f"{API_BASE_URL}/api/v1/skills",
        "method": "GET",
        "description": "测试获取技能列表接口"
    },
    {
        "name": "民事咨询聊天",
        "url": f"{API_BASE_URL}/api/v1/chat",
        "method": "POST",
        "data": {
            "message": "一般民事纠纷怎么处理？",
            "user_id": 1001,
            "app_id": "miniprogram_civil"
        },
        "description": "测试民事咨询小程序聊天"
    },
    {
        "name": "婚姻家事聊天",
        "url": f"{API_BASE_URL}/api/v1/chat",
        "method": "POST",
        "data": {
            "message": "我想离婚，需要什么材料？",
            "user_id": 1002,
            "app_id": "miniprogram_family"
        },
        "description": "测试婚姻家事小程序聊天"
    },
    {
        "name": "合同起草聊天",
        "url": f"{API_BASE_URL}/api/v1/chat",
        "method": "POST",
        "data": {
            "message": "帮我起草一份房屋租赁合同",
            "user_id": 1003,
            "app_id": "miniprogram_contract_draft"
        },
        "description": "测试合同起草小程序聊天"
    },
    {
        "name": "直接调用财产分割技能",
        "url": f"{API_BASE_URL}/api/v1/skills/property_division",
        "method": "POST",
        "data": {
            "message": "我们家房产和存款怎么分？",
            "user_id": 1004,
            "app_id": "miniprogram_family"
        },
        "description": "测试直接调用技能"
    }
]


def test_api():
    """测试API接口"""
    
    logger.info("=" * 60)
    logger.info("开始测试统一API网关")
    logger.info("=" * 60)
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n{'=' * 60}")
        logger.info(f"测试用例 {i}/{len(test_cases)}: {test_case['name']}")
        logger.info(f"{'=' * 60}")
        logger.info(f"描述: {test_case['description']}")
        logger.info(f"URL: {test_case['url']}")
        logger.info(f"方法: {test_case['method']}")
        
        try:
            # 发送请求
            if test_case['method'] == 'GET':
                response = requests.get(test_case['url'], timeout=120)
            else:
                response = requests.post(
                    test_case['url'],
                    json=test_case['data'],
                    timeout=120
                )
            
            # 解析响应
            result = response.json()
            
            logger.info(f"状态码: {response.status_code}")
            logger.info(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}...")
            
            # 验证结果
            if response.status_code == 200:
                if result.get('success', True):
                    logger.info(f"✅ 测试通过")
                    passed += 1
                else:
                    logger.warning(f"❌ 测试失败：业务逻辑错误")
                    logger.warning(f"   错误: {result.get('error', '未知错误')}")
                    failed += 1
            else:
                logger.warning(f"❌ 测试失败：HTTP错误")
                logger.warning(f"   状态码: {response.status_code}")
                failed += 1
        
        except requests.exceptions.ConnectionError:
            logger.error(f"❌ 测试失败：连接失败，请检查服务器是否启动")
            failed += 1
            break
        
        except requests.exceptions.Timeout:
            logger.error(f"❌ 测试失败：请求超时")
            failed += 1
        
        except Exception as e:
            logger.error(f"❌ 测试失败：{e}")
            failed += 1
    
    # 输出测试总结
    logger.info("\n" + "=" * 60)
    logger.info("测试总结")
    logger.info("=" * 60)
    logger.info(f"✅ 通过: {passed}/{len(test_cases)}")
    logger.info(f"❌ 失败: {failed}/{len(test_cases)}")
    
    if failed == 0:
        logger.info("🎉 所有测试通过！")
        return True
    else:
        logger.warning(f"⚠️  有 {failed} 个测试失败")
        return False


if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
