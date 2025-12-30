import logging
from src.core.mcp_client import mcp
from src.utils.notification import send_notification_for_one, create_notification, NotificationTypes
from src.utils.session import session_manager
from fuzzywuzzy import process

logger = logging.getLogger(__name__)

@mcp.tool()
async def StartFixedRoaming(position: str, session_id: str):
    """
    固定路径漫游开始漫游,从头开始漫游。

    参数:
    position: 漫游位置缩写或名称
        LD315(一号坝体廊道(上侧廊道)),
        LD290(二号坝体廊道(下侧廊道)),
        LD350.2(直坝电梯进入),
        FDCF(大坝发电厂房),
        DB(大坝),
        ZGD(张公岛)
    session_id: 会话ID

    返回:
    漫游结果
    """
    try:
        # 定义位置映射
        options = {
            "一号坝体廊道（上侧廊道）": "LD315",
            "二号坝体廊道（下侧廊道）": "LD290",
            "直坝电梯进入": "LD350.2",
            "大坝发电厂房": "FDCF",
            "大坝": "DB",
            "张公岛": "ZGD",
            # 同时支持缩写直接匹配
            "LD315": "LD315",
            "LD290": "LD290",
            "LD350.2": "LD350.2",
            "FDCF": "FDCF",
            "DB": "DB",
            "ZGD": "ZGD"
        }
        
        # 尝试找到最匹配的选项
        best_match = process.extractOne(position, list(options.keys()))
        logger.info(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")
        
        # 只有相似度足够高时才执行
        if best_match[1] > 70:
            # 获取对应的位置代码
            position_code = options[best_match[0]]
            
            # 创建漫游命令
            result = {
                "type": "Roaming",
                "function": "StartFixedRoaming",
                "data": position_code
            }
            
            # 发送通知
            success = send_notification_for_one(
                session_id, 
                {'data': result}, 
                session_manager.get_sessions()
            )
            
            if success:
                return f"开始漫游: {best_match[0]}"
            else:
                return f"操作失败：无法发送通知到会话 {session_id}"
        else:
            return f"未找到匹配的漫游位置: {position}"
    except Exception as e:
        logger.error(f"执行StartFixedRoaming时出错: {str(e)}")
        return f"漫游操作失败: {str(e)}"

@mcp.tool()
async def StopRoaming(session_id: str):
    """
    停止当前漫游
    
    参数:
    session_id: 会话ID
    
    返回:
    操作结果
    """
    try:
        result = {
            "type": "Roaming",
            "function": "StopRoaming",
            "data": True
        }
        
        success = send_notification_for_one(
            session_id, 
            {'data': result}, 
            session_manager.get_sessions()
        )
        
        if success:
            return "已停止漫游"
        else:
            return f"操作失败：无法发送通知到会话 {session_id}"
    except Exception as e:
        logger.error(f"停止漫游时出错: {str(e)}")
        return f"操作失败: {str(e)}"

@mcp.tool()
async def PauseRoaming(session_id: str):
    """
    暂停当前漫游
    
    参数:
    session_id: 会话ID
    
    返回:
    操作结果
    """
    try:
        result = {
            "type": "Roaming",
            "function": "PauseRoaming",
            "data": True
        }
        
        success = send_notification_for_one(
            session_id, 
            {'data': result}, 
            session_manager.get_sessions()
        )
        
        if success:
            return "已暂停漫游"
        else:
            return f"操作失败：无法发送通知到会话 {session_id}"
    except Exception as e:
        logger.error(f"暂停漫游时出错: {str(e)}")
        return f"操作失败: {str(e)}"

@mcp.tool()
async def ResumeRoaming(session_id: str):
    """
    恢复已暂停的漫游
    
    参数:
    session_id: 会话ID
    
    返回:
    操作结果
    """
    try:
        result = {
            "type": "Roaming",
            "function": "ResumeRoaming",
            "data": True
        }
        
        success = send_notification_for_one(
            session_id, 
            {'data': result}, 
            session_manager.get_sessions()
        )
        
        if success:
            return "已恢复漫游"
        else:
            return f"操作失败：无法发送通知到会话 {session_id}"
    except Exception as e:
        logger.error(f"恢复漫游时出错: {str(e)}")
        return f"操作失败: {str(e)}"

@mcp.tool()
async def GetRoamingPositions():
    """
    获取所有可用的漫游位置
    
    返回:
    可用漫游位置列表
    """
    try:
        positions = [
            "一号坝体廊道（上侧廊道）",
            "二号坝体廊道（下侧廊道）",
            "直坝电梯进入",
            "大坝发电厂房",
            "大坝",
            "张公岛"
        ]
        return f"可用漫游位置: {', '.join(positions)}"
    except Exception as e:
        logger.error(f"获取漫游位置时出错: {str(e)}")
        return f"操作失败: {str(e)}"