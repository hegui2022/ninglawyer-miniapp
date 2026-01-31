"""
日志聚合模块
提供日志查询、统计和导出功能
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from loguru import logger


class LogAggregator:
    """日志聚合器"""
    
    def __init__(self, log_dir: str = None):
        """
        初始化日志聚合器
        
        Args:
            log_dir: 日志目录路径
        """
        self.log_dir = Path(log_dir) if log_dir else Path('logs')
        self.log_files = []
        self._scan_log_files()
    
    def _scan_log_files(self):
        """扫描日志文件"""
        if not self.log_dir.exists():
            logger.warning(f"日志目录不存在: {self.log_dir}")
            return
        
        # 扫描.log文件
        for log_file in self.log_dir.glob('*.log'):
            self.log_files.append(log_file)
        
        logger.info(f"扫描到 {len(self.log_files)} 个日志文件")
    
    def parse_log_line(self, line: str) -> Optional[Dict]:
        """
        解析日志行
        
        Args:
            line: 日志行
            
        Returns:
            解析后的日志字典
        """
        # Loguru默认格式: 2024-02-01 12:00:00.000000 | LEVEL | message
        # 使用更宽松的正则表达式匹配，支持可变长度的微秒
        pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+)\s*\|\s*(\w+)\s*\|\s*(.+)'
        match = re.match(pattern, line.strip())
        
        if match:
            return {
                'timestamp': match.group(1),
                'level': match.group(2),
                'message': match.group(3)
            }
        
        return None
    
    def search_logs(self,
                    keyword: str = None,
                    level: str = None,
                    start_time: str = None,
                    end_time: str = None,
                    limit: int = 100) -> List[Dict]:
        """
        搜索日志
        
        Args:
            keyword: 关键词
            level: 日志级别（INFO, ERROR, WARNING等）
            start_time: 开始时间（格式: YYYY-MM-DD HH:MM:SS）
            end_time: 结束时间（格式: YYYY-MM-DD HH:MM:SS）
            limit: 返回结果数量限制
            
        Returns:
            日志列表
        """
        results = []
        
        # 解析时间（支持带或不带毫秒）
        if start_time:
            try:
                start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        else:
            start_dt = None
        
        if end_time:
            try:
                end_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                end_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        else:
            end_dt = None
        
        # 遍历日志文件
        for log_file in self.log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        log_entry = self.parse_log_line(line)
                        if not log_entry:
                            continue
                        
                        # 过滤级别
                        if level and log_entry['level'].upper() != level.upper():
                            continue
                        
                        # 过滤关键词
                        if keyword and keyword.lower() not in log_entry['message'].lower():
                            continue
                        
                        # 过滤时间
                        if start_dt or end_dt:
                            log_time = datetime.strptime(log_entry['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                            if start_dt and log_time < start_dt:
                                continue
                            if end_dt and log_time > end_dt:
                                continue
                        
                        # 添加文件信息
                        log_entry['file'] = str(log_file.name)
                        results.append(log_entry)
                        
                        # 检查结果数量
                        if len(results) >= limit:
                            break
            except Exception as e:
                logger.warning(f"读取日志文件失败: {log_file}, 错误: {e}")
            
            if len(results) >= limit:
                break
        
        # 按时间排序（最新在前）
        results.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return results[:limit]
    
    def get_error_logs(self, hours: int = 24, limit: int = 100) -> List[Dict]:
        """
        获取错误日志
        
        Args:
            hours: 最近几小时的错误日志
            limit: 返回结果数量限制
            
        Returns:
            错误日志列表
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        return self.search_logs(
            level='ERROR',
            start_time=start_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
            end_time=end_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
            limit=limit
        )
    
    def get_log_stats(self, hours: int = 24) -> Dict:
        """
        获取日志统计
        
        Args:
            hours: 最近几小时的日志
            
        Returns:
            统计信息
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        logs = self.search_logs(
            start_time=start_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
            end_time=end_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
            limit=10000
        )
        
        # 统计各级别日志数量
        stats = {
            'total': len(logs),
            'by_level': {},
            'by_file': {},
            'errors': []
        }
        
        for log in logs:
            # 按级别统计
            level = log['level']
            stats['by_level'][level] = stats['by_level'].get(level, 0) + 1
            
            # 按文件统计
            file = log['file']
            stats['by_file'][file] = stats['by_file'].get(file, 0) + 1
            
            # 收集错误
            if level == 'ERROR':
                stats['errors'].append(log)
        
        return stats
    
    def export_logs(self,
                    output_file: str = None,
                    keyword: str = None,
                    level: str = None,
                    start_time: str = None,
                    end_time: str = None,
                    format: str = 'json') -> str:
        """
        导出日志
        
        Args:
            output_file: 输出文件路径
            keyword: 关键词
            level: 日志级别
            start_time: 开始时间
            end_time: 结束时间
            format: 导出格式（json或txt）
            
        Returns:
            导出文件路径
        """
        logs = self.search_logs(
            keyword=keyword,
            level=level,
            start_time=start_time,
            end_time=end_time,
            limit=10000
        )
        
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'logs_export_{timestamp}.{format}'
        
        output_path = Path(output_file)
        
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        else:  # txt
            with open(output_path, 'w', encoding='utf-8') as f:
                for log in logs:
                    f.write(f"{log['timestamp']} | {log['level']} | {log['message']}\n")
        
        logger.info(f"导出日志到: {output_path}")
        return str(output_path)
    
    def clear_old_logs(self, days: int = 30) -> int:
        """
        清理旧日志
        
        Args:
            days: 保留最近几天的日志
            
        Returns:
            删除的文件数量
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0
        
        for log_file in self.log_files:
            try:
                # 获取文件修改时间
                file_mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                
                if file_mtime < cutoff_date:
                    log_file.unlink()
                    logger.info(f"删除旧日志: {log_file}")
                    deleted_count += 1
            except Exception as e:
                logger.warning(f"删除日志文件失败: {log_file}, 错误: {e}")
        
        return deleted_count


# 全局聚合器实例
_log_aggregator = None


def get_log_aggregator(log_dir: str = None) -> LogAggregator:
    """
    获取日志聚合器实例
    
    Args:
        log_dir: 日志目录路径
    """
    global _log_aggregator
    if _log_aggregator is None or log_dir is not None:
        _log_aggregator = LogAggregator(log_dir)
    return _log_aggregator
