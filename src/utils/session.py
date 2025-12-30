import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from config import config

logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.cleanup_task: Optional[asyncio.Task] = None
        self.is_running = False
    
    def get_sessions(self) -> Dict[str, dict]:
        """
        获取所有会话
        """
        return self.sessions
    
    def create_session(self, session_id: str) -> dict:
        """
        创建新会话
        
        参数:
            session_id: 会话ID
        
        返回:
            dict: 会话信息
        """
        if session_id in self.sessions:
            logger.warning(f"会话 {session_id} 已存在，将更新会话信息")
        
        # 创建新会话
        self.sessions[session_id] = {
            'created_at': datetime.now(),
            'last_active': datetime.now(),
            'queue': asyncio.Queue(maxsize=config.NOTIFICATION_QUEUE_SIZE)
        }
        
        logger.debug(f"已创建会话: {session_id}")
        return self.sessions[session_id]
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """
        获取特定会话
        
        参数:
            session_id: 会话ID
        
        返回:
            Optional[dict]: 会话信息，如果不存在则返回None
        """
        session = self.sessions.get(session_id)
        if session:
            # 更新会话活跃时间
            session['last_active'] = datetime.now()
        return session
    
    def update_session(self, session_id: str, **kwargs) -> bool:
        """
        更新会话信息
        
        参数:
            session_id: 会话ID
            **kwargs: 要更新的会话属性
        
        返回:
            bool: 更新成功返回True，否则返回False
        """
        if session_id not in self.sessions:
            logger.warning(f"会话 {session_id} 不存在")
            return False
        
        # 更新会话信息
        for key, value in kwargs.items():
            self.sessions[session_id][key] = value
        
        # 更新会话活跃时间
        self.sessions[session_id]['last_active'] = datetime.now()
        
        logger.debug(f"已更新会话: {session_id}")
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """
        删除会话
        
        参数:
            session_id: 会话ID
        
        返回:
            bool: 删除成功返回True，否则返回False
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.debug(f"已删除会话: {session_id}")
            return True
        else:
            logger.warning(f"会话 {session_id} 不存在")
            return False
    
    async def cleanup_expired_sessions(self):
        """
        定期清理过期会话
        """
        while self.is_running:
            current_time = datetime.now()
            expired_sessions = []
            
            # 找出过期的会话
            for session_id, session_info in self.sessions.items():
                if (current_time - session_info['last_active']).seconds > config.SESSION_EXPIRE_TIME:
                    expired_sessions.append(session_id)
            
            # 清理过期会话
            for session_id in expired_sessions:
                logger.info(f"清理过期会话: {session_id}")
                self.delete_session(session_id)
            
            # 每5分钟检查一次
            await asyncio.sleep(300)
    
    def start_cleanup_task(self):
        """
        启动会话清理任务
        """
        if not self.is_running:
            self.is_running = True
            self.cleanup_task = asyncio.create_task(self.cleanup_expired_sessions())
            logger.info("会话清理任务已启动")
    
    async def stop_cleanup_task(self):
        """
        停止会话清理任务
        """
        if self.cleanup_task and not self.cleanup_task.done():
            self.is_running = False
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
            self.cleanup_task = None
            logger.info("会话清理任务已停止")

# 创建会话管理器实例
session_manager = SessionManager()

# 兼容旧接口
def get_ue_sessions() -> Dict[str, dict]:
    """
    获取UE会话字典（兼容旧接口）
    """
    return session_manager.get_sessions()