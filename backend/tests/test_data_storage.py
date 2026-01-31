"""
测试数据统一存储功能
"""

import os
import sys

# 添加backend目录到sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from loguru import logger

from database import init_db
from src.repositories import (
    get_user_repository,
    get_session_repository,
    get_message_repository,
)
from src.utils.cache_manager import CacheManager
from src.utils.data_consistency import DataConsistencyGuard


def test_user_repository():
    """测试用户Repository"""
    logger.info("=" * 60)
    logger.info("🧪 测试用户Repository")
    logger.info("=" * 60)
    
    # 初始化缓存管理器
    cache_manager = CacheManager()
    user_repo = get_user_repository(cache_manager)
    
    try:
        # 0. 清理测试数据（如果存在）
        logger.info("\n📝 0. 清理测试数据...")
        test_openid = "test_openid_002"
        test_phone = "13900139000"
        existing_user = user_repo.get_by_openid(test_openid)
        if existing_user:
            user_repo.delete(existing_user.id)
            logger.info(f"✅ 清理已存在的测试用户: id={existing_user.id}")
        
        # 1. 创建用户
        logger.info("\n📝 1. 创建用户...")
        user = user_repo.create_user(
            openid=test_openid,
            phone=test_phone,
            nickname="测试用户"
        )
        
        if user:
            logger.info(f"✅ 用户创建成功: id={user.id}, openid={user.openid}, nickname={user.nickname}")
        else:
            logger.error("❌ 用户创建失败")
            return False
        
        # 2. 根据ID获取用户
        logger.info("\n📝 2. 根据ID获取用户...")
        fetched_user = user_repo.get_by_id(user.id)
        
        if fetched_user:
            logger.info(f"✅ 获取用户成功: id={fetched_user.id}, nickname={fetched_user.nickname}")
        else:
            logger.error("❌ 获取用户失败")
            return False
        
        # 3. 根据openid获取用户
        logger.info("\n📝 3. 根据openid获取用户...")
        user_by_openid = user_repo.get_by_openid(test_openid)
        
        if user_by_openid:
            logger.info(f"✅ 根据openid获取用户成功: id={user_by_openid.id}")
        else:
            logger.error("❌ 根据openid获取用户失败")
            return False
        
        # 4. 根据phone获取用户
        logger.info("\n📝 4. 根据phone获取用户...")
        user_by_phone = user_repo.get_by_phone(test_phone)
        
        if user_by_phone:
            logger.info(f"✅ 根据phone获取用户成功: id={user_by_phone.id}")
        else:
            logger.error("❌ 根据phone获取用户失败")
            return False
        
        # 5. 获取用户类型
        logger.info("\n📝 5. 获取用户类型...")
        user_type = user_repo.get_user_type(user.id)
        logger.info(f"✅ 用户类型: {user_type}")
        
        # 6. 更新用户类型
        logger.info("\n📝 6. 更新用户类型...")
        updated_user = user_repo.update_user_type(user.id, "premium")
        
        if updated_user:
            logger.info(f"✅ 用户类型更新成功: subscription_type={updated_user.subscription_type}")
        else:
            logger.error("❌ 用户类型更新失败")
            return False
        
        # 7. 增加使用次数
        logger.info("\n📝 7. 增加使用次数...")
        success = user_repo.increment_usage_count(user.id, "consultation")
        
        if success:
            logger.info("✅ 使用次数增加成功")
        else:
            logger.error("❌ 使用次数增加失败")
            return False
        
        # 8. 获取使用统计
        logger.info("\n📝 8. 获取使用统计...")
        usage_stats = user_repo.get_user_usage_stats(user.id)
        logger.info(f"✅ 使用统计: {usage_stats}")
        
        # 9. 统计用户数量
        logger.info("\n📝 9. 统计用户数量...")
        count = user_repo.count()
        logger.info(f"✅ 用户数量: {count}")
        
        # 10. 分页查询
        logger.info("\n📝 10. 分页查询...")
        page_result = user_repo.paginate(page=1, page_size=10)
        logger.info(f"✅ 分页结果: total={page_result['total']}, items={len(page_result['items'])}")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ 测试用户Repository失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_session_repository():
    """测试会话Repository"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 测试会话Repository")
    logger.info("=" * 60)
    
    # 初始化缓存管理器
    cache_manager = CacheManager()
    session_repo = get_session_repository(cache_manager)
    user_repo = get_user_repository(cache_manager)
    
    try:
        # 1. 创建或获取用户
        logger.info("\n📝 1. 创建或获取用户...")
        user = user_repo.get_by_openid("test_openid_001")
        
        if not user:
            user = user_repo.create_user(openid="test_openid_001", nickname="测试用户")
        
        if not user:
            logger.error("❌ 获取用户失败")
            return False
        
        # 2. 创建会话
        logger.info("\n📝 2. 创建会话...")
        session = session_repo.create_session(
            user_id=user.id,
            skill_type="consultation",
            title="测试会话"
        )
        
        if session:
            logger.info(f"✅ 会话创建成功: id={session.id}, title={session.title}")
        else:
            logger.error("❌ 会话创建失败")
            return False
        
        # 3. 获取活跃会话
        logger.info("\n📝 3. 获取活跃会话...")
        active_session = session_repo.get_active_session(user.id, "consultation")
        
        if active_session:
            logger.info(f"✅ 获取活跃会话成功: id={active_session.id}")
        else:
            logger.error("❌ 获取活跃会话失败")
            return False
        
        # 4. 获取用户会话列表
        logger.info("\n📝 4. 获取用户会话列表...")
        sessions = session_repo.get_user_sessions(user.id, "consultation")
        logger.info(f"✅ 用户会话列表: count={len(sessions)}")
        
        # 5. 获取或创建会话
        logger.info("\n📝 5. 获取或创建会话...")
        session_or_created = session_repo.get_or_create_session(user.id, "consultation")
        logger.info(f"✅ 获取或创建会话成功: id={session_or_created.id}")
        
        # 6. 更新会话标题
        logger.info("\n📝 6. 更新会话标题...")
        updated_session = session_repo.update_session_title(session.id, "更新后的标题")
        
        if updated_session:
            logger.info(f"✅ 会话标题更新成功: title={updated_session.title}")
        else:
            logger.error("❌ 会话标题更新失败")
            return False
        
        # 7. 关闭会话
        logger.info("\n📝 7. 关闭会话...")
        closed_session = session_repo.close_session(session.id)
        
        if closed_session:
            logger.info(f"✅ 会话关闭成功: is_active={closed_session.is_active}")
        else:
            logger.error("❌ 会话关闭失败")
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"❌ 测试会话Repository失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_message_repository():
    """测试消息Repository"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 测试消息Repository")
    logger.info("=" * 60)
    
    # 初始化缓存管理器
    cache_manager = CacheManager()
    message_repo = get_message_repository(cache_manager)
    session_repo = get_session_repository(cache_manager)
    user_repo = get_user_repository(cache_manager)
    
    try:
        # 1. 创建或获取用户和会话
        logger.info("\n📝 1. 创建或获取用户和会话...")
        user = user_repo.get_by_openid("test_openid_001")
        
        if not user:
            user = user_repo.create_user(openid="test_openid_001", nickname="测试用户")
        
        session = session_repo.get_or_create_session(user.id, "consultation")
        
        if not session:
            logger.error("❌ 获取会话失败")
            return False
        
        # 2. 创建用户消息
        logger.info("\n📝 2. 创建用户消息...")
        user_message = message_repo.create_message(
            session_id=session.id,
            role="user",
            content="你好，我想咨询一个法律问题"
        )
        
        if user_message:
            logger.info(f"✅ 用户消息创建成功: id={user_message.id}, content={user_message.content}")
        else:
            logger.error("❌ 用户消息创建失败")
            return False
        
        # 3. 创建助手消息
        logger.info("\n📝 3. 创建助手消息...")
        assistant_message = message_repo.create_message(
            session_id=session.id,
            role="assistant",
            content="您好，请问您想咨询什么法律问题？"
        )
        
        if assistant_message:
            logger.info(f"✅ 助手消息创建成功: id={assistant_message.id}, content={assistant_message.content}")
        else:
            logger.error("❌ 助手消息创建失败")
            return False
        
        # 4. 获取会话消息列表
        logger.info("\n📝 4. 获取会话消息列表...")
        messages = message_repo.get_session_messages(session.id)
        logger.info(f"✅ 会话消息列表: count={len(messages)}")
        
        for msg in messages:
            logger.info(f"  - [{msg.role}]: {msg.content[:30]}...")
        
        # 5. 获取会话消息字典列表
        logger.info("\n📝 5. 获取会话消息字典列表...")
        messages_dict = message_repo.get_session_messages_dict(session.id)
        logger.info(f"✅ 会话消息字典列表: count={len(messages_dict)}")
        
        # 6. 获取最后一条消息
        logger.info("\n📝 6. 获取最后一条消息...")
        last_message = message_repo.get_last_message(session.id)
        
        if last_message:
            logger.info(f"✅ 最后一条消息: [{last_message.role}] {last_message.content[:30]}...")
        else:
            logger.error("❌ 获取最后一条消息失败")
            return False
        
        # 7. 获取消息数量
        logger.info("\n📝 7. 获取消息数量...")
        count = message_repo.get_message_count(session.id)
        logger.info(f"✅ 消息数量: {count}")
        
        # 8. 获取对话历史
        logger.info("\n📝 8. 获取对话历史...")
        history = message_repo.get_conversation_history(session.id)
        logger.info(f"✅ 对话历史: count={len(history)}")
        
        for item in history:
            logger.info(f"  - [{item['role']}]: {item['content'][:30]}...")
        
        # 9. 批量创建消息
        logger.info("\n📝 9. 批量创建消息...")
        bulk_messages = [
            {"role": "user", "content": "用户消息3"},
            {"role": "assistant", "content": "助手消息3"},
        ]
        created_messages = message_repo.bulk_create_messages(session.id, bulk_messages)
        logger.info(f"✅ 批量创建消息成功: count={len(created_messages)}")
        
        # 10. 再次获取消息列表（验证批量创建）
        logger.info("\n📝 10. 再次获取消息列表...")
        messages = message_repo.get_session_messages(session.id)
        logger.info(f"✅ 会话消息列表: count={len(messages)}")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ 测试消息Repository失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_consistency():
    """测试数据一致性保障"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 测试数据一致性保障")
    logger.info("=" * 60)
    
    # 初始化缓存管理器和一致性保障
    cache_manager = CacheManager()
    consistency_guard = DataConsistencyGuard(cache_manager)
    user_repo = get_user_repository(cache_manager)
    
    try:
        # 1. 测试安全读取（Cache-Aside）
        logger.info("\n📝 1. 测试安全读取...")
        user = user_repo.get_by_openid("test_openid_001")
        
        if user:
            user_data = consistency_guard.safe_read(
                cache_key=f"user:{user.id}",
                db_operation=lambda: user_repo.to_dict(user_repo.get_by_id(user.id)),
                cache_ttl=3600
            )
            logger.info(f"✅ 安全读取成功: nickname={user_data.get('nickname')}")
        else:
            logger.warning("⚠️ 未找到测试用户")
        
        # 2. 测试安全更新
        logger.info("\n📝 2. 测试安全更新...")
        if user:
            updated_user = consistency_guard.safe_update(
                db_operation=lambda: user_repo.update_user_type(user.id, "premium"),
                cache_key=f"user:{user.id}",
                cache_value=user_repo.to_dict(user_repo.get_by_id(user.id)),
                cache_ttl=3600,
                invalidate_keys=[f"user_type:{user.id}"]
            )
            logger.info(f"✅ 安全更新成功: subscription_type={updated_user.subscription_type}")
        
        # 3. 测试缓存失效
        logger.info("\n📝 3. 测试缓存失效...")
        if user:
            success = consistency_guard.cache_consistency.invalidate_cache([
                f"user:{user.id}",
                f"user_type:{user.id}"
            ])
            logger.info(f"✅ 缓存失效: {'成功' if success else '失败'}")
        
        # 4. 测试事务管理
        logger.info("\n📝 4. 测试事务管理...")
        with consistency_guard.transaction_manager.transaction() as db:
            logger.info("✅ 事务上下文管理器工作正常")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ 测试数据一致性保障失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("🔧 数据统一存储功能测试")
    logger.info("=" * 60)
    
    # 初始化数据库
    logger.info("\n🔨 初始化数据库...")
    init_db()
    logger.info("✅ 数据库初始化完成")
    
    # 测试结果
    test_results = {}
    
    # 1. 测试用户Repository
    test_results['user_repository'] = test_user_repository()
    
    # 2. 测试会话Repository
    test_results['session_repository'] = test_session_repository()
    
    # 3. 测试消息Repository
    test_results['message_repository'] = test_message_repository()
    
    # 4. 测试数据一致性保障
    test_results['data_consistency'] = test_data_consistency()
    
    # 输出测试结果
    logger.info("\n" + "=" * 60)
    logger.info("📊 测试结果汇总")
    logger.info("=" * 60)
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        logger.info(f"{test_name}: {status}")
    
    # 统计
    passed = sum(test_results.values())
    total = len(test_results)
    
    logger.info(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        logger.info("\n🎉 所有测试通过！")
        return True
    else:
        logger.error(f"\n❌ 有 {total - passed} 个测试失败")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
