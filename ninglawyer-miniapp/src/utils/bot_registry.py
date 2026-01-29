"""
Bot注册表 - 用于管理和调用扣子Bot
这是连接主脑调度器和扣子Bot的关键组件
支持新版Coze API (v3)
"""

import json
import os
from typing import Dict, Any, Optional
import requests
from loguru import logger

# Bot配置文件路径
BOT_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'config',
    'coze_bots.json'
)


class BotRegistry:
    """Bot注册表 - 管理所有扣子Bot"""
    
    def __init__(self):
        """初始化Bot注册表"""
        self.bots: Dict[str, Dict[str, Any]] = {}
        self._load_bots()
    
    def _load_bots(self):
        """从配置文件加载Bot信息"""
        try:
            if os.path.exists(BOT_CONFIG_PATH):
                with open(BOT_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    self.bots = json.load(f)
                logger.info(f"成功加载 {len(self.bots)} 个Bot配置")
            else:
                logger.warning(f"Bot配置文件不存在：{BOT_CONFIG_PATH}")
                self._create_default_config()
        except Exception as e:
            logger.error(f"加载Bot配置失败：{str(e)}")
            self._create_default_config()
    
    def _create_default_config(self):
        """创建默认的Bot配置文件"""
        default_bots = {
            "desensitize": {
                "name": "脱敏Bot",
                "description": "对证据数据进行脱敏处理",
                "bot_id": "",
                "api_token": "",
                "api_url": "https://api.coze.cn/v3/chat",
                "enabled": False
            },
            "civil_consult": {
                "name": "民事咨询Bot",
                "description": "民事法律咨询",
                "bot_id": "",
                "api_token": "",
                "api_url": "https://api.coze.cn/v3/chat",
                "enabled": False
            },
            "contract_draft": {
                "name": "合同起草Bot",
                "description": "起草各类合同",
                "bot_id": "",
                "api_token": "",
                "api_url": "https://api.coze.cn/v3/chat",
                "enabled": False
            },
            "contract_review": {
                "name": "合同审查Bot",
                "description": "审查合同风险",
                "bot_id": "",
                "api_token": "",
                "api_url": "https://api.coze.cn/v3/chat",
                "enabled": False
            }
        }
        
        # 确保目录存在
        os.makedirs(os.path.dirname(BOT_CONFIG_PATH), exist_ok=True)
        
        # 写入默认配置
        with open(BOT_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(default_bots, f, ensure_ascii=False, indent=2)
        
        self.bots = default_bots
        logger.info(f"创建默认Bot配置文件：{BOT_CONFIG_PATH}")
    
    def register_bot(self, bot_type: str, bot_id: str, api_token: str, name: str, description: str = ""):
        """
        注册一个新的Bot
        
        Args:
            bot_type: Bot类型（desensitize、civil_consult等）
            bot_id: Bot ID（从扣子获取）
            api_token: API Token（从扣子获取）
            name: Bot名称
            description: Bot描述
        """
        self.bots[bot_type] = {
            "name": name,
            "description": description,
            "bot_id": bot_id,
            "api_token": api_token,
            "api_url": "https://api.coze.cn/v3/chat",
            "enabled": True
        }
        
        # 保存到配置文件
        self._save_bots()
        logger.info(f"成功注册Bot：{name} ({bot_type})")
    
    def _save_bots(self):
        """保存Bot配置到文件"""
        try:
            with open(BOT_CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.bots, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存Bot配置失败：{str(e)}")
    
    def get_bot(self, bot_type: str) -> Optional[Dict[str, Any]]:
        """
        获取Bot信息
        
        Args:
            bot_type: Bot类型
        
        Returns:
            Bot信息，如果不存在返回None
        """
        bot = self.bots.get(bot_type)
        
        if bot and bot.get('enabled', False):
            return bot
        else:
            logger.warning(f"Bot不存在或未启用：{bot_type}")
            return None
    
    def call_bot(self, bot_type: str, query: str, user_id: str = "default") -> Dict[str, Any]:
        """
        调用Bot（新版API v3）
        
        Args:
            bot_type: Bot类型
            query: 用户输入
            user_id: 用户ID
        
        Returns:
            Bot的回复结果
        """
        # 获取Bot信息
        bot = self.get_bot(bot_type)
        
        if not bot:
            return {
                'success': False,
                'error': f'Bot不存在或未启用：{bot_type}'
            }
        
        try:
            # 使用新版Coze API v3
            url = bot.get('api_url', 'https://api.coze.cn/v3/chat')
            
            headers = {
                'Authorization': f'Bearer {bot["api_token"]}',
                'Content-Type': 'application/json'
            }
            
            # 新版API格式
            data = {
                'bot_id': bot['bot_id'],
                'user_id': user_id,
                'stream': False,
                'additional_messages': [
                    {
                        'content': query,
                        'content_type': 'text',
                        'role': 'user',
                        'type': 'question'
                    }
                ],
                'parameters': {}
            }
            
            logger.info(f"调用Bot：{bot['name']}，查询：{query}")
            
            # 发送请求
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            # 提取回复内容
            content = self._extract_content(result)
            
            logger.info(f"Bot调用成功：{bot['name']}")
            
            return {
                'success': True,
                'data': result,
                'content': content,
                'bot_name': bot['name']
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Bot调用失败：{str(e)}")
            return {
                'success': False,
                'error': f'网络错误：{str(e)}'
            }
        except Exception as e:
            logger.error(f"Bot调用异常：{str(e)}")
            return {
                'success': False,
                'error': f'服务器错误：{str(e)}'
            }
    
    def _extract_content(self, result: Dict[str, Any]) -> str:
        """
        从API响应中提取内容
        
        Args:
            result: API响应结果
        
        Returns:
            提取的内容字符串
        """
        try:
            # 新版API可能的响应结构
            if 'messages' in result:
                for msg in result['messages']:
                    if msg.get('type') == 'answer':
                        return msg.get('content', '')
            
            # 旧版响应结构
            if 'data' in result:
                data = result['data']
                if isinstance(data, dict):
                    return data.get('content', str(data))
                return str(data)
            
            # 直接返回整个结果
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"提取内容失败：{str(e)}")
            return json.dumps(result, ensure_ascii=False)
    
    def list_bots(self) -> Dict[str, Dict[str, Any]]:
        """
        列出所有Bot
        
        Returns:
            所有Bot的列表
        """
        return self.bots
    
    def enable_bot(self, bot_type: str):
        """启用Bot"""
        if bot_type in self.bots:
            self.bots[bot_type]['enabled'] = True
            self._save_bots()
            logger.info(f"已启用Bot：{bot_type}")
    
    def disable_bot(self, bot_type: str):
        """禁用Bot"""
        if bot_type in self.bots:
            self.bots[bot_type]['enabled'] = False
            self._save_bots()
            logger.info(f"已禁用Bot：{bot_type}")


# 全局单例
_bot_registry_instance: Optional[BotRegistry] = None


def get_bot_registry() -> BotRegistry:
    """获取Bot注册表单例"""
    global _bot_registry_instance
    
    if _bot_registry_instance is None:
        _bot_registry_instance = BotRegistry()
    
    return _bot_registry_instance
