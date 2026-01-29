#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宁律师小程序矩阵 - 简化集成测试
不依赖环境变量，仅测试核心架构
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def test_imports():
    """测试核心模块导入"""
    print("\n=== 测试核心模块导入 ===")
    try:
        # 导入工具
        from src.utils.config import load_config, get_config
        from src.utils.logger import setup_logger, log_function_call
        from src.utils.response import success_response, error_response, ResponseCode
        
        # 导入存储
        from src.storage.cache import CacheManager
        from src.storage.db import DatabaseManager
        
        # 导入 Agent
        from src.agents.master_agent import MasterAgent
        from src.agents.lawyer_factory import LawyerAgentFactory
        
        print("✓ 所有核心模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 模块导入失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_config_loading():
    """测试配置加载"""
    print("\n=== 测试配置加载 ===")
    try:
        from src.utils.config import load_config
        
        config = load_config()
        
        assert config is not None, "配置不应为空"
        assert 'API_PORT' in config, "应包含 API_PORT"
        assert 'MODEL_NAME' in config, "应包含 MODEL_NAME"
        
        print(f"✓ 配置加载成功")
        print(f"  - API 端口: {config['API_PORT']}")
        print(f"  - 模型名称: {config['MODEL_NAME']}")
        return True
    except Exception as e:
        print(f"✗ 配置加载失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_lawyer_factory():
    """测试律师工厂"""
    print("\n=== 测试律师工厂 ===")
    try:
        from src.agents.lawyer_factory import LawyerAgentFactory
        
        factory = LawyerAgentFactory()
        
        # 获取所有律师
        lawyers = factory.list_lawyers()
        
        assert lawyers is not None, "律师列表不应为空"
        assert len(lawyers) > 0, "应至少有一个律师"
        
        print(f"✓ 律师工厂测试通过")
        print(f"  - 可用律师数量: {len(lawyers)}")
        for lawyer_id in lawyers:
            print(f"    • {lawyer_id}")
        
        return True
    except Exception as e:
        print(f"✗ 律师工厂测试失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_lawyer_info():
    """测试律师信息获取"""
    print("\n=== 测试律师信息获取 ===")
    try:
        from src.agents.lawyer_factory import LawyerAgentFactory
        
        factory = LawyerAgentFactory()
        
        # 获取民事律师信息
        civil_info = factory.get_lawyer_info('civil')
        
        assert civil_info is not None, "律师信息不应为空"
        assert 'name' in civil_info, "应包含名称"
        assert 'icon' in civil_info, "应包含图标"
        assert 'description' in civil_info, "应包含描述"
        
        print(f"✓ 律师信息获取成功")
        print(f"  - 名称: {civil_info['name']}")
        print(f"  - 图标: {civil_info['icon']}")
        print(f"  - 描述: {civil_info['description']}")
        
        return True
    except Exception as e:
        print(f"✗ 律师信息获取失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_response_utils():
    """测试响应工具"""
    print("\n=== 测试响应工具 ===")
    try:
        from src.utils.response import (
            success_response,
            error_response,
            paginate_response,
            ResponseCode
        )
        
        # 测试成功响应
        success = success_response({"key": "value"}, "操作成功")
        assert success['success'] is True
        assert success['message'] == "操作成功"
        
        # 测试错误响应
        error = error_response("操作失败", ResponseCode.BAD_REQUEST.value)
        assert error['success'] is False
        assert error['message'] == "操作失败"
        
        # 测试分页响应
        paginate = paginate_response([1, 2, 3], 10, 1, 3)
        assert paginate['data']['pagination']['total'] == 10
        assert paginate['data']['pagination']['page'] == 1
        
        print("✓ 响应工具测试通过")
        return True
    except Exception as e:
        print(f"✗ 响应工具测试失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_component_structure():
    """测试组件结构"""
    print("\n=== 测试组件结构 ===")
    try:
        # 检查组件目录
        components_dir = os.path.join(project_root, 'components')
        
        if os.path.exists(components_dir):
            components = os.listdir(components_dir)
            print(f"✓ 组件目录存在")
            print(f"  - 组件数量: {len(components)}")
            for component in components:
                print(f"    • {component}")
        else:
            print("⚠ 组件目录不存在（可能在其他项目中）")
        
        return True
    except Exception as e:
        print(f"✗ 组件结构测试失败：{str(e)}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("宁律师小程序矩阵 - 简化集成测试")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_imports),
        ("配置加载", test_config_loading),
        ("律师工厂", test_lawyer_factory),
        ("律师信息", test_lawyer_info),
        ("响应工具", test_response_utils),
        ("组件结构", test_component_structure),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # 打印总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    print(f"通过率: {passed / total * 100:.1f}%")
    
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
