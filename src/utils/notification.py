import logging
import asyncio
from datetime import datetime
from typing import Dict, Any
from config import config

# 避免循环导入，直接使用notifications模块中定义的函数
logger = logging.getLogger(__name__)

# 通知类型常量
class NotificationTypes:
    VIEW_CONTROL = "ViewAngleManager"
    ROAMING = "Roaming"
    MARKER = "Marker"
    SYSTEM = "System"

# 发送通知给特定会话
def send_notification_for_one(session_id: str, notification_data: Dict[str, Any], ue_sessions: Dict[str, dict]) -> bool:
    """
    向特定会话发送通知
    
    参数:
        session_id: 会话ID
        notification_data: 通知数据
        ue_sessions: 会话字典
    
    返回:
        bool: 发送成功返回True，否则返回False
    """
    try:
        if session_id in ue_sessions:
            # 更新会话活跃时间
            ue_sessions[session_id]['last_active'] = datetime.now()
            # 尝试发送通知
            try:
                ue_sessions[session_id]['queue'].put_nowait(notification_data)
                logger.debug(f"通知已发送到会话 {session_id}")
                return True
            except asyncio.QueueFull:
                logger.warning(f"会话 {session_id} 的通知队列已满")
                return False
        else:
            logger.warning(f"会话 {session_id} 不存在")
            return False
    except Exception as e:
        logger.error(f"发送通知时出错: {str(e)}")
        return False

# 发送通知给所有会话
def send_notification_for_all(notification_data: Dict[str, Any], ue_sessions: Dict[str, dict]) -> int:
    """
    向所有活跃会话发送通知
    
    参数:
        notification_data: 通知数据
        ue_sessions: 会话字典
    
    返回:
        int: 成功发送的会话数量
    """
    success_count = 0
    for session_id, session_info in ue_sessions.items():
        try:
            # 更新会话活跃时间
            session_info['last_active'] = datetime.now()
            # 尝试发送通知
            try:
                session_info['queue'].put_nowait(notification_data)
                success_count += 1
            except asyncio.QueueFull:
                logger.warning(f"会话 {session_id} 的通知队列已满")
        except Exception as e:
            logger.error(f"向会话 {session_id} 发送通知时出错: {str(e)}")
    
    logger.debug(f"已向 {success_count}/{len(ue_sessions)} 个会话发送通知")
    return success_count

# 创建标准通知格式
def create_notification(notification_type: str, function_name: str, data: Any) -> Dict[str, Any]:
    """
    创建标准格式的通知
    
    参数:
        notification_type: 通知类型
        function_name: 函数名
        data: 数据内容
    
    返回:
        Dict[str, Any]: 格式化的通知数据
    """
    return {
        'data': {
            'type': notification_type,
            'function': function_name,
            'data': data
        }
    }