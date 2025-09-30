# 导入MCP客户端
from src.ue_mcp.client import mcp

# 导入所有工具函数
from .tools import (
    FirstPerson,
    ThirdPerson,
    MarkLocation,
    flyto,
    ZoomIn,
    ZoomOut,
    StartFixedRoaming,
    StopRoaming,
    PauseRoaming,
    ResumeRoaming,
    GetRoamingPositions
)

__all__ = [
    'mcp',
    'FirstPerson',
    'ThirdPerson',
    'MarkLocation',
    'flyto',
    'ZoomIn',
    'ZoomOut',
    'StartFixedRoaming',
    'StopRoaming',
    'PauseRoaming',
    'ResumeRoaming',
    'GetRoamingPositions'
]