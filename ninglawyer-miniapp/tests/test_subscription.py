"""
套餐权限系统测试
测试套餐升级、权限检查、使用量限制等功能
"""

import sys
import os
import json

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from datetime import datetime, timedelta
from src.storage.db import get_db_session
from src.models.models import User
from loguru import logger

# API 基础 URL
API_BASE_URL = "http://localhost:5000"


class SubscriptionSystemTest:
    """套餐系统测试"""
    
    def __init__(self):
        self.session = get_db_session()
        self.test_user = None
        
    def setup_test_user(self):
        """创建测试用户"""
        logger.info("🔧 设置测试用户...")
        
        # 查找或创建测试用户
        test_user = self.session.query(User).filter(
            User.phone == "13800000001"
        ).first()
        
        if not test_user:
            test_user = User(
                phone="13800000001",
                nickname="测试用户",
                subscription_type="basic",
                usage_stats={}
            )
            self.session.add(test_user)
            self.session.commit()
            logger.info("✅ 创建测试用户")
        else:
            logger.info("✅ 使用已有测试用户")
        
        self.test_user = test_user
        return test_user
    
    def test_1_get_all_plans(self):
        """测试1：获取所有套餐"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 1: 获取所有套餐")
        logger.info("=" * 60)
        
        try:
            response = requests.get(f"{API_BASE_URL}/api/subscription/plans")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    plans = data.get("data", [])
                    logger.info(f"✅ 获取成功，共 {len(plans)} 个套餐")
                    for plan in plans:
                        logger.info(f"  - {plan['name']}: ¥{plan['price']}/{plan['duration']}天")
                    return True
                else:
                    logger.error(f"❌ 返回失败: {data.get('error')}")
                    return False
            else:
                logger.error(f"❌ HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 请求失败: {str(e)}")
            return False
    
    def test_2_get_user_subscription(self):
        """测试2：获取用户当前套餐"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 2: 获取用户当前套餐")
        logger.info("=" * 60)
        
        try:
            user_id = self.test_user.id
            response = requests.get(
                f"{API_BASE_URL}/api/user/subscription",
                params={"user_id": user_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    subscription = data.get("data", {})
                    logger.info(f"✅ 获取成功")
                    logger.info(f"  套餐类型: {subscription.get('subscription_name')}")
                    logger.info(f"  价格: ¥{subscription.get('subscription_price')}")
                    logger.info(f"  可用模块: {len(subscription.get('modules', []))}个")
                    return True
                else:
                    logger.error(f"❌ 返回失败: {data.get('error')}")
                    return False
            else:
                logger.error(f"❌ HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 请求失败: {str(e)}")
            return False
    
    def test_3_upgrade_subscription(self):
        """测试3：升级套餐"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 3: 升级套餐")
        logger.info("=" * 60)
        
        try:
            user_id = self.test_user.id
            
            # 先获取当前套餐
            current_subscription = self.test_user.subscription_type
            logger.info(f"当前套餐: {current_subscription}")
            
            # 确定目标套餐
            target_plan = "premium" if current_subscription == "basic" else "enterprise"
            logger.info(f"目标套餐: {target_plan}")
            
            response = requests.post(
                f"{API_BASE_URL}/api/subscription/upgrade",
                json={
                    "user_id": user_id,
                    "plan": target_plan
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    logger.info("✅ 升级成功")
                    
                    # 刷新用户数据
                    self.session.refresh(self.test_user)
                    logger.info(f"  新套餐: {self.test_user.subscription_type}")
                    return True
                else:
                    logger.error(f"❌ 升级失败: {data.get('error')}")
                    return False
            else:
                logger.error(f"❌ HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 请求失败: {str(e)}")
            return False
    
    def test_4_get_available_modules(self):
        """测试4：获取可用模块"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 4: 获取可用模块")
        logger.info("=" * 60)
        
        try:
            user_id = self.test_user.id
            response = requests.get(
                f"{API_BASE_URL}/api/subscription/modules",
                params={"user_id": user_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    modules = data.get("data", {}).get("modules", [])
                    logger.info(f"✅ 获取成功，可用模块: {len(modules)}个")
                    for module in modules:
                        logger.info(f"  - {module['name']}: {module['description']}")
                    return True
                else:
                    logger.error(f"❌ 返回失败: {data.get('error')}")
                    return False
            else:
                logger.error(f"❌ HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 请求失败: {str(e)}")
            return False
    
    def test_5_permission_check(self):
        """测试5：权限检查"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 5: 权限检查")
        logger.info("=" * 60)
        
        try:
            user_id = self.test_user.id
            
            # 测试基础套餐用户尝试使用专业版功能
            if self.test_user.subscription_type == "basic":
                logger.info("测试场景：基础套餐用户尝试使用合同起草功能")
                response = requests.post(
                    f"{API_BASE_URL}/api/consultation/consult",
                    json={
                        "user_id": user_id,
                        "domain": "contract",
                        "question": "起草一个借款合同"
                    }
                )
                
                if response.status_code == 403:
                    logger.info("✅ 权限检查生效（拒绝访问）")
                    return True
                else:
                    logger.warning(f"⚠️ 权限检查可能未生效（状态码: {response.status_code}）")
                    return False
            else:
                logger.info("当前用户套餐非基础版，跳过此测试")
                return True
                
        except Exception as e:
            logger.error(f"❌ 测试失败: {str(e)}")
            return False
    
    def test_6_downgrade_subscription(self):
        """测试6：降级套餐"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 6: 降级套餐")
        logger.info("=" * 60)
        
        try:
            user_id = self.test_user.id
            
            # 如果当前不是基础版，则降级到基础版
            if self.test_user.subscription_type != "basic":
                logger.info(f"当前套餐: {self.test_user.subscription_type}")
                logger.info("目标套餐: basic")
                
                response = requests.post(
                    f"{API_BASE_URL}/api/subscription/downgrade",
                    json={
                        "user_id": user_id,
                        "plan": "basic"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        logger.info("✅ 降级成功")
                        
                        # 刷新用户数据
                        self.session.refresh(self.test_user)
                        logger.info(f"  新套餐: {self.test_user.subscription_type}")
                        return True
                    else:
                        logger.error(f"❌ 降级失败: {data.get('error')}")
                        return False
                else:
                    logger.error(f"❌ HTTP错误: {response.status_code}")
                    return False
            else:
                logger.info("当前已是基础版，跳过降级测试")
                return True
                
        except Exception as e:
            logger.error(f"❌ 请求失败: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        logger.info("\n" + "🚀" * 30)
        logger.info("开始套餐权限系统测试")
        logger.info("🚀" * 30)
        
        # 设置测试用户
        self.setup_test_user()
        
        # 运行测试
        tests = [
            ("获取所有套餐", self.test_1_get_all_plans),
            ("获取用户套餐", self.test_2_get_user_subscription),
            ("升级套餐", self.test_3_upgrade_subscription),
            ("获取可用模块", self.test_4_get_available_modules),
            ("权限检查", self.test_5_permission_check),
            ("降级套餐", self.test_6_downgrade_subscription),
        ]
        
        results = []
        for test_name, test_func in tests:
            result = test_func()
            results.append((test_name, result))
        
        # 输出测试结果
        logger.info("\n" + "=" * 60)
        logger.info("测试结果汇总")
        logger.info("=" * 60)
        
        passed = 0
        failed = 0
        
        for test_name, result in results:
            status = "✅ 通过" if result else "❌ 失败"
            logger.info(f"{status}: {test_name}")
            if result:
                passed += 1
            else:
                failed += 1
        
        logger.info("\n" + "-" * 60)
        logger.info(f"总计: {len(results)} 个测试")
        logger.info(f"通过: {passed} 个")
        logger.info(f"失败: {failed} 个")
        logger.info(f"通过率: {passed/len(results)*100:.1f}%")
        logger.info("-" * 60)
        
        return passed == len(results)


if __name__ == "__main__":
    test = SubscriptionSystemTest()
    success = test.run_all_tests()
    
    sys.exit(0 if success else 1)
