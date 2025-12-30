import logging
from src.core.mcp_client import mcp
from src.utils.notification import send_notification_for_one
from src.utils.session import session_manager

logger = logging.getLogger(__name__)

@mcp.tool()
async def ResetScene(session_id: str):
    """
    重置场景当前摄像机观察位置和朝向。

    参数:
    session_id: 会话id，用于区分不同的用户  

    返回:
    场景重置的结果
    """
    result = {
        "type": "ToolFunctionManager",
        "function": "ResetScene",
        "data": "",
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

@mcp.tool()
async def SetCursorState(cursorState: bool, session_id: str):
    """
    重置场景当前摄像机观察位置和朝向。

    参数：
    cursorState: 鼠标状态，true显示，false隐藏
    session_id: 会话id，用于区分不同的用户  

    返回:
    场景重置的结果
    """
    result = {
        "type": "ToolFunctionManager",
        "function": "SetCursorState",
        "data": cursorState,
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