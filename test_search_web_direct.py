#!/usr/bin/env python3
"""
直接测试 search_web 方法
"""

import asyncio
from src.tool import Tool
from src.memory import get_shared_memory

async def test_search_web_direct():
    # 获取共享记忆实例
    memory = get_shared_memory()
    
    # 创建工具实例
    tools = Tool(memory)
    
    print("直接测试 search_web 方法...")
    # 直接调用 search_web 方法
    result = await tools.search_web("Python 异步编程", 3)
    
    # 打印结果
    print(f"搜索结果: {result}")
    
    print("测试完成！")

if __name__ == "__main__":
    asyncio.run(test_search_web_direct())
