"""
共享记忆管理器
用于在不同 Bot 实例之间共享对话记忆
"""

import os
import platform
import time
from typing import List
from src.ai import Message
from tools.memory_bot import MemoryBot
from src.prompt import BotPromt
from config.config import load_config
from tools.doc import Doc  



class SharedMemory:
    """
    共享记忆类
    
    管理对话历史，支持多个 Bot 实例共享同一份记忆。
    """
    
    def __init__(self):
        self.messages: List[Message] = []
        self.memory_bot = MemoryBot()
        self.prompt = BotPromt()
        self.config = load_config()
        self.doc = Doc()
        self.tools = None
    
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
    
    def set_tools(self, tools):
        """
        设置工具实例
        
        Args:
            tools: 工具实例
        """
        self.tools = tools
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
        # 判断当前对话历史只有系统提示词（即只有system角色的消息）
        if all(msg.role == "system" for msg in self.messages):
            return
        content = self.memory_bot.save_memory(self.messages)
        self.messages.clear()
        prompt=self.prompt.get_prompt("Bot.txt")
        msg = Message(
            role="system",
            content=prompt
        )   
        self.add_message(msg)
        prompt = self.prompt.get_prompt("Safe.txt")
        msg = Message(
            role="system",
            content=prompt
        )   
        self.add_message(msg)
        prompt = self.prompt.get_prompt("Self.txt")
        msg = Message(
            role="system",
            content=prompt
        )   
        self.add_message(msg)
        
        prompt = self.prompt.get_prompt("Command.txt")
        msg = Message(
            role="system",
            content=prompt
        )   
        self.add_message(msg)
        # 前面添加记忆
        self.add_message(Message(
            role="system",
            content=content
        ))

        set_msg = self.init_system_prompt()
        if set_msg:
            self.add_message(set_msg)
    def init_system_prompt(self):
        """初始化系统提示"""
        if self.tools is None:
            return None
            
        # 获取当前操作系统为Windows
        if os.name == "nt":
            Os = "Windows"
        elif platform.system() == "Darwin":
            Os = "macOS"
        else:
            Os = "Linux"
        doc_list = str(self.doc.value)
        skill_list = str(self.tools.skill.skill_dict)
        role_list = str(self.tools.role.role_dict)
        prompt=self.prompt.get_prompt("Sys.txt").format(
        stop_file=self.config.stop.file,
        time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        os = Os,
        docs=doc_list,
        skills=skill_list,
        roles=role_list
        )
        msg = Message(
            role="system",
            content=prompt
        )   
        return msg
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
