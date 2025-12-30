import logging
from src.core.mcp_client import mcp
from src.utils.notification import send_notification_for_one
from src.utils.session import session_manager
from fuzzywuzzy import process

logger = logging.getLogger(__name__)

@mcp.tool()
async def ManagementScopeLine(lineName: str, isShow: bool, session_id: str):
    """
    控制单个范围线、水工标签、水面。

    参数:
    lineName: 范围线名字，例如：管理范围线，保护范围线，确权土地范围线，未确权土地范围线，水工标签，水面
    isShow: 是否显示
    session_id: 会话id，用于区分不同的用户  

    返回:
    单个范围线、水工标签的结果
    """
    options = {'管理范围线': 'GLQ', '保护范围线': 'BHQ', '确权土地范围线': 'QQ', '未确权土地范围线': 'WQQ', '水工标签': 'MarkManager', '水面控制': 'WaterPlane'}
    best_match = process.extractOne(lineName, list(options.keys()))
    logger.info(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")
    
    data = {
        "lineName": options[best_match[0]],
        "isShow": isShow
    }
    result = {
        "type": "CoverageManager",
        "function": "ManagementScopeLine",
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
async def ManagementScopeLineAllShow(isAllShow: bool, session_id: str):
    """
    所有范围线管理功能，控制全部范围线。

    参数:
    isAllShow: 是否显示，true即所有范围线显示，false即所有范围线隐藏
    session_id: 会话id，用于区分不同的用户  

    返回:
    单个范围线、水工标签的结果
    """
    result = {
        "type": "CoverageManager",
        "function": "ManagementScopeLineAllShow",
        "data": isAllShow,
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
async def DamMarkControll(isShowDamMark: bool, session_id: str):
    """
    控制三门峡大坝，发电信息，孔洞信息的标签。

    参数:
    isShowDamMark: 是否显示，true标签显示，false标签隐藏
    session_id: 会话id，用于区分不同的用户  

    返回:
    标签显示的结果
    """
    result = {
        "type": "CoverageManager",
        "function": "DamMarkControll",
        "data": isShowDamMark,
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
async def FDCFMarkShowControll(isShowFDCFMark: bool, session_id: str):
    """
    控制发电厂房内发电设施的标签。

    参数:
    isShowFDCFMark: 是否显示，true标签显示，false标签隐藏
    session_id: 会话id，用于区分不同的用户  

    返回:
    标签显示的结果
    """
    result = {
        "type": "CoverageManager",
        "function": "FDCFMarkShowControll",
        "data": isShowFDCFMark,
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
async def XJDShowControll(XJDShowControll: bool, session_id: str):
    """
    控制巡检点显隐。

    参数:
    XJDShowControll: 是否显示，true标签显示，false标签隐藏
    session_id: 会话id，用于区分不同的用户  

    返回:
    巡检点显隐的结果
    """
    result = {
        "type": "CoverageManager",
        "function": "XJDShowControll",
        "data": XJDShowControll,
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
async def OverlyShow(isOverlyShow: bool, overlytag: str, session_id: str):# DK底孔,SK深孔,DLD导流洞
    """
    场景中中控，底孔，导流洞闪烁。

    参数:
    isOverlyShow: 是否显示，true闪烁，false不闪烁
    overlytag: 巡检点类型，例如：底孔,深孔,导流洞
    session_id: 会话id，用于区分不同的用户  

    返回:
    设置闪烁的结果
    """
    options = {'底孔': 'DK', '深孔': 'SK', '导流洞': 'DLD'}
    best_match = process.extractOne(overlytag, list(options.keys()))
    logger.info(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")

    data = {
      "overlyshow": isOverlyShow,
      "overlytag": options[best_match[0]]
    }
    result = {
        "type": "CoverageManager",
        "function": "OverlyShow",
        "data": [data],
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