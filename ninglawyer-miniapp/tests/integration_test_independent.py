#!/usr/bin/env python3
"""
集成测试脚本 - 测试所有技能模块
"""

import os
import sys
import time
import requests
import json
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class SkillsTestRunner:
    """技能测试运行器"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.test_results: List[Dict[str, Any]] = []
        self.pass_count = 0
        self.fail_count = 0
    
    def request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """发送请求"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            else:
                response = requests.post(url, headers=headers, json=data, timeout=60)
            
            return {
                'status_code': response.status_code,
                'json': response.json() if response.content else {}
            }
        except Exception as e:
            return {
                'status_code': 500,
                'json': {'error': str(e)}
            }
    
    def run_test(self, test_name: str, method: str, endpoint: str, 
                 data: Dict = None, expected_keys: List[str] = None) -> bool:
        """运行单个测试"""
        logger.info(f"🧪 测试：{test_name}")
        
        result = self.request(method, endpoint, data)
        
        # 判断测试是否通过
        passed = True
        
        if result['status_code'] < 200 or result['status_code'] >= 500:
            passed = False
            logger.warning(f"  ❌ HTTP状态码：{result['status_code']}")
        
        if expected_keys:
            for key in expected_keys:
                if key not in result['json']:
                    passed = False
                    logger.warning(f"  ❌ 缺少响应字段：{key}")
        
        # 记录结果
        test_result = {
            'test_name': test_name,
            'method': method,
            'endpoint': endpoint,
            'data': data,
            'status_code': result['status_code'],
            'response': result['json'],
            'passed': passed,
            'timestamp': time.time()
        }
        
        self.test_results.append(test_result)
        
        if passed:
            self.pass_count += 1
            logger.success(f"  ✅ 通过")
        else:
            self.fail_count += 1
            logger.error(f"  ❌ 失败")
            logger.error(f"  响应：{json.dumps(result['json'], ensure_ascii=False)}")
        
        return passed
    
    def run_all_tests(self):
        """运行所有测试"""
        logger.info("=" * 60)
        logger.info("开始集成测试 - 独立架构版本")
        logger.info("=" * 60)
        
        # 1. 基础测试
        self.test_basic_endpoints()
        
        # 2. 脱敏技能测试
        self.test_desensitize_skill()
        
        # 3. 民事咨询技能测试
        self.test_civil_consult_skill()
        
        # 4. 合同起草技能测试
        self.test_contract_skill()
        
        # 5. 主脑路由测试
        self.test_master_brain_routing()
        
        # 输出测试报告
        self.print_report()
    
    def test_basic_endpoints(self):
        """测试基础接口"""
        logger.info("\n📋 测试基础接口")
        
        self.run_test(
            test_name="健康检查",
            method="GET",
            endpoint="/health",
            expected_keys=["status"]
        )
        
        self.run_test(
            test_name="主脑测试接口",
            method="GET",
            endpoint="/api/master/test",
            expected_keys=["message", "available_skills"]
        )
        
        self.run_test(
            test_name="列出所有技能",
            method="GET",
            endpoint="/api/master/list-skills",
            expected_keys=["success", "data"]
        )
    
    def test_desensitize_skill(self):
        """测试脱敏技能"""
        logger.info("\n📋 测试脱敏技能")
        
        test_cases = [
            {
                "name": "脱敏-姓名和手机号",
                "text": "我叫张三，手机号是13812345678"
            },
            {
                "name": "脱敏-身份证号",
                "text": "我的身份证号是123456789012345678"
            },
            {
                "name": "脱敏-地址",
                "text": "我住在北京市朝阳区xxx街道100号"
            }
        ]
        
        for case in test_cases:
            self.run_test(
                test_name=case["name"],
                method="POST",
                endpoint="/api/master/desensitize",
                data={"text": case["text"]},
                expected_keys=["success", "data"]
            )
    
    def test_civil_consult_skill(self):
        """测试民事咨询技能"""
        logger.info("\n📋 测试民事咨询技能")
        
        test_cases = [
            {
                "name": "咨询-债务纠纷",
                "question": "朋友借钱不还怎么办"
            },
            {
                "name": "咨询-婚姻问题",
                "question": "离婚后孩子抚养费怎么算"
            },
            {
                "name": "咨询-劳动争议",
                "question": "公司无故辞退怎么办"
            }
        ]
        
        for case in test_cases:
            self.run_test(
                test_name=case["name"],
                method="POST",
                endpoint="/api/master/consult",
                data={"question": case["question"]},
                expected_keys=["success", "data"]
            )
    
    def test_contract_skill(self):
        """测试合同起草技能"""
        logger.info("\n📋 测试合同起草技能")
        
        # 合同起草测试
        self.run_test(
            test_name="合同-起草借款合同",
            method="POST",
            endpoint="/api/master/contract",
            data={
                "text": "帮我起草一个借款合同，借款方：张三，出借方：李四，金额：10000元"
            },
            expected_keys=["success", "data"]
        )
        
        self.run_test(
            test_name="合同-起草租赁合同",
            method="POST",
            endpoint="/api/master/contract",
            data={
                "text": "起草一个房屋租赁合同，出租方：王五，承租方：赵六"
            },
            expected_keys=["success", "data"]
        )
        
        # 合同审查测试
        self.run_test(
            test_name="合同-审查合同",
            method="POST",
            endpoint="/api/master/contract",
            data={
                "text": "帮我审查这个合同：甲方：张三，乙方：李四。甲方向乙方借款10000元。"
            },
            expected_keys=["success", "data"]
        )
    
    def test_master_brain_routing(self):
        """测试主脑路由"""
        logger.info("\n📋 测试主脑路由")
        
        test_cases = [
            {
                "name": "路由-脱敏请求",
                "input": "帮我脱敏一下，我叫张三，手机号13812345678"
            },
            {
                "name": "路由-民事咨询",
                "input": "我欠别人钱被起诉了怎么办"
            },
            {
                "name": "路由-合同起草",
                "input": "帮我起草一个借款合同"
            }
        ]
        
        for case in test_cases:
            self.run_test(
                test_name=case["name"],
                method="POST",
                endpoint="/api/master/route",
                data={"user_input": case["input"]},
                expected_keys=["success"]
            )
    
    def print_report(self):
        """输出测试报告"""
        logger.info("\n" + "=" * 60)
        logger.info("测试报告")
        logger.info("=" * 60)
        logger.info(f"✅ 通过：{self.pass_count}")
        logger.info(f"❌ 失败：{self.fail_count}")
        logger.info(f"📊 通过率：{self.pass_count / (self.pass_count + self.fail_count) * 100:.2f}%")
        logger.info("=" * 60)
        
        # 保存测试结果
        report_file = project_root / "test_report_independent.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📄 详细报告已保存到：{report_file}")
        
        return self.fail_count == 0


def main():
    """主函数"""
    # 获取API地址
    base_url = os.getenv('API_URL', 'http://localhost:5000')
    
    # 创建测试器
    tester = SkillsTestRunner(base_url)
    
    # 运行所有测试
    success = tester.run_all_tests()
    
    # 退出码
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
