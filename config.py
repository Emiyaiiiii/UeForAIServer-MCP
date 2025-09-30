import os
import secrets
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类，基于环境变量"""
    # 服务器配置
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '9002'))
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # 安全配置
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_urlsafe(32))
    
    # MCP配置
    MCP_APP_NAME = os.getenv('MCP_APP_NAME', 'UeForAI')
    MCP_LOG_LEVEL = os.getenv('MCP_LOG_LEVEL', 'INFO')
    
    # 会话配置
    SESSION_EXPIRE_TIME = int(os.getenv('SESSION_EXPIRE_TIME', '3600'))
    
    # 通知队列大小
    NOTIFICATION_QUEUE_SIZE = int(os.getenv('NOTIFICATION_QUEUE_SIZE', '100'))

# 导出配置实例
config = Config()