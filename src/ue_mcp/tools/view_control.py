import logging
from src.ue_mcp.client import mcp
from src.utils.notification import send_notification_for_one, create_notification, NotificationTypes
from src.utils.session import session_manager
from typing import Optional

logger = logging.getLogger(__name__)

@mcp.tool()
async def FirstPerson(isFirstPerson: bool, session_id: Optional[str] = None):
    """
    是否要切换为第一人称。

    参数:
    isFirstPerson: 是否要切换为第一人称 (例如: true)
    session_id: 会话ID，如果提供则仅发送给特定会话

    返回:
    切换第一人称的结果
    """
    try:
        result = {
            "type": "ViewAngleManager",
            "function": "FirstPerson",
            "data": isFirstPerson
        }
        
        if session_id:
            # 发送给特定会话
            success = send_notification_for_one(
                session_id, 
                {'data': result}, 
                session_manager.get_sessions()
            )
            if success:
                return "操作成功"
            else:
                return f"操作失败：无法发送通知到会话 {session_id}"
        else:
            # 如果没有会话ID，使用兼容模式
            from src.utils.notification import notifications
            notifications.append({'data': result})
            return "操作成功"
    except Exception as e:
        logger.error(f"切换第一人称时出错: {str(e)}")
        return f"操作失败: {str(e)}"

@mcp.tool()
async def ThirdPerson(isThirdPerson: bool, session_id: Optional[str] = None):
    """
    是否要切换为第三人称。

    参数:
    isThirdPerson: 是否要切换为第三人称 (例如: true)
    session_id: 会话ID，如果提供则仅发送给特定会话

    返回:
    切换第三人称的结果
    """
    try:
        result = {
            "type": "ViewAngleManager",
            "function": "ThirdPerson",
            "data": isThirdPerson
        }
        
        if session_id:
            # 发送给特定会话
            success = send_notification_for_one(
                session_id, 
                {'data': result}, 
                session_manager.get_sessions()
            )
            if success:
                return "操作成功"
            else:
                return f"操作失败：无法发送通知到会话 {session_id}"
        else:
            # 如果没有会话ID，使用兼容模式
            from src.utils.notification import notifications
            notifications.append({'data': result})
            return "操作成功"
    except Exception as e:
        logger.error(f"切换第三人称时出错: {str(e)}")
        return f"操作失败: {str(e)}"

@mcp.tool()
async def MarkLocation(MarkID: str, session_id: Optional[str] = None):
    """
    防汛点，重大危险源，仓库位置点标签定位。

    参数:
    MarkID: 标签的ID
    session_id: 会话ID，如果提供则仅发送给特定会话

    返回:
    标签定位的结果
    """
    try:
        result = {
            "type": "ViewAngleManager",
            "function": "2DMarkLocation",
            "data": MarkID
        }
        
        if session_id:
            # 发送给特定会话
            success = send_notification_for_one(
                session_id, 
                {'data': result}, 
                session_manager.get_sessions()
            )
            if success:
                return "操作成功"
            else:
                return f"操作失败：无法发送通知到会话 {session_id}"
        else:
            # 如果没有会话ID，使用兼容模式
            from src.utils.notification import notifications
            notifications.append({'data': result})
            return "操作成功"
    except Exception as e:
        logger.error(f"标记位置时出错: {str(e)}")
        return f"操作失败: {str(e)}"

@mcp.tool()
async def flyto(location: str, session_id: str, type: str):
    """
    视角定位、飞行至场景某个位置。

    参数:
    location: 位置名称,根据type不同,有不同的含义,
        "Reservoir": 水库名称,例如"小浪底","万家寨","古贤"等黄河流域水库名称
        "Province"/"city"/"town": 位置名称,包括"河南","河北","陕西"等全国各省以及所有城市和城镇
        "River": 河流名称,包括"沁河","汾河","泾河"黄河各支流
    session_id: 会话id,用于区分不同的用户  
    type: 视角类型,默认是"Reservoir",也可以是"Province"/"city"/"town"/"Reservoir"或"River"

    返回:
    视角定位的结果
    """
    try:
        result = {
            "type": type,
            "parameter": location
        }
        
        success = send_notification_for_one(
            session_id, 
            {'data': result}, 
            session_manager.get_sessions()
        )
        
        if success:
            return "操作成功"
        else:
            return f"操作失败：无法发送通知到会话 {session_id}"
    except Exception as e:
        logger.error(f"执行flyto操作时出错: {str(e)}")
        return f"操作失败: {str(e)}"

@mcp.tool()
async def ZoomIn(session_id: str, level: float = 1.0):
    """
    放大视角
    
    参数:
    session_id: 会话ID
    level: 放大级别，默认为1.0
    
    返回:
    操作结果
    """
    try:
        result = {
            "type": "ViewAngleManager",
            "function": "ZoomIn",
            "data": level
        }
        
        success = send_notification_for_one(
            session_id, 
            {'data': result}, 
            session_manager.get_sessions()
        )
        
        if success:
            return "放大视角成功"
        else:
            return f"操作失败：无法发送通知到会话 {session_id}"
    except Exception as e:
        logger.error(f"放大视角时出错: {str(e)}")
        return f"操作失败: {str(e)}"

@mcp.tool()
async def ZoomOut(session_id: str, level: float = 1.0):
    """
    缩小视角
    
    参数:
    session_id: 会话ID
    level: 缩小级别，默认为1.0
    
    返回:
    操作结果
    """
    try:
        result = {
            "type": "ViewAngleManager",
            "function": "ZoomOut",
            "data": level
        }
        
        success = send_notification_for_one(
            session_id, 
            {'data': result}, 
            session_manager.get_sessions()
        )
        
        if success:
            return "缩小视角成功"
        else:
            return f"操作失败：无法发送通知到会话 {session_id}"
    except Exception as e:
        logger.error(f"缩小视角时出错: {str(e)}")
        return f"操作失败: {str(e)}"