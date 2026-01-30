"""
法律知识库数据适配器（Legal Knowledge Adapter）
专门用于将扣子知识库返回的法律数据转换为微信小程序格式
"""

import re
from typing import Dict, Any, List, Optional
from loguru import logger

from .base_adapter import DataAdapterBase


class LegalKnowledgeAdapter(DataAdapterBase):
    """法律知识库数据适配器"""
    
    def __init__(self, enable_llm_enhance: bool = True):
        """
        初始化法律知识库适配器
        
        Args:
            enable_llm_enhance: 是否启用大模型增强
        """
        super().__init__(enable_llm_enhance)
        
        # 初始化法律相关的正则表达式模式
        self._init_legal_patterns()
    
    def _init_legal_patterns(self):
        """初始化法律相关的正则表达式模式"""
        # 法条相关
        self.patterns.update({
            # 法条编号：第二百六十四条
            "law_article": r"第[零一二三四五六七八九十百千万]+条",
            
            # 刑期：三年以下有期徒刑、拘役、管制
            "penalty_term": r"([一二三四五六七八九十]+)[年][以下以上]?[，、]?\s*(有期徒刑|拘役|管制)",
            
            # 金额：三千元以上、三万元以下
            "money_amount": r"([零一二三四五六七八九十百千万]+)[元][以下以上]?",
            
            # 法条名称：《中华人民共和国刑法》
            "law_name": r"《([^》]+)》",
            
            # 罪名：【盗窃罪】
            "crime_name": r"【([^】]+)】",
            
            # 刑罚类型：罚金、没收财产
            "punishment_type": r"(并处或者单处|并处|单处)?\s*(罚金|没收财产)",
            
            # 情节：数额较大、多次盗窃、入户盗窃
            "circumstance": r"(数额较大|数额巨大|数额特别巨大|多次盗窃|入户盗窃|携带凶器盗窃|扒窃)"
        })
    
    def get_target_format(self) -> str:
        """获取目标格式类型"""
        return "wechat_miniprogram"
    
    def _format_single_item(self, item: Dict) -> Dict:
        """
        格式化单个法律数据项
        
        Args:
            item: 数据项
            
        Returns:
            格式化后的数据项
        """
        formatted_item = super()._format_single_item(item)
        
        content = item.get("content", "")
        
        # 1. 提取法条编号
        article_number = self._extract_article_number(content)
        if article_number:
            formatted_item["article_number"] = article_number
        
        # 2. 提取法条名称
        law_name = self._extract_law_name(content)
        if law_name:
            formatted_item["law_name"] = law_name
        
        # 3. 提取罪名
        crime_name = self._extract_crime_name(content)
        if crime_name:
            formatted_item["crime_name"] = crime_name
        
        # 4. 提取刑期信息
        penalties = self._extract_penalties(content)
        if penalties:
            formatted_item["penalties"] = penalties
        
        # 5. 提取金额信息
        amounts = self._extract_amounts(content)
        if amounts:
            formatted_item["amounts"] = amounts
        
        # 6. 提取情节
        circumstances = self._extract_circumstances(content)
        if circumstances:
            formatted_item["circumstances"] = circumstances
        
        # 7. 内容分段
        formatted_item["content_sections"] = self._split_content_sections(content)
        
        # 8. 提取关键词
        formatted_item["keywords"] = self._extract_keywords(content)
        
        return formatted_item
    
    def _extract_article_number(self, content: str) -> Optional[str]:
        """提取法条编号"""
        match = re.search(self.patterns["law_article"], content)
        return match.group() if match else None
    
    def _extract_law_name(self, content: str) -> Optional[str]:
        """提取法条名称"""
        match = re.search(self.patterns["law_name"], content)
        return match.group(1) if match else None
    
    def _extract_crime_name(self, content: str) -> Optional[str]:
        """提取罪名"""
        match = re.search(self.patterns["crime_name"], content)
        return match.group(1) if match else None
    
    def _extract_penalties(self, content: str) -> List[Dict[str, Any]]:
        """提取刑期信息"""
        penalties = []
        
        matches = re.finditer(self.patterns["penalty_term"], content)
        for match in matches:
            penalties.append({
                "term": match.group(1),  # 三年、五年等
                "type": match.group(2)   # 有期徒刑、拘役、管制
            })
        
        return penalties
    
    def _extract_amounts(self, content: str) -> List[str]:
        """提取金额信息"""
        amounts = []
        
        matches = re.finditer(self.patterns["money_amount"], content)
        for match in matches:
            amounts.append(match.group())
        
        return amounts
    
    def _extract_circumstances(self, content: str) -> List[str]:
        """提取情节"""
        circumstances = []
        
        matches = re.finditer(self.patterns["circumstance"], content)
        for match in matches:
            circumstance = match.group()
            if circumstance not in circumstances:
                circumstances.append(circumstance)
        
        return circumstances
    
    def _split_content_sections(self, content: str) -> List[Dict[str, str]]:
        """
        内容分段
        
        将法条内容分段，便于小程序显示
        """
        sections = []
        
        # 按【】分段（罪名、分则等）
        if "【" in content:
            parts = content.split("【")
            for i, part in enumerate(parts[1:], 1):  # 跳过第一段（通常是法条标题）
                section_name = part.split("】")[0]
                section_content = part.split("】")[1] if "】" in part else part
                sections.append({
                    "section_id": f"section_{i}",
                    "section_name": f"【{section_name}】",
                    "content": section_content.strip()
                })
        else:
            # 按句号分段
            sentences = re.split(r'[。；;]', content)
            for i, sentence in enumerate(sentences):
                if sentence.strip():
                    sections.append({
                        "section_id": f"section_{i}",
                        "section_name": f"第{i+1}段",
                        "content": sentence.strip()
                    })
        
        return sections
    
    def _extract_keywords(self, content: str) -> List[str]:
        """
        提取关键词
        
        使用正则表达式提取关键词
        """
        keywords = set()
        
        # 提取法条编号
        article_match = re.search(self.patterns["law_article"], content)
        if article_match:
            keywords.add(article_match.group())
        
        # 提取罪名
        crime_match = re.search(self.patterns["crime_name"], content)
        if crime_match:
            keywords.add(crime_match.group(1))
        
        # 提取情节
        circumstances = self._extract_circumstances(content)
        keywords.update(circumstances)
        
        return list(keywords)
    
    def _llm_enhance(self, data: Dict[str, Any], context: Dict = None) -> Dict[str, Any]:
        """
        使用大模型增强法律数据
        
        Args:
            data: 数据
            context: 上下文
            
        Returns:
            增强后的数据
        """
        if not self.enable_llm_enhance:
            return data
        
        try:
            # 调用大模型生成摘要和关键点
            from coze_coding_dev_sdk import LLMClient
            from coze_coding_utils.runtime_ctx.context import new_context
            
            client = LLMClient(ctx=new_context(method="invoke"))
            
            # 处理每条数据
            if "data" in data and isinstance(data["data"], list):
                for item in data["data"]:
                    content = item.get("content", "")
                    
                    # 生成摘要（如果内容较长）
                    if len(content) > 100:
                        summary = self._generate_summary(client, content)
                        item["summary"] = summary
                    
                    # 提取关键点
                    key_points = self._extract_key_points(client, content)
                    item["key_points"] = key_points
            
            return data
            
        except Exception as e:
            logger.error(f"❌ LLM增强失败：{str(e)}")
            # 降级：返回未增强的数据
            return data
    
    def _generate_summary(self, client, content: str) -> str:
        """生成摘要"""
        prompt = f"""请用简洁的语言总结以下法律条文的主要内容和要点，不超过100字：

{content}

只返回摘要内容，不要其他内容。"""
        
        response = client.invoke(
            messages=[
                {"role": "system", "content": "你是法律摘要专家，擅长提取法律条文的要点"},
                {"role": "user", "content": prompt}
            ],
            model="doubao-seed-1-8-251228",
            max_completion_tokens=500
        )
        
        return response.content.strip()
    
    def _extract_key_points(self, client, content: str) -> List[str]:
        """提取关键点"""
        prompt = f"""请从以下法律条文中提取3-5个关键要点，每点不超过20字：

{content}

返回格式（JSON）：
{{
  "key_points": ["要点1", "要点2", "要点3"]
}}

只返回JSON，不要其他内容。"""
        
        response = client.invoke(
            messages=[
                {"role": "system", "content": "你是法律要点提取专家"},
                {"role": "user", "content": prompt}
            ],
            model="doubao-seed-1-8-251228",
            max_completion_tokens=500
        )
        
        import json
        content_str = response.content.strip()
        
        # 尝试提取JSON
        json_match = re.search(r'\{[^{}]*\}', content_str, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
                return result.get("key_points", [])
            except json.JSONDecodeError:
                pass
        
        # 降级：返回空列表
        return []


# 全局实例
_legal_knowledge_adapter = None


def get_legal_knowledge_adapter(enable_llm_enhance: bool = True) -> LegalKnowledgeAdapter:
    """
    获取法律知识库适配器实例（单例模式）
    
    Args:
        enable_llm_enhance: 是否启用大模型增强
        
    Returns:
        LegalKnowledgeAdapter 实例
    """
    global _legal_knowledge_adapter
    
    if _legal_knowledge_adapter is None:
        _legal_knowledge_adapter = LegalKnowledgeAdapter(enable_llm_enhance)
    
    return _legal_knowledge_adapter
