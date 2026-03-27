"""
MCP (Model Context Protocol) 客户端模块
负责连接 MCP Server、发现工具、转发调用

支持两种传输方式:
- stdio: 通过子进程启动本地 MCP Server
- sse: 通过 HTTP SSE 连接远程 MCP Server
"""

import asyncio
import json
import os
import sys
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

import anyio
from mcp import ClientSession, StdioServerParameters, stdio_client
from mcp.types import TextContent, ImageContent, Tool


@dataclass
class MCPServerConfig:
    """单个 MCP Server 的配置"""
    name: str
    transport: str = "stdio"
    command: str = ""
    args: list = field(default_factory=list)
    env: dict = field(default_factory=dict)
    url: str = ""
    description: str = ""


class MCPServerConnection:
    """单个 MCP Server 的连接管理"""

    def __init__(self, config: MCPServerConfig):
        self.config = config
        self.tools: List[Tool] = []
        self._connected = False
        self._session: Optional[ClientSession] = None
        self._ready = False
        self._error: Optional[str] = None

    async def run_forever(self) -> bool:
        """运行连接并保持"""
        try:
            if self.config.transport == "stdio":
                env = {**os.environ, **self.config.env}
                server_params = StdioServerParameters(
                    command=self.config.command,
                    args=self.config.args,
                    env=env
                )
                async with stdio_client(server_params) as (read_stream, write_stream):
                    async with ClientSession(read_stream, write_stream) as session:
                        self._session = session
                        await session.initialize()
                        tools_result = await session.list_tools()
                        self.tools = tools_result.tools
                        self._connected = True
                        self._ready = True
                        await anyio.sleep_forever()
            elif self.config.transport == "sse":
                from mcp.client.sse import sse_client
                async with sse_client(self.config.url) as (read_stream, write_stream):
                    async with ClientSession(read_stream, write_stream) as session:
                        self._session = session
                        await session.initialize()
                        tools_result = await session.list_tools()
                        self.tools = tools_result.tools
                        self._connected = True
                        self._ready = True
                        await anyio.sleep_forever()
            else:
                self._error = f"不支持的传输方式: {self.config.transport}"
                self._ready = True
                return False
        except anyio.get_cancelled_exc_class():
            raise
        except Exception as e:
            self._error = str(e)
            self._ready = True
            return False
        return True

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """调用 MCP Server 上的工具"""
        if not self._connected or not self._session:
            return f"MCP Server [{self.config.name}] 未连接"

        try:
            result = await self._session.call_tool(name=tool_name, arguments=arguments)

            texts = []
            if result.content:
                for content_item in result.content:
                    if isinstance(content_item, TextContent):
                        texts.append(content_item.text)
                    elif hasattr(content_item, 'text'):
                        texts.append(content_item.text)
                    else:
                        texts.append(str(content_item))

            if result.isError:
                return f"[MCP 错误] {chr(10).join(texts) if texts else '未知错误'}"

            return "\n".join(texts) if texts else "（工具返回空结果）"

        except Exception as e:
            return f"MCP 工具调用失败 [{self.config.name}/{tool_name}]: {str(e)}"

    async def disconnect(self):
        """断开连接"""
        self._session = None
        self._connected = False
        self.tools = []


class MCPClientManager:
    """MCP 客户端生命周期管理器"""
    
    _instance = None
    
    def __init__(self):
        self._tg = None
        self._task = None
        self._connections: Dict[str, MCPServerConnection] = {}
        self._tool_to_server: Dict[str, str] = {}
        self._blocked_tools: set = set()
        self._blocked_servers: set = set()
        self._initialized = False
        self._started = anyio.Event()
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    async def start(self, servers_config: List[MCPServerConfig]) -> int:
        """启动 MCP 客户端"""
        if not servers_config:
            return 0
            
        print("\n[MCP] 正在初始化 MCP Servers...")
        
        async def _run_all():
            async with anyio.create_task_group() as tg:
                self._tg = tg
                self._started.set()
                
                for server_config in servers_config:
                    if server_config.name in self._blocked_servers:
                        print(f"  ⊘ MCP Server [{server_config.name}] 已被安全策略屏蔽，跳过")
                        continue

                    conn = MCPServerConnection(server_config)
                    self._connections[server_config.name] = conn
                    tg.start_soon(conn.run_forever)
                
                await anyio.sleep_forever()
        
        self._task = asyncio.create_task(_run_all())
        await self._started.wait()
        
        for _ in range(1200):  # 120 seconds timeout for npm install
            await asyncio.sleep(0.1)
            all_ready = all(
                conn._ready or conn._error
                for conn in self._connections.values()
            )
            if all_ready:
                break
        
        total_tools = 0
        for server_name, conn in list(self._connections.items()):
            if conn._connected:
                for tool in conn.tools:
                    if tool.name not in self._blocked_tools:
                        self._tool_to_server[tool.name] = server_name
                active_tools = len([t for t in conn.tools if t.name not in self._blocked_tools])
                total_tools += active_tools
                print(f"  ✓ MCP Server [{server_name}] 已连接，发现 {active_tools} 个工具")
            elif conn._error:
                print(f"  ✗ MCP Server [{server_name}] 连接失败: {conn._error}")
            else:
                print(f"  ✗ MCP Server [{server_name}] 连接超时")

        self._initialized = True
        print(f"[MCP] 初始化完成，共 {total_tools} 个 MCP 工具可用\n")
        return total_tools
    
    async def stop(self):
        """停止 MCP 客户端"""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        
        self._connections.clear()
        self._tool_to_server.clear()
        self._initialized = False
    
    @property
    def connections(self) -> Dict[str, MCPServerConnection]:
        return self._connections
    
    @property
    def initialized(self) -> bool:
        return self._initialized
    
    def get_tools_definition(self) -> list:
        result = []
        for server_name, conn in self._connections.items():
            for tool in conn.tools:
                if tool.name in self._blocked_tools:
                    continue

                desc = tool.description or ""
                prefix = f"[MCP:{server_name}] "
                full_desc = prefix + desc

                parameters = tool.inputSchema if tool.inputSchema else {
                    "type": "object",
                    "properties": {}
                }

                result.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": full_desc,
                        "parameters": parameters
                    }
                })

        return result

    def get_mcp_tools_summary(self) -> str:
        if not self._connections:
            return "MCP: 未连接任何 Server"

        lines = ["MCP 已连接 Servers:"]
        for server_name, conn in self._connections.items():
            tool_names = [t.name for t in conn.tools if t.name not in self._blocked_tools]
            lines.append(f"  [{server_name}] {len(tool_names)} 个工具: {', '.join(tool_names)}")

        return "\n".join(lines)

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        if tool_name in self._blocked_tools:
            return f"MCP 工具 [{tool_name}] 已被安全策略屏蔽"

        server_name = self._tool_to_server.get(tool_name)
        if not server_name:
            return f"未找到 MCP 工具: {tool_name}"

        if server_name in self._blocked_servers:
            return f"MCP Server [{server_name}] 已被安全策略屏蔽"

        conn = self._connections.get(server_name)
        if not conn or not conn._connected:
            return f"MCP Server [{server_name}] 未连接"

        return await conn.call_tool(tool_name, arguments)

    def is_mcp_tool(self, tool_name: str) -> bool:
        return tool_name in self._tool_to_server

    def block_tool(self, tool_name: str):
        self._blocked_tools.add(tool_name)

    def unblock_tool(self, tool_name: str):
        self._blocked_tools.discard(tool_name)

    def block_server(self, server_name: str):
        self._blocked_servers.add(server_name)

    def unblock_server(self, server_name: str):
        self._blocked_servers.discard(server_name)

    def get_server_names(self) -> List[str]:
        return list(self._connections.keys())

    def get_tool_count(self) -> int:
        return len(self._tool_to_server)


class MCPClient:
    """
    MCP 客户端管理器
    管理所有 MCP Server 连接，提供统一的工具发现和调用接口
    """

    def __init__(self):
        self._manager = MCPClientManager.get_instance()
        self._blocked_tools: set = set()
        self._blocked_servers: set = set()

    @property
    def connections(self) -> Dict[str, MCPServerConnection]:
        return self._manager.connections

    @property
    def initialized(self) -> bool:
        return self._manager.initialized

    async def connect_all(self, servers_config: List[MCPServerConfig]) -> int:
        return await self._manager.start(servers_config)

    def get_tools_definition(self) -> list:
        return self._manager.get_tools_definition()

    def get_mcp_tools_summary(self) -> str:
        return self._manager.get_mcp_tools_summary()

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        return await self._manager.call_tool(tool_name, arguments)

    def is_mcp_tool(self, tool_name: str) -> bool:
        return self._manager.is_mcp_tool(tool_name)

    def block_tool(self, tool_name: str):
        self._manager.block_tool(tool_name)

    def unblock_tool(self, tool_name: str):
        self._manager.unblock_tool(tool_name)

    def block_server(self, server_name: str):
        self._manager.block_server(server_name)

    def unblock_server(self, server_name: str):
        self._manager.unblock_server(server_name)

    async def disconnect_all(self):
        await self._manager.stop()

    def get_server_names(self) -> List[str]:
        return self._manager.get_server_names()

    def get_tool_count(self) -> int:
        return self._manager.get_tool_count()
