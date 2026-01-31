"""
异常处理模块
提供分级异常处理机制，保证系统稳定性和用户体验
"""

import logging
from functools import wraps
from enum import Enum
from typing import Callable, Any, Optional
from loguru import logger


class ExceptionLevel(Enum):
    """异常级别"""
    INFO = "info"          # 轻微异常，仅记录
    WARNING = "warning"    # 警告，需要关注
    ERROR = "error"        # 错误，需要告警
    CRITICAL = "critical"  # 严重错误，立即告警


# 自定义异常类
class KnowledgeRetrievalError(Exception):
    """知识检索异常"""
    pass


class ModelCallError(Exception):
    """模型调用异常"""
    pass


class RouteError(Exception):
    """路由异常"""
    pass


class SkillExecutionError(Exception):
    """技能执行异常"""
    pass


class exception_handler:
    """
    通用异常装饰器
    
    支持降级策略和分级异常处理
    """
    
    def __init__(
        self,
        default_return: Any = None,
        log_level: ExceptionLevel = ExceptionLevel.ERROR,
        fallback_func: Optional[Callable] = None,
        fallback_args: Optional[dict] = None,
        user_friendly: bool = True
    ):
        """
        Args:
            default_return: 默认返回值
            log_level: 日志级别
            fallback_func: 降级函数
            fallback_args: 降级函数参数
            user_friendly: 是否返回用户友好的错误提示
        """
        self.default_return = default_return
        self.log_level = log_level
        self.fallback_func = fallback_func
        self.fallback_args = fallback_args or {}
        self.user_friendly = user_friendly
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            # 知识检索失败：降级处理
            except KnowledgeRetrievalError as e:
                logger.warning(f"⚠️ 知识检索失败，降级处理：{e}")
                
                # 尝试清空知识字段，继续执行
                if "context" in kwargs and isinstance(kwargs["context"], dict):
                    kwargs["context"]["knowledge"] = ""
                    try:
                        return func(*args, **kwargs)
                    except Exception as e2:
                        logger.error(f"❌ 降级后仍失败：{e2}")
                
                if self.fallback_func:
                    try:
                        return self.fallback_func(*args, **kwargs)
                    except Exception as e3:
                        logger.error(f"❌ 降级函数也失败：{e3}")
                
                return self._get_user_friendly_response(
                    "抱歉，知识检索出现问题，我尽力为您解答～"
                )
            
            # 模型调用失败：切换备用模型
            except ModelCallError as e:
                logger.warning(f"⚠️ 模型调用失败，尝试切换备用模型：{e}")
                
                if self.fallback_func:
                    try:
                        logger.info("🔄 正在切换到备用模型...")
                        return self.fallback_func(*args, **kwargs)
                    except Exception as e2:
                        logger.error(f"❌ 备用模型也失败：{e2}")
                
                return self._get_user_friendly_response(
                    "抱歉，我这边有点问题，稍等一下再试～"
                )
            
            # 路由失败：返回"暂无法解答"
            except RouteError as e:
                logger.error(f"❌ 路由失败：{e}")
                self._send_alert(f"路由失败：{e}")
                
                return self._get_user_friendly_response(
                    "抱歉，我暂时无法解答这个问题，可以换个方式问吗？"
                )
            
            # 技能执行失败
            except SkillExecutionError as e:
                logger.error(f"❌ 技能执行失败：{e}")
                self._send_alert(f"技能执行失败：{e}")
                
                return self._get_user_friendly_response(
                    "抱歉，执行这个技能时出现了问题，请稍后再试～"
                )
            
            # 其他异常
            except Exception as e:
                self._log_exception(e)
                
                if self.fallback_func:
                    try:
                        logger.info("🔄 尝试执行降级函数...")
                        return self.fallback_func(*args, **kwargs)
                    except Exception as e2:
                        logger.error(f"❌ 降级函数失败：{e2}")
                
                return self._get_user_friendly_response(
                    "抱歉，我这边有点小问题，稍等一下再试～"
                )
        
        return wrapper
    
    def _get_user_friendly_response(self, message: str) -> dict:
        """
        获取用户友好的响应
        
        Args:
            message: 错误提示信息
        
        Returns:
            响应字典
        """
        if self.user_friendly:
            return {
                "success": False,
                "reply": message,
                "error": "service_unavailable"
            }
        else:
            return self.default_return or {"success": False, "reply": message}
    
    def _log_exception(self, e: Exception):
        """
        记录异常日志
        
        Args:
            e: 异常对象
        """
        if self.log_level == ExceptionLevel.CRITICAL:
            logger.critical(f"🚨 严重错误：{e}", exc_info=True)
            self._send_alert(f"严重错误：{e}")
        
        elif self.log_level == ExceptionLevel.ERROR:
            logger.error(f"❌ 错误：{e}", exc_info=True)
            self._send_alert(f"错误：{e}")
        
        elif self.log_level == ExceptionLevel.WARNING:
            logger.warning(f"⚠️ 警告：{e}")
        
        else:  # INFO
            logger.info(f"ℹ️ 信息：{e}")
    
    def _send_alert(self, message: str):
        """
        发送告警（如果启用）
        
        Args:
            message: 告警消息
        """
        import os
        
        if os.getenv("ALERT_ENABLED", "false") == "true":
            webhook_url = os.getenv("ALERT_WEBHOOK_URL")
            if webhook_url:
                try:
                    import requests
                    requests.post(webhook_url, json={"text": message}, timeout=3)
                    logger.info("📢 告警已发送")
                except Exception as e:
                    logger.error(f"❌ 告警发送失败：{e}")


# 便捷装饰器
def safe_execute(default_return=None, log_level=ExceptionLevel.ERROR):
    """
    安全执行装饰器（快捷方式）
    
    用法：
    @safe_execute(default_return={"success": False})
    def my_function():
        ...
    """
    return exception_handler(default_return=default_return, log_level=log_level)


def with_fallback(fallback_func, fallback_args=None):
    """
    带降级函数的装饰器（快捷方式）
    
    用法：
    @with_fallback(backup_function, {"arg1": "value1"})
    def my_function():
        ...
    """
    return exception_handler(fallback_func=fallback_func, fallback_args=fallback_args)


# 测试代码
if __name__ == "__main__":
    # 测试异常处理
    @exception_handler(default_return="默认返回")
    def test_function():
        raise Exception("测试异常")
    
    result = test_function()
    print(f"测试结果：{result}")
