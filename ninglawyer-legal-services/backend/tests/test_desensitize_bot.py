"""
测试脱敏Bot调用
验证配置是否正确
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.bot_registry import get_bot_registry
from loguru import logger

def test_desensitize_bot():
    """测试脱敏Bot"""
    logger.info("=" * 50)
    logger.info("开始测试脱敏Bot")
    logger.info("=" * 50)
    
    # 获取Bot注册表
    registry = get_bot_registry()
    
    # 列出所有Bot
    bots = registry.list_bots()
    logger.info(f"已加载的Bot数量：{len(bots)}")
    for bot_type, bot_info in bots.items():
        logger.info(f"  - {bot_type}: {bot_info['name']} (enabled: {bot_info.get('enabled', False)})")
    
    # 测试脱敏Bot
    logger.info("\n" + "=" * 50)
    logger.info("调用脱敏Bot")
    logger.info("=" * 50)
    
    result = registry.call_bot(
        bot_type='desensitize',
        query='帮我脱敏：姓名张三，身份证110101199001011234，手机13800138000',
        user_id='test_user'
    )
    
    logger.info(f"\n调用结果：")
    logger.info(f"成功：{result.get('success')}")
    logger.info(f"Bot名称：{result.get('bot_name')}")
    
    if result.get('success'):
        logger.info(f"返回内容：{result.get('content')}")
        logger.info(f"完整数据：{result.get('data')}")
        logger.info("\n✅ 脱敏Bot测试成功！")
        return True
    else:
        logger.error(f"错误信息：{result.get('error')}")
        logger.error("\n❌ 脱敏Bot测试失败！")
        return False

if __name__ == '__main__':
    success = test_desensitize_bot()
    sys.exit(0 if success else 1)
