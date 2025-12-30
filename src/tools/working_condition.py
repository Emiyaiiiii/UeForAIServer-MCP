import logging
from src.core.mcp_client import mcp
from src.utils.notification import send_notification_for_one
from src.utils.session import session_manager
from fuzzywuzzy import process

logger = logging.getLogger(__name__)

@mcp.tool()
async def GateState(gateName: str, isOn: bool, session_id: str):
    """
    设置闸门启闭状态。

    参数:
    gateName: 闸门名字或者泄洪孔洞名字;可以单个控制 ；例如: dkhao、skhao控制泄流孔洞；闸门名字单个控制，例如DKGZZM_11、DKSGJXZM_09
    isOn: 是否开启
    session_id: 会话id，用于区分不同的用户  

    返回:
    闸门启闭状态结果
    """
    options = {
        '1号深孔': 'skhao1',
        '2号深孔': 'skhao2',
        '3号深孔': 'skhao3',
        '4号深孔': 'skhao4',
        '7号深孔': 'skhao7',
        '8号深孔': 'skhao8',
        '9号深孔': 'skhao9',
        '1号底孔': 'dkhao1',
        '2号底孔': 'dkhao2',
        '3号底孔': 'dkhao3',
        '4号底孔': 'dkhao4',
        '5号底孔': 'dkhao5',
        '6号底孔': 'dkhao6',
        '7号底孔': 'dkhao7',
        '8号底孔': 'dkhao8',
        '9号底孔': 'dkhao9',
        '10号底孔': 'dkhao10',
        '11号底孔': 'dkhao11',
        '12号底孔': 'dkha12',
        '13号底孔': 'dkhao13',
        '14号底孔': 'dkhao14',
        '15号底孔': 'dkhao15',
        '1号导流洞': 'dld1',
        '2号导流洞': 'dld2',
        '1号深孔工作闸门': 'SKGZZM_01',
        '2号深孔工作闸门': 'SKGZZM_02',
        '3号深孔工作闸门': 'SKGZZM_03',
        '4号深孔工作闸门': 'SKGZZM_04',
        '5号深孔工作闸门': 'SKGZZM_05',
        '6号深孔工作闸门': 'SKGZZM_06',
        '7号深孔工作闸门': 'SKGZZM_07',
        '8号深孔工作闸门': 'SKGZZM_08',
        '9号深孔工作闸门': 'SKGZZM_09',
        '1号底孔工作闸门': 'DKGZZM_01',
        '2号底孔工作闸门': 'DKGZZM_02',
        '3号底孔工作闸门': 'DKGZZM_03',
        '4号底孔工作闸门': 'DKGZZM_04',
        '5号底孔工作闸门': 'DKGZZM_05',
        '6号底孔工作闸门': 'DKGZZM_06',
        '7号底孔工作闸门': 'DKGZZM_07',
        '8号底孔工作闸门': 'DKGZZM_08',
        '9号底孔工作闸门': 'DKGZZM_09',
        '10号底孔工作闸门': 'DKGZZM_10',
        '11号底孔工作闸门': 'DKGZZM_11',
        '12号底孔工作闸门': 'DKGZZM_12',
        '13号底孔工作闸门': 'DKGZZM_13',
        '14号底孔工作闸门': 'DKGZZM_14',
        '15号底孔工作闸门': 'DKGZZM_15',
        '1号底孔事故检修闸门': 'DKSGJXZM_01',
        '2号底孔事故检修闸门': 'DKSGJXZM_02',
        '3号底孔事故检修闸门': 'DKSGJXZM_03',
        '4号底孔事故检修闸门': 'DKSGJXZM_04',
        '5号底孔事故检修闸门': 'DKSGJXZM_05',
        '6号底孔事故检修闸门': 'DKSGJXZM_06',
        '7号底孔事故检修闸门': 'DKSGJXZM_07',
        '8号底孔事故检修闸门': 'DKSGJXZM_08',
        '9号底孔事故检修闸门': 'DKSGJXZM_09',
        '10号底孔事故检修闸门': 'DKSGJXZM_10',
        '11号底孔事故检修闸门': 'DKSGJXZM_11',
        '12号底孔事故检修闸门': 'DKSGJXZM_12',
        '导流洞导流门1': 'ZAXLSD_DLM_01',
        '导流洞导流门2': 'ZAXLSD_DLM_02',
        '导流洞弧形闸门1': 'ZAXLSD_HXZM_01',
        '导流洞弧形闸门2': 'ZAXLSD_HXZM_02',
        '导流洞事故检修闸门1': 'ZAXLSD_SGJXZM_01',
        '导流洞事故检修闸门2': 'ZAXLSD_SGJXZM_02',
        '导流洞事故检修闸门3': 'ZAXLSD_SGJXZM_03',
        '导流洞事故检修闸门4': 'ZAXLSD_SGJXZM_04'
    }
    best_match = process.extractOne(gateName, list(options.keys()))
    logger.info(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")

    data = {
        "gateName": options[best_match[0]],
        "isOn": isOn
    }
    result = {
        "type": "WorkingConditionManager",
        "function": "GateState",
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
async def OnlyGateEnable(isOnlyGateEnable: bool, session_id: str):
    """
    设置闸门不透明,除闸门以外其他全透明。

    参数:
    isOnlyGateEnable: 是否只看闸门，其他半透。
    session_id: 会话id，用于区分不同的用户  

    返回:
    闸门显示结果
    """
    result = {
        "type": "WorkingConditionManager",
        "function": "GateEnable",
        "data": isOnlyGateEnable,
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
async def FocusingGatePoint(gateId: str, session_id: str):
    """
    聚焦显示对应ID号闸门，并且高亮提示。

    参数:
    gateId: 闸门id
    session_id: 会话id，用于区分不同的用户  

    返回:
    闸门显示结果
    """
    result = {
        "type": "WorkingConditionManager",
        "function": "FocusingGatePoint",
        "data": gateId,
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