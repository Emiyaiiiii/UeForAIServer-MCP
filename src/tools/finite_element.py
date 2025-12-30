import logging
from src.core.mcp_client import mcp
from src.utils.notification import send_notification_for_one
from src.utils.session import session_manager
from fuzzywuzzy import process

logger = logging.getLogger(__name__)

@mcp.tool()
async def CreateMesh(type: str, meshIndexPath: str, resultPath: str, session_id: str): 
    """
    有限元云图生成。

    参数：
    type: 类型，例如：合位移,水平向位移,竖直位移,最大主应力,最小主应力,水平应力,垂直应力
    meshIndexPath: 网格索引路径，例如：整体,电站坝段,右岸非溢流坝段,溢流坝段2,溢流坝段3
    resultPath: 结果路径，例如：318
    session_id: 会话id，用于区分不同的用户  

    返回:
    有限元云图生成的结果
    """
    type_options = {'合位移': 0, '水平向位移': 1, '竖直位移': 2, '最大主应力': 3, '最小主应力': 4, '水平应力': 5, '垂直应力': 6}
    meshIndexPath_options = {'整体': 'ZhengTi', '电站坝段': 'DZBD_5', '右岸非溢流坝段': 'YAFYLBD_3', '溢流坝段2': 'YLB`D_2', '溢流坝段3': 'YLBD_3'}
    type_best_match = process.extractOne(type, list(type_options.keys()))
    meshIndexPath_best_match = process.extractOne(meshIndexPath, list(meshIndexPath_options.keys()))

    logger.info(f"type最匹配的选项是: {type_best_match[0]}，相似度得分: {type_best_match[1]}")
    logger.info(f"type最匹配的选项是: {meshIndexPath_best_match[0]}，相似度得分: {meshIndexPath_best_match[1]}")

    data = {
      "type": type_options[type_best_match[0]],
      "MeshIndexPath": meshIndexPath_options[meshIndexPath_best_match[0]],
      "ResultPath": resultPath
    }
    result = {
        "type": "SeepageManager",
        "function": "CreateMesh",
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
async def DestoryMesh(isClear: bool, isHide: bool, session_id: str):
    """
    销毁，隐藏有限元云图。

    参数：
    isClear: 是否清除，true清除，false不清除
    isHide: 是否隐藏，true隐藏，false不隐藏
    session_id: 会话id，用于区分不同的用户  

    返回:
    销毁，隐藏有限元云图的结果
    """
    data = {
      "IsClear": isClear,
      "IsHide": isHide
    }
    result = {
        "type": "SeepageManager",
        "function": "DestoryMesh",
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