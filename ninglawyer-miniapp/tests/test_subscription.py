"""
套餐权限系统测试（简化版）
直接测试数据库、配置和权限检查逻辑
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 设置环境变量
os.environ.setdefault('DATABASE_URL', 'sqlite:///ninglawyer.db')

from sqlalchemy import text
from src.database import engine, get_db_context
from src.models.models import User, SkillPermission
from src.config.subscription import (
    SUBSCRIPTION_PLANS, 
    MODULE_TO_MINIPROGRAM, 
    check_permission, 
    get_available_modules
)
from src.utils.skill_registry import skill_registry
from src import skills  # 导入技能模块以触发注册
from loguru import logger


class SubscriptionSystemTest:
    """套餐系统测试"""
    
    def __init__(self):
        self.test_user = None
        
    def setup_test_user(self):
        """设置测试用户"""
        logger.info("🔧 设置测试用户...")
        
        with get_db_context() as session:
            # 查找测试用户
            test_user = session.execute(
                text("SELECT * FROM users WHERE phone = '13800000001'")
            ).fetchone()
            
            if test_user:
                logger.info("✅ 使用已有测试用户")
                # 创建User对象
                self.test_user = User(
                    id=test_user[0],
                    phone=test_user[6],
                    nickname=test_user[3],
                    subscription_type=test_user[9],
                    usage_stats={}
                )
            else:
                logger.error("❌ 测试用户不存在")
                return False
        
        return True
    
    def test_1_get_all_plans(self):
        """测试1：获取所有套餐配置"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 1: 获取所有套餐配置")
        logger.info("=" * 60)
        
        try:
            plans = list(SUBSCRIPTION_PLANS.values())
            logger.info(f"✅ 获取成功，共 {len(plans)} 个套餐")
            for plan in plans:
                logger.info(f"  - {plan['name']}: ¥{plan['price']}/{plan['duration']}天")
                logger.info(f"    模块: {len(plan.get('modules', []))}个")
            return True
        except Exception as e:
            logger.error(f"❌ 获取失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_2_check_permission_logic(self):
        """测试2：权限检查逻辑"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 2: 权限检查逻辑")
        logger.info("=" * 60)
        
        try:
            test_cases = [
                ("basic", "basic", True, "基础版用户访问基础版功能"),
                ("basic", "premium", False, "基础版用户访问专业版功能"),
                ("premium", "basic", True, "专业版用户访问基础版功能"),
                ("premium", "premium", True, "专业版用户访问专业版功能"),
                ("premium", "enterprise", False, "专业版用户访问企业版功能"),
                ("enterprise", "basic", True, "企业版用户访问基础版功能"),
                ("enterprise", "premium", True, "企业版用户访问专业版功能"),
                ("enterprise", "enterprise", True, "企业版用户访问企业版功能"),
            ]
            
            all_passed = True
            for user_sub, required_sub, expected, desc in test_cases:
                result = check_permission(user_sub, required_sub)
                status = "✅" if result == expected else "❌"
                if result != expected:
                    all_passed = False
                    logger.error(f"{status} {desc} - 期望 {expected}, 实际 {result}")
                else:
                    logger.info(f"{status} {desc} - {result}")
            
            return all_passed
        except Exception as e:
            logger.error(f"❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_3_get_available_modules(self):
        """测试3：获取可用模块"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 3: 获取可用模块")
        logger.info("=" * 60)
        
        try:
            # 测试不同套餐的可用模块
            for plan_id in ["basic", "premium", "enterprise"]:
                modules = get_available_modules(plan_id)
                logger.info(f"{plan_id}: {len(modules)} 个模块")
                for module in modules:
                    logger.info(f"  - {module}")
            
            return True
        except Exception as e:
            logger.error(f"❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_4_skill_registry(self):
        """测试4：技能注册表"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 4: 技能注册表")
        logger.info("=" * 60)
        
        try:
            skills = skill_registry.list_skills()
            logger.info(f"✅ 获取成功，共 {len(skills)} 个技能")
            
            for skill_name, skill in skills.items():
                required = skill.get("required_subscription", "basic")
                logger.info(f"  - {skill_name}: {skill.get('description')} (需要{required}套餐)")
            
            return True
        except Exception as e:
            logger.error(f"❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_5_permission_check_for_user(self):
        """测试5：用户权限检查"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 5: 用户权限检查")
        logger.info("=" * 60)
        
        try:
            # 设置技能注册表的数据库会话
            skill_registry.set_db_session(engine)
            
            # 检查测试用户的权限
            test_skills = [
                ("desensitize", "隐私脱敏"),
                ("civil_consult", "民事咨询"),
                ("contract_draft", "合同起草"),
                ("contract_review", "合同审查"),
            ]
            
            all_passed = True
            for skill_name, skill_desc in test_skills:
                result = skill_registry.check_user_permission(
                    skill_name, 
                    self.test_user.id if self.test_user else None
                )
                status = "✅" if result["has_permission"] else "❌"
                logger.info(f"{status} {skill_desc}: {result.get('has_permission')}")
                if not result["has_permission"]:
                    logger.info(f"  原因: {result.get('error')}")
            
            return True
        except Exception as e:
            logger.error(f"❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_6_database_data(self):
        """测试6：数据库数据验证"""
        logger.info("\n" + "=" * 60)
        logger.info("测试 6: 数据库数据验证")
        logger.info("=" * 60)
        
        try:
            with get_db_context() as session:
                # 检查用户表
                user_count = session.execute(text("SELECT COUNT(*) FROM users")).scalar()
                logger.info(f"✅ Users表: {user_count} 条记录")
                
                # 检查技能权限表
                skill_count = session.execute(text("SELECT COUNT(*) FROM skill_permissions")).scalar()
                logger.info(f"✅ SkillPermissions表: {skill_count} 条记录")
                
                # 检查测试用户的套餐信息
                if self.test_user:
                    logger.info(f"✅ 测试用户: {self.test_user.nickname}")
                    logger.info(f"  套餐: {self.test_user.subscription_type}")
                    logger.info(f"  使用统计: {self.test_user.usage_stats}")
                
                return True
        except Exception as e:
            logger.error(f"❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        logger.info("\n" + "🚀" * 30)
        logger.info("开始套餐权限系统测试")
        logger.info("🚀" * 30)
        
        # 设置测试用户
        if not self.setup_test_user():
            logger.error("无法设置测试用户，退出测试")
            return False
        
        # 运行测试
        tests = [
            ("获取套餐配置", self.test_1_get_all_plans),
            ("权限检查逻辑", self.test_2_check_permission_logic),
            ("获取可用模块", self.test_3_get_available_modules),
            ("技能注册表", self.test_4_skill_registry),
            ("用户权限检查", self.test_5_permission_check_for_user),
            ("数据库数据验证", self.test_6_database_data),
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
