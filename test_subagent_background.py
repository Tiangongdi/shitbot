import asyncio
from src.agent.subagent_manager import get_subagent_manager
from src.memory import SharedMemory

async def test_background_task():
    print("开始测试SubAgent后台执行功能")
    print("=" * 60)
    
    # 创建主智能体的共享记忆
    main_memory = SharedMemory()
    
    # 获取SubAgent管理器
    manager = get_subagent_manager()
    
    # 测试后台执行任务
    role = "你是一个助手，负责执行简单的任务"
    task = "请计算1+2+3+...+100的和，并详细说明计算过程"
    
    print("执行后台任务1：", task)
    start_message = manager.run_background_task(role, task, main_memory)
    print("返回的提示信息：", start_message)
    
    role = "你是一个网络调查助手，负责搜索查看网页整理信息"
    task = "在网络上面搜索2月相关的AI新闻，创建一个文档保存在临时文件"
    
    print("执行后台任务2：", task)
    start_message = manager.run_background_task(role, task, main_memory)
    print("返回的提示信息：", start_message)
    
    role = "你是一个编程助手，请阅读coder文档"
    task = r"在D:\project\创建一个文件夹，文件夹名称为test_folder用python实现一个计算器"
    
    print("执行后台任务3：", task)
    start_message = manager.run_background_task(role, task, main_memory)
    print("返回的提示信息：", start_message)
    
    # 等待一段时间，让后台任务有时间执行
    print("\n等待后台任务执行...")
    i = 0   
    while manager.get_task_count() > 0:  # 等待所有任务完成
        i += 1
        print(f"等待中... {i}秒")   
        print(f"当前任务数量：{manager.get_task_count()}")
        await asyncio.sleep(1)
    
    # 检查主智能体记忆中是否有任务完成报告
    print("\n检查主智能体记忆...")
    messages = main_memory.get_messages()
    print(f"记忆中的消息数量：{len(messages)}")
    
    # 打印记忆中的所有消息
    for i, msg in enumerate(messages):
        print(f"\n消息 {i+1}:")
        print(f"角色: {msg.role}")
        print(f"内容: {msg.content[:200]}..." if len(msg.content) > 200 else f"内容: {msg.content}")
    
    print("\n" + "=" * 60)
    print("测试完成")

if __name__ == "__main__":
    asyncio.run(test_background_task())
