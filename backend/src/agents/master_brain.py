"""
主脑智能体（Master Brain）
负责任务路由和协调各个技能模块
"""

import os
import re
import json
from typing import Dict, Any, List
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from loguru import logger

from src.utils.skill_registry import skill_registry


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
        
        # 系统提示词
        self.system_prompt = """你是宁律师主脑智能体，负责理解用户意图并路由到对应的技能模块。

## 你的职责
1. 理解用户输入的真实意图
2. 根据意图选择合适的技能模块
3. 将用户请求转发给对应技能
4. 整合技能返回的结果

## 可用技能模块
### 1. 脱敏技能（desensitize）
- 功能：对敏感信息进行脱敏处理
- 触发关键词：脱敏、隐私、匿名、隐藏信息、XXX
- 处理内容：姓名、身份证、手机号、地址等

### 2. 民事咨询技能（civil_consult）
- 功能：提供民事法律咨询服务
- 触发关键词：咨询、法律、纠纷、起诉、官司、怎么办、怎么处理
- 涵盖领域：债务纠纷、婚姻家庭、劳动争议、侵权责任等

### 3. 合同起草技能（contract）
- 功能：起草和审查合同
- 触发关键词：合同、协议、条款、起草、审查、模板
- 支持类型：借款合同、租赁合同、劳动合同、买卖合同等

## 工作流程
1. 分析用户输入，识别意图
2. 选择合适的技能模块
3. 返回JSON格式的路由决策：
   {
     "skill": "技能名称",
     "confidence": 置信度(0-1),
     "reasoning": "选择理由",
     "parameters": "传递给技能的参数"
   }

## 注意事项
- 如果用户意图不明确，设置 confidence 较低
- 优先选择最相关的技能
- reasoning 字段简要说明选择理由
"""
        
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
        if confidence < 0.5:
            # 置信度低，需要澄清
            return {
                "success": False,
                "error": "意图不明确，请问您需要：\n1. 脱敏信息\n2. 法律咨询\n3. 合同起草/审查",
                "clarification_needed": True
            }
        
        # 3. 权限检查
        if user_id:
            permission_check = skill_registry.check_user_permission(skill_name, user_id)
            if not permission_check["has_permission"]:
                logger.warning(f"⚠️ 用户 {user_id} 无权限使用技能：{skill_name}")
                return {
                    "success": False,
                    "error": permission_check["error"],
                    "upgrade_required": True,
                    "required_subscription": permission_check.get("required_subscription")
                }
        
        # 4. 执行对应技能
        result = skill_registry.execute_skill(
            skill_name, 
            user_id=user_id,
            user_input=user_input, 
            context=context or {}
        )
        
        return result
    
    def _identify_intent(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        识别用户意图
        
        Args:
            user_input: 用户输入
            context: 上下文
            
        Returns:
            意图识别结果
        """
        try:
            # 构造提示词
            prompt = f"""用户输入：{user_input}

请识别用户意图并返回JSON格式结果：
{{
  "skill": "技能名称(desensitize/civil_consult/contract)",
  "confidence": 置信度(0-1),
  "reasoning": "选择理由",
  "parameters": "传递给技能的参数"
}}

只返回JSON，不要其他内容。"""
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            # 调用LLM
            response = self.client.invoke(
                messages=messages,
                model=self.model,
                temperature=0.3,
                max_completion_tokens=2000
            )
            
            # 解析响应
            content = response.content
            if isinstance(content, str):
                content = content.strip()
            
            # 提取JSON
            json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
            if json_match:
                decision = json.loads(json_match.group())
            else:
                decision = json.loads(content)
            
            logger.info(f"🎯 意图识别：{decision}")
            
            return {
                "success": True,
                "data": decision
            }
            
        except Exception as e:
            logger.error(f"❌ 意图识别失败：{str(e)}")
            
            # 降级处理：基于关键词匹配
            return self._keyword_routing(user_input)
    
    def _keyword_routing(self, user_input: str) -> Dict[str, Any]:
        """
        基于关键词的降级路由
        
        Args:
            user_input: 用户输入
            
        Returns:
            路由决策
        """
        input_lower = user_input.lower()
        
        # 关键词匹配规则
        if any(keyword in input_lower for keyword in ["脱敏", "隐私", "匿名", "隐藏"]):
            skill = "desensitize"
            confidence = 0.8
            reasoning = "关键词匹配到脱敏功能"
        elif any(keyword in input_lower for keyword in ["咨询", "法律", "纠纷", "起诉", "官司", "怎么办"]):
            skill = "civil_consult"
            confidence = 0.85
            reasoning = "关键词匹配到法律咨询"
        elif any(keyword in input_lower for keyword in ["合同", "协议", "条款", "起草", "审查"]):
            skill = "contract"
            confidence = 0.85
            reasoning = "关键词匹配到合同功能"
        else:
            skill = "civil_consult"  # 默认
            confidence = 0.3
            reasoning = "无法明确识别，默认法律咨询"
        
        return {
            "success": True,
            "data": {
                "skill": skill,
                "confidence": confidence,
                "reasoning": reasoning,
                "parameters": user_input
            }
        }
    
    def list_available_skills(self) -> Dict[str, Any]:
        """列出所有可用技能"""
        skills = skill_registry.list_skills()
        
        result = {}
        for name, skill in skills.items():
            result[name] = {
                "name": skill["name"],
                "description": skill["description"],
                "category": skill["category"]
            }
        
        return result


# 全局主脑实例
master_brain = MasterBrain()
