"""
宁律师V1 API测试脚本
测试宁律师的咨询功能
"""

import requests
import json
from loguru import logger

# API配置
BASE_URL = "http://localhost:5000"
CHAT_ENDPOINT = "/api/v1/ninglawyer/chat"
INFO_ENDPOINT = "/api/v1/ninglawyer/info"
PERSONALITIES_ENDPOINT = "/api/v1/ninglawyer/personalities"


class NingLawyerTester:
    """宁律师测试类"""
    
    def __init__(self):
        self.base_url = BASE_URL
        logger.info("🧪 宁律师测试类初始化完成")
    
    def test_chat(
        self,
        query: str,
        user_id: str = "test_user",
        user_type: str = "individual"
    ) -> dict:
        """
        测试聊天接口
        
        Args:
            query: 用户输入的问题
            user_id: 用户ID
            user_type: 用户类型
            
        Returns:
            响应结果
        """
        url = f"{self.base_url}{CHAT_ENDPOINT}"
        data = {
            "query": query,
            "user_id": user_id,
            "user_type": user_type
        }
        
        logger.info(f"🚀 测试聊天接口 - 问题: {query[:50]}...")
        logger.info(f"📋 请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        try:
            response = requests.post(url, json=data, timeout=60)
            result = response.json()
            
            logger.info(f"📊 响应状态码: {response.status_code}")
            logger.info(f"📊 响应数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result.get('success'):
                data_result = result.get('data', {})
                logger.info(f"✅ 聊天成功")
                logger.info(f"💬 宁律师回复: {data_result.get('answer', '')[:100]}...")
                logger.info(f"🎭 使用人设: {data_result.get('personality', {}).get('name', '')}")
                logger.info(f"🎯 识别意图: {data_result.get('intent_desc', '')}")
            else:
                logger.error(f"❌ 聊天失败: {result.get('message', '')}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 请求异常: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def test_info(self) -> dict:
        """
        测试获取宁律师信息接口
        
        Returns:
            响应结果
        """
        url = f"{self.base_url}{INFO_ENDPOINT}"
        
        logger.info(f"🚀 测试获取宁律师信息接口")
        
        try:
            response = requests.get(url, timeout=10)
            result = response.json()
            
            logger.info(f"📊 响应状态码: {response.status_code}")
            logger.info(f"📊 响应数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result.get('success'):
                logger.info(f"✅ 获取宁律师信息成功")
            else:
                logger.error(f"❌ 获取宁律师信息失败: {result.get('message', '')}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 请求异常: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def test_personalities(self) -> dict:
        """
        测试获取人设列表接口
        
        Returns:
            响应结果
        """
        url = f"{self.base_url}{PERSONALITIES_ENDPOINT}"
        
        logger.info(f"🚀 测试获取人设列表接口")
        
        try:
            response = requests.get(url, timeout=10)
            result = response.json()
            
            logger.info(f"📊 响应状态码: {response.status_code}")
            logger.info(f"📊 响应数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result.get('success'):
                logger.info(f"✅ 获取人设列表成功")
            else:
                logger.error(f"❌ 获取人设列表失败: {result.get('message', '')}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 请求异常: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def run_all_tests(self):
        """运行所有测试"""
        logger.info("=" * 80)
        logger.info("🧪 开始宁律师V1 API测试")
        logger.info("=" * 80)
        
        # 测试1: 获取宁律师信息
        logger.info("\n【测试1】获取宁律师信息")
        self.test_info()
        
        # 测试2: 获取人设列表
        logger.info("\n【测试2】获取人设列表")
        self.test_personalities()
        
        # 测试3: 普通法律咨询
        logger.info("\n【测试3】普通法律咨询")
        self.test_chat(
            query="你好，我想咨询一下法律问题",
            user_id="test_user_1",
            user_type="individual"
        )
        
        # 测试4: 婚姻家事咨询（触发温暖陪伴型人设）
        logger.info("\n【测试4】婚姻家事咨询（温暖陪伴型人设）")
        self.test_chat(
            query="我和老公感情破裂，想离婚，孩子抚养权怎么判？",
            user_id="test_user_2",
            user_type="individual"
        )
        
        # 测试5: 合同签署咨询（触发意图识别）
        logger.info("\n【测试5】合同签署咨询（意图识别）")
        self.test_chat(
            query="我需要在线签署一份租房合同，该怎么操作？",
            user_id="test_user_3",
            user_type="individual"
        )
        
        # 测试6: 裁判观点查询（触发意图识别）
        logger.info("\n【测试6】裁判观点查询（意图识别）")
        self.test_chat(
            query="我想查一下类似交通事故的判决，胜诉率大概是多少？",
            user_id="test_user_4",
            user_type="individual"
        )
        
        # 测试7: 企业用户咨询
        logger.info("\n【测试7】企业用户咨询（企业商务型人设）")
        self.test_chat(
            query="我们公司需要做劳动合规，应该注意哪些方面？",
            user_id="test_company_1",
            user_type="corporate"
        )
        
        logger.info("\n" + "=" * 80)
        logger.info("🎉 宁律师V1 API测试完成")
        logger.info("=" * 80)


if __name__ == "__main__":
    # 配置日志
    logger.add(
        "logs/test_ninglawyer_v1.log",
        rotation="500 MB",
        retention="10 days",
        level="INFO"
    )
    
    # 创建测试实例
    tester = NingLawyerTester()
    
    # 运行所有测试
    tester.run_all_tests()
