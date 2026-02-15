"""
共享记忆管理器
用于在不同 Bot 实例之间共享对话记忆
"""

from typing import List
from ai import Message
from tools.memory_bot import MemoryBot


class SharedMemory:
    """
    共享记忆类
    
    管理对话历史，支持多个 Bot 实例共享同一份记忆。
    """
    
    def __init__(self):
        self.messages: List[Message] = []
        self.memory_bot = MemoryBot()
    
    def add_message(self, message: Message):
        """
        添加消息到记忆
        
        Args:
            message: 要添加的消息
        """
        self.messages.append(message)
    
    def add_messages(self, messages: List[Message]):
        """
        批量添加消息到记忆
        
        Args:
            messages: 要添加的消息列表
        """
        self.messages.extend(messages)
    def set_message(self, message: Message,index:int):
        """
        设置记忆
        
        Args:
            message: 要设置的消息
            index: 要设置的消息索引
        """
        if 0 <= index <= len(self.messages):
            self.messages[index] = message
    
    def get_messages(self) -> List[Message]:
        """
        获取所有消息
        
        Returns:
            List[Message]: 消息列表
        """
        return self.messages
    
    def clear(self):
        """清空记忆"""
        self.memory_bot.save_memory(self.messages)
        self.messages.clear()
    
    def get_message_count(self) -> int:
        """
        获取消息数量
        
        Returns:
            int: 消息数量
        """
        return len(self.messages)
    
    def get_last_n_messages(self, n: int) -> List[Message]:
        """
        获取最后 n 条消息
        
        Args:
            n: 要获取的消息数量
            
        Returns:
            List[Message]: 最后 n 条消息
        """
        return self.messages[-n:] if n > 0 else []
    


# 全局共享记忆实例
_global_memory = None


def get_shared_memory() -> SharedMemory:
    """
    获取全局共享记忆实例（单例模式）
    
    Returns:
        SharedMemory: 全局共享记忆实例
    """
    global _global_memory
    if _global_memory is None:
        _global_memory = SharedMemory()
    return _global_memory
