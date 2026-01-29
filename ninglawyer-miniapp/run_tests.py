#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宁律师小程序矩阵 - 集成测试脚本
"""

import os
import sys
import json
import asyncio
import traceback
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server/src'))

from langchain_core.messages import HumanMessage, AIMessage

# 导入 agent 构建函数
from agents.legal_mentor.agent import build_agent as build_legal_mentor_agent
from agents.ma_shang_qian_yue.agent import build_agent as build_contract_agent
from agents.li_yue.agent import build_agent as build_contract_perf_agent


class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
    
    def run_test(self, test_name, test_func):
        """运行单个测试"""
        print(f"\n{'=' * 60}")
        print(f"运行测试: {test_name}")
        print(f"{'=' * 60}")
        
        try:
            result = test_func()
            self.test_results.append({
                'name': test_name,
                'status': 'PASS',
                'duration': str(datetime.now() - self.start_time),
                'result': result
            })
            print(f"✅ 测试通过: {test_name}")
            return True
        except Exception as e:
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            self.test_results.append({
                'name': test_name,
                'status': 'FAIL',
                'duration': str(datetime.now() - self.start_time),
                'error': error_msg
            })
            print(f"❌ 测试失败: {test_name}")
            print(f"错误信息: {str(e)}")
            return False
    
    def print_summary(self):
        """打印测试总结"""
        print(f"\n{'=' * 60}")
        print("测试总结")
        print(f"{'=' * 60}")
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        
        print(f"总测试数: {total}")
        print(f"通过: {passed}")
        print(f"失败: {failed}")
        print(f"通过率: {passed / total * 100:.1f}%")
        
        if failed > 0:
            print("\n失败的测试:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"  - {result['name']}")
                    print(f"    错误: {result.get('error', 'Unknown error')[:200]}")
        
        # 保存测试报告
        report_path = 'test_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total': total,
                    'passed': passed,
                    'failed': failed,
                    'pass_rate': f"{passed / total * 100:.1f}%"
                },
                'results': self.test_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n测试报告已保存到: {report_path}")
        
        return failed == 0


def test_legal_mentor_agent():
    """测试法律教官 Agent"""
    print("初始化法律教官 Agent...")
    agent = build_legal_mentor_agent()
    
    print("测试简单咨询...")
    messages = [HumanMessage(content="合同违约怎么办？")]
    
    response = agent.invoke({"messages": messages})
    
    print(f"Agent 回复: {response['messages'][-1].content[:200]}")
    
    assert len(response['messages']) > 0, "应该有回复"
    assert len(response['messages'][-1].content) > 0, "回复内容不应为空"
    
    return {"response_length": len(response['messages'][-1].content)}


def test_contract_agent():
    """测试码上签约 Agent"""
    print("初始化码上签约 Agent...")
    agent = build_contract_agent()
    
    print("测试合同起草...")
    messages = [HumanMessage(content="帮我起草一个采购合同")]
    
    response = agent.invoke({"messages": messages})
    
    print(f"Agent 回复: {response['messages'][-1].content[:200]}")
    
    assert len(response['messages']) > 0, "应该有回复"
    assert len(response['messages'][-1].content) > 0, "回复内容不应为空"
    
    return {"response_length": len(response['messages'][-1].content)}


def test_contract_perf_agent():
    """测试理约 Agent"""
    print("初始化理约 Agent...")
    agent = build_contract_perf_agent()
    
    print("测试合同履约...")
    messages = [HumanMessage(content="如何管理合同履约？")]
    
    response = agent.invoke({"messages": messages})
    
    print(f"Agent 回复: {response['messages'][-1].content[:200]}")
    
    assert len(response['messages']) > 0, "应该有回复"
    assert len(response['messages'][-1].content) > 0, "回复内容不应为空"
    
    return {"response_length": len(response['messages'][-1].content)}


def test_config_loading():
    """测试配置文件加载"""
    print("测试配置文件加载...")
    
    config_paths = [
        'server/config/agent_llm_config.json',
    ]
    
    for path in config_paths:
        full_path = os.path.join(os.path.dirname(__file__), path)
        assert os.path.exists(full_path), f"配置文件不存在: {path}"
        
        with open(full_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        assert 'config' in config, "配置文件必须包含 config 字段"
        assert 'sp' in config, "配置文件必须包含 sp 字段"
        assert 'tools' in config, "配置文件必须包含 tools 字段"
        
        print(f"✅ 配置文件加载成功: {path}")
    
    return {"loaded_configs": len(config_paths)}


def test_tools_import():
    """测试工具导入"""
    print("测试工具导入...")
    
    tool_paths = [
        'server/src/tools/contract_tool.py',
        'server/src/tools/database_tool.py',
    ]
    
    imported_tools = []
    
    for tool_path in tool_paths:
        try:
            # 将路径转换为模块名
            module_name = tool_path.replace('server/src/', '').replace('/', '.').replace('.py', '')
            
            # 导入模块
            __import__(module_name)
            imported_tools.append(module_name)
            print(f"✅ 工具导入成功: {module_name}")
        except ImportError as e:
            print(f"⚠️  工具导入失败: {module_name} - {e}")
    
    return {"imported_tools": imported_tools}


def main():
    """主函数"""
    print("宁律师小程序矩阵 - 集成测试")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    runner = TestRunner()
    
    # 运行测试
    runner.run_test("配置文件加载", test_config_loading)
    runner.run_test("工具导入", test_tools_import)
    runner.run_test("法律教官 Agent", test_legal_mentor_agent)
    runner.run_test("码上签约 Agent", test_contract_agent)
    runner.run_test("理约 Agent", test_contract_perf_agent)
    
    # 打印总结
    success = runner.print_summary()
    
    print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
