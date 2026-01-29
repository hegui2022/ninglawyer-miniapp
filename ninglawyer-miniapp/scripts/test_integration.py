#!/usr/bin/env python3
"""
前后端集成测试脚本
测试套餐管理API端点是否正确工作
"""

import requests
import json
import time
import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# API 基础 URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """打印标题"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(text):
    """打印成功信息"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """打印错误信息"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    """打印信息"""
    print(f"{Colors.YELLOW}ℹ️  {text}{Colors.END}")

def test_health_check():
    """测试健康检查"""
    print_info("测试健康检查...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success(f"健康检查通过: {response.json()}")
            return True
        else:
            print_error(f"健康检查失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"健康检查异常: {str(e)}")
        return False

def test_get_plans():
    """测试获取套餐列表"""
    print_info("测试获取套餐列表...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/subscription/plans", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                plans = data.get("data", [])
                print_success(f"获取套餐列表成功: {len(plans)} 个套餐")
                for plan in plans:
                    print(f"   - {plan['name']}: ¥{plan['price']}/{plan['duration']}天 ({len(plan['modules'])}个模块)")
                return True
            else:
                print_error(f"获取套餐列表失败: {data.get('error')}")
                return False
        else:
            print_error(f"获取套餐列表失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"获取套餐列表异常: {str(e)}")
        return False

def test_get_user_subscription():
    """测试获取用户套餐"""
    print_info("测试获取用户套餐...")
    try:
        # 使用测试用户ID（需要在数据库中存在）
        response = requests.get(
            f"{API_BASE_URL}/api/subscription/user",
            params={"user_id": "1"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                subscription = data.get("data", {})
                print_success(f"获取用户套餐成功")
                print(f"   - 套餐类型: {subscription.get('subscription_name')}")
                print(f"   - 到期时间: {subscription.get('subscription_end_at')}")
                print(f"   - 可用模块: {len(subscription.get('modules', []))}个")
                return True
            else:
                print_error(f"获取用户套餐失败: {data.get('error')}")
                return False
        else:
            print_error(f"获取用户套餐失败: HTTP {response.status_code}")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print_error(f"获取用户套餐异常: {str(e)}")
        return False

def test_upgrade_subscription():
    """测试升级套餐"""
    print_info("测试升级套餐...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/subscription/upgrade",
            json={
                "user_id": "1",
                "plan": "premium"
            },
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success(f"升级套餐成功")
                return True
            else:
                print_error(f"升级套餐失败: {data.get('error')}")
                return False
        else:
            print_error(f"升级套餐失败: HTTP {response.status_code}")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print_error(f"升级套餐异常: {str(e)}")
        return False

def test_get_modules():
    """测试获取可用模块"""
    print_info("测试获取可用模块...")
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/subscription/modules",
            params={"user_id": "1"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                modules = data.get("data", {}).get("modules", [])
                print_success(f"获取可用模块成功: {len(modules)} 个模块")
                for module in modules:
                    print(f"   - {module.get('name')}: {module.get('id')}")
                return True
            else:
                print_error(f"获取可用模块失败: {data.get('error')}")
                return False
        else:
            print_error(f"获取可用模块失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"获取可用模块异常: {str(e)}")
        return False

def main():
    """主函数"""
    print_header("宁律师小程序 - 前后端集成测试")

    # 等待服务启动
    print_info("等待服务启动...")
    time.sleep(2)

    # 测试结果
    results = []

    # 测试健康检查
    print_header("测试1: 健康检查")
    results.append(("健康检查", test_health_check()))

    # 测试获取套餐列表
    print_header("测试2: 获取套餐列表")
    results.append(("获取套餐列表", test_get_plans()))

    # 测试获取用户套餐
    print_header("测试3: 获取用户套餐")
    results.append(("获取用户套餐", test_get_user_subscription()))

    # 测试获取可用模块
    print_header("测试4: 获取可用模块")
    results.append(("获取可用模块", test_get_modules()))

    # 测试升级套餐（可选）
    print_header("测试5: 升级套餐")
    results.append(("升级套餐", test_upgrade_subscription()))

    # 汇总结果
    print_header("测试结果汇总")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        if result:
            print_success(f"{name}")
        else:
            print_error(f"{name}")

    print(f"\n{Colors.BOLD}总计: {passed}/{total} 通过{Colors.END}")

    if passed == total:
        print_success("所有测试通过！前后端联动成功！")
        return 0
    else:
        print_error(f"{total - passed} 个测试失败")
        return 1

if __name__ == "__main__":
    exit(main())
