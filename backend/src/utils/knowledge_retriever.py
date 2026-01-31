"""
知识检索层
支持扣子知识库（当前主要知识源）
预留北大法宝MCP接口（未来扩展）
"""

import os
import hashlib
import json
import requests
from loguru import logger
from src.services.coze_knowledge_service import CozeKnowledgeService
from .exception_handler import KnowledgeRetrievalError


class KnowledgeRetriever:
    """
    知识检索器
    
    功能：
    - 调用扣子知识库（当前主要知识源）
    - 预留北大法宝MCP接口（未来扩展）
    - 支持知识检索缓存
    """
    
    def __init__(self):
        # 扣子知识库配置
        access_token = os.getenv("COZE_ACCESS_TOKEN", "")
        dataset_id = os.getenv("COZE_KNOWLEDGE_BASE_ID", "")
        self.knowledge_service = CozeKnowledgeService(
            access_token=access_token,
            dataset_id=dataset_id
        )
        
        # 北大法宝MCP配置（预留，未来扩展）
        self.pkulaw_enabled = os.getenv("PKULAW_ENABLED", "false") == "true"
        if self.pkulaw_enabled:
            self.pkulaw_api_key = os.getenv("PKULAW_MCP_KEY", "")
            self.pkulaw_base_url = os.getenv("PKULAW_MCP_URL", "https://mcp.pkulaw.com/api/v1")
            logger.info("📚 北大法宝MCP已启用")
        
        # Redis客户端（用于缓存）
        self.redis_client = None
        try:
            from storage.redis_client import RedisClient
            self.redis_client = RedisClient()
        except Exception as e:
            logger.warning(f"⚠️ Redis客户端初始化失败，知识检索将不缓存：{e}")
        
        logger.info("📚 知识检索器初始化完成")
    
    def retrieve(self, query: str, scenario: str = None, top_k: int = 3) -> str:
        """
        检索知识
        
        Args:
            query: 查询内容
            scenario: 场景类型（用于未来扩展：不同场景使用不同知识源）
            top_k: 返回结果数量
        
        Returns:
            检索结果（格式化的文本）
        """
        logger.info(f"🔍 知识检索：query='{query}', scenario={scenario}")
        
        # 1. 先查缓存
        cache_key = self._get_cache_key(query, scenario)
        if self.redis_client:
            cached_result = self.redis_client.client.get(cache_key)
            if cached_result:
                logger.info(f"✅ 缓存命中：{cache_key}")
                return cached_result
        
        # 2. 优先级1：北大法宝（如果启用）
        if self.pkulaw_enabled:
            try:
                pkulaw_result = self._retrieve_pkulaw(query, top_k)
                if pkulaw_result:
                    # 缓存结果
                    if self.redis_client:
                        self.redis_client.client.setex(cache_key, 86400, pkulaw_result)  # 24小时过期
                    logger.info(f"✅ 北大法宝检索成功")
                    return pkulaw_result
            except Exception as e:
                logger.warning(f"⚠️ 北大法宝检索失败，降级到扣子知识库：{e}")
        
        # 3. 优先级2：扣子知识库（当前主要知识源）
        try:
            coze_result = self._retrieve_coze(query, top_k)
            if coze_result:
                # 缓存结果
                if self.redis_client:
                    self.redis_client.client.setex(cache_key, 86400, coze_result)  # 24小时过期
                logger.info(f"✅ 扣子知识库检索成功")
                return coze_result
        except Exception as e:
            logger.error(f"❌ 扣子知识库检索失败：{e}")
            raise KnowledgeRetrievalError(f"扣子知识库检索失败：{e}")
        
        logger.warning(f"⚠️ 知识检索无结果：query='{query}'")
        return ""
    
    def _retrieve_coze(self, query: str, top_k: int = 3) -> str:
        """
        调用扣子知识库
        
        Args:
            query: 查询内容
            top_k: 返回结果数量
        
        Returns:
            检索结果（格式化的文本）
        """
        try:
            response = self.knowledge_service.search(
                query=query,
                top_k=top_k
            )
            
            if response and response.get("success") and response.get("data"):
                formatted = "\n\n【参考知识】\n"
                for i, item in enumerate(response["data"], 1):
                    content = item.get('content', '')
                    score = item.get('score', 0.0)
                    # 限制内容长度
                    content_preview = content[:200] + "..." if len(content) > 200 else content
                    formatted += f"{i}. [{score:.2f}] {content_preview}\n"
                return formatted
            
            logger.warning(f"⚠️ 扣子知识库无匹配结果")
            return ""
        
        except Exception as e:
            logger.error(f"❌ 扣子知识库调用失败：{e}")
            raise
    
    def _retrieve_pkulaw(self, query: str, top_k: int = 3) -> str:
        """
        调用北大法宝MCP（预留接口，未来扩展）
        
        Args:
            query: 查询内容
            top_k: 返回结果数量
        
        Returns:
            检索结果（格式化的文本）
        """
        if not self.pkulaw_api_key:
            logger.warning("⚠️ 未配置北大法宝API密钥")
            return ""
        
        headers = {
            "Authorization": f"Bearer {self.pkulaw_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "query": query,
            "type": "law+case",  # 检索法条+案例
            "top_k": top_k
        }
        
        try:
            response = requests.post(
                f"{self.pkulaw_base_url}/search",
                headers=headers,
                json=data,
                timeout=5
            )
            
            if response.status_code == 200:
                results = response.json().get("data", [])
                if results:
                    formatted = "\n\n【权威依据】\n"
                    for i, res in enumerate(results, 1):
                        title = res.get('title', '无标题')
                        content = res.get('content', '')
                        # 限制内容长度
                        content_preview = content[:200] + "..." if len(content) > 200 else content
                        formatted += f"{i}. {title}：{content_preview}\n"
                    return formatted
            
            return ""
        
        except Exception as e:
            logger.error(f"❌ 北大法宝调用失败：{e}")
            raise
    
    def _get_cache_key(self, query: str, scenario: str = None) -> str:
        """
        生成缓存键
        
        Args:
            query: 查询内容
            scenario: 场景类型
        
        Returns:
            缓存键
        """
        # 使用MD5哈希作为缓存键
        cache_str = f"{query}:{scenario or 'general'}"
        cache_hash = hashlib.md5(cache_str.encode('utf-8')).hexdigest()
        return f"knowledge:{cache_hash}"
    
    def clear_cache(self, query: str = None, scenario: str = None):
        """
        清除缓存
        
        Args:
            query: 查询内容（None表示清除所有）
            scenario: 场景类型
        """
        if not self.redis_client:
            logger.warning("⚠️ Redis客户端未初始化")
            return
        
        if query:
            cache_key = self._get_cache_key(query, scenario)
            self.redis_client.client.delete(cache_key)
            logger.info(f"✅ 已清除缓存：{cache_key}")
        else:
            # 清除所有知识缓存
            keys = self.redis_client.client.keys("knowledge:*")
            if keys:
                self.redis_client.client.delete(*keys)
                logger.info(f"✅ 已清除所有知识缓存（共{len(keys)}个）")


# 全局实例
knowledge_retriever = KnowledgeRetriever()


# 导出
__all__ = [
    'KnowledgeRetriever',
    'knowledge_retriever',
]
