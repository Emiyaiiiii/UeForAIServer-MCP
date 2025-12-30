from starlette.routing import Route, Mount
from starlette.responses import JSONResponse, HTMLResponse, PlainTextResponse
from datetime import datetime
from mcp.server.sse import SseServerTransport
from sse_starlette.sse import EventSourceResponse
import uuid
import asyncio
from src.core.mcp_client import mcp
from src.utils.session import session_manager
import logging

logger = logging.getLogger(__name__)

# Create SSE transport
sse = SseServerTransport("/messages/")

# MCP SSE handler function
async def handle_sse(request):
    """处理MCP SSE连接"""
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        await mcp._mcp_server.run(
            read_stream, write_stream, mcp._mcp_server.create_initialization_options()
        )

async def notification_generator(request):
    """生成通知事件的SSE流"""
    # 获取会话ID
    session_id = request.query_params.get('session_id')
    
    if not session_id:
        session_id = str(uuid.uuid4())
        logger.warning(f"未提供会话ID，生成新的会话ID: {session_id}")
    
    # 确保会话存在
    session = session_manager.get_session(session_id)
    if not session:
        session = session_manager.create_session(session_id)
    
    # 更新会话ID到请求会话
    request.session['session_id'] = session_id
    
    logger.info(f"客户端已连接到SSE流，会话ID: {session_id}")
    
    try:
        while True:
            # 从该会话的队列获取通知
            notification = await session['queue'].get()
            yield {
                "event": "notification",
                "data": {
                    **notification['data'],
                    "session_id": session_id  # 将会话ID包含在数据中
                }
            }
            session['queue'].task_done()
    except asyncio.CancelledError:
        # 客户端断开连接
        logger.debug(f"SSE连接已关闭，会话: {session_id}")
    except Exception as e:
        logger.error(f"SSE连接发生错误，会话: {session_id}, 错误: {str(e)}")
    finally:
        # 清理资源
        # 注意：我们不移除会话，让会话管理器的定期清理任务来处理
        logger.info(f"SSE生成器已退出，会话: {session_id}")

async def health_check(request):
    """健康检查端点"""
    return JSONResponse({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(session_manager.get_sessions())
    })

async def get_sessions_info(request):
    """获取所有会话信息"""
    sessions = session_manager.get_sessions()
    result = {
        "total_sessions": len(sessions),
        "sessions": {}
    }
    
    for session_id, session_info in sessions.items():
        result["sessions"][session_id] = {
            "created_at": session_info['created_at'].isoformat(),
            "last_active": session_info['last_active'].isoformat(),
            "queue_size": session_info['queue'].qsize(),
            "queue_max_size": session_info['queue']._maxsize
        }
    
    return JSONResponse(result)

# All routes list, including standard web routes and MCP routes
routes = [
    # 健康检查和管理端点
    Route("/health", endpoint=health_check),
    Route("/api/sessions", endpoint=get_sessions_info),
    
    # MCP related routes
    Route("/sse", endpoint=handle_sse),
    Route("/ue_sse", lambda request: EventSourceResponse(notification_generator(request))),
    Mount("/messages/", app=sse.handle_post_message),
]