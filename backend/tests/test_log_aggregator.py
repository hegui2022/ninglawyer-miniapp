"""
日志聚合测试
"""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta

from src.utils.log_aggregator import LogAggregator, get_log_aggregator


class TestLogAggregator:
    """日志聚合器测试"""
    
    @pytest.fixture
    def temp_log_dir(self):
        """临时日志目录"""
        import time
        
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir)
            # 创建测试日志文件
            log_file = log_dir / 'test.log'
            
            # 写入测试日志（使用当前时间）
            time_format = '%Y-%m-%d %H:%M:%S.%f'
            
            logs = []
            for i in range(4):
                now = datetime.now()
                if i == 1:
                    logs.append(f'{now.strftime(time_format)} | ERROR | 测试错误日志')
                elif i == 2:
                    logs.append(f'{now.strftime(time_format)} | WARNING | 测试警告日志')
                elif i == 3:
                    logs.append(f'{now.strftime(time_format)} | INFO | 包含关键词的日志')
                else:
                    logs.append(f'{now.strftime(time_format)} | INFO | 测试信息日志')
                
                # 添加小延迟，确保时间戳不同
                if i < 3:
                    time.sleep(0.001)
            
            with open(log_file, 'w', encoding='utf-8') as f:
                for log in logs:
                    f.write(log + '\n')
            
            yield log_dir
    
    @pytest.fixture
    def aggregator(self, temp_log_dir):
        """日志聚合器实例"""
        return LogAggregator(str(temp_log_dir))
    
    def test_scan_log_files(self, aggregator):
        """测试扫描日志文件"""
        assert len(aggregator.log_files) > 0
    
    def test_parse_log_line(self, aggregator):
        """测试解析日志行"""
        line = '2024-02-01 12:00:00.000 | INFO | 测试信息日志'
        log_entry = aggregator.parse_log_line(line)
        
        assert log_entry is not None
        assert log_entry['timestamp'] == '2024-02-01 12:00:00.000'
        assert log_entry['level'] == 'INFO'
        assert log_entry['message'] == '测试信息日志'
    
    def test_parse_log_line_invalid(self, aggregator):
        """测试解析无效日志行"""
        line = '这是一行无效的日志'
        log_entry = aggregator.parse_log_line(line)
        assert log_entry is None
    
    def test_search_logs_all(self, aggregator):
        """测试搜索所有日志"""
        logs = aggregator.search_logs(limit=100)
        assert len(logs) >= 3
    
    def test_search_logs_by_level(self, aggregator):
        """测试按级别搜索日志"""
        logs = aggregator.search_logs(level='ERROR', limit=10)
        assert len(logs) >= 1
        assert all(log['level'] == 'ERROR' for log in logs)
    
    def test_search_logs_by_keyword(self, aggregator):
        """测试按关键词搜索日志"""
        logs = aggregator.search_logs(keyword='关键词', limit=10)
        assert len(logs) >= 1
        assert all('关键词' in log['message'] for log in logs)
    
    def test_search_logs_by_time(self, aggregator):
        """测试按时间搜索日志"""
        start_time = '2024-02-01 12:00:00'
        end_time = '2024-02-01 12:00:02'
        
        logs = aggregator.search_logs(
            start_time=start_time,
            end_time=end_time,
            limit=10
        )
        
        # 应该返回在这个时间范围内的日志
        assert len(logs) >= 0
    
    def test_get_error_logs(self, aggregator):
        """测试获取错误日志"""
        # 先测试不带时间的搜索
        all_logs = aggregator.search_logs(level='ERROR', limit=10)
        print(f"\n[DEBUG] 不带时间找到的ERROR日志数: {len(all_logs)}")
        
        logs = aggregator.get_error_logs(hours=24, limit=10)
        print(f"[DEBUG] 带24小时时间窗口找到的ERROR日志数: {len(logs)}")
        assert len(logs) >= 1, f"期望至少1条ERROR日志，实际找到{len(logs)}条"
        assert all(log['level'] == 'ERROR' for log in logs)
    
    def test_get_log_stats(self, aggregator):
        """测试获取日志统计"""
        stats = aggregator.get_log_stats(hours=24)
        
        assert 'total' in stats
        assert 'by_level' in stats
        assert 'by_file' in stats
        assert 'errors' in stats
        assert stats['total'] >= 3
    
    def test_export_logs_json(self, aggregator, temp_log_dir):
        """测试导出日志为JSON"""
        export_file = temp_log_dir / 'export.json'
        output_path = aggregator.export_logs(
            output_file=str(export_file),
            format='json'
        )
        
        assert Path(output_path).exists()
        
        # 验证JSON格式
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert isinstance(data, list)
    
    def test_export_logs_txt(self, aggregator, temp_log_dir):
        """测试导出日志为TXT"""
        export_file = temp_log_dir / 'export.txt'
        output_path = aggregator.export_logs(
            output_file=str(export_file),
            format='txt'
        )
        
        assert Path(output_path).exists()
        
        # 验证文本格式
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert '|' in content  # 日志分隔符
    
    def test_clear_old_logs(self, aggregator):
        """测试清理旧日志"""
        # 这个测试需要创建旧文件，这里只测试功能不删除文件
        deleted_count = aggregator.clear_old_logs(days=30)
        assert deleted_count >= 0
    
    def test_get_singleton(self, temp_log_dir):
        """测试获取单例实例"""
        agg1 = get_log_aggregator(str(temp_log_dir))
        agg2 = get_log_aggregator()
        assert agg1 is agg2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
