from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import secrets
import logging
from config import config
from .routes import routes
from src.utils.session import session_manager

logger = logging.getLogger(__name__)

# 创建Starlette应用
app = Starlette(
    debug=config.DEBUG,
    routes=routes,
)

# 添加会话中间件
app.add_middleware(
    SessionMiddleware,
    secret_key=config.SECRET_KEY,
    session_cookie="session_id"
)

# 添加跨域资源共享中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 应用启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行的操作"""
    logger.info(f"服务器启动中，主机: {config.HOST}, 端口: {config.PORT}")
    # 启动会话清理任务
    session_manager.start_cleanup_task()

# 应用关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行的操作"""
    logger.info("服务器正在关闭...")
    # 停止会话清理任务
    await session_manager.stop_cleanup_task()

__all__ = ['app']