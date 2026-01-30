"""
数据适配基类（Data Adapter Base Class）
负责将第三方API返回的数据转换为小程序前端需要的格式
采用正则表达式（优先）+ 大模型共同处理的方式
"""

import re
from typing import Dict, Any, List, Optional
from loguru import logger
from abc import ABC, abstractmethod


class DataAdapterBase(ABC):
    """数据适配基类"""
    
    def __init__(self, enable_llm_enhance: bool = True):
        """
        初始化数据适配器
        
        Args:
            enable_llm_enhance: 是否启用大模型增强（默认启用）
        """
        self.enable_llm_enhance = enable_llm_enhance
        
        # 初始化正则表达式模式
        self._init_regex_patterns()
        
        logger.info(f"🔄 数据适配器初始化完成（LLM增强：{enable_llm_enhance}）")
    
    def _init_regex_patterns(self):
        """初始化正则表达式模式（子类可重写）"""
        # 默认模式
        self.patterns = {
            "law_article": r"第[零一二三四五六七八九十百千万]+条",
            "law_number": r"[零一二三四五六七八九十百千万]+",
            "penalty": r"[一二三四五六七八九十]+年[以下以上]?[有期徒刑|拘役|管制]*",
            "amount": r"[零一二三四五六七八九十百千万]+元[以下以上]?"
        }
    
    def adapt(self, raw_data: Dict[str, Any], context: Dict = None) -> Dict[str, Any]:
        """
        适配数据（主入口）
        
        三阶段处理：
        1. 数据清洗（Data Cleaning）
        2. 格式转换（Format Conversion）
        3. 智能增强（LLM Enhancement）
        
        Args:
            raw_data: 原始数据
            context: 上下文信息
            
        Returns:
            适配后的数据
        """
        logger.info("🔄 开始数据适配...")
        
        try:
            # 阶段1：数据清洗
            cleaned_data = self._clean_data(raw_data, context)
            logger.debug(f"✅ 阶段1完成：数据清洗")
            
            # 阶段2：格式转换
            formatted_data = self._format_data(cleaned_data, context)
            logger.debug(f"✅ 阶段2完成：格式转换")
            
            # 阶段3：智能增强
            enhanced_data = self._enhance_data(formatted_data, context)
            logger.debug(f"✅ 阶段3完成：智能增强")
            
            logger.info("✅ 数据适配完成")
            return enhanced_data
            
        except Exception as e:
            logger.error(f"❌ 数据适配失败：{str(e)}")
            return self._create_error_response(str(e))
    
    def _clean_data(self, raw_data: Dict[str, Any], context: Dict = None) -> Dict[str, Any]:
        """
        阶段1：数据清洗
        - 去除多余空格和换行
- 合并重复内容
- 过滤低质量数据
        Args:
            raw_data: 原始数据
            context: 上下文
            
        Returns:
            清洗后的数据
        """
        logger.debug("🧹 开始数据清洗...")
        
        cleaned_data = raw_data.copy()
        
        # 清洗数据列表
        if "data" in cleaned_data and isinstance(cleaned_data["data"], list):
            cleaned_list = []
            
            for item in cleaned_data["data"]:
                # 清洗单个项目
                cleaned_item = self._clean_single_item(item)
                
                # 过滤低质量数据（内容太短或相似度太低）
                if self._is_high_quality(cleaned_item):
                    cleaned_list.append(cleaned_item)
            
            cleaned_data["data"] = cleaned_list
            cleaned_data["total"] = len(cleaned_list)
        
        return cleaned_data
    
    def _clean_single_item(self, item: Dict) -> Dict:
        """
        清洗单个数据项
        
        Args:
            item: 数据项
            
        Returns:
            清洗后的数据项
        """
        cleaned_item = item.copy()
        
        # 清洗content字段
        if "content" in cleaned_item:
            content = cleaned_item["content"]
            
            # 去除多余空格
            content = re.sub(r'\s+', ' ', content)
            
            # 去除特殊字符（保留中文、标点、英文）
            content = re.sub(r'[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\w\s,，.。!！?？;；:：""''（）()【】\[\]]', '', content)
            
            cleaned_item["content"] = content.strip()
        
        # 清洗其他文本字段
        for key in ["title", "summary", "description"]:
            if key in cleaned_item:
                cleaned_item[key] = re.sub(r'\s+', ' ', cleaned_item[key]).strip()
        
        return cleaned_item
    
    def _is_high_quality(self, item: Dict) -> bool:
        """
        判断数据质量
        
        Args:
            item: 数据项
            
        Returns:
            是否高质量
        """
        # 内容长度至少20个字符
        if "content" in item and len(item["content"]) < 20:
            return False
        
        # 相似度至少0.5
        if "score" in item and item["score"] < 0.5:
            return False
        
        return True
    
    def _format_data(self, cleaned_data: Dict[str, Any], context: Dict = None) -> Dict[str, Any]:
        """
        阶段2：格式转换
        - 结构化数据提取
        - 字段映射
        - 正则表达式匹配
        Args:
            cleaned_data: 清洗后的数据
            context: 上下文
            
        Returns:
            格式化后的数据
        """
        logger.debug("📋 开始格式转换...")
        
        formatted_data = cleaned_data.copy()
        
        # 处理数据列表
        if "data" in formatted_data and isinstance(formatted_data["data"], list):
            formatted_list = []
            
            for item in formatted_data["data"]:
                # 格式化单个项目
                formatted_item = self._format_single_item(item)
                formatted_list.append(formatted_item)
            
            formatted_data["data"] = formatted_list
        
        return formatted_data
    
    def _format_single_item(self, item: Dict) -> Dict:
        """
        格式化单个数据项（使用正则表达式）
        
        Args:
            item: 数据项
            
        Returns:
            格式化后的数据项
        """
        formatted_item = item.copy()
        
        # 提取法条编号
        if "content" in item:
            content = item["content"]
            
            # 提取法条编号
            article_match = re.search(self.patterns["law_article"], content)
            if article_match:
                formatted_item["article_number"] = article_match.group()
            
            # 提取刑期
            penalty_match = re.search(self.patterns["penalty"], content)
            if penalty_match:
                formatted_item["penalty"] = penalty_match.group()
            
            # 提取金额
            amount_match = re.search(self.patterns["amount"], content)
            if amount_match:
                formatted_item["amount"] = amount_match.group()
        
        # 添加格式化标记
        formatted_item["formatted"] = True
        
        return formatted_item
    
    def _enhance_data(self, formatted_data: Dict[str, Any], context: Dict = None) -> Dict[str, Any]:
        """
        阶段3：智能增强（使用大模型）
        - 内容摘要
        - 关键点提取
        - 智能分类
        Args:
            formatted_data: 格式化后的数据
            context: 上下文
            
        Returns:
            增强后的数据
        """
        logger.debug("🤖 开始智能增强...")
        
        if not self.enable_llm_enhance:
            logger.debug("⏭️  跳过LLM增强（未启用）")
            return formatted_data
        
        # 使用大模型增强
        enhanced_data = self._llm_enhance(formatted_data, context)
        
        return enhanced_data
    
    def _llm_enhance(self, data: Dict[str, Any], context: Dict = None) -> Dict[str, Any]:
        """
        使用大模型增强数据（子类可重写）
        
        Args:
            data: 数据
            context: 上下文
            
        Returns:
            增强后的数据
        """
        # 默认实现：不做增强
        return data
    
    def _create_error_response(self, error_msg: str) -> Dict[str, Any]:
        """创建错误响应"""
        return {
            "success": False,
            "error": error_msg,
            "error_type": "data_adaptation_error"
        }
    
    # ==================== 子类可重写的方法 ====================
    
    @abstractmethod
    def get_target_format(self) -> str:
        """
        获取目标格式类型（子类必须实现）
        
        Returns:
            格式类型（如 "wechat_miniprogram", "web", "api"）
        """
        pass
