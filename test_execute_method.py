#!/usr/bin/env python3
"""
测试 execute 方法是否能正确处理异步工具调用
"""

import asyncio
from src.agent.ai import Message
from src.tool import Tool
from src.memory import get_shared_memory

class MockToolCall:
    def __init__(self, name, arguments):
        self.function = MockFunction(name, arguments)
        self.id = "test_tool_call"

class MockFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

async def test_execute_method():
    # 获取共享记忆实例
    memory = get_shared_memory()
    
    # 创建工具实例
    tools = Tool(memory)
    
    # 创建测试消息
    test_message = Message(
        role="assistant",
        content="",
        tool_calls=[]
    )
    
    # 手动创建 MockToolCall 对象
    tool_call = MockToolCall(
        "search_web",
        '{"query": "Python 异步编程", "count": 3}'
    )
    test_message.tool_calls.append(tool_call)
    
    print("测试 execute 方法处理异步工具调用...")
    # 执行工具
    tool_messages = await tools.execute(test_message, True)
    
    # 打印结果
    if tool_messages:
        for msg in tool_messages:
            print(f"工具执行结果: {msg.content[:500]}...")
    else:
        print("工具执行无结果")
    
    print("测试完成！")

if __name__ == "__main__":
    asyncio.run(test_execute_method())
