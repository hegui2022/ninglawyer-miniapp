"""
第三方API基础封装类（通用骨架）
所有第三方API服务都应该继承此类，保持统一的封装规范
"""

import requests
from typing import Dict, Any, Optional
from loguru import logger
from abc import ABC, abstractmethod


class BaseThirdPartyAPIService(ABC):
    """第三方API基础封装类（通用骨架）"""
    
    def __init__(self, api_key: str, base_url: str, timeout: int = 30):
        """
        初始化基础服务
        
        Args:
            api_key: 通用身份凭证（Token/API Key等）
            base_url: API基础URL
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.headers = self._get_default_headers()
        
        logger.info(f"✅ {self.__class__.__name__} 初始化完成 (URL: {base_url})")
    
    def _get_default_headers(self) -> Dict[str, str]:
        """
        获取默认请求头（子类可重写）
        
        Returns:
            默认请求头字典
        """
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def _request(
        self,
        method: str,
        path: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        通用请求方法（封装GET/POST/PUT等）
        
        Args:
            method: HTTP方法（GET/POST/PUT/DELETE等）
            path: API路径（如 /v1/bot/run）
            **kwargs: 其他requests参数
            
        Returns:
            统一格式的响应结果
        """
        url = f"{self.base_url}{path}"
        
        try:
            logger.info(f"📤 请求: {method} {url}")
            
            response = requests.request(
                method,
                url,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            error_msg = f"请求超时（{self.timeout}秒）"
            logger.error(f"❌ {error_msg}")
            return self._create_error_response("timeout", error_msg)
            
        except requests.exceptions.ConnectionError:
            error_msg = "网络连接失败，请检查网络设置"
            logger.error(f"❌ {error_msg}")
            return self._create_error_response("connection_error", error_msg)
            
        except Exception as e:
            error_msg = f"请求异常：{str(e)}"
            logger.error(f"❌ {error_msg}")
            return self._create_error_response("unknown_error", error_msg)
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        通用响应处理（子类可重写）
        
        Args:
            response: HTTP响应对象
            
        Returns:
            格式化的响应结果
        """
        # 记录响应状态
        logger.info(f"📥 响应: HTTP {response.status_code}")
        
        # 检查HTTP状态码
        if response.status_code == 200:
            return self._handle_success_response(response)
        elif response.status_code == 401:
            return self._handle_401_error(response)
        elif response.status_code == 404:
            return self._handle_404_error(response)
        elif response.status_code == 400:
            return self._handle_400_error(response)
        elif response.status_code == 429:
            return self._handle_429_error(response)
        else:
            return self._handle_other_http_error(response)
    
    def _handle_success_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        处理成功响应（HTTP 200）
        
        Args:
            response: HTTP响应对象
            
        Returns:
            格式化的成功响应
        """
        try:
            result = response.json()
            
            # 检查业务状态码（不同的API可能有不同的字段）
            if self._is_business_success(result):
                return self._create_success_response(
                    data=self._extract_business_data(result),
                    raw=result
                )
            else:
                business_error_msg = self._extract_business_error(result)
                return self._create_error_response(
                    "business_error",
                    business_error_msg,
                    code=self._extract_business_code(result)
                )
                
        except Exception as e:
            error_msg = f"响应解析失败：{str(e)}"
            logger.error(f"❌ {error_msg}")
            return self._create_error_response("parse_error", error_msg)
    
    def _handle_401_error(self, response: requests.Response) -> Dict[str, Any]:
        """处理401错误（Token过期或无效）"""
        error_msg = "Access Token无效或已过期，请重新获取"
        logger.error(f"❌ {error_msg}")
        return self._create_error_response(
            "token_expired",
            error_msg,
            http_status=401
        )
    
    def _handle_404_error(self, response: requests.Response) -> Dict[str, Any]:
        """处理404错误（资源不存在）"""
        error_msg = f"资源不存在：{response.url}"
        logger.error(f"❌ {error_msg}")
        return self._create_error_response(
            "not_found",
            error_msg,
            http_status=404
        )
    
    def _handle_400_error(self, response: requests.Response) -> Dict[str, Any]:
        """处理400错误（请求参数错误）"""
        error_msg = "请求参数错误，请检查输入"
        logger.error(f"❌ {error_msg}")
        return self._create_error_response(
            "bad_request",
            error_msg,
            http_status=400
        )
    
    def _handle_429_error(self, response: requests.Response) -> Dict[str, Any]:
        """处理429错误（请求过于频繁）"""
        error_msg = "请求过于频繁，请稍后再试"
        logger.error(f"❌ {error_msg}")
        return self._create_error_response(
            "rate_limit",
            error_msg,
            http_status=429
        )
    
    def _handle_other_http_error(self, response: requests.Response) -> Dict[str, Any]:
        """处理其他HTTP错误"""
        error_msg = f"请求失败，HTTP状态码：{response.status_code}"
        logger.error(f"❌ {error_msg}")
        return self._create_error_response(
            "http_error",
            error_msg,
            http_status=response.status_code
        )
    
    # ==================== 可被子类重写的方法 ====================
    
    def _is_business_success(self, result: Dict) -> bool:
        """
        判断业务是否成功（子类可重写）
        
        默认实现：检查 result.get("code") == 0 或 result.get("success") == True
        
        Args:
            result: 解析后的JSON结果
            
        Returns:
            业务是否成功
        """
        return result.get("code") == 0 or result.get("success") is True
    
    def _extract_business_data(self, result: Dict) -> Any:
        """
        提取业务数据（子类可重写）
        
        默认实现：返回 result.get("data")
        
        Args:
            result: 解析后的JSON结果
            
        Returns:
            业务数据
        """
        return result.get("data", result)
    
    def _extract_business_error(self, result: Dict) -> str:
        """
        提取业务错误信息（子类可重写）
        
        默认实现：返回 result.get("msg") 或 result.get("message", "未知错误")
        
        Args:
            result: 解析后的JSON结果
            
        Returns:
            错误信息
        """
        return result.get("msg", result.get("message", "未知错误"))
    
    def _extract_business_code(self, result: Dict) -> Optional[str]:
        """
        提取业务错误码（子类可重写）
        
        默认实现：返回 result.get("code")
        
        Args:
            result: 解析后的JSON结果
            
        Returns:
            业务错误码
        """
        return result.get("code")
    
    # ==================== 辅助方法 ====================
    
    def _create_success_response(self, data: Any, raw: Dict = None) -> Dict[str, Any]:
        """创建成功响应"""
        response = {
            "success": True,
            "data": data
        }
        if raw:
            response["raw"] = raw
        return response
    
    def _create_error_response(
        self,
        error_type: str,
        error_msg: str,
        code: Any = None,
        http_status: int = None
    ) -> Dict[str, Any]:
        """创建错误响应"""
        response = {
            "success": False,
            "error": error_msg,
            "error_type": error_type
        }
        if code is not None:
            response["code"] = code
        if http_status is not None:
            response["http_status"] = http_status
        return response
    
    def set_api_key(self, api_key: str):
        """设置新的API Key"""
        self.api_key = api_key
        self.headers = self._get_default_headers()
        logger.info("✅ API Key已更新")
    
    def set_timeout(self, timeout: int):
        """设置新的超时时间"""
        self.timeout = timeout
        logger.info(f"✅ 超时时间已更新为 {timeout} 秒")
