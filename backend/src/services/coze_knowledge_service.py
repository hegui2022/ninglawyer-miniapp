"""
扣子知识库服务（Coze Knowledge Service）
提供调用扣子平台知识库检索的API接口
"""

import requests
import time
from typing import Dict, Any, Optional, List
from loguru import logger


class CozeKnowledgeService:
    """扣子知识库服务"""
    
    def __init__(self, access_token: str = None, dataset_id: str = None):
        """
        初始化知识库服务
        
        Args:
            access_token: 访问令牌（Access Token）
            dataset_id: 知识库ID（Dataset ID）
        """
        self.access_token = access_token or "ACCESS_TOKEN"  # 占位符
        self.dataset_id = dataset_id or "DATASET_ID"  # 占位符
        self.base_url = "https://api.coze.cn"
        
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
        
        # 构建请求URL
        url = f"{self.base_url}/v1/dataset/retrieve"
        
        # 构建请求头
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # 构建请求体
        data = {
            "dataset_id": target_dataset_id,
            "query": query,
            "top_k": top_k
        }
        
        # 如果设置了最小分数，添加到请求中
        if min_score > 0.0:
            data["min_score"] = min_score
        
        try:
            logger.info(f"🔍 检索知识库：{query[:50]}... (Dataset: {target_dataset_id})")
            
            # 发送请求
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            # 处理响应
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            error_msg = "请求超时，请检查网络连接"
            logger.error(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "timeout"
            }
            
        except requests.exceptions.ConnectionError:
            error_msg = "网络连接失败，请检查网络设置"
            logger.error(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "connection_error"
            }
            
        except Exception as e:
            error_msg = f"检索失败：{str(e)}"
            logger.error(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "unknown_error"
            }
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        处理API响应
        
        Args:
            response: HTTP响应对象
            
        Returns:
            格式化的结果
        """
        # 检查HTTP状态码
        if response.status_code == 200:
            try:
                result = response.json()
                
                # 检查业务状态码
                if result.get("code") == 0 or result.get("success") is True:
                    # 成功
                    logger.info(f"✅ 检索成功，返回 {len(result.get('data', []))} 条结果")
                    return {
                        "success": True,
                        "data": self._format_results(result.get("data", [])),
                        "total": len(result.get("data", [])),
                        "query": result.get("query", "")
                    }
                else:
                    # 业务错误
                    error_msg = result.get("msg", result.get("message", "未知错误"))
                    logger.error(f"❌ 业务错误：{error_msg}")
                    return {
                        "success": False,
                        "error": error_msg,
                        "error_type": "business_error",
                        "code": result.get("code")
                    }
                    
            except Exception as e:
                # JSON解析失败
                error_msg = f"响应解析失败：{str(e)}"
                logger.error(f"❌ {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "error_type": "parse_error",
                    "response_text": response.text[:500]
                }
        
        elif response.status_code == 401:
            # Token过期或无效
            error_msg = "Access Token无效或已过期，请重新获取"
            logger.error(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "token_expired",
                "http_status": 401
            }
        
        elif response.status_code == 404:
            # Dataset ID不存在
            error_msg = f"Dataset ID不存在：{response.request.get('dataset_id', 'unknown')}"
            logger.error(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "dataset_not_found",
                "http_status": 404
            }
        
        elif response.status_code == 400:
            # 请求参数错误
            error_msg = "请求参数错误，请检查输入"
            logger.error(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "bad_request",
                "http_status": 400
            }
        
        elif response.status_code == 429:
            # 请求过于频繁
            error_msg = "请求过于频繁，请稍后再试"
            logger.error(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "rate_limit",
                "http_status": 429
            }
        
        else:
            # 其他HTTP错误
            error_msg = f"请求失败，HTTP状态码：{response.status_code}"
            logger.error(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "http_error",
                "http_status": response.status_code,
                "response_text": response.text[:500]
            }
    
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
    
    def set_access_token(self, access_token: str):
        """
        设置Access Token
        
        Args:
            access_token: 新的Access Token
        """
        self.access_token = access_token
        logger.info("✅ Access Token已更新")
    
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


def get_coze_knowledge_service(access_token: str = None, dataset_id: str = None) -> CozeKnowledgeService:
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
            _coze_knowledge_service.set_access_token(access_token)
        if dataset_id:
            _coze_knowledge_service.set_dataset_id(dataset_id)
    
    return _coze_knowledge_service


# 导出
__all__ = [
    "CozeKnowledgeService",
    "get_coze_knowledge_service"
]
