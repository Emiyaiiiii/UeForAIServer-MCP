import logging
from src.core.mcp_client import mcp
from src.utils.notification import send_notification_for_one
from src.utils.session import session_manager
from fuzzywuzzy import process

logger = logging.getLogger(__name__)

@mcp.tool()
async def SetWeather(weather: str, session_id: str):
    """
    设置不同类型天气。

    参数：
    weather: 天气类型，例如：晴天,少云,多云,阴天,多雾,小雨,中雨,大雨,雷雨,小雪,中雪,暴雪
    session_id: 会话id，用于区分不同的用户  

    返回:
    设置不同类型天气的结果
    """
    options = {'晴天': 'fine', '少云': 'partcloudy', '多云': 'cloudy', '阴天': 'overcast', '多雾': 'thickness', '小雨': 'lightrain', '中雨': 'moderaterain', '大雨': 'heavyrain', '雷雨': 'thunderstorm', '小雪': 'lightsnow', '中雪': 'moderatesnow', '暴雪': 'blizzard'}
    best_match = process.extractOne(weather, list(options.keys()))
    logger.info(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")

    result = {
        "type": "WeatherManager",
        "function": "SetWeather",
        "data": options[best_match[0]],
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
async def SetTime(time: str, session_id: str): # 18:30
    """
    设置不同的时间。

    参数：
    time: 时间，例如：18:30
    session_id: 会话id，用于区分不同的用户  

    返回:
    设置不同的时间的结果
    """
    result = {
        "type": "ToolFunctionManager",
        "function": "SetTime",
        "data": time,
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