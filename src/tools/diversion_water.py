import logging
from src.core.mcp_client import mcp
from src.utils.notification import send_notification_for_one
from src.utils.session import session_manager
from fuzzywuzzy import process

logger = logging.getLogger(__name__)

@mcp.tool()
async def DiversionWaterOpenClose(homename: str, isOpen: bool, isClear: bool, session_id: str):
    """
    引泄水系统各条孔洞是否泄水及各条泄流动画模拟。

    参数:
    homename: 孔洞缩写:dkhao1(1号底孔), dkhao2(2号底孔), dkhao3(3号底孔), dkhao4(4号底孔), dkhao5(5号底孔), dkhao6(6号底孔), dkhao7(7号底孔), dkhao8(8号底孔), dkhao9(9号底孔), dkhao10(10号底孔), dkhao11(11号底孔), dkhao12(12号底孔), skhao1(1号深孔), skhao2(2号深孔), skhao3(3号深孔), skhao4(4号深孔), skhao5(5号深孔), skhao6(6号深孔), skhao7(7号深孔), skhao8(8号深孔), skhao9(9号深孔), skhao10(10号深孔), skhao11(11号深孔), skhao12(12号深孔), dld1(1号导流洞), dld2(2号导流洞)
    isOpen: 是否开启
    isClear: 是否清水
    session_id: 会话id，用于区分不同的用户  

    返回:
    动画模拟结果
    """
    options = {
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
        '12号底孔': 'dkhao12',
        '1号深孔': 'skhao1',
        '2号深孔': 'skhao2',
        '3号深孔': 'skhao3',
        '4号深孔': 'skhao4',
        '5号深孔': 'skhao5',
        '6号深孔': 'skhao6',
        '7号深孔': 'skhao7',
        '8号深孔': 'skhao8',
        '9号深孔': 'skhao9',
        '10号深孔': 'skhao10',
        '11号深孔': 'skhao11',
        '12号深孔': 'skhao12',
        '1号导流洞': 'dld1',
        '2号导流洞': 'dld2'
    }
    best_match = process.extractOne(homename, list(options.keys()))
    logger.info(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")

    data = {
        "homename": options[best_match[0]],
        "isopen": "1" if isOpen else "0",
        "color": "qingshui" if isClear else "zhuoshui"
    }
    result = {
        "type": "DiversionWaterManager",
        "function": "DiversionWaterOpenClose",
        "data": data
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
async def DiversionWaterPlaneUpDown(start: str, end: str, speed: int, session_id: str):
    """
    控制水面升降。

    参数:
    start: 开始位置水位,例如 343.418733
    end: 结束位置水位（370）
    speed: 速度（m/s）
    session_id: 会话id，用于区分不同的用户  

    返回:
    控制水面升降结果
    """
    data = {
        "start": start,
        "end": end,
        "speed": speed
    }
    result = {
        "type": "DiversionWaterManager",
        "function": "DiversionWaterPlaneUpDown",
        "data": data
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
async def diversion_water_plane_up_down_close(session_id: str):
    """
    退出水面升降。

    参数:
    session_id: 会话id，用于区分不同的用户  

    返回:
    退出水面升降结果
    """
    result = {
        "type": "DiversionWaterManager",
        "function": "DiversionWaterPlaneUpDownClose",
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