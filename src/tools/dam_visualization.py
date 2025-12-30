import logging
from src.core.mcp_client import mcp
from src.utils.notification import send_notification_for_one
from src.utils.session import session_manager

logger = logging.getLogger(__name__)

@mcp.tool()
async def DamTransparent(isShow: bool, session_id: str):
    """
    控制坝段透明/显示。

    参数:
    isShow: 是否透明，1 控制为透明状态，0表示为正常状态。
    session_id: 会话id，用于区分不同的用户  

    返回:
    控制坝段透明结果
    """
    result = {
        "type": "DamManager",
        "function": "DamTransparent",
        "data": "0" if isShow else "1",
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
async def CivilTransparent(isShow : bool, session_id: str):
    """
    控制土建透明/显示。

    参数:
    isShow: 是否透明，1 控制为透明状态，0表示为正常状态。
    session_id: 会话id，用于区分不同的用户  

    返回:
    控制土建透明结果
    """
    result = {
        "type": "DamManager",
        "function": "CivilTransparent",
        "data": "0" if isShow else "1",
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
async def EquipmentShowHide(isShow: bool, session_id: str):
    """
    控制机电设备显示/隐藏。

    参数:
    isShow: 是否透明，1 控制为透明状态，0表示为正常状态。
    session_id: 会话id，用于区分不同的用户  

    返回:
    控制土建透明结果
    """
    result = {
        "type": "DamManager",
        "function": "EquipmentShowHide",
        "data": "0" if isShow else "1",
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
async def BIMHighlight(BIMID: str, isHighlight: bool, session_id: str):
    """
    控制设备（建筑物）高亮和正常显示。

    参数:
    BIMID: 设备的ID
    isHighlight: 是否高亮,取消高亮时候BIMID传什么都行，只要高亮值为0.
    session_id: 会话id，用于区分不同的用户  

    返回:
    高亮显示结果
    """
    data = {
        "BIMID": BIMID,
        "isHighlight": "1" if isHighlight else "0"
    }
    result = {
        "type": "DamManager",
        "function": "BIMHighlight",
        "data": data,
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
async def SettleWarnCloud(date: str, isShow: bool, session_id: str):
    """
    按日期显示坝顶沉降云图。

    参数:
    date: 日期，例如 2025-02-14
    isShow: 是否显示
    session_id: 会话id，用于区分不同的用户  

    返回:
    高亮显示结果
    """
    data = {
        "date": "result_" + date,
        "isShow": isShow
    }
    result = {
        "type": "DamManager",
        "function": "SettleWarnCloud",
        "data": data,
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