"""
主脑智能体（Master Brain）
负责任务路由和协调各个技能模块
新架构：单一宁律师 + 主脑调度技能 + 动态人设选择 + 知识检索
"""

import os
import re
import json
from typing import Dict, Any, List, Optional
from loguru import logger

from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context

from src.utils.skill_registry import skill_registry
from src.utils.knowledge_retriever import knowledge_retriever
from src.personas.personality_selector import personality_selector
from src.prompts.manager import PromptManager
from src.utils.exception_handler import exception_handler, RouteError, ExceptionLevel


class MasterBrain:
    """
    主脑智能体
    
    功能：
    1. 识别用户类型（个人/企业）
    2. 识别场景类型（family_law/commercial/compliance/general）
    3. 选择人设（静默切换）
    4. 智能触发知识检索（仅法律场景）
    5. 路由到对应技能
    6. 传递完整的上下文信息
    """
    
    def __init__(self, model: str = "doubao-seed-1-8-251228"):
        """
        初始化主脑
        
        Args:
            model: 使用的模型
        """
        self.model = model
        self.client = LLMClient(ctx=new_context(method="invoke"))
        
        # 获取提示词模板（从提示词管理器）
        self.prompt_template = PromptManager.get_skill_prompt('master_brain')
        
        # 初始化人设选择器
        self.personality_selector = personality_selector
        
        # 场景关键词映射
        self.scenario_keywords = {
            "family_law": ["离婚", "婚姻", "夫妻", "配偶", "妻子", "丈夫", "老公", "老婆", 
                          "抚养权", "抚养费", "子女抚养", "孩子", "抚养", "探视", "探视权",
                          "财产分割", "财产", "分割", "房产", "房子", "存款", "股票", "车",
                          "家暴", "暴力", "打人", "保护令", "打我", "老公打", "老婆打", "丈夫打", "妻子打",
                          "出轨", "分居", "彩礼", "感情", "结婚证", "领证"],
            "commercial": ["合同", "协议", "公司", "企业", "商事", "股权", "股东", "投资", "融资",
                          "起草", "审查", "风险", "签约", "签约"],
            "compliance": ["合规", "监管", "制度", "规定", "法规", "标准", "审计", "内控"]
        }
        
        logger.info("🧠 主脑智能体初始化完成（新架构：单一宁律师 + 动态人设 + 知识检索）")
    
    @exception_handler(
        default_return={"success": False, "error": "路由失败", "reply": "抱歉，我这边有点问题，请稍后再试～"},
        log_level=ExceptionLevel.ERROR
    )
    def route(self, user_input: str, user_id: int = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        路由请求到对应技能
        
        新架构流程：
        1. 识别用户类型（个人/企业）
        2. 识别场景类型（family_law/commercial/compliance/general）
        3. 选择人设（静默切换）
        4. 智能触发知识检索（仅法律场景）
        5. 路由到对应技能
        6. 传递完整的上下文信息
        
        Args:
            user_input: 用户输入
            user_id: 用户ID（用于权限检查和用户类型识别）
            context: 上下文信息
            
        Returns:
            路由结果
        """
        logger.info(f"🔍 路由请求：{user_input[:50]}... (用户ID: {user_id})")
        
        # 初始化上下文
        if context is None:
            context = {}
        
        # 1. 识别用户类型（从缓存或数据库）
        user_type = self._get_user_type(user_id, context)
        context["user_type"] = user_type
        
        # 2. 识别场景类型
        scenario = self._identify_scenario(user_input)
        context["scenario"] = scenario
        
        # 3. 选择人设（静默切换，不告知用户）
        # 根据小程序标识、用户类型和场景选择人设
        personality_id = self.personality_selector.select(user_type, scenario, app_id=context.get('app_id'))
        context["personality_id"] = personality_id
        
        logger.info(f"🎭 选择人设：{personality_id} (用户类型={user_type}, 场景={scenario}, 小程序={context.get('app_id', 'default')})")
        
        # 4. 智能触发知识检索（仅法律场景）
        legal_scenarios = ["family_law", "commercial", "compliance"]
        if scenario in legal_scenarios:
            logger.info(f"📚 触发知识检索（场景={scenario}）")
            try:
                knowledge = knowledge_retriever.retrieve(user_input, scenario)
                context["knowledge"] = knowledge
            except Exception as e:
                logger.warning(f"⚠️ 知识检索失败，降级处理：{e}")
                context["knowledge"] = ""  # 知识检索失败时使用空字符串
        else:
            context["knowledge"] = ""  # 情感场景无需知识
        
        # 5. 意图识别 + 路由到技能
        routing_decision = self._identify_intent(user_input, context)
        
        if not routing_decision["success"]:
            return routing_decision
        
        skill_name = routing_decision["data"]["skill"]
        confidence = routing_decision["data"]["confidence"]
        
        logger.info(f"🎯 路由到技能：{skill_name} (置信度：{confidence:.2f})")
        
        # 6. 执行技能（传递完整上下文）
        skill_result = skill_registry.execute(skill_name, user_input, context)
        
        # 处理技能返回结果
        if isinstance(skill_result, str):
            # 技能返回字符串，包装成字典
            result = {
                "success": True,
                "reply": skill_result,
                "skill_used": skill_name,
                "personality_used": personality_id,
                "scenario_used": scenario
            }
        elif isinstance(skill_result, dict):
            # 技能返回字典，添加元数据
            skill_result["skill_used"] = skill_name
            skill_result["personality_used"] = personality_id
            skill_result["scenario_used"] = scenario
            result = skill_result
        else:
            # 未知类型，返回错误
            result = {
                "success": False,
                "error": f"技能返回类型不支持: {type(skill_result)}",
                "skill_used": skill_name,
                "personality_used": personality_id,
                "scenario_used": scenario
            }
        
        return result
    
    def _get_user_type(self, user_id: int, context: Dict[str, Any]) -> str:
        """
        获取用户类型（个人/企业）
        
        Args:
            user_id: 用户ID
            context: 上下文信息
        
        Returns:
            用户类型 ("personal" | "corporate")
        """
        # 优先从上下文获取
        if context and "user_type" in context:
            return context["user_type"]
        
        # 从缓存获取
        if user_id:
            try:
                from src.utils.redis_client import RedisClient
                redis_client = RedisClient()
                user_type = redis_client.get_user_type(user_id)
                if user_type:
                    return user_type
            except Exception as e:
                logger.warning(f"⚠️ 从Redis获取用户类型失败：{e}")
        
        # 默认返回个人用户
        return "personal"
    
    def _identify_scenario(self, user_input: str) -> str:
        """
        识别场景类型
        
        Args:
            user_input: 用户输入
        
        Returns:
            场景类型 ("family_law" | "commercial" | "compliance" | "general")
        """
        question_lower = user_input.lower()
        
        # 检查各场景关键词
        for scenario, keywords in self.scenario_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                logger.info(f"🏷️ 识别场景：{scenario} (关键词匹配)")
                return scenario
        
        # 默认场景
        logger.info(f"🏷️ 识别场景：general (默认)")
        return "general"
    
    def _identify_intent(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        识别用户意图
        
        Args:
            user_input: 用户输入
            context: 上下文信息
        
        Returns:
            意图识别结果
        """
        try:
            # 使用提示词模板
            messages = self.prompt_template.format_messages(
                user_input=user_input
            )
            
            # 调用 LLM
            response = self.client.invoke(
                messages=messages,
                model=self.model,
                temperature=0.3,
                max_completion_tokens=1000
            )
            
            content = response.content.strip()
            logger.debug(f"📝 意图识别返回：{content[:200]}...")
            
            # 解析 JSON
            try:
                json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
                if json_match:
                    decision = json.loads(json_match.group())
                else:
                    decision = json.loads(content)
                
                logger.info(f"✅ 意图识别成功：{decision.get('skill')}")
                
                return {
                    "success": True,
                    "data": decision
                }
            except json.JSONDecodeError as e:
                logger.error(f"❌ JSON解析失败：{e}")
                logger.debug(f"原始内容：{content}")
                # 降级策略：使用关键词匹配
                return self._fallback_intent_recognition(user_input, context)
            
        except Exception as e:
            logger.error(f"❌ 意图识别失败：{str(e)}")
            # 降级策略：使用关键词匹配
            return self._fallback_intent_recognition(user_input, context)
    
    def _fallback_intent_recognition(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        降级意图识别（关键词匹配）
        
        Args:
            user_input: 用户输入
            context: 上下文信息
        
        Returns:
            意图识别结果
        """
        question_lower = user_input.lower()
        
        # 家暴维权（优先级最高）
        if any(keyword in question_lower for keyword in ["家暴", "暴力", "打人", "保护令", "打我", "老公打", "老婆打", "丈夫打", "妻子打"]):
            return {
                "success": True,
                "data": {
                    "skill": "domestic_violence",
                    "confidence": 0.9,
                    "reasoning": "关键词匹配到家暴维权功能",
                    "parameters": user_input
                }
            }
        
        # 财产分割
        elif any(keyword in question_lower for keyword in ["财产分割", "财产", "分割", "房产", "房子", "存款", "股票", "车", "怎么分"]):
            return {
                "success": True,
                "data": {
                    "skill": "property_division",
                    "confidence": 0.85,
                    "reasoning": "关键词匹配到财产分割功能",
                    "parameters": user_input
                }
            }
        
        # 子女抚养
        elif any(keyword in question_lower for keyword in ["抚养权", "抚养费", "子女抚养", "孩子归谁", "孩子抚养", "探视权", "探视"]):
            return {
                "success": True,
                "data": {
                    "skill": "child_custody",
                    "confidence": 0.85,
                    "reasoning": "关键词匹配到子女抚养功能",
                    "parameters": user_input
                }
            }
        
        # 离婚流程
        elif any(keyword in question_lower for keyword in ["离婚流程", "怎么离婚", "离婚", "离婚材料", "协议离婚", "诉讼离婚"]):
            return {
                "success": True,
                "data": {
                    "skill": "divorce_procedure",
                    "confidence": 0.85,
                    "reasoning": "关键词匹配到离婚流程功能",
                    "parameters": user_input
                }
            }
        
        # 脱敏
        elif any(keyword in question_lower for keyword in ["脱敏", "隐私", "匿名", "隐藏", "xxx"]):
            return {
                "success": True,
                "data": {
                    "skill": "desensitize",
                    "confidence": 0.9,
                    "reasoning": "关键词匹配到脱敏功能",
                    "parameters": user_input
                }
            }
        
        # 合同审查
        elif any(keyword in question_lower for keyword in ["合同审查", "合同风险", "审查合同"]):
            return {
                "success": True,
                "data": {
                    "skill": "contract_review",
                    "confidence": 0.85,
                    "reasoning": "关键词匹配到合同审查功能",
                    "parameters": user_input
                }
            }
        
        # 合同起草
        elif any(keyword in question_lower for keyword in ["合同起草", "起草合同", "合同", "协议", "协议起草"]):
            return {
                "success": True,
                "data": {
                    "skill": "contract_draft",
                    "confidence": 0.85,
                    "reasoning": "关键词匹配到合同起草功能",
                    "parameters": user_input
                }
            }
        
        # 法律咨询（默认）
        else:
            return {
                "success": True,
                "data": {
                    "skill": "civil_consult",
                    "confidence": 0.5,
                    "reasoning": "默认路由到法律咨询",
                    "parameters": user_input
                }
            }


# 全局实例
master_brain = MasterBrain()
