from langchain.tools import tool
from langchain.tools import ToolRuntime
from coze_coding_dev_sdk import KnowledgeClient, Config
from coze_coding_utils.runtime_ctx.context import new_context


@tool
def search_legal_knowledge(query: str, runtime: ToolRuntime) -> str:
    """
    搜索法律知识库：查询相关法律条文、案例和解答
    
    Args:
        query: 法律问题或关键词，如"拖欠工资怎么办"、"担保责任"等
    
    Returns:
        相关法律知识和建议
    """
    try:
        ctx = new_context(method="knowledge.search")
        config = Config()
        client = KnowledgeClient(config=config, ctx=ctx)
        
        # 搜索知识库，返回最相关的3条结果
        response = client.search(
            query=query,
            top_k=3,
            min_score=0.5  # 设置最低相关性分数
        )
        
        if response.code == 0 and response.chunks:
            results = []
            for i, chunk in enumerate(response.chunks, 1):
                results.append(f"【相关法律知识{i}】\n{chunk.content}")
            
            return "\n\n".join(results)
        else:
            return "知识库中没有找到相关的法律信息，建议咨询专业律师。"
            
    except Exception as e:
        return f"知识库搜索失败：{str(e)}"
