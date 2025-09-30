# 通知列表 - 用于兼容旧接口
notifications = []

# 从子模块导入常用函数和类
from .notification import (
    send_notification_for_one,
    send_notification_for_all,
    create_notification,
    NotificationTypes
)
from .session import session_manager, get_ue_sessions

__all__ = [
    'notifications',
    'send_notification_for_one',
    'send_notification_for_all',
    'create_notification',
    'NotificationTypes',
    'session_manager',
    'get_ue_sessions'
]