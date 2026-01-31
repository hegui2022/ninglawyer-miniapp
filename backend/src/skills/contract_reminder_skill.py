"""
合同提醒技能模块（Contract Reminder Skill）
管理合同提醒（乐约小程序）
"""

import re
import json
from typing import Dict, Any
from datetime import datetime, timedelta
from loguru import logger


class ContractReminderSkill:
    """合同提醒技能"""
    
    def __init__(self, model: str = "doubao-seed-1-8-251228"):
        """
        初始化合同提醒技能
        
        Args:
            model: 使用的模型
        """
        self.model = model
        
        logger.info("🔔 合同提醒技能初始化完成")
    
    def execute(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行合同提醒
        
        Args:
            user_input: 用户输入（设置提醒或查询提醒）
            context: 上下文信息
            
        Returns:
            提醒设置结果或提醒列表
        """
        logger.info(f"🔔 处理合同提醒请求...")
        
        try:
            # 判断用户意图（设置提醒/查询提醒）
            if any(keyword in user_input for keyword in ["设置", "添加", "新建", "创建"]):
                return self._set_reminder(user_input, context)
            elif any(keyword in user_input for keyword in ["查询", "查看", "列表", "我的提醒"]):
                return self._query_reminders(user_input, context)
            else:
                # 默认：分析合同并提供提醒建议
                return self._analyze_reminders(user_input, context)
        
        except Exception as e:
            logger.error(f"❌ 合同提醒处理失败：{str(e)}")
            # 降级：返回提示信息
            return {
                "success": False,
                "error": "合同提醒处理失败，请稍后重试"
            }
    
    def _set_reminder(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        设置合同提醒
        
        Args:
            user_input: 用户输入
            context: 上下文信息
            
        Returns:
            提醒设置结果
        """
        logger.info("🔔 设置合同提醒...")
        
        # 构建提示词
        from src.prompts.skills.contract_reminder import CONTRACT_REMINDER_SYSTEM
        
        system_prompt = CONTRACT_REMINDER_SYSTEM.format(disclaimer="")
        user_message = f"""用户请求：
{user_input}

请提取用户的提醒设置信息，并以JSON格式返回：
{{
  "contract_name": "合同名称",
  "contract_type": "合同类型",
  "reminder_type": "提醒类型（到期提醒/付款提醒/续签提醒/重要事项提醒）",
  "reminder_date": "提醒日期（YYYY-MM-DD）",
  "reminder_time": "提醒时间（HH:MM，可选）",
  "reminder_content": "提醒内容",
  "advance_days": 提前天数（可选，默认7天）
}}

只返回JSON，不要其他内容。"""
        
        # 调用 LLM
        from coze_coding_dev_sdk import LLMClient
        from coze_coding_utils.runtime_ctx.context import new_context
        
        client = LLMClient(ctx=new_context(method="invoke"))
        response = client.invoke(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model=self.model,
            temperature=0.3,
            max_completion_tokens=1500
        )
        
        content = response.content
        if isinstance(content, str):
            content = content.strip()
        
        # 解析JSON
        try:
            json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
            if json_match:
                reminder_info = json.loads(json_match.group())
            else:
                reminder_info = json.loads(content)
        except:
            # 解析失败，返回提示
            return {
                "success": False,
                "error": "无法解析提醒信息，请提供更详细的描述（如：合同名称、提醒日期、提醒类型）"
            }
        
        # 验证必要字段
        required_fields = ["contract_name", "reminder_type", "reminder_date"]
        for field in required_fields:
            if field not in reminder_info or not reminder_info[field]:
                return {
                    "success": False,
                    "error": f"缺少必要字段：{field}"
                }
        
        # 模拟保存提醒（实际应该存入数据库）
        reminder_id = f"REM{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        logger.info("✅ 合同提醒设置成功")
        return {
            "success": True,
            "data": {
                "reminder_id": reminder_id,
                "contract_name": reminder_info["contract_name"],
                "contract_type": reminder_info.get("contract_type", "未指定"),
                "reminder_type": reminder_info["reminder_type"],
                "reminder_date": reminder_info["reminder_date"],
                "reminder_time": reminder_info.get("reminder_time", "09:00"),
                "reminder_content": reminder_info.get("reminder_content", ""),
                "advance_days": reminder_info.get("advance_days", 7),
                "status": "已设置",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "message": f"提醒设置成功！将在{reminder_info['reminder_date']}提醒您"
        }
    
    def _query_reminders(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        查询合同提醒列表
        
        Args:
            user_input: 用户输入
            context: 上下文信息
            
        Returns:
            提醒列表
        """
        logger.info("🔔 查询合同提醒列表...")
        
        # 模拟查询提醒列表（实际应该从数据库查询）
        # 这里返回一个示例列表
        today = datetime.now().strftime("%Y-%m-%d")
        next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        
        logger.info("✅ 查询完成")
        return {
            "success": True,
            "data": {
                "total": 2,
                "reminders": [
                    {
                        "reminder_id": "REM20240101000000",
                        "contract_name": "房屋租赁合同",
                        "contract_type": "租赁合同",
                        "reminder_type": "到期提醒",
                        "reminder_date": next_week,
                        "reminder_time": "09:00",
                        "reminder_content": "租赁合同即将到期，请提前准备续签或退租",
                        "status": "待提醒"
                    },
                    {
                        "reminder_id": "REM20240115000000",
                        "contract_name": "借款合同",
                        "contract_type": "借款合同",
                        "reminder_type": "付款提醒",
                        "reminder_date": today,
                        "reminder_time": "14:00",
                        "reminder_content": "还款日到了，请及时还款",
                        "status": "已提醒"
                    }
                ]
            },
            "message": "查询成功！您共有2个提醒"
        }
    
    def _analyze_reminders(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        分析合同并提供提醒建议
        
        Args:
            user_input: 用户输入
            context: 上下文信息
            
        Returns:
            提醒建议
        """
        logger.info("🔔 分析合同并生成提醒建议...")
        
        # 构建提示词
        from src.prompts.skills.contract_reminder import CONTRACT_REMINDER_SYSTEM
        
        system_prompt = CONTRACT_REMINDER_SYSTEM.format(disclaimer="")
        user_message = f"""合同内容：
{user_input}

请分析这份合同，建议需要设置哪些提醒，并以JSON格式返回：
{{
  "analysis": "合同分析",
  "suggested_reminders": [
    {{
      "reminder_type": "提醒类型",
      "reminder_content": "提醒内容",
      "suggested_date": "建议提醒日期",
      "advance_days": 建议提前天数
    }}
  ],
  "key_points": ["关键点1", "关键点2"],
  "recommendations": ["建议1", "建议2"]
}}

只返回JSON，不要其他内容。"""
        
        # 调用 LLM
        from coze_coding_dev_sdk import LLMClient
        from coze_coding_utils.runtime_ctx.context import new_context
        
        client = LLMClient(ctx=new_context(method="invoke"))
        response = client.invoke(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model=self.model,
            temperature=0.5,
            max_completion_tokens=2000
        )
        
        content = response.content
        if isinstance(content, str):
            content = content.strip()
        
        # 解析JSON
        try:
            json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(content)
        except:
            # 解析失败，返回默认建议
            result = {
                "analysis": "未能完全分析合同内容",
                "suggested_reminders": [],
                "key_points": [],
                "recommendations": ["请提供完整的合同内容以获取准确的提醒建议"]
            }
        
        logger.info("✅ 提醒建议生成完成")
        return {
            "success": True,
            "data": result
        }


# 全局实例
contract_reminder_skill = ContractReminderSkill()


# 执行函数（用于注册）
def execute_contract_reminder(user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """合同提醒技能执行函数"""
    return contract_reminder_skill.execute(user_input, context)
