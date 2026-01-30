"""
扣子智能体API调用示例
"""

from backend.src.services.coze_agent_service import get_coze_agent_service
import os


def example_run_bot():
    """示例：运行智能体"""
    # 确保配置了环境变量
    # COZE_CLIENT_ID=your_client_id
    # COZE_CLIENT_SECRET=your_client_secret
    # COZE_API_BASE_URL=https://api.coze.cn
    
    # 获取服务实例
    service = get_coze_agent_service()
    
    # 运行智能体
    result = service.run_bot(
        bot_id="your_bot_id",  # 替换为实际的Bot ID
        query="你好，请帮我检索刑法第二百六十四条",
        user_id="user_12345"
    )
    
    print("智能体执行结果：")
    print(f"成功: {result.get('success')}")
    print(f"会话ID: {result.get('conversation_id')}")
    print(f"回答: {result.get('answer')}")
    
    return result


def example_run_bot_stream():
    """示例：流式运行智能体"""
    service = get_coze_agent_service()
    
    print("流式输出：")
    
    for chunk in service.run_bot_stream(
        bot_id="your_bot_id",  # 替换为实际的Bot ID
        query="你好，请帮我检索刑法第二百六十四条",
        user_id="user_12345"
    ):
        if chunk.get("event") == "message":
            print(chunk.get("data", {}).get("content", ""), end="")
        elif chunk.get("event") == "conversation.message.completed":
            print("\n\n对话完成！")
        elif chunk.get("event") == "error":
            print(f"\n错误: {chunk.get('data', {}).get('error')}")


def example_multi_turn_conversation():
    """示例：多轮对话"""
    service = get_coze_agent_service()
    
    conversation_id = None
    
    # 第一轮
    print("第一轮对话：")
    result1 = service.run_bot(
        bot_id="your_bot_id",
        query="盗窃罪的定义是什么？",
        user_id="user_12345"
    )
    print(result1.get("answer"))
    conversation_id = result1.get("conversation_id")
    
    # 第二轮（使用会话ID）
    print("\n第二轮对话：")
    result2 = service.run_bot(
        bot_id="your_bot_id",
        query="那量刑标准呢？",
        user_id="user_12345",
        conversation_id=conversation_id
    )
    print(result2.get("answer"))


def example_get_bot_list():
    """示例：获取Bot列表"""
    service = get_coze_agent_service()
    
    result = service.get_bot_list(page_size=20)
    
    if result.get("success"):
        print(f"共找到 {result.get('total')} 个Bot:")
        for bot in result.get("bots", []):
            print(f"- {bot.get('bot_id')}: {bot.get('bot_name')}")
    else:
        print(f"获取Bot列表失败: {result.get('error')}")


def example_get_bot_info():
    """示例：获取Bot详细信息"""
    service = get_coze_agent_service()
    
    result = service.get_bot_info(bot_id="your_bot_id")
    
    if result.get("success"):
        info = result.get("bot_info")
        print(f"Bot名称: {info.get('bot_name')}")
        print(f"Bot描述: {info.get('description')}")
        print(f"创建时间: {info.get('create_time')}")
    else:
        print(f"获取Bot信息失败: {result.get('error')}")


if __name__ == "__main__":
    # 检查环境变量
    if not os.getenv("COZE_CLIENT_ID") or not os.getenv("COZE_CLIENT_SECRET"):
        print("❌ 错误：请先配置环境变量")
        print("COZE_CLIENT_ID=your_client_id")
        print("COZE_CLIENT_SECRET=your_client_secret")
    else:
        # 运行示例
        print("🚀 运行智能体API示例\n")
        
        # 选择要运行的示例
        # example_run_bot()
        # example_run_bot_stream()
        # example_multi_turn_conversation()
        # example_get_bot_list()
        # example_get_bot_info()
        
        print("请取消注释其中一个示例函数来运行")
