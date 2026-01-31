"""
响应质量监控测试
"""

import pytest
import time
from src.utils.quality_monitor import ResponseQualityMonitor, get_quality_monitor, monitor_response


class TestResponseQualityMonitor:
    """响应质量监控器测试"""
    
    @pytest.fixture
    def monitor(self):
        """监控器实例"""
        return ResponseQualityMonitor(max_history=100)
    
    def test_record_success_request(self, monitor):
        """测试记录成功请求"""
        monitor.record_request('test_endpoint', 0.5, True)
        
        metrics = monitor.get_metrics('test_endpoint')
        assert metrics['total_requests'] == 1
        assert metrics['successful_requests'] == 1
        assert metrics['failed_requests'] == 0
        assert metrics['success_rate'] == 100.0
        assert metrics['error_rate'] == 0.0
    
    def test_record_failed_request(self, monitor):
        """测试记录失败请求"""
        monitor.record_request('test_endpoint', 0.3, False, 'TestError')
        
        metrics = monitor.get_metrics('test_endpoint')
        assert metrics['total_requests'] == 1
        assert metrics['successful_requests'] == 0
        assert metrics['failed_requests'] == 1
        assert metrics['success_rate'] == 0.0
        assert metrics['error_rate'] == 100.0
        assert 'TestError' in metrics['errors']
    
    def test_multiple_requests(self, monitor):
        """测试记录多个请求"""
        # 记录10个请求，其中2个失败
        for i in range(10):
            success = i < 8
            monitor.record_request('test_endpoint', 0.1 + i * 0.1, success)
        
        metrics = monitor.get_metrics('test_endpoint')
        assert metrics['total_requests'] == 10
        assert metrics['successful_requests'] == 8
        assert metrics['failed_requests'] == 2
        assert metrics['success_rate'] == 80.0
        assert metrics['error_rate'] == 20.0
    
    def test_response_time_stats(self, monitor):
        """测试响应时间统计"""
        # 记录不同响应时间的请求
        response_times = [0.1, 0.2, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0]
        for rt in response_times:
            monitor.record_request('test_endpoint', rt, True)
        
        metrics = monitor.get_metrics('test_endpoint')
        assert metrics['avg_response_time'] > 0
        assert metrics['max_response_time'] == 3.0
        assert metrics['min_response_time'] == 0.1
        assert metrics['p95_response_time'] > 0
        assert metrics['p99_response_time'] > 0
    
    def test_check_quality_alerts_no_alerts(self, monitor):
        """测试检查质量告警（无告警）"""
        # 记录正常请求
        for i in range(10):
            monitor.record_request('test_endpoint', 0.1 + i * 0.05, True)
        
        alerts = monitor.check_quality_alerts('test_endpoint')
        assert len(alerts) == 0
    
    def test_check_quality_alerts_high_error_rate(self, monitor):
        """测试检查质量告警（高错误率）"""
        # 记录10个请求，其中6个失败（错误率60%）
        for i in range(10):
            success = i < 4
            monitor.record_request('test_endpoint', 0.1, success)
        
        alerts = monitor.check_quality_alerts('test_endpoint')
        assert len(alerts) > 0
        assert any(a['type'] == 'high_error_rate' for a in alerts)
    
    def test_check_quality_alerts_slow_response(self, monitor):
        """测试检查质量告警（慢响应）"""
        # 记录慢速请求（平均响应时间>2秒）
        for i in range(10):
            monitor.record_request('test_endpoint', 2.5 + i * 0.1, True)
        
        alerts = monitor.check_quality_alerts('test_endpoint')
        assert len(alerts) > 0
        assert any(a['type'] == 'slow_response' for a in alerts)
    
    def test_get_all_metrics(self, monitor):
        """测试获取所有指标"""
        monitor.record_request('endpoint1', 0.1, True)
        monitor.record_request('endpoint2', 0.2, True)
        
        all_metrics = monitor.get_all_metrics()
        assert 'endpoint1' in all_metrics
        assert 'endpoint2' in all_metrics
    
    def test_decorator(self):
        """测试监控装饰器"""
        call_count = 0
        
        @monitor_response('test_decorated_function')
        def test_function():
            nonlocal call_count
            call_count += 1
            return "result"
        
        result = test_function()
        assert result == "result"
        assert call_count == 1
        
        # 检查是否记录了请求
        monitor = get_quality_monitor()
        metrics = monitor.get_metrics('test_decorated_function')
        assert metrics['total_requests'] >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
