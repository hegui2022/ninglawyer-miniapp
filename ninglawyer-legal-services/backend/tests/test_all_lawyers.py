"""
完整测试 - 测试所有宁律师
"""

import sys
import os
# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.agents.lawyer_factory import LawyerAgentFactory
from src.agents.lawyer_civil import NingLawyerCivil
from src.agents.lawyer_criminal import NingLawyerCriminal
from src.agents.lawyer_labor import NingLawyerLabor
from src.agents.lawyer_company import NingLawyerCompany
from src.agents.lawyer_ip import NingLawyerIP
from src.agents.lawyer_marriage import NingLawyerMarriage
from src.agents.lawyer_contract import NingLawyerContract
from loguru import logger


def test_all_lawyers():
    """测试所有宁律师"""
    logger.info("=" * 50)
    logger.info("开始测试所有宁律师")
    logger.info("=" * 50)
    
    lawyers = {
        'civil': NingLawyerCivil,
        'criminal': NingLawyerCriminal,
        'labor': NingLawyerLabor,
        'company': NingLawyerCompany,
        'ip': NingLawyerIP,
        'marriage': NingLawyerMarriage,
        'contract': NingLawyerContract
    }
    
    results = []
    
    for name, LawyerClass in lawyers.items():
        logger.info(f"=== 测试 {name} ===")
        try:
            lawyer = LawyerClass()
            info = lawyer.get_info()
            
            assert info is not None
            assert 'name' in info
            assert 'skills' in info
            
            logger.success(f"✓ {name} 测试通过")
            results.append((name, True))
        except Exception as e:
            logger.error(f"✗ {name} 测试失败：{str(e)}")
            results.append((name, False))
    
    # 测试 Lawyer Factory
    logger.info("=== 测试 Lawyer Factory ===")
    try:
        factory = LawyerAgentFactory()
        
        # 测试所有领域
        for domain in lawyers.keys():
            lawyer = factory.get_lawyer(domain)
            assert lawyer is not None
        
        # 测试列表
        lawyer_list = factory.list_lawyers()
        assert len(lawyer_list) == 7
        
        # 测试获取信息
        for domain in lawyers.keys():
            info = factory.get_lawyer_info(domain)
            assert info is not None
        
        logger.success("✓ Lawyer Factory 测试通过")
        results.append(('LawyerFactory', True))
    except Exception as e:
        logger.error(f"✗ Lawyer Factory 测试失败：{str(e)}")
        results.append(('LawyerFactory', False))
    
    # 输出测试结果
    logger.info("=" * 50)
    logger.info("测试结果汇总")
    logger.info("=" * 50)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        logger.info(f"{name}: {status}")
    
    # 统计
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    logger.info("=" * 50)
    logger.info(f"总计：{passed}/{total} 通过")
    logger.info("=" * 50)
    
    return passed == total


if __name__ == '__main__':
    success = test_all_lawyers()
    sys.exit(0 if success else 1)
