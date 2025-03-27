from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from starlette.middleware.cors import CORSMiddleware
from mcp.server import Server
import uvicorn
import asyncio
from fuzzywuzzy import process

mcp = FastMCP("docs")

notifications = []

@mcp.tool()
async def get_docs(query: str, library: str):
    """
    搜索给定查询和库的最新文档。
    支持 langchain、llama-index、autogen、agno、openai-agents-sdk、mcp-doc、camel-ai 和 crew-ai。

    参数:
    query: 要搜索的查询 (例如 "React Agent")
    library: 要搜索的库 (例如 "agno")

    返回:
    文档中的文本
    """
    if library not in docs_urls:
        raise ValueError(f"Library {library} not supported by this tool")

    query = f"site:{docs_urls[library]} {query}"
    results = await search_web(query)
    if len(results["organic"]) == 0:
        return "No results found"

    text = ""
    for result in results["organic"]:
        text += await fetch_url(result["link"])

    return text


#TODO 视角管理
@mcp.tool()
async def FirstPerson(isFirstPerson: bool):
    """
    是否要切换为第一人称。

    参数:
    isFirstPerson: 是否要切换为第一人称 (例如: true)

    返回:
    切换第一人称的结果
    """
    result = {
        "type": "ViewAngleManager",
        "function": "FirstPerson",
        "data": isFirstPerson
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def ThirdPerson(isThirdPerson: bool):
    """
    是否要切换为第三人称。

    参数:
    isThirdPerson: 是否要切换为第三人称 (例如: true)

    返回:
    切换第三人称的结果
    """
    result = {
        "type": "ViewAngleManager",
        "function": "ThirdPerson",
        "data": isThirdPerson
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def MarkLocation(MarkID: str):
    """
    防汛点，重大危险源，仓库位置点标签定位。

    参数:
    MarkID: 标签的ID

    返回:
    标签定位的结果
    """
    result = {
        "type": "ViewAngleManager",
        "function": "2DMarkLocation",
        "data": MarkID
    }
    notifications.append({'data': result})
    return "操作成功"


# TODO 地下洞群三位可视化表达
@mcp.tool()
async def StartFixedRoaming(position: str):
    """
    固定路径漫游开始漫游,从头开始漫游。

    参数:
    position: 漫游位置缩写:LD315(一号坝体廊道(上侧廊道)),LD290(二号坝体廊道(下侧廊道)),LD350.2(直坝电梯进入),FDCF(大坝发电厂房),DB(大坝),ZGD(张公岛)


    返回:
    漫游结果
    """
    options = {
        "一号坝体廊道（上侧廊道）": "LD315",
        "二号坝体廊道（下侧廊道）": "LD290",
        "直坝电梯进入": "LD350.2",
        "大坝发电厂房": "FDCF",
        "大坝": "DB",
        "张公岛": "ZGD"
    }
    best_match = process.extractOne(position, list(options.keys()))
    print(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")

    result = {
        "type": "UndergroundCavernManager",
        "function": "StartFixedRoaming",
        "data": options[best_match[0]]
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def SuspendFixedRoaming(position: str):
    """
    固定路径漫游，暂停漫游，暂停后鼠标左键可点击但不可位置移动。

    参数:
    position: 漫游位置缩写:LD315(一号坝体廊道(上侧廊道)),LD290(二号坝体廊道(下侧廊道)),LD350.2(直坝电梯进入),FDCF(大坝发电厂房),DB(大坝),ZGD(张公岛)


    返回:
    漫游结果
    """
    options = {
        "一号坝体廊道（上侧廊道）": "LD315",
        "二号坝体廊道（下侧廊道）": "LD290",
        "直坝电梯进入": "LD350.2",
        "大坝发电厂房": "FDCF",
        "大坝": "DB",
        "张公岛": "ZGD"
    }
    best_match = process.extractOne(position, list(options.keys()))
    print(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")

    result = {
        "type": "ViewAngleManager",
        "function": "SuspendFixedRoaming",
        "data": options[best_match[0]]
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def ContinueFixedRoaming(position: str):

    options = {
        "一号坝体廊道（上侧廊道）": "LD315",
        "二号坝体廊道（下侧廊道）": "LD290",
        "直坝电梯进入": "LD350.2",
        "大坝发电厂房": "FDCF",
        "大坝": "DB",
        "张公岛": "ZGD"
    }
    best_match = process.extractOne(position, list(options.keys()))
    print(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")

    result = {
        "type": "ViewAngleManager",
        "function": "ContinueFixedRoaming",
        "data": options[best_match[0]]
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def ExitFixedRoaming(position: str):
    options = {
        "一号坝体廊道（上侧廊道）": "LD315",
        "二号坝体廊道（下侧廊道）": "LD290",
        "直坝电梯进入": "LD350.2",
        "大坝发电厂房": "FDCF",
        "大坝": "DB",
        "张公岛": "ZGD"
    }
    best_match = process.extractOne(position, list(options.keys()))
    print(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")

    result = {
        "type": "ViewAngleManager",
        "function": "ExitFixedRoaming",
        "data": options[best_match[0]]
    }
    notifications.append({'data': result})
    return "操作成功"


# TODO 引泄水三维可视化表达 dkhao1（1号底孔），dkhao2（2号底孔），dkhao3（3号底孔），dkhao4（4号底孔），dkhao5（5号底孔），dkhao6（6号底孔），dkhao7（7号底孔），dkhao8（8号底孔），dkhao9（9号底孔），dkhao10（10号底孔），dkhao11（11号底孔），dkhao12（12号底孔），skhao1（1号深孔），skhao2（2号深孔），skhao3（3号深孔），skhao4（4号深孔），skhao5（5号深孔），skhao6（6号深孔），skhao7（7号深孔），skhao8（8号深孔），skhao9（9号深孔），skhao10（10号深孔），skhao11（11号深孔），skhao12（12号深孔），dld1(1号导流洞)，dld2（2号导流洞）
@mcp.tool()
async def DiversionWaterOpenClose(homename: str, isOpen: bool, isClear: bool):
    options = {
        '1号底孔': 'dkhao1',
        '2号底孔': 'dkhao2',
        '3号底孔': 'dkhao3',
        '4号底孔': 'dkhao4',
        '5号底孔': 'dkhao5',
        '6号底孔': 'dkhao6',
        '7号底孔': 'dkhao7',
        '8号底孔': 'dkhao8',
        '9号底孔': 'dkhao9',
        '10号底孔': 'dkhao10',
        '11号底孔': 'dkhao11',
        '12号底孔': 'dkhao12',
        '1号深孔': 'skhao1',
        '2号深孔': 'skhao2',
        '3号深孔': 'skhao3',
        '4号深孔': 'skhao4',
        '5号深孔': 'skhao5',
        '6号深孔': 'skhao6',
        '7号深孔': 'skhao7',
        '8号深孔': 'skhao8',
        '9号深孔': 'skhao9',
        '10号深孔': 'skhao10',
        '11号深孔': 'skhao11',
        '12号深孔': 'skhao12',
        '1号导流洞': 'dld1',
        '2号导流洞': 'dld2'
    }
    best_match = process.extractOne(homename, list(options.keys()))
    print(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")

    data = {
        "homename": options[best_match[0]],
        # "homename": homename,
        "isopen": "1" if isOpen else "0",
        "color": "qingshui" if isClear else "zhuoshui"
    }
    result = {
        "type": "DiversionWaterManager",
        "function": "DiversionWaterOpenClose",
        "data": data
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def DiversionWaterPlaneUpDown(start: str, end: str, speed: int):
    data = {
        "start": start,
        "end": end,
        "speed": speed
    }
    result = {
        "type": "DiversionWaterManager",
        "function": "DiversionWaterPlaneUpDown",
        "data": data
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def DiversionWaterPlaneUpDownClose():
    result = {
        "type": "DiversionWaterManager",
        "function": "DiversionWaterPlaneUpDownClose",
    }
    notifications.append({'data': result})
    return "操作成功"

# TODO 大坝三维可视化
@mcp.tool()
async def DamTransparent(isTransparent: bool):
    result = {
        "type": "DamManager",
        "function": "DamTransparent",
        "data": "0" if isTransparent else "1",
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def CivilTransparent(isTransparent : bool):
    result = {
        "type": "DamManager",
        "function": "CivilTransparent",
        "data": "0" if isTransparent else "1",
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def EquipmentShowHide(isTransparent: bool):
    result = {
        "type": "DamManager",
        "function": "EquipmentShowHide",
        "data": "0" if isTransparent else "1",
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def BIMHighlight(BIMID: str, isHighlight: bool):
    data = {
        "BIMID": BIMID,
        "isHighlight": "1" if isHighlight else "0"
    }
    result = {
        "type": "DamManager",
        "function": "BIMHighlight",
        "data": data,
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def SettleWarnCloud(date: str, isShow: bool): # "2025-02-14"
    data = {
        "date": "result_" + date,
        "isShow": isShow
    }
    result = {
        "type": "DamManager",
        "function": "SettleWarnCloud",
        "data": data,
    }
    notifications.append({'data': result})
    return "操作成功"


#TODO 工况模拟三维场景可视化表达
"""
泄洪孔洞名字：        
skhao1:1号深孔    
skhao2:2号深孔     
skhao3:3号深孔     
skhao4:4号深孔     
skhao7:7号深孔     
skhao8:8号深孔     
skhao9:9号深孔

dkhao1:1号底孔     dkhao2:2号底孔  
dkhao3:3号底孔     dkhao4:4号底孔
dkhao5:5号底孔     dkhao6:6号底孔
dkhao7:7号底孔     dkhao8:8号底孔
dkhao9:9号底孔     dkhao10:10号底孔  
dkhao11:11号底孔   dkha12:12号底孔
dkhao13:13号底孔   dkhao14:14号底孔
dkhao15:15号底孔  

dld1:1号导流洞;
dld2:2号导流洞;



闸门名字：
SKGZZM_01:1号深孔工作闸门
SKGZZM_02:2号深孔工作闸门
SKGZZM_03:3号深孔工作闸门
SKGZZM_04:4号深孔工作闸门
SKGZZM_05:5号深孔工作闸门
SKGZZM_06:6号深孔工作闸门
SKGZZM_07:7号深孔工作闸门
SKGZZM_08:8号深孔工作闸门
SKGZZM_09:9号深孔工作闸门

DKGZZM_01:1号底孔工作闸门
DKGZZM_02:2号底孔工作闸门
DKGZZM_03:3号底孔工作闸门
DKGZZM_04:4号底孔工作闸门
DKGZZM_05:5号底孔工作闸门
DKGZZM_06:6号底孔工作闸门
DKGZZM_07:7号底孔工作闸门
DKGZZM_08:8号底孔工作闸门
DKGZZM_09:9号底孔工作闸门
DKGZZM_10:10号底孔工作闸门
DKGZZM_11:11号底孔工作闸门
DKGZZM_12:12号底孔工作闸门
DKGZZM_13:13号底孔工作闸门
DKGZZM_14:14号底孔工作闸门
DKGZZM_15:15号底孔工作闸门

DKSGJXZM_01:1号底孔事故检修闸门
DKSGJXZM_02:2号底孔事故检修闸门
DKSGJXZM_03:3号底孔事故检修闸门
DKSGJXZM_04:4号底孔事故检修闸门
DKSGJXZM_05:5号底孔事故检修闸门
DKSGJXZM_06:6号底孔事故检修闸门
DKSGJXZM_07:7号底孔事故检修闸门
DKSGJXZM_08:8号底孔事故检修闸门
DKSGJXZM_09:9号底孔事故检修闸门
DKSGJXZM_10:10号底孔事故检修闸门
DKSGJXZM_11:11号底孔事故检修闸门
DKSGJXZM_12:12号底孔事故检修闸门


ZAXLSD_DLM_01:导流洞导流门1
ZAXLSD_DLM_02:导流洞导流门2
ZAXLSD_HXZM_01:导流洞弧形闸门1
ZAXLSD_HXZM_02:导流洞弧形闸门2
ZAXLSD_SGJXZM_01:导流洞事故检修闸门1
ZAXLSD_SGJXZM_02:导流洞事故检修闸门2
ZAXLSD_SGJXZM_03:导流洞事故检修闸门3
ZAXLSD_SGJXZM_04:导流洞事故检修闸门4
"""
@mcp.tool()
async def GateState(gateName: str, isOn: bool):
    options = {
        '1号深孔': 'skhao1',
        '2号深孔': 'skhao2',
        '3号深孔': 'skhao3',
        '4号深孔': 'skhao4',
        '7号深孔': 'skhao7',
        '8号深孔': 'skhao8',
        '9号深孔': 'skhao9',
        '1号底孔': 'dkhao1',
        '2号底孔': 'dkhao2',
        '3号底孔': 'dkhao3',
        '4号底孔': 'dkhao4',
        '5号底孔': 'dkhao5',
        '6号底孔': 'dkhao6',
        '7号底孔': 'dkhao7',
        '8号底孔': 'dkhao8',
        '9号底孔': 'dkhao9',
        '10号底孔': 'dkhao10',
        '11号底孔': 'dkhao11',
        '12号底孔': 'dkha12',
        '13号底孔': 'dkhao13',
        '14号底孔': 'dkhao14',
        '15号底孔': 'dkhao15',
        '1号导流洞': 'dld1',
        '2号导流洞': 'dld2',
        '1号深孔工作闸门': 'SKGZZM_01',
        '2号深孔工作闸门': 'SKGZZM_02',
        '3号深孔工作闸门': 'SKGZZM_03',
        '4号深孔工作闸门': 'SKGZZM_04',
        '5号深孔工作闸门': 'SKGZZM_05',
        '6号深孔工作闸门': 'SKGZZM_06',
        '7号深孔工作闸门': 'SKGZZM_07',
        '8号深孔工作闸门': 'SKGZZM_08',
        '9号深孔工作闸门': 'SKGZZM_09',
        '1号底孔工作闸门': 'DKGZZM_01',
        '2号底孔工作闸门': 'DKGZZM_02',
        '3号底孔工作闸门': 'DKGZZM_03',
        '4号底孔工作闸门': 'DKGZZM_04',
        '5号底孔工作闸门': 'DKGZZM_05',
        '6号底孔工作闸门': 'DKGZZM_06',
        '7号底孔工作闸门': 'DKGZZM_07',
        '8号底孔工作闸门': 'DKGZZM_08',
        '9号底孔工作闸门': 'DKGZZM_09',
        '10号底孔工作闸门': 'DKGZZM_10',
        '11号底孔工作闸门': 'DKGZZM_11',
        '12号底孔工作闸门': 'DKGZZM_12',
        '13号底孔工作闸门': 'DKGZZM_13',
        '14号底孔工作闸门': 'DKGZZM_14',
        '15号底孔工作闸门': 'DKGZZM_15',
        '1号底孔事故检修闸门': 'DKSGJXZM_01',
        '2号底孔事故检修闸门': 'DKSGJXZM_02',
        '3号底孔事故检修闸门': 'DKSGJXZM_03',
        '4号底孔事故检修闸门': 'DKSGJXZM_04',
        '5号底孔事故检修闸门': 'DKSGJXZM_05',
        '6号底孔事故检修闸门': 'DKSGJXZM_06',
        '7号底孔事故检修闸门': 'DKSGJXZM_07',
        '8号底孔事故检修闸门': 'DKSGJXZM_08',
        '9号底孔事故检修闸门': 'DKSGJXZM_09',
        '10号底孔事故检修闸门': 'DKSGJXZM_10',
        '11号底孔事故检修闸门': 'DKSGJXZM_11',
        '12号底孔事故检修闸门': 'DKSGJXZM_12',
        '导流洞导流门1': 'ZAXLSD_DLM_01',
        '导流洞导流门2': 'ZAXLSD_DLM_02',
        '导流洞弧形闸门1': 'ZAXLSD_HXZM_01',
        '导流洞弧形闸门2': 'ZAXLSD_HXZM_02',
        '导流洞事故检修闸门1': 'ZAXLSD_SGJXZM_01',
        '导流洞事故检修闸门2': 'ZAXLSD_SGJXZM_02',
        '导流洞事故检修闸门3': 'ZAXLSD_SGJXZM_03',
        '导流洞事故检修闸门4': 'ZAXLSD_SGJXZM_04'
    }
    best_match = process.extractOne(gateName, list(options.keys()))
    print(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")

    data = {
        "gateName": options[best_match[0]],
        # "gateName": gateName,
        "isOn": isOn
    }
    result = {
        "type": "WorkingConditionManager",
        "function": "GateState",
        "data": data,
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def OnlyGateEnable(isOnlyGateEnable: bool):
    result = {
        "type": "WorkingConditionManager",
        "function": "GateEnable",
        "data": isOnlyGateEnable,
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def FocusingGatePoint(gateId: str):
    result = {
        "type": "WorkingConditionManager",
        "function": "FocusingGatePoint",
        "data": gateId,
    }
    notifications.append({'data': result})
    return "操作成功"


# TODO 图层控制功能管理
"""
LineName: GLQ 管理范围线
          BHQ  保护范围线
          QQ  确权土地范围线
          WQQ   未确权土地范围线
          MarkManager 水工标签
          WaterPlane   水面控制
"""
@mcp.tool()
async def ManagementScopeLine(lineName: str, isShow: bool):
    options = {'管理范围线': 'GLQ', '保护范围线': 'BHQ', '确权土地范围线': 'QQ', '未确权土地范围线': 'WQQ', '水工标签': 'MarkManager', '水面控制': 'WaterPlane'}
    best_match = process.extractOne(lineName, list(options.keys()))
    print(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")
    
    data = {
        "lineName": options[best_match[0]],
        # "lineName": lineName,
        "isShow": isShow
    }
    result = {
        "type": "CoverageManager",
        "function": "ManagementScopeLine",
        "data": data,
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def ManagementScopeLineAllShow(isAllShow: bool):
    result = {
        "type": "CoverageManager",
        "function": "ManagementScopeLineAllShow",
        "data": isAllShow,
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def DamMarkControll(isShowDamMark: bool):
    result = {
        "type": "CoverageManager",
        "function": "DamMarkControll",
        "data": isShowDamMark,
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def FDCFMarkShowControll(isShowFDCFMark: bool):
    result = {
        "type": "CoverageManager",
        "function": "FDCFMarkShowControll",
        "data": isShowFDCFMark,
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def XJDShowControll(isShowFDCFMark: bool):
    result = {
        "type": "CoverageManager",
        "function": "XJDShowControll",
        "data": isShowFDCFMark,
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def OverlyShow(isOverlyShow: bool, overlytag: str):# DK底孔,SK深孔,DLD导流洞
    options = {'底孔': 'DK', '深孔': 'SK', '导流洞': 'DLD'}
    best_match = process.extractOne(overlytag, list(options.keys()))
    print(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")

    data = {
      "overlyshow": isOverlyShow,
      "overlytag": options[best_match[0]]

    }
    result = {
        "type": "CoverageManager",
        "function": "OverlyShow",
        "data": [data],
    }
    notifications.append({'data': result})
    return "操作成功"

# TODO 通用方法
@mcp.tool()
async def ResetScene():
    result = {
        "type": "ToolFunctionManager",
        "function": "ResetScene",
        "data": "",
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def SetCursorState(cursorState: str):
    result = {
        "type": "ToolFunctionManager",
        "function": "SetCursorState",
        "data": cursorState,
    }
    notifications.append({'data': result})
    return "操作成功"


# TODO 天气系统
"""
fine 晴天
partcloudy 少云
cloudy 多云
overcast 阴天
thickness 多雾
lightrain 小雨 
moderaterain 中雨
heavyrain 大雨
thunderstorm 雷雨
lightsnow 小雪
moderatesnow 中雪
blizzard 暴雪

"""
@mcp.tool()
async def SetWeather(weather: str):
    options = {'晴天': 'fine', '少云': 'partcloudy', '多云': 'cloudy', '阴天': 'overcast', '多雾': 'thickness', '小雨': 'lightrain', '中雨': 'moderaterain', '大雨': 'heavyrain', '雷雨': 'thunderstorm', '小雪': 'lightsnow', '中雪': 'moderatesnow', '暴雪': 'blizzard'}
    best_match = process.extractOne(weather, list(options.keys()))
    print(f"最匹配的选项是: {best_match[0]}，相似度得分: {best_match[1]}")
    
    result = {
        "type": "WeatherManager",
        "function": "SetWeather",
        "data": options[best_match[0]],
        # "data": weather
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def SetTime(time: str): # 18:30
    result = {
        "type": "ToolFunctionManager",
        "function": "SetTime",
        "data": time,
    }
    notifications.append({'data': result})
    return "操作成功"


# TODO 有限元预测
@mcp.tool()
async def CreateMesh(type: str, meshIndexPath: str, resultPath: str): 
    type_options = {'合位移': 0, '水平向位移': 1, '竖直位移': 2, '最大主应力': 3, '最小主应力': 4, '水平应力': 5, '垂直应力': 6}
    meshIndexPath_options = {'整体': 'ZhengTi', '电站坝段': 'DZBD_5', '右岸非溢流坝段': 'YAFYLBD_3', '溢流坝段2': 'YLB`D_2', '溢流坝段3': 'YLBD_3'}
    type_best_match = process.extractOne(type, list(type_options.keys()))
    meshIndexPath_best_match = process.extractOne(meshIndexPath, list(meshIndexPath_options.keys()))

    print(f"type最匹配的选项是: {type_best_match[0]}，相似度得分: {type_best_match[1]}")
    print(f"type最匹配的选项是: {meshIndexPath_best_match[0]}，相似度得分: {meshIndexPath_best_match[1]}")

    data = {
      "type": type_options[type_best_match[0]],
      "MeshIndexPath": meshIndexPath_options[meshIndexPath_best_match[0]],
      "ResultPath": resultPath
    }
    result = {
        "type": "SeepageManager",
        "function": "CreateMesh",
        "data": data,
    }
    notifications.append({'data': result})
    return "操作成功"

@mcp.tool()
async def DestoryMesh(isClear: bool, isHide: bool):
    data = {
      "IsClear": isClear,
      "IsHide": isHide
    }
    result = {
        "type": "SeepageManager",
        "function": "DestoryMesh",
        "data": data,
    }
    notifications.append({'data': result})
    return "操作成功"


## sse传输
def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can serve the provided mcp server with SSE."""
    sse = SseServerTransport("/messages/")
    async def handle_Tool_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    async def notification_generator():
        # 这里可以使用队列或者其他机制来存储通知​
        while True:
            if notifications:
                yield {
                    "event": "notification",
                    "data": notifications.pop(0)
                }
            await asyncio.sleep(1)

    app = Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_Tool_sse),
            Route("/ue_sse", lambda request: EventSourceResponse(notification_generator())),
            Mount("/messages/", app=sse.handle_post_message)
        ],
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有源访问，生产环境中应替换为实际允许的源​
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    return app

if __name__ == "__main__":
    mcp_server = mcp._mcp_server

    import argparse

    parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8020, help='Port to listen on')
    args = parser.parse_args()

    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    uvicorn.run(starlette_app, host=args.host, port=args.port)
