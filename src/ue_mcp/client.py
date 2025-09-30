from mcp.server.fastmcp.server import FastMCP
from config import config
import logging

logger = logging.getLogger(__name__)

# 初始化MCP客户端
mcp = FastMCP(
    config.MCP_APP_NAME,
    log_level=config.MCP_LOG_LEVEL
)

logger.info(f"MCP客户端已初始化，应用名称: {config.MCP_APP_NAME}, 日志级别: {config.MCP_LOG_LEVEL}")

__all__ = ['mcp']