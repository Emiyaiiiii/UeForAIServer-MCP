from starlette.routing import Route, Mount
from starlette.responses import JSONResponse, HTMLResponse, PlainTextResponse
from datetime import datetime
from mcp.server.sse import SseServerTransport
from sse_starlette.sse import EventSourceResponse
from starlette.requests import Request
import uuid
import asyncio
from tools import mcp
from tools import get_ue_sessions

import logging
logger = logging.getLogger(__name__)

# Create SSE transport
sse = SseServerTransport("/messages/")

ue_sessions = get_ue_sessions() 

# MCP SSE handler function
async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        await mcp._mcp_server.run(
            read_stream, write_stream, mcp._mcp_server.create_initialization_options()
        )

async def notification_generator(request: Request):
    """生成通知事件的SSE流"""
    # 获取或创建会话ID
    session_id = request.query_params.get('session_id')
    # session_id = str(uuid.uuid4())
    # session_id = request.session.get('session_id')
    print("session_id: ", session_id)
    request.session['session_id'] = session_id
    ue_sessions[session_id] = {
        'created_at': datetime.now(),
        'last_active': datetime.now(),
        'queue': asyncio.Queue()
    }
    # 更新会话活跃时间
    ue_sessions[session_id]['last_active'] = datetime.now()
    try:
        while True:
            # 从该会话的队列获取通知
            notification = await ue_sessions[session_id]['queue'].get()
            yield {
                "event": "notification",
                "data": {
                    **notification,
                    "session_id": session_id  # 将会话ID包含在数据中
                }
            }
            ue_sessions[session_id]['queue'].task_done()
    except asyncio.CancelledError:
        # 客户端断开连接
        logger.debug(f"SSE connection closed for session {session_id}")
    finally:
        # 清理资源
        if session_id in ue_sessions:
            del ue_sessions[session_id]
          
# All routes list, including standard web routes and MCP routes
routes = [
    # MCP related routes
    Route("/sse", endpoint=handle_sse),
    Route("/ue_sse", lambda request: EventSourceResponse(notification_generator(request))),
    Mount("/messages/", app=sse.handle_post_message),
]