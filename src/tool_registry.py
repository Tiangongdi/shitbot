"""
工具注册表 - 使用装饰器自动生成OpenAI Function Calling Schema

原理：通过装饰器收集工具函数，自动从函数签名、类型注解、docstring生成JSON schema
这样就不用手动维护两份定义了，实现和定义保持一致
"""

import inspect
import functools
from typing import get_type_hints, Callable, Dict, List, Any, Optional


# Python类型到JSON Schema类型的映射
TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
    type(None): "null",
    Any: "string",  # 默认处理为string
}


class ToolRegistry:
    """工具注册表，自动收集并生成工具定义"""
    
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._implementations: Dict[str, Callable] = {}
    
    def tool(self, description: Optional[str] = None) -> Callable:
        """
        工具装饰器，将函数标记为工具并自动注册
        
        Args:
            description: 工具描述，如果不提供则使用函数docstring
            
        Usage:
            @registry.tool("读取指定文件内容")
            def read_file(file_path: str) -> str:
                ...
        """
        def decorator(func: Callable) -> Callable:
            # 获取函数信息
            name = func.__name__
            doc = description or func.__doc__ or "No description available"
            
            # 解析函数签名生成schema
            schema = self._function_to_schema(func, name, doc)
            
            # 注册
            self._tools[name] = schema
            self._implementations[name] = func
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            return wrapper
        
        return decorator
    
    def _function_to_schema(self, func: Callable, name: str, description: str) -> Dict[str, Any]:
        """从函数自动生成OpenAI function calling schema"""
        signature = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        properties = {}
        required = []

        for param_name, param in signature.parameters.items():
            # 跳过 self 参数（类实例方法的第一个参数）
            if param_name == 'self':
                continue

            # 获取参数类型
            param_type = type_hints.get(param_name, Any)
            json_type = TYPE_MAP.get(param_type, "string")

            # 获取参数默认值注释（从docstring中提取，或者使用参数名）
            param_doc = self._extract_param_doc(func.__doc__ or "", param_name)

            properties[param_name] = {
                "type": json_type,
                "description": param_doc or param_name
            }

            # 如果没有默认值，标记为必填
            if param.default == inspect._empty:
                required.append(param_name)

            # 如果有默认值，添加到schema中
            else:
                properties[param_name]["default"] = param.default
        
        schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": description.strip() if description else "",
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }
        
        return schema
    
    def _extract_param_doc(self, docstring: str, param_name: str) -> str:
        """从docstring中提取参数描述"""
        # 支持多种格式：:param name:, Args:    name: description, etc.
        lines = docstring.split('\n')
        
        # 搜索 :param name: 格式
        for line in lines:
            line = line.strip()
            if f":param {param_name}:" in line:
                desc = line.split(f":param {param_name}:")[1].strip()
                return desc
            if f"Args:" in line or f"Parameters:" in line:
                continue
            if line.startswith(f"{param_name}:"):
                desc = line.split(f"{param_name}:")[1].strip()
                return desc
        
        return ""
    
    def get_tools_definition(self, if_not_timer: bool = True, if_not_subagent: bool = True) -> List[Dict[str, Any]]:
        """获取所有工具定义，用于AI调用
        
        支持过滤：某些工具只在特定条件下可用
        - if_not_timer: 是否包含定时器相关工具（当调用方是用户而非定时器时为True）
        - if_not_subagent: 是否包含子智能体相关工具（当调用方是主智能体而非子智能体时为True）
        """
        tools = list(self._tools.values())
        
        # 需要过滤掉的工具
        filtered_tools = []
        
        # 定时器相关工具名
        timer_tools = {"once_after", "interval", "daily_at", "cancel_timer", "pause_timer", "resume_timer", "list"}
        # delete_file也只对用户可见
        if not if_not_timer:
            # 定时器上下文，不包含定时器工具
            tools = [t for t in tools if t["function"]["name"] not in timer_tools]
        else:
            # 用户上下文，包含delete_file（只有用户能删文件）
            pass  # delete_file已经注册，包含
        
        # 子智能体相关工具
        if not if_not_subagent:
            # 子智能体上下文，不包含create_subagent工具
            tools = [t for t in tools if t["function"]["name"] != "create_subagent"]
        
        return tools
    
    def get_implementation(self, tool_name: str) -> Optional[Callable]:
        """根据工具名获取实现函数"""
        return self._implementations.get(tool_name)
    
    def list_tools(self) -> List[str]:
        """列出所有已注册工具名"""
        return list(self._tools.keys())
    
    def has_tool(self, tool_name: str) -> bool:
        """检查工具是否存在"""
        return tool_name in self._implementations


# 创建全局注册表实例
registry = ToolRegistry()


# ==================== 示例用法 ====================

if __name__ == "__main__":
    # 测试装饰器
    
    @registry.tool("读取指定文件内容")
    def read_file(file_path: str) -> str:
        """
        读取指定文件的内容
        
        :param file_path: 要读取的文件路径
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @registry.tool("给指定文件写入内容")
    def write_file(file_path: str, content: str) -> str:
        """
        写入内容到指定文件
        
        :param file_path: 要写入的文件路径
        :param content: 要写入的内容
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"成功写入: {file_path}"
    
    @registry.tool("搜索网络信息")
    def search_web(query: str, count: int = 5) -> str:
        """
        在网络上搜索信息
        
        :param query: 搜索查询词
        :param count: 返回结果数量，默认为5
        """
        return f"搜索结果 for {query}"
    
    # 输出生成的schema
    import json
    print(json.dumps(registry.get_tools_definition(), indent=2, ensure_ascii=False))
