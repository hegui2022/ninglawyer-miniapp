"""
数据适配器使用示例
展示如何将扣子知识库返回的数据转换为微信小程序格式
"""

from backend.src.services import get_coze_knowledge_service
from backend.src.adapters import get_legal_knowledge_adapter


def example_basic_adaptation():
    """示例：基础数据适配"""
    print("=== 基础数据适配示例 ===\n")
    
    # 1. 调用扣子知识库API
    kb_service = get_coze_knowledge_service(
        access_token="ACCESS_TOKEN",
        dataset_id="DATASET_ID"
    )
    
    raw_result = kb_service.search(
        query="刑法第二百六十四条",
        top_k=3
    )
    
    print(f"原始数据：")
    print(f"  成功: {raw_result.get('success')}")
    print(f"  总数: {raw_result.get('total')}")
    
    if raw_result.get("success") and raw_result.get("data"):
        print(f"  第一条内容: {raw_result['data'][0].get('content', '')[:100]}...")
    
    # 2. 使用数据适配器转换格式
    adapter = get_legal_knowledge_adapter(enable_llm_enhance=False)
    adapted_result = adapter.adapt(raw_result)
    
    print(f"\n适配后数据：")
    print(f"  成功: {adapted_result.get('success')}")
    print(f"  总数: {adapted_result.get('total')}")
    
    if adapted_result.get("success") and adapted_result.get("data"):
        first_item = adapted_result['data'][0]
        print(f"  法条编号: {first_item.get('article_number')}")
        print(f"  法条名称: {first_item.get('law_name')}")
        print(f"  罪名: {first_item.get('crime_name')}")
        print(f"  刑期: {first_item.get('penalties')}")
        print(f"  金额: {first_item.get('amounts')}")
        print(f"  情节: {first_item.get('circumstances')}")
        print(f"  关键词: {first_item.get('keywords')}")
    
    return adapted_result


def example_llm_enhanced_adaptation():
    """示例：启用LLM增强的数据适配"""
    print("=== LLM增强数据适配示例 ===\n")
    
    # 1. 调用扣子知识库API
    kb_service = get_coze_knowledge_service(
        access_token="ACCESS_TOKEN",
        dataset_id="DATASET_ID"
    )
    
    raw_result = kb_service.search(
        query="盗窃罪的量刑标准",
        top_k=2
    )
    
    # 2. 使用数据适配器（启用LLM增强）
    adapter = get_legal_knowledge_adapter(enable_llm_enhance=True)
    adapted_result = adapter.adapt(raw_result)
    
    print(f"适配后数据（LLM增强）：")
    
    if adapted_result.get("success") and adapted_result.get("data"):
        for i, item in enumerate(adapted_result['data'], 1):
            print(f"\n--- 第{i}条 ---")
            print(f"  法条编号: {item.get('article_number')}")
            print(f"  摘要: {item.get('summary', '无')}")
            print(f"  关键点: {item.get('key_points', [])}")
    
    return adapted_result


def example_wechat_miniprogram_format():
    """示例：转换为微信小程序格式"""
    print("=== 微信小程序格式转换示例 ===\n")
    
    # 1. 调用扣子知识库API
    kb_service = get_coze_knowledge_service(
        access_token="ACCESS_TOKEN",
        dataset_id="DATASET_ID"
    )
    
    raw_result = kb_service.search(
        query="刑法第二百六十四条",
        top_k=1
    )
    
    # 2. 适配为微信小程序格式
    adapter = get_legal_knowledge_adapter(enable_llm_enhance=True)
    adapted_result = adapter.adapt(raw_result)
    
    # 3. 转换为微信小程序专用格式
    wechat_format = _convert_to_wechat_format(adapted_result)
    
    print("微信小程序格式：")
    import json
    print(json.dumps(wechat_format, ensure_ascii=False, indent=2))
    
    return wechat_format


def _convert_to_wechat_format(data: dict) -> dict:
    """
    转换为微信小程序专用格式
    
    Args:
        data: 适配后的数据
        
    Returns:
        微信小程序格式数据
    """
    if not data.get("success"):
        return data
    
    wechat_data = {
        "success": True,
        "data": {
            "law_articles": [],
            "total": data.get("total", 0),
            "query": data.get("raw", {}).get("query", "")
        }
    }
    
    # 转换法条数据
    for item in data.get("data", []):
        wechat_data["data"]["law_articles"].append({
            "article_id": item.get("document_id", ""),
            "article_number": item.get("article_number", ""),
            "law_name": item.get("law_name", ""),
            "crime_name": item.get("crime_name", ""),
            "content": item.get("content", ""),
            "content_sections": item.get("content_sections", []),
            "penalties": item.get("penalties", []),
            "amounts": item.get("amounts", []),
            "circumstances": item.get("circumstances", []),
            "keywords": item.get("keywords", []),
            "summary": item.get("summary", ""),
            "key_points": item.get("key_points", []),
            "score": item.get("score", 0),
            "highlight": _generate_highlight(item)
        })
    
    return wechat_data


def _generate_highlight(item: dict) -> str:
    """生成高亮文本"""
    content = item.get("content", "")
    keywords = item.get("keywords", [])
    
    # 高亮关键词
    highlighted = content
    for keyword in keywords:
        highlighted = highlighted.replace(
            keyword,
            f"<highlight>{keyword}</highlight>"
        )
    
    return highlighted


def example_error_handling():
    """示例：错误处理"""
    print("=== 错误处理示例 ===\n")
    
    # 模拟错误的原始数据
    raw_error_data = {
        "success": False,
        "error": "知识库检索失败"
    }
    
    # 使用适配器处理错误数据
    adapter = get_legal_knowledge_adapter()
    result = adapter.adapt(raw_error_data)
    
    print(f"适配结果: {result}")
    print(f"错误类型: {result.get('error_type')}")


def example_performance_comparison():
    """示例：性能对比（正则 vs LLM）"""
    import time
    
    print("=== 性能对比示例 ===\n")
    
    # 准备测试数据
    kb_service = get_coze_knowledge_service(
        access_token="ACCESS_TOKEN",
        dataset_id="DATASET_ID"
    )
    
    raw_result = kb_service.search(
        query="盗窃罪",
        top_k=5
    )
    
    if not raw_result.get("success"):
        print("检索失败，跳过性能测试")
        return
    
    # 测试1：仅使用正则表达式
    adapter_no_llm = get_legal_knowledge_adapter(enable_llm_enhance=False)
    
    start_time = time.time()
    result_no_llm = adapter_no_llm.adapt(raw_result)
    time_no_llm = time.time() - start_time
    
    print(f"仅正则表达式：{time_no_llm:.2f}秒")
    
    # 测试2：使用正则 + LLM
    adapter_with_llm = get_legal_knowledge_adapter(enable_llm_enhance=True)
    
    start_time = time.time()
    result_with_llm = adapter_with_llm.adapt(raw_result)
    time_with_llm = time.time() - start_time
    
    print(f"正则 + LLM：{time_with_llm:.2f}秒")
    
    print(f"\n性能提升：{(time_with_llm / time_no_llm):.2f}倍")
    print(f"注：LLM增强提供了更丰富的信息（摘要、关键点等）")


def example_batch_adaptation():
    """示例：批量适配"""
    print("=== 批量适配示例 ===\n")
    
    # 模拟多个查询
    queries = [
        "刑法第二百六十四条",
        "盗窃罪的量刑标准",
        "入户盗窃和扒窃的区别"
    ]
    
    adapter = get_legal_knowledge_adapter(enable_llm_enhance=False)
    kb_service = get_coze_knowledge_service(
        access_token="ACCESS_TOKEN",
        dataset_id="DATASET_ID"
    )
    
    results = []
    
    for query in queries:
        print(f"处理查询：{query}")
        
        # 1. 检索
        raw_result = kb_service.search(query=query, top_k=2)
        
        # 2. 适配
        adapted_result = adapter.adapt(raw_result)
        
        results.append({
            "query": query,
            "result": adapted_result
        })
    
    print(f"\n批量适配完成，共处理 {len(results)} 个查询")
    
    return results


if __name__ == "__main__":
    print("=" * 60)
    print("  数据适配器使用示例")
    print("=" * 60)
    print()
    
    # 选择要运行的示例
    # example_basic_adaptation()
    # example_llm_enhanced_adaptation()
    # example_wechat_miniprogram_format()
    # example_error_handling()
    # example_performance_comparison()
    # example_batch_adaptation()
    
    print("\n请取消注释其中一个示例函数来运行")
    print("\n⚠️  提示：请先替换代码中的 ACCESS_TOKEN 和 DATASET_ID 为实际值！")
