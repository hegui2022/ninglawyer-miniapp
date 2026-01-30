"""
扣子知识库服务（Coze Knowledge Service）
提供调用扣子平台知识库检索的API接口
基于BaseThirdPartyAPIService基类实现
"""

from typing import Dict, Any, Optional, List
from loguru import logger

from .base_service import BaseThirdPartyAPIService


class CozeKnowledgeService(BaseThirdPartyAPIService):
    """扣子知识库服务（继承基础服务类）"""
    
    def __init__(self, access_token: str = None, dataset_id: str = None):
        """
        初始化知识库服务
        
        Args:
            access_token: 访问令牌（可选）
            dataset_id: 知识库ID（默认Dataset ID）
        """
        # 使用占位符初始化
        api_key = access_token or "ACCESS_TOKEN"
        base_url = "https://api.coze.cn"
        
        super().__init__(api_key=api_key, base_url=base_url, timeout=30)
        
        self.dataset_id = dataset_id or "DATASET_ID"
        
        logger.info("📚 扣子知识库服务初始化完成")
    
    def search(
        self,
        query: str,
        dataset_id: str = None,
        top_k: int = 5,
        min_score: float = 0.0
    ) -> Dict[str, Any]:
        """
        检索知识库
        
        Args:
            query: 用户问题（查询关键词）
            dataset_id: 知识库ID（可选，默认使用初始化时的ID）
            top_k: 返回结果数量，默认5
            min_score: 最小相似度分数，默认0.0
            
        Returns:
            检索结果
        """
        # 使用传入的dataset_id或默认的dataset_id
        target_dataset_id = dataset_id or self.dataset_id
        
        # 构建请求体
        data = {
            "dataset_id": target_dataset_id,
            "query": query,
            "top_k": top_k
        }
        
        # 如果设置了最小分数，添加到请求中
        if min_score > 0.0:
            data["min_score"] = min_score
        
        logger.info(f"🔍 检索知识库：{query[:50]}... (Dataset: {target_dataset_id})")
        
        # 调用基础请求方法
        result = self._request(
            method="POST",
            path="/v1/dataset/retrieve",
            json=data
        )
        
        # 格式化返回结果
        if result.get("success"):
            data = result.get("data", [])
            result["data"] = self._format_results(data)
            result["total"] = len(data)
            result["query"] = query
        
        return result
    
    def _format_results(self, data: List[Dict]) -> List[Dict[str, Any]]:
        """
        格式化检索结果
        
        Args:
            data: 原始数据
            
        Returns:
            格式化后的结果
        """
        formatted = []
        
        for item in data:
            formatted_item = {
                "content": item.get("content", ""),
                "score": item.get("score", 0.0),
                "document_id": item.get("doc_id", item.get("document_id", "")),
                "metadata": item.get("metadata", {})
            }
            
            # 提取其他可能的字段
            if "title" in item:
                formatted_item["title"] = item.get("title")
            if "chunk_id" in item:
                formatted_item["chunk_id"] = item.get("chunk_id")
            
            formatted.append(formatted_item)
        
        return formatted
    
    def set_dataset_id(self, dataset_id: str):
        """
        设置Dataset ID
        
        Args:
            dataset_id: 新的Dataset ID
        """
        self.dataset_id = dataset_id
        logger.info("✅ Dataset ID已更新")


# 全局实例（单例）
_coze_knowledge_service = None


def get_coze_knowledge_service(
    access_token: str = None,
    dataset_id: str = None
) -> CozeKnowledgeService:
    """
    获取扣子知识库服务实例（单例模式）
    
    Args:
        access_token: Access Token
        dataset_id: Dataset ID
        
    Returns:
        CozeKnowledgeService 实例
    """
    global _coze_knowledge_service
    
    if _coze_knowledge_service is None:
        _coze_knowledge_service = CozeKnowledgeService(access_token, dataset_id)
    else:
        # 如果提供了新的参数，更新现有实例
        if access_token:
            _coze_knowledge_service.set_api_key(access_token)
        if dataset_id:
            _coze_knowledge_service.set_dataset_id(dataset_id)
    
    return _coze_knowledge_service


# 导出
__all__ = [
    "CozeKnowledgeService",
    "get_coze_knowledge_service"
]
