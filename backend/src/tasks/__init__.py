"""
异步任务模块
"""

from tasks.async_tasks import (
    celery_app,
    send_notification_task,
    cleanup_expired_sessions_task,
    generate_report_task,
    backup_database_task,
    analyze_user_behavior_task,
    send_daily_report_task
)

__all__ = [
    'celery_app',
    'send_notification_task',
    'cleanup_expired_sessions_task',
    'generate_report_task',
    'backup_database_task',
    'analyze_user_behavior_task',
    'send_daily_report_task'
]
