"""
脱敏技能模块（Desensitize Skill）
对敏感信息进行脱敏处理
"""

import re
import json
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from loguru import logger


class DesensitizeSkill:
    """脱敏技能"""
    
    def __init__(self, model: str = "doubao-seed-1-8-251228"):
        """
        初始化脱敏技能
        
        Args:
            model: 使用的模型
        """
        self.model = model
        self.client = LLMClient(ctx=new_context(method="invoke"))
        
        # 系统提示词
        self.system_prompt = """你是宁律师脱敏助手，负责对敏感信息进行脱敏处理。

## 你的职责
识别并脱敏以下类型的敏感信息：
1. **姓名**：保留姓氏，名字用*替换（如：张三 → 张*）
2. **身份证号**：保留前3位和后2位，中间用*替换（如：123456789012345678 → 123***********678）
3. **手机号**：保留前3位和后4位，中间用*替换（如：13812345678 → 138****5678）
4. **地址**：保留省市区，详细地址用*替换（如：北京市朝阳区xxx街道100号 → 北京市朝阳区***）
5. **邮箱**：保留@前的首字母和域名（如：zhangsan@example.com → z***@example.com）

## 工作流程
1. 分析输入文本，识别敏感信息
2. 按照脱敏规则进行处理
3. 返回JSON格式结果：
   {
     "original": "原始文本",
     "desensitized": "脱敏后文本",
     "details": [
       {
         "type": "信息类型",
         "original": "原始值",
         "desensitized": "脱敏后值"
       }
     ]
   }

## 注意事项
- 确保脱敏后的文本仍然可读
- 对于无法识别的信息，保持原样
- 只返回JSON格式结果
"""
        
        logger.info("🔒 脱敏技能初始化完成")
    
    def execute(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行脱敏
        
        Args:
            user_input: 用户输入（包含敏感信息的文本）
            context: 上下文信息
            
        Returns:
            脱敏结果
        """
        logger.info(f"🔒 开始脱敏处理：{user_input[:50]}...")
        
        try:
            # 使用LLM进行智能脱敏
            result = self._llm_desensitize(user_input)
            
            logger.info("✅ 脱敏处理完成")
            return {
                "success": True,
                "data": result
            }
            
        except Exception as e:
            logger.error(f"❌ 脱敏失败：{str(e)}")
            
            # 降级处理：使用规则脱敏
            result = self._rule_based_desensitize(user_input)
            
            return {
                "success": True,
                "data": result,
                "fallback": True
            }
    
    def _llm_desensitize(self, text: str) -> Dict[str, Any]:
        """
        使用LLM进行智能脱敏
        
        Args:
            text: 输入文本
            
        Returns:
            脱敏结果
        """
        prompt = f"""请对以下文本中的敏感信息进行脱敏处理：

{text}

返回JSON格式：
{{
  "original": "原始文本",
  "desensitized": "脱敏后文本",
  "details": [
    {{
      "type": "信息类型",
      "original": "原始值",
      "desensitized": "脱敏后值"
    }}
  ]
}}

只返回JSON，不要其他内容。"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.client.invoke(
            messages=messages,
            model=self.model,
            temperature=0.2,
            max_completion_tokens=2000
        )
        
        content = response.content
        if isinstance(content, str):
            content = content.strip()
        
        # 解析JSON
        json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(content)
        
        return result
    
    def _rule_based_desensitize(self, text: str) -> Dict[str, Any]:
        """
        基于规则的脱敏（降级方案）
        
        Args:
            text: 输入文本
            
        Returns:
            脱敏结果
        """
        details = []
        desensitized = text
        
        # 1. 身份证号脱敏
        id_pattern = r'\b(\d{3})\d{12}(\d{3})\b'
        id_matches = re.findall(id_pattern, text)
        for match in id_matches:
            original = match[0] + 'X' * 12 + match[1]
            desensitized_value = match[0] + '*' * 12 + match[1]
            desensitized = desensitized.replace(original, desensitized_value)
            details.append({
                "type": "身份证号",
                "original": original,
                "desensitized": desensitized_value
            })
        
        # 2. 手机号脱敏
        phone_pattern = r'\b(1[3-9]\d)(\d{4})(\d{4})\b'
        phone_matches = re.findall(phone_pattern, text)
        for match in phone_matches:
            original = match[0] + match[1] + match[2]
            desensitized_value = match[0] + '****' + match[2]
            desensitized = desensitized.replace(original, desensitized_value)
            details.append({
                "type": "手机号",
                "original": original,
                "desensitized": desensitized_value
            })
        
        # 3. 姓名脱敏（简单规则：2-3个汉字）
        name_pattern = r'([一-龥]{1})([一-龥]{1,2})'
        name_matches = re.findall(name_pattern, text)
        # 只在明确标识为姓名时脱敏（避免过度脱敏）
        
        return {
            "original": text,
            "desensitized": desensitized,
            "details": details
        }


# 全局脱敏技能实例
desensitize_skill = DesensitizeSkill()


# 执行函数（用于注册）
def execute_desensitize(user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """脱敏技能执行函数"""
    return desensitize_skill.execute(user_input, context)
