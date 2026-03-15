"""
Bot 共享记忆使用示例
展示如何让多个 Bot 实例共享记忆
"""

from Bot import Bot
from memory import SharedMemory, get_shared_memory


def example1_shared_memory():
    """方式1：创建共享记忆对象并传递给多个 Bot"""
    print("=" * 60)
    print("方式1：使用共享记忆对象")
    print("=" * 60)
    
    shared_memory = SharedMemory()
    bot1 = Bot(shared_memory=shared_memory)
    bot2 = Bot(shared_memory=shared_memory)
    
    bot1.init_prompt()
    
    print("\nBot1 对话:")
    response1 = bot1.chat("你好，我叫黎梓轩")
    print(f"  用户: 你好，我叫黎梓轩")
    print(f"  Bot1: {response1}")
    
    print("\nBot2 对话（应该知道黎梓轩的名字）:")
    response2 = bot2.chat("你好，我叫什么？")
    print(f"  用户: 你好，我叫什么？")
    print(f"  Bot2: {response2}")
    
    print(f"\n当前消息数量: {bot1.get_message_count()}")


def example2_global_memory():
    """方式2：使用全局共享记忆（单例模式）"""
    print("\n" + "=" * 60)
    print("方式2：使用全局共享记忆（单例模式）")
    print("=" * 60)
    
    bot3 = Bot(shared_memory=get_shared_memory())
    bot4 = Bot(shared_memory=get_shared_memory())
    
    bot3.init_prompt()
    
    print("\nBot3 对话:")
    response3 = bot3.chat("我喜欢编程，特别是 Python")
    print(f"  用户: 我喜欢编程，特别是 Python")
    print(f"  Bot3: {response3}")
    
    print("\nBot4 对话（应该知道编程偏好）:")
    response4 = bot4.chat("我喜欢什么？")
    print(f"  用户: 我喜欢什么？")
    print(f"  Bot4: {response4}")
    
    print(f"\n当前消息数量: {bot3.get_message_count()}")


def example3_independent_memory():
    """方式3：独立记忆（不共享）"""
    print("\n" + "=" * 60)
    print("方式3：独立记忆（不共享）")
    print("=" * 60)
    
    bot5 = Bot()
    bot6 = Bot()
    
    bot5.init_prompt()
    bot6.init_prompt()
    
    print("\nBot5 对话:")
    response5 = bot5.chat("我是张三")
    print(f"  用户: 我是张三")
    print(f"  Bot5: {response5}")
    
    print("\nBot6 对话（不应该知道张三的名字）:")
    response6 = bot6.chat("我是谁？")
    print(f"  用户: 我是谁？")
    print(f"  Bot6: {response6}")
    
    print(f"\nBot5 消息数量: {bot5.get_message_count()}")
    print(f"Bot6 消息数量: {bot6.get_message_count()}")


if __name__ == "__main__":
    example1_shared_memory()
    example2_global_memory()
    example3_independent_memory()
    
    print("\n" + "=" * 60)
    print("所有示例完成")
    print("=" * 60)
