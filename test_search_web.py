#!/usr/bin/env python3
"""
测试 search_web 方法的执行
"""

import asyncio
from src.agent.ai import Message
from src.tool import Tool
from src.memory import get_shared_memory

async def test_search_web():
    # 获取共享记忆实例
    memory = get_shared_memory()
    
    # 创建工具实例
    tools = Tool(memory)
    
    # 创建测试消息
    test_message = Message(
        role="assistant",
        content="",
        tool_calls=[{
            "id": "test_tool_call",
            "type": "function",
            "function": {
                "name": "search_web",
                "arguments": '{"query": "Python 异步编程", "count": 3}'
            }
        }]
    )
    
    print("测试 search_web 方法...")
    # 执行工具
    tool_messages = await tools.execute(test_message, True)
    
    # 打印结果
    if tool_messages:
        for msg in tool_messages:
            print(f"工具执行结果: {msg.content}")
    else:
        print("工具执行无结果")
    
    print("测试完成！")

if __name__ == "__main__":
    asyncio.run(test_search_web())
