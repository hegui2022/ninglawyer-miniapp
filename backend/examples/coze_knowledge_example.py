"""
扣子知识库API调用示例
"""

from backend.src.services.coze_knowledge_service import get_coze_knowledge_service


def example_basic_search():
    """示例：基础检索"""
    print("=== 基础检索示例 ===\n")
    
    # 初始化服务
    # 注意：ACCESS_TOKEN 和 DATASET_ID 是占位符，需要替换为实际值
    ACCESS_TOKEN = "ACCESS_TOKEN"  # 替换为实际的Access Token
    DATASET_ID = "DATASET_ID"      # 替换为实际的Dataset ID
    
    service = get_coze_knowledge_service(
        access_token=ACCESS_TOKEN,
        dataset_id=DATASET_ID
    )
    
    # 检索知识库
    result = service.search(
        query="刑法第二百六十四条",
        top_k=3
    )
    
    if result.get("success"):
        print(f"✅ 检索成功！共返回 {result.get('total')} 条结果\n")
        
        for i, item in enumerate(result.get("data", []), 1):
            print(f"--- 结果 {i} ---")
            print(f"相似度：{item.get('score', 0):.4f}")
            print(f"内容：{item.get('content', '')[:100]}...")
            print(f"文档ID：{item.get('document_id', '')}")
            print()
    else:
        print(f"❌ 检索失败：{result.get('error')}")
        print(f"错误类型：{result.get('error_type')}")
    
    return result


def example_search_with_filters():
    """示例：带过滤条件的检索"""
    print("=== 带过滤条件的检索示例 ===\n")
    
    service = get_coze_knowledge_service(
        access_token="ACCESS_TOKEN",
        dataset_id="DATASET_ID"
    )
    
    # 设置最小相似度分数
    result = service.search(
        query="盗窃罪的量刑标准",
        top_k=5,
        min_score=0.7  # 只返回相似度大于0.7的结果
    )
    
    if result.get("success"):
        print(f"✅ 检索成功！共返回 {result.get('total')} 条结果（相似度>0.7）\n")
        
        for item in result.get("data", []):
            print(f"相似度：{item.get('score', 0):.4f}")
            print(f"内容：{item.get('content', '')[:150]}...")
            print()
    
    return result


def example_error_handling():
    """示例：错误处理"""
    print("=== 错误处理示例 ===\n")
    
    # 测试Token过期
    print("1. 测试无效Token：")
    service = get_coze_knowledge_service(
        access_token="invalid_token",
        dataset_id="DATASET_ID"
    )
    result = service.search(query="测试")
    
    if not result.get("success"):
        print(f"   错误：{result.get('error')}")
        print(f"   错误类型：{result.get('error_type')}")
        print()
    
    # 测试Dataset ID错误
    print("2. 测试无效Dataset ID：")
    service.set_access_token("ACCESS_TOKEN")
    service.set_dataset_id("invalid_dataset_id")
    result = service.search(query="测试")
    
    if not result.get("success"):
        print(f"   错误：{result.get('error')}")
        print(f"   错误类型：{result.get('error_type')}")
        print()


def example_multi_search():
    """示例：多次检索"""
    print("=== 多次检索示例 ===\n")
    
    queries = [
        "盗窃罪的构成要件",
        "盗窃罪的量刑标准",
        "盗窃罪与诈骗罪的区别"
    ]
    
    service = get_coze_knowledge_service(
        access_token="ACCESS_TOKEN",
        dataset_id="DATASET_ID"
    )
    
    for i, query in enumerate(queries, 1):
        print(f"查询 {i}：{query}")
        
        result = service.search(query=query, top_k=2)
        
        if result.get("success"):
            print(f"  返回 {result.get('total')} 条结果")
            for item in result.get("data", []):
                print(f"    - 相似度：{item.get('score', 0):.4f}")
        else:
            print(f"  失败：{result.get('error')}")
        
        print()


def example_update_config():
    """示例：动态更新配置"""
    print("=== 动态更新配置示例 ===\n")
    
    service = get_coze_knowledge_service(
        access_token="ACCESS_TOKEN",
        dataset_id="DATASET_ID"
    )
    
    # 第一次检索
    print("使用Dataset ID: DATASET_ID")
    result1 = service.search(query="测试")
    print(f"结果：{result1.get('success')}\n")
    
    # 更新Dataset ID
    print("更新Dataset ID为：NEW_DATASET_ID")
    service.set_dataset_id("NEW_DATASET_ID")
    
    # 第二次检索
    result2 = service.search(query="测试")
    print(f"结果：{result2.get('success')}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("  扣子知识库API调用示例")
    print("=" * 60)
    print()
    
    # 注意：运行前请替换 ACCESS_TOKEN 和 DATASET_ID 为实际值
    
    # 选择要运行的示例
    # example_basic_search()
    # example_search_with_filters()
    # example_error_handling()
    # example_multi_search()
    # example_update_config()
    
    print("\n请取消注释其中一个示例函数来运行")
    print("\n⚠️  提示：请先替换代码中的 ACCESS_TOKEN 和 DATASET_ID 为实际值！")
