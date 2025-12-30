"""MCP工具集模块

该模块包含所有MCP工具的注册和管理
"""

import logging

logger = logging.getLogger(__name__)

# 导入所有工具模块
from . import view_control
from . import roaming
from . import dam_visualization
from . import diversion_water
from . import working_condition
from . import layer_control
from . import common_tools
from . import weather_system
from . import finite_element
from . import data_query

logger.info("所有MCP工具模块已加载")