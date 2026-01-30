#!/usr/bin/env python3
"""
宁律师小程序 - 集成测试脚本
测试所有API接口的功能
"""

import os
import sys
import time
import requests
import json
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载环境变量
load_dotenv()


class APITester:
    """API 测试器"""
    
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
                response = requests.get(url, headers=headers, timeout=10)
            else:
                response = requests.post(url, headers=headers, json=data, timeout=30)
            
            return {
                'status_code': response.status_code,
                'json': response.json() if response.content else {}
            }
        except Exception as e:
            return {
                'status_code': 500,
                'json': {'error': str(e)}
            }
    
    def run_test(self, test_name: str, method: str, endpoint: str, data: Dict = None, 
                 expected_keys: List[str] = None, should_fail: bool = False) -> bool:
        """运行单个测试"""
        logger.info(f"🧪 测试：{test_name}")
        
        result = self.request(method, endpoint, data)
        
        # 判断测试是否通过
        passed = True
        
        if should_fail:
            # 期望失败的情况
            if result['status_code'] >= 200 and result['status_code'] < 500:
                passed = False
                logger.warning(f"  ❌ 期望失败但成功了")
        else:
            # 期望成功的情况
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
        logger.info("开始集成测试")
        logger.info("=" * 60)
        
        # 1. 基础测试
        self.test_basic_endpoints()
        
        # 2. 主脑路由测试
        self.test_master_routing()
        
        # 3. 脱敏功能测试
        self.test_desensitize()
        
        # 4. 法律咨询测试
        self.test_consultation()
        
        # 5. 合同功能测试
        self.test_contract()
        
        # 6. 错误处理测试
        self.test_error_handling()
        
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
            test_name="API根路径",
            method="GET",
            endpoint="/",
            expected_keys=["service", "version"]
        )
        
        self.run_test(
            test_name="API测试接口",
            method="GET",
            endpoint="/api/test",
            expected_keys=["message"]
        )
        
        self.run_test(
            test_name="主脑测试接口",
            method="GET",
            endpoint="/api/master/test",
            expected_keys=["message", "available_apis"]
        )
    
    def test_master_routing(self):
        """测试主脑路由"""
        logger.info("\n📋 测试主脑路由")
        
        test_cases = [
            {
                "name": "路由-脱敏请求",
                "input": "帮我脱敏一下，我叫张三，身份证号123456789012345678",
                "expected_bot": "脱敏"
            },
            {
                "name": "路由-民事咨询",
                "input": "我欠别人钱被起诉了怎么办",
                "expected_bot": "民事咨询"
            },
            {
                "name": "路由-合同起草",
                "input": "帮我起草一个借款合同",
                "expected_bot": "合同起草"
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
    
    def test_desensitize(self):
        """测试脱敏功能"""
        logger.info("\n📋 测试脱敏功能")
        
        # 正常脱敏
        self.run_test(
            test_name="脱敏-完整信息",
            method="POST",
            endpoint="/api/master/desensitize",
            data={
                "name": "张三",
                "id_card": "123456789012345678",
                "phone": "13812345678",
                "address": "北京市朝阳区xxx"
            },
            expected_keys=["success"]
        )
        
        # 部分脱敏
        self.run_test(
            test_name="脱敏-部分信息",
            method="POST",
            endpoint="/api/master/desensitize",
            data={
                "name": "李四",
                "phone": "13987654321"
            },
            expected_keys=["success"]
        )
        
        # 空数据
        self.run_test(
            test_name="脱敏-空数据",
            method="POST",
            endpoint="/api/master/desensitize",
            data={},
            should_fail=True
        )
    
    def test_consultation(self):
        """测试法律咨询"""
        logger.info("\n📋 测试法律咨询")
        
        test_cases = [
            {
                "name": "咨询-债务纠纷",
                "question": "朋友借钱不还怎么办",
                "domain": "民事"
            },
            {
                "name": "咨询-婚姻问题",
                "question": "离婚后孩子抚养费怎么算",
                "domain": "婚姻"
            },
            {
                "name": "咨询-劳动争议",
                "question": "公司无故辞退怎么办",
                "domain": "劳动"
            }
        ]
        
        for case in test_cases:
            self.run_test(
                test_name=case["name"],
                method="POST",
                endpoint="/api/master/consult",
                data={
                    "question": case["question"],
                    "domain": case["domain"]
                },
                expected_keys=["success"]
            )
    
    def test_contract(self):
        """测试合同功能"""
        logger.info("\n📋 测试合同功能")
        
        # 合同起草
        self.run_test(
            test_name="合同-起草借款合同",
            method="POST",
            endpoint="/api/master/draft-contract",
            data={
                "contract_type": "借款合同",
                "details": "借款方：张三，出借方：李四，金额：10000元，期限：6个月"
            },
            expected_keys=["success"]
        )
        
        self.run_test(
            test_name="合同-起草租赁合同",
            method="POST",
            endpoint="/api/master/draft-contract",
            data={
                "contract_type": "租赁合同",
                "details": "出租方：王五，承租方：赵六，房屋：北京市朝阳区xxx"
            },
            expected_keys=["success"]
        )
        
        # 合同审查
        self.run_test(
            test_name="合同-审查",
            method="POST",
            endpoint="/api/master/review-contract",
            data={
                "contract_content": "甲方：张三，乙方：李四。甲方借款10000元给乙方..."
            },
            expected_keys=["success"]
        )
        
        # 错误情况
        self.run_test(
            test_name="合同-缺少类型",
            method="POST",
            endpoint="/api/master/draft-contract",
            data={},
            should_fail=True
        )
    
    def test_error_handling(self):
        """测试错误处理"""
        logger.info("\n📋 测试错误处理")
        
        # 缺少参数
        self.run_test(
            test_name="错误处理-路由缺少输入",
            method="POST",
            endpoint="/api/master/route",
            data={},
            should_fail=True
        )
        
        self.run_test(
            test_name="错误处理-咨询缺少问题",
            method="POST",
            endpoint="/api/master/consult",
            data={},
            should_fail=True
        )
        
        self.run_test(
            test_name="错误处理-审查缺少内容",
            method="POST",
            endpoint="/api/master/review-contract",
            data={},
            should_fail=True
        )
        
        # 不存在的接口
        self.run_test(
            test_name="错误处理-404接口",
            method="GET",
            endpoint="/api/not-exist",
            should_fail=True
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
        report_file = project_root / "test_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📄 详细报告已保存到：{report_file}")
        
        return self.fail_count == 0


def main():
    """主函数"""
    # 获取API地址
    base_url = os.getenv('API_URL', 'http://localhost:5000')
    
    # 创建测试器
    tester = APITester(base_url)
    
    # 运行所有测试
    success = tester.run_all_tests()
    
    # 退出码
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
