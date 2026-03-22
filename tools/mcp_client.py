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

from mcp import ClientSession, StdioServerParameters, stdio_client
from mcp.types import TextContent, ImageContent, Tool


@dataclass
class MCPServerConfig:
    """单个 MCP Server 的配置"""
    name: str
    transport: str = "stdio"       # "stdio" 或 "sse"
    command: str = ""              # stdio 模式的启动命令
    args: list = field(default_factory=list)  # stdio 模式的命令参数
    env: dict = field(default_factory=dict)   # 环境变量
    url: str = ""                  # SSE 模式的 URL
    description: str = ""


class MCPServerConnection:
    """单个 MCP Server 的连接管理"""

    def __init__(self, config: MCPServerConfig):
        self.config = config
        self.session: Optional[ClientSession] = None
        self.tools: List[Tool] = []
        self._cm = None  # async context manager
        self._connected = False

    async def connect(self) -> bool:
        """连接到 MCP Server，返回是否成功"""
        try:
            if self.config.transport == "stdio":
                # 合并环境变量
                env = {**os.environ, **self.config.env}

                server_params = StdioServerParameters(
                    command=self.config.command,
                    args=self.config.args,
                    env=env
                )
                self._cm = stdio_client(server_params)
                read_stream, write_stream = await self._cm.__aenter__()

            elif self.config.transport == "sse":
                from mcp.client.sse import sse_client
                self._cm = sse_client(self.config.url)
                read_stream, write_stream = await self._cm.__aenter__()
            else:
                print(f"  ✗ MCP Server [{self.config.name}] 不支持的传输方式: {self.config.transport}")
                return False

            self.session = ClientSession(read_stream, write_stream)
            await self.session.initialize()

            # 发现工具
            tools_result = await self.session.list_tools()
            self.tools = tools_result.tools
            self._connected = True

            return True

        except Exception as e:
            print(f"  ✗ MCP Server [{self.config.name}] 连接失败: {e}")
            self._connected = False
            return False

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """调用 MCP Server 上的工具"""
        if not self._connected or not self.session:
            return f"MCP Server [{self.config.name}] 未连接"

        try:
            result = await self.session.call_tool(name=tool_name, arguments=arguments)

            # 提取内容
            texts = []
            if result.content:
                for content_item in result.content:
                    if isinstance(content_item, TextContent):
                        texts.append(content_item.text)
                    elif hasattr(content_item, 'text'):
                        texts.append(content_item.text)
                    else:
                        # 其他类型（如 ImageContent）转为字符串
                        texts.append(str(content_item))

            if result.isError:
                return f"[MCP 错误] {chr(10).join(texts) if texts else '未知错误'}"

            return "\n".join(texts) if texts else "（工具返回空结果）"

        except Exception as e:
            return f"MCP 工具调用失败 [{self.config.name}/{tool_name}]: {str(e)}"

    async def disconnect(self):
        """断开连接"""
        try:
            if self._cm:
                await self._cm.__aexit__(None, None, None)
        except Exception:
            pass
        finally:
            self.session = None
            self._cm = None
            self._connected = False
            self.tools = []


class MCPClient:
    """
    MCP 客户端管理器
    管理所有 MCP Server 连接，提供统一的工具发现和调用接口
    """

    def __init__(self):
        self.connections: Dict[str, MCPServerConnection] = {}
        self._tool_to_server: Dict[str, str] = {}  # 工具名 → Server 名映射
        self._blocked_tools: set = set()           # 黑名单工具
        self._blocked_servers: set = set()         # 黑名单 Server
        self._initialized = False

    @property
    def initialized(self) -> bool:
        return self._initialized

    async def connect_all(self, servers_config: List[MCPServerConfig]) -> int:
        """
        连接所有配置的 MCP Server

        Args:
            servers_config: MCP Server 配置列表

        Returns:
            成功连接的工具总数
        """
        if not servers_config:
            return 0

        total_tools = 0
        print("\n[MCP] 正在连接 MCP Servers...")

        for server_config in servers_config:
            # 跳过被屏蔽的 Server
            if server_config.name in self._blocked_servers:
                print(f"  ⊘ MCP Server [{server_config.name}] 已被安全策略屏蔽，跳过")
                continue

            conn = MCPServerConnection(server_config)
            success = await conn.connect()

            if success:
                self.connections[server_config.name] = conn

                # 建立工具名到 Server 的映射
                for tool in conn.tools:
                    if tool.name not in self._blocked_tools:
                        self._tool_to_server[tool.name] = server_config.name

                active_tools = len([t for t in conn.tools if t.name not in self._blocked_tools])
                total_tools += active_tools
                print(f"  ✓ MCP Server [{server_config.name}] 已连接，发现 {len(conn.tools)} 个工具"
                      + (f"（{len(conn.tools) - active_tools} 个被屏蔽）" if active_tools < len(conn.tools) else ""))

        self._initialized = True
        print(f"[MCP] 初始化完成，共 {total_tools} 个 MCP 工具可用\n")
        return total_tools

    def get_tools_definition(self) -> list:
        """
        将所有 MCP 工具转换为 OpenAI function calling 格式
        用于注入到 AI 的 tools 参数中

        Returns:
            OpenAI function calling 格式的工具定义列表
        """
        result = []
        for server_name, conn in self.connections.items():
            for tool in conn.tools:
                if tool.name in self._blocked_tools:
                    continue

                # 构建 description，标注来源
                desc = tool.description or ""
                prefix = f"[MCP:{server_name}] "
                full_desc = prefix + desc

                # 构建 parameters
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
        """
        获取 MCP 工具摘要信息（用于日志和调试）

        Returns:
            MCP 工具摘要字符串
        """
        if not self.connections:
            return "MCP: 未连接任何 Server"

        lines = ["MCP 已连接 Servers:"]
        for server_name, conn in self.connections.items():
            tool_names = [t.name for t in conn.tools if t.name not in self._blocked_tools]
            lines.append(f"  [{server_name}] {len(tool_names)} 个工具: {', '.join(tool_names)}")

        return "\n".join(lines)

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        根据工具名路由到对应的 MCP Server 并调用

        Args:
            tool_name: 工具名称
            arguments: 工具参数

        Returns:
            工具执行结果字符串
        """
        # 安全检查
        if tool_name in self._blocked_tools:
            return f"MCP 工具 [{tool_name}] 已被安全策略屏蔽"

        server_name = self._tool_to_server.get(tool_name)
        if not server_name:
            return f"未找到 MCP 工具: {tool_name}"

        if server_name in self._blocked_servers:
            return f"MCP Server [{server_name}] 已被安全策略屏蔽"

        conn = self.connections.get(server_name)
        if not conn or not conn._connected:
            return f"MCP Server [{server_name}] 未连接"

        return await conn.call_tool(tool_name, arguments)

    def is_mcp_tool(self, tool_name: str) -> bool:
        """判断是否为 MCP 工具"""
        return tool_name in self._tool_to_server

    def block_tool(self, tool_name: str):
        """屏蔽某个 MCP 工具"""
        self._blocked_tools.add(tool_name)

    def unblock_tool(self, tool_name: str):
        """解除屏蔽某个 MCP 工具"""
        self._blocked_tools.discard(tool_name)

    def block_server(self, server_name: str):
        """屏蔽某个 MCP Server"""
        self._blocked_servers.add(server_name)

    def unblock_server(self, server_name: str):
        """解除屏蔽某个 MCP Server"""
        self._blocked_servers.discard(server_name)

    async def disconnect_all(self):
        """断开所有 MCP Server 连接"""
        for conn in self.connections.values():
            await conn.disconnect()
        self.connections.clear()
        self._tool_to_server.clear()
        self._initialized = False

    def get_server_names(self) -> List[str]:
        """获取所有已连接的 Server 名称"""
        return list(self.connections.keys())

    def get_tool_count(self) -> int:
        """获取可用 MCP 工具总数"""
        return len(self._tool_to_server)
