# UeForAIServer-MCP

## 项目介绍
UeForAIServer-MCP是一个用于控制虚幻引擎(UE)场景中视角和漫游功能的服务端应用。它提供了基于MCP(Message Control Protocol)的WebSocket接口和SSE(Server-Sent Events)通知机制，使客户端能够实时控制和接收场景更新。

## 功能特性
- 视角控制：第一/第三人称视角切换、位置标记、视角飞行
- 漫游控制：固定路径漫游的开始、停止、暂停和恢复
- 通知系统：实时向客户端推送场景更新和操作反馈
- 会话管理：支持多客户端同时连接和独立操作

## 技术栈
- **后端框架**：Starlette
- **服务器**：Uvicorn
- **通信协议**：MCP、WebSocket、SSE
- **语言**：Python 3.11+

## 快速开始

### 环境要求
- Python 3.11+
- Git

### 安装步骤
1. 克隆项目代码
   ```bash
   git clone <repository-url>
   cd UeForAIServer_MCP
   ```

2. 创建虚拟环境
   ```bash
   python -m venv .venv
   ```

3. 激活虚拟环境
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

5. 配置环境变量
   复制 `.env.example` 文件并重命名为 `.env`，根据需要修改配置：
   ```bash
   cp .env.example .env
   # 编辑.env文件
   ```

### 运行服务器
```bash
# 使用uvicorn直接运行
uvicorn main:app --host 0.0.0.0 --port 9002

# 或者使用项目入口文件
python main.py --host 0.0.0.0 --port 9002

# 使用uv运行(如果已安装)
uv run main.py --host 0.0.0.0 --port 9002
```

## API接口

### 健康检查
- **GET /health**
  - 描述：检查服务器运行状态
  - 返回：JSON格式的状态信息

### 会话管理
- **GET /api/sessions**
  - 描述：获取所有活跃会话信息
  - 返回：JSON格式的会话列表

### SSE通知接口
- **GET /ue_sse?session_id=xxx**
  - 描述：建立SSE连接，接收场景更新通知
  - 参数：
    - `session_id`：可选，客户端会话ID，如果不提供则自动生成
  - 返回：SSE流，事件类型为"notification"

### MCP接口
- **GET /sse**
  - 描述：MCP协议WebSocket连接入口

## 工具函数

### 视角控制
- `FirstPerson(session_id: str)`: 切换到第一人称视角
- `ThirdPerson(session_id: str)`: 切换到第三人称视角
- `MarkLocation(session_id: str, location_name: str)`: 在当前位置创建标记点
- `flyto(location: str, session_id: str, type: str = "Reservoir")`: 飞行到指定位置
- `ZoomIn(session_id: str)`: 放大视角
- `ZoomOut(session_id: str)`: 缩小视角

### 漫游控制
- `StartFixedRoaming(session_id: str, path_name: str)`: 开始固定路径漫游
- `StopRoaming(session_id: str)`: 停止漫游
- `PauseRoaming(session_id: str)`: 暂停漫游
- `ResumeRoaming(session_id: str)`: 恢复漫游
- `GetRoamingPositions()`: 获取所有可用的漫游路径

## 配置说明
配置文件位于 `config.py`，支持通过环境变量覆盖默认值：
- `HOST`: 服务器主机地址，默认为"0.0.0.0"
- `PORT`: 服务器端口，默认为8020
- `DEBUG`: 调试模式开关，默认为False
- `LOG_LEVEL`: 日志级别，默认为"INFO"
- `SECRET_KEY`: 会话加密密钥
- `NOTIFICATION_QUEUE_MAX_SIZE`: 通知队列最大长度

## 开发指南
1. 确保遵循项目的代码结构和命名规范
2. 新功能应该在适当的模块中实现
3. 提交代码前请确保所有功能正常运行

## 注意事项
- 请确保虚拟环境已正确激活
- 生产环境中请设置`DEBUG=False`和适当的`SECRET_KEY`
- 若遇到端口冲突，请修改`.env`文件中的`PORT`配置

## License
MIT