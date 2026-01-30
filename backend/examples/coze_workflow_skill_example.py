"""
扣子工作流和技能API使用示例
"""

from backend.src.services import (
    get_coze_workflow_service,
    get_coze_skill_service
)


def example_run_workflow():
    """示例：运行工作流"""
    print("=== 工作流运行示例 ===\n")
    
    # 初始化工作流服务
    service = get_coze_workflow_service(access_token="ACCESS_TOKEN")
    
    # 运行工作流
    result = service.run_workflow(
        workflow_id="your_workflow_id",
        params={
            "input_text": "请分析这段法律文本",
            "analysis_type": "criminal"
        },
        user_id="user_123"
    )
    
    if result.get("success"):
        data = result.get("data", {})
        print(f"✅ 工作流执行成功")
        print(f"工作流ID: {data.get('workflow_id')}")
        print(f"状态: {data.get('status')}")
        print(f"执行时间: {data.get('execution_time')}秒")
        print(f"结果: {data.get('result')}")
    else:
        print(f"❌ 工作流执行失败: {result.get('error')}")
        print(f"错误类型: {result.get('error_type')}")


def example_run_workflow_stream():
    """示例：流式运行工作流"""
    print("=== 流式工作流运行示例 ===\n")
    
    service = get_coze_workflow_service(access_token="ACCESS_TOKEN")
    
    print("流式输出：\n")
    
    for chunk in service.run_workflow_stream(
        workflow_id="your_workflow_id",
        params={
            "input_text": "请分析这段法律文本"
        },
        user_id="user_123"
    ):
        if chunk.get("event") == "message":
            print(chunk.get("data", {}).get("content", ""), end="")
        elif chunk.get("event") == "workflow.completed":
            print("\n\n✅ 工作流完成！")
        elif chunk.get("event") == "error":
            print(f"\n❌ 错误: {chunk.get('data', {}).get('error')}")


def example_call_skill():
    """示例：调用技能"""
    print("=== 技能调用示例 ===\n")
    
    # 初始化技能服务
    service = get_coze_skill_service(access_token="ACCESS_TOKEN")
    
    # 调用技能
    result = service.call_skill(
        skill_id="your_skill_id",
        skill_params={
            "query": "盗窃罪的量刑标准",
            "law_type": "criminal"
        },
        user_id="user_123"
    )
    
    if result.get("success"):
        data = result.get("data", {})
        print(f"✅ 技能调用成功")
        print(f"技能ID: {data.get('skill_id')}")
        print(f"执行时间: {data.get('execution_time')}秒")
        print(f"结果: {data.get('result')}")
    else:
        print(f"❌ 技能调用失败: {result.get('error')}")
        print(f"错误类型: {result.get('error_type')}")


def example_get_workflow_info():
    """示例：获取工作流信息"""
    print("=== 获取工作流信息示例 ===\n")
    
    service = get_coze_workflow_service(access_token="ACCESS_TOKEN")
    
    result = service.get_workflow_info(workflow_id="your_workflow_id")
    
    if result.get("success"):
        print(f"✅ 获取工作流信息成功")
        print(f"详情: {result.get('data')}")
    else:
        print(f"❌ 获取工作流信息失败: {result.get('error')}")


def example_list_workflows():
    """示例：列出工作流"""
    print("=== 列出工作流示例 ===\n")
    
    service = get_coze_workflow_service(access_token="ACCESS_TOKEN")
    
    result = service.list_workflows(page_size=10)
    
    if result.get("success"):
        print(f"✅ 获取工作流列表成功")
        workflows = result.get("data", [])
        print(f"共 {len(workflows)} 个工作流")
        for wf in workflows:
            print(f"  - {wf.get('name')} (ID: {wf.get('id')})")
    else:
        print(f"❌ 获取工作流列表失败: {result.get('error')}")


def example_get_skill_info():
    """示例：获取技能信息"""
    print("=== 获取技能信息示例 ===\n")
    
    service = get_coze_skill_service(access_token="ACCESS_TOKEN")
    
    result = service.get_skill_info(skill_id="your_skill_id")
    
    if result.get("success"):
        print(f"✅ 获取技能信息成功")
        print(f"详情: {result.get('data')}")
    else:
        print(f"❌ 获取技能信息失败: {result.get('error')}")


def example_list_skills():
    """示例：列出技能"""
    print("=== 列出技能示例 ===\n")
    
    service = get_coze_skill_service(access_token="ACCESS_TOKEN")
    
    result = service.list_skills(page_size=10)
    
    if result.get("success"):
        print(f"✅ 获取技能列表成功")
        skills = result.get("data", [])
        print(f"共 {len(skills)} 个技能")
        for skill in skills:
            print(f"  - {skill.get('name')} (ID: {skill.get('id')})")
    else:
        print(f"❌ 获取技能列表失败: {result.get('error')}")


def example_workflow_with_retry():
    """示例：带重试的工作流调用"""
    from tenacity import retry, stop_after_attempt, wait_exponential
    
    service = get_coze_workflow_service(access_token="ACCESS_TOKEN")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def call_workflow_with_retry():
        """带重试的工作流调用"""
        return service.run_workflow(
            workflow_id="your_workflow_id",
            params={"input_text": "测试"}
        )
    
    try:
        result = call_workflow_with_retry()
        print(f"✅ 工作流调用成功（可能重试了多次）")
        print(f"结果: {result.get('data')}")
    except Exception as e:
        print(f"❌ 工作流调用失败（已重试3次）: {str(e)}")


def example_skill_with_cache():
    """示例：带缓存的技能调用"""
    from functools import lru_cache

    service = get_coze_skill_service(access_token="ACCESS_TOKEN")
    
    # 使用LRU缓存，最多缓存100个结果
    @lru_cache(maxsize=100)
    def call_skill_cached(query: str):
        """带缓存的技能调用"""
        return service.call_skill(
            skill_id="your_skill_id",
            skill_params={"query": query}
        )
    
    # 第一次调用
    result1 = call_skill_cached("盗窃罪的定义")
    print(f"第一次调用: {result1.get('success')}")
    
    # 第二次调用（从缓存读取）
    result2 = call_skill_cached("盗窃罪的定义")
    print(f"第二次调用（缓存）: {result2.get('success')}")


if __name__ == "__main__":
    print("=" * 60)
    print("  扣子工作流和技能API调用示例")
    print("=" * 60)
    print()
    
    # 选择要运行的示例
    # example_run_workflow()
    # example_run_workflow_stream()
    # example_call_skill()
    # example_get_workflow_info()
    # example_list_workflows()
    # example_get_skill_info()
    # example_list_skills()
    # example_workflow_with_retry()
    # example_skill_with_cache()
    
    print("\n请取消注释其中一个示例函数来运行")
    print("\n⚠️  提示：请先替换代码中的 ACCESS_TOKEN 和工作流/技能ID为实际值！")
