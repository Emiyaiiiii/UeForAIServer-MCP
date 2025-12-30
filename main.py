import uvicorn
import logging
import sys
import os
from dotenv import load_dotenv
from config import config

# 设置日志配置
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 导入工具模块以注册所有MCP工具
from src import tools

def main():
    """主函数，启动Web服务器"""
    # 从命令行参数中获取主机和端口，否则使用配置文件中的值
    host = config.HOST
    port = config.PORT
    
    # 处理命令行参数
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == '--host' and i + 1 < len(sys.argv):
                host = sys.argv[i + 1]
            elif sys.argv[i] == '--port' and i + 1 < len(sys.argv):
                try:
                    port = int(sys.argv[i + 1])
                except ValueError:
                    logger.error(f"无效的端口号: {sys.argv[i + 1]}")
                    sys.exit(1)
    
    logger.info(f"Starting server on {host}:{port}")
    
    # 导入app模块
    from src.api.app import app
    
    # 启动UVicorn服务器
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=config.LOG_LEVEL.lower(),
        reload=config.DEBUG
    )

if __name__ == "__main__":
    main()
