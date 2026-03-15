#!/usr/bin/env python3
"""
测试定时任务功能
"""

import asyncio
from tools.timer import get_timer

async def main():
    print("测试定时任务功能")
    print("=" * 60)
    
    # 获取全局定时器实例
    timer = get_timer()
    
    # 显示当前任务列表
    print("当前任务列表:")
    tasks = timer.get_tasks()
    for task in tasks:
        print(f"  - {task}")
    
    # 添加一个测试任务（5秒后执行）
    print("\n添加一个5秒后执行的测试任务...")
    task_id = timer.once_after("测试定时任务执行", 5)
    print(f"  任务ID: {task_id}")
    
    # 显示更新后的任务列表
    print("\n更新后的任务列表:")
    tasks = timer.get_tasks()
    for task in tasks:
        print(f"  - {task}")
    
    # 等待任务执行
    print("\n等待5秒，观察任务执行...")
    await asyncio.sleep(6)
    
    # 显示任务执行后的列表
    print("\n任务执行后的列表:")
    tasks = timer.get_tasks()
    for task in tasks:
        print(f"  - {task}")
    
    print("\n测试完成")

if __name__ == "__main__":
    asyncio.run(main())
