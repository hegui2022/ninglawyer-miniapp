"""
主脑智能体（Master Brain）
负责任务路由和协调各个技能模块
"""

import os
import re
import json
from typing import Dict, Any, List
from loguru import logger

from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context

from src.utils.skill_registry import skill_registry
from src.prompts.manager import PromptManager


class MasterBrain:
    """主脑智能体"""
    
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
        
        logger.info("🧠 主脑智能体初始化完成")
    
    def route(self, user_input: str, user_id: int = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        路由请求到对应技能（带权限检查）
        
        Args:
            user_input: 用户输入
            user_id: 用户ID（用于权限检查）
            context: 上下文信息
            
        Returns:
            路由结果
        """
        logger.info(f"🔍 路由请求：{user_input[:50]}... (用户ID: {user_id})")
        
        # 1. 意图识别
        routing_decision = self._identify_intent(user_input, context)
        
        if not routing_decision["success"]:
            return routing_decision
        
        skill_name = routing_decision["data"]["skill"]
        confidence = routing_decision["data"]["confidence"]
        
        logger.info(f"🎯 路由到：{skill_name} (置信度：{confidence:.2f})")
        
        # 2. 执行技能
        try:
            result = self._execute_skill(skill_name, user_input, user_id, context)
            return result
        except Exception as e:
            logger.error(f"❌ 技能执行失败：{str(e)}")
            return {
                "success": False,
                "error": f"技能执行失败：{str(e)}",
                "skill": skill_name
            }
    
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
            
            # 解析 JSON
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
            
        except Exception as e:
            logger.error(f"❌ 意图识别失败：{str(e)}")
            # 降级策略：使用关键词匹配
            return self._fallback_intent_recognition(user_input)
    
    def _fallback_intent_recognition(self, user_input: str) -> Dict[str, Any]:
        """
        降级意图识别（关键词匹配）
        
        Args:
            user_input: 用户输入
            
        Returns:
            意图识别结果
        """
        question_lower = user_input.lower()
        
        # 脱敏
        if any(keyword in question_lower for keyword in ["脱敏", "隐私", "匿名", "隐藏", "xxx"]):
            return {
                "success": True,
                "data": {
                    "skill": "desensitize",
                    "confidence": 0.9,
                    "reasoning": "关键词匹配到脱敏功能",
                    "parameters": user_input
                }
            }
        
        # 合同
        elif any(keyword in question_lower for keyword in ["合同", "协议", "起草", "审查"]):
            if "审查" in question_lower or "风险" in question_lower:
                return {
                    "success": True,
                    "data": {
                        "skill": "contract_review",
                        "confidence": 0.85,
                        "reasoning": "关键词匹配到合同审查功能",
                        "parameters": user_input
                    }
                }
            else:
                return {
                    "success": True,
                    "data": {
                        "skill": "contract_draft",
                        "confidence": 0.85,
                        "reasoning": "关键词匹配到合同起草功能",
                        "parameters": user_input
                    }
                }
        
        # 法律咨询
        elif any(keyword in question_lower for keyword in ["咨询", "法律", "纠纷", "起诉", "官司", "怎么办"]):
            return {
                "success": True,
                "data": {
                    "skill": "civil_consult",
                    "confidence": 0.8,
                    "reasoning": "关键词匹配到法律咨询功能",
                    "parameters": user_input
                }
            }
        
        # 默认
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
    
    def _execute_skill(self, skill_name: str, user_input: str, user_id: int, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行技能
        
        Args:
            skill_name: 技能名称
            user_input: 用户输入
            user_id: 用户ID
            context: 上下文信息
            
        Returns:
            执行结果
        """
        # 从技能注册表获取技能
        skill = skill_registry.get_skill(skill_name)
        
        if not skill:
            logger.warning(f"⚠️ 技能不存在：{skill_name}")
            return {
                "success": False,
                "error": f"技能不存在：{skill_name}"
            }
        
        # 检查权限
        if user_id:
            if not skill_registry.check_permission(user_id, skill_name):
                logger.warning(f"⚠️ 用户无权限使用技能：{skill_name}")
                return {
                    "success": False,
                    "error": "无权限使用该功能，请升级套餐",
                    "skill": skill_name
                }
        
        # 执行技能
        logger.info(f"🚀 执行技能：{skill_name}")
        result = skill.execute(user_input, context)
        
        return result


# 创建全局实例
master_brain = MasterBrain()
