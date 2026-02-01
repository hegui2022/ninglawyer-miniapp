"""
响应质量监控模块
跟踪API响应时间、错误率等指标
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from functools import wraps
from collections import defaultdict, deque
from loguru import logger

from utils.cache_manager import CacheManager


class ResponseQualityMonitor:
    """响应质量监控器"""
    
    def __init__(self, max_history: int = 1000):
        """
        初始化监控器
        
        Args:
            max_history: 保留的最大历史记录数
        """
        self.max_history = max_history
        self.cache_manager = CacheManager()
        
        # 内存存储（用于快速访问）
        self.metrics = defaultdict(lambda: {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_response_time': 0,
            'response_times': deque(maxlen=max_history),
            'errors': defaultdict(int)
        })
    
    def record_request(self, endpoint: str, response_time: float, success: bool, error_code: str = None):
        """
        记录请求
        
        Args:
            endpoint: API端点
            response_time: 响应时间（秒）
            success: 是否成功
            error_code: 错误码（如果失败）
        """
        now = datetime.now()
        date_key = now.strftime('%Y-%m-%d')
        hour_key = now.strftime('%Y-%m-%d:%H')
        
        # 更新内存指标
        metrics = self.metrics[endpoint]
        metrics['total_requests'] += 1
        metrics['total_response_time'] += response_time
        metrics['response_times'].append({
            'time': now.isoformat(),
            'response_time': response_time,
            'success': success,
            'error_code': error_code
        })
        
        if success:
            metrics['successful_requests'] += 1
        else:
            metrics['failed_requests'] += 1
            if error_code:
                metrics['errors'][error_code] += 1
        
        # 持久化到缓存（24小时过期）
        cache_key = f"quality_monitor:{date_key}:{endpoint}"
        try:
            self.cache_manager.set(
                cache_key,
                {
                    'total_requests': metrics['total_requests'],
                    'successful_requests': metrics['successful_requests'],
                    'failed_requests': metrics['failed_requests'],
                    'avg_response_time': metrics['total_response_time'] / metrics['total_requests']
                },
                ttl=86400
            )
        except Exception as e:
            logger.warning(f"保存监控指标到缓存失败: {e}")
    
    def get_metrics(self, endpoint: str, hours: int = 24) -> Dict:
        """
        获取指标
        
        Args:
            endpoint: API端点
            hours: 获取最近几小时的指标
            
        Returns:
            指标数据
        """
        metrics = self.metrics[endpoint]
        
        if metrics['total_requests'] == 0:
            return {
                'endpoint': endpoint,
                'total_requests': 0,
                'success_rate': 0,
                'error_rate': 0,
                'avg_response_time': 0,
                'max_response_time': 0,
                'min_response_time': 0,
                'p95_response_time': 0,
                'p99_response_time': 0,
                'errors': {}
            }
        
        # 计算响应时间统计
        response_times = [r['response_time'] for r in metrics['response_times']]
        sorted_times = sorted(response_times)
        
        success_rate = (metrics['successful_requests'] / metrics['total_requests']) * 100
        error_rate = (metrics['failed_requests'] / metrics['total_requests']) * 100
        
        # 计算百分位数
        n = len(sorted_times)
        p95_index = int(n * 0.95)
        p99_index = int(n * 0.99)
        
        return {
            'endpoint': endpoint,
            'total_requests': metrics['total_requests'],
            'successful_requests': metrics['successful_requests'],
            'failed_requests': metrics['failed_requests'],
            'success_rate': round(success_rate, 2),
            'error_rate': round(error_rate, 2),
            'avg_response_time': round(metrics['total_response_time'] / metrics['total_requests'], 3),
            'max_response_time': round(max(response_times), 3),
            'min_response_time': round(min(response_times), 3),
            'p95_response_time': round(sorted_times[min(p95_index, n - 1)], 3),
            'p99_response_time': round(sorted_times[min(p99_index, n - 1)], 3),
            'errors': dict(metrics['errors'])
        }
    
    def get_all_metrics(self) -> Dict[str, Dict]:
        """获取所有端点的指标"""
        return {
            endpoint: self.get_metrics(endpoint)
            for endpoint in self.metrics.keys()
        }
    
    def check_quality_alerts(self, endpoint: str) -> List[Dict]:
        """
        检查质量告警
        
        Args:
            endpoint: API端点
            
        Returns:
            告警列表
        """
        alerts = []
        metrics = self.get_metrics(endpoint)
        
        # 检查错误率（超过5%）
        if metrics['error_rate'] > 5:
            alerts.append({
                'type': 'high_error_rate',
                'severity': 'warning',
                'message': f"错误率过高: {metrics['error_rate']}%",
                'value': metrics['error_rate']
            })
        
        # 检查平均响应时间（超过2秒）
        if metrics['avg_response_time'] > 2:
            alerts.append({
                'type': 'slow_response',
                'severity': 'warning',
                'message': f"平均响应时间过长: {metrics['avg_response_time']}s",
                'value': metrics['avg_response_time']
            })
        
        # 检查P99响应时间（超过5秒）
        if metrics['p99_response_time'] > 5:
            alerts.append({
                'type': 'very_slow_response',
                'severity': 'critical',
                'message': f"P99响应时间过长: {metrics['p99_response_time']}s",
                'value': metrics['p99_response_time']
            })
        
        return alerts


# 全局监控器实例
_quality_monitor = ResponseQualityMonitor()


def get_quality_monitor() -> ResponseQualityMonitor:
    """获取监控器实例"""
    return _quality_monitor


def monitor_response(endpoint: str):
    """
    响应监控装饰器
    
    Args:
        endpoint: API端点名称
        
    Usage:
        @monitor_response('user_login')
        def login():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            success = True
            error_code = None
            
            try:
                result = f(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                error_code = str(type(e).__name__)
                raise
            finally:
                response_time = time.time() - start_time
                monitor = get_quality_monitor()
                monitor.record_request(endpoint, response_time, success, error_code)
        
        return decorated_function
    return decorator
