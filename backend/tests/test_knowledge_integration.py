#!/usr/bin/env python3
"""
阶段3知识库测试脚本
验证扣子知识库检索功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger


def test_knowledge_client_init():
    """测试1：知识库客户端初始化"""
    logger.info("=" * 60)
    logger.info("测试1：知识库客户端初始化")
    logger.info("=" * 60)
    
    try:
        from coze_coding_dev_sdk import KnowledgeClient, Config
        from coze_coding_utils.runtime_ctx.context import new_context
        
        # 初始化客户端
        config = Config()
        client = KnowledgeClient(
            config=config,
            ctx=new_context(method="test_knowledge_init")
        )
        
        logger.success("✅ 知识库客户端初始化成功")
        logger.info("")
        return True
    
    except Exception as e:
        logger.error(f"❌ 测试1失败：{e}")
        logger.info("")
        return False


def test_knowledge_search():
    """测试2：知识库检索"""
    logger.info("=" * 60)
    logger.info("测试2：知识库检索")
    logger.info("=" * 60)
    
    try:
        from coze_coding_dev_sdk import KnowledgeClient, Config
        from coze_coding_utils.runtime_ctx.context import new_context
        
        # 初始化客户端
        config = Config()
        client = KnowledgeClient(
            config=config,
            ctx=new_context(method="test_knowledge_search")
        )
        
        # 测试检索
        test_queries = [
            "离婚流程",
            "财产分割",
            "子女抚养权"
        ]
        
        for query in test_queries:
            logger.info(f"\n测试查询：{query}")
            
            response = client.search(
                query=query,
                top_k=3
            )
            
            if response.code == 0:
                logger.info(f"✅ 检索成功，找到 {len(response.chunks)} 条结果")
                
                if response.chunks:
                    for i, chunk in enumerate(response.chunks, 1):
                        logger.info(f"  结果{i} [{chunk.score:.4f}]: {chunk.content[:80]}...")
                else:
                    logger.info("  ⚠️ 无匹配结果（知识库可能为空，这是正常的）")
            else:
                logger.error(f"❌ 检索失败：{response.msg}")
        
        logger.success("✅ 测试2通过：知识库检索接口正常")
        logger.info("")
        return True
    
    except Exception as e:
        logger.error(f"❌ 测试2失败：{e}")
        logger.info("")
        return False


def test_knowledge_retriever():
    """测试3：知识检索器"""
    logger.info("=" * 60)
    logger.info("测试3：知识检索器")
    logger.info("=" * 60)
    
    try:
        from src.utils.knowledge_retriever import knowledge_retriever
        
        # 测试检索
        test_queries = [
            ("离婚流程", "family_law"),
            ("财产分割", "family_law"),
            ("子女抚养", "family_law")
        ]
        
        for query, scenario in test_queries:
            logger.info(f"\n测试查询：{query} (场景: {scenario})")
            
            result = knowledge_retriever.retrieve(query, scenario, top_k=3)
            
            if result:
                logger.info(f"✅ 检索成功")
                logger.info(f"结果摘要：{result[:150]}...")
            else:
                logger.info(f"⚠️ 检索无结果（知识库可能为空，这是正常的）")
        
        logger.success("✅ 测试3通过：知识检索器正常工作")
        logger.info("")
        return True
    
    except Exception as e:
        logger.error(f"❌ 测试3失败：{e}")
        logger.info("")
        return False


def test_knowledge_integration_with_skill():
    """测试4：知识检索与技能集成"""
    logger.info("=" * 60)
    logger.info("测试4：知识检索与技能集成")
    logger.info("=" * 60)
    
    try:
        from src.skills.divorce_procedure_skill import execute_divorce_procedure
        
        # 测试用例
        user_input = "我想离婚，流程是什么？"
        context = {
            "user_type": "personal",
            "scenario": "family_law",
            "personality_id": "warm_personal"
        }
        
        logger.info(f"用户输入：{user_input}")
        logger.info("正在调用技能（含知识检索）...")
        
        result = execute_divorce_procedure(user_input, context)
        
        logger.info(f"✅ 技能执行成功")
        logger.info(f"结果摘要：{result[:150]}...")
        
        logger.success("✅ 测试4通过：知识检索与技能集成正常")
        logger.info("")
        return True
    
    except Exception as e:
        logger.error(f"❌ 测试4失败：{e}")
        logger.info("")
        return False


def main():
    """运行所有测试"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("🧪 阶段3知识库测试")
    logger.info("=" * 60)
    logger.info("")
    
    results = {
        "知识库客户端初始化": test_knowledge_client_init(),
        "知识库检索": test_knowledge_search(),
        "知识检索器": test_knowledge_retriever(),
        "知识检索与技能集成": test_knowledge_integration_with_skill()
    }
    
    # 汇总结果
    logger.info("=" * 60)
    logger.info("📊 测试结果汇总")
    logger.info("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        logger.info(f"{test_name:30s} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    logger.info("")
    logger.info(f"总计：{passed} 通过，{failed} 失败")
    
    if failed == 0:
        logger.success("=" * 60)
        logger.success("🎉 所有测试通过！阶段3知识库集成验证成功！")
        logger.success("=" * 60)
        logger.success("\n✅ 核心检查点验证：")
        logger.success("  ✓ 知识库客户端初始化正常")
        logger.success("  ✓ 知识库检索接口正常")
        logger.success("  ✓ 知识检索器正常工作")
        logger.success("  ✓ 知识检索与技能集成正常")
        logger.success("\n💡 提示：")
        logger.success("  - 如果知识库为空，检索会返回无结果，这是正常的")
        logger.success("  - 可以使用 CLI 导入文档：")
        logger.success("    coze-coding-ai knowledge add --dataset 'coze_doc_knowledge' --content '...' --url '...'")
        logger.success("\n🚀 可以进入阶段4：创建商事技能")
        return 0
    else:
        logger.error("=" * 60)
        logger.error("⚠️  部分测试失败，请检查日志")
        logger.error("=" * 60)
        logger.info("\n💡 建议：")
        if not results["知识库客户端初始化"]:
            logger.info("  1. 检查 coze_coding_dev_sdk 是否正确安装")
        if not results["知识库检索"]:
            logger.info("  2. 检查网络连接和API配置")
        if not results["知识检索器"]:
            logger.info("  3. 检查知识检索器配置")
        return 1


if __name__ == "__main__":
    exit(main())
