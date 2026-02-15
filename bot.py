from pydoc import doc
from re import S
import time
import asyncio
from typing import Optional, List
from ai import AIClient,Message
from prompt import BotPromt  
from config import load_config          
from tool import Tool,get_tools_definition
from memory import SharedMemory, get_shared_memory
import platform
import os
from tools.doc import Doc 
from log import Log
class Bot:
    """AI 智能体"""
    def __init__(self, shared_memory: Optional[SharedMemory] = None):
        """
        初始化 Bot
        
        Args:
            shared_memory: 共享记忆对象，如果提供则使用共享记忆，
                        否则使用独立的记忆
        """
        self.config = load_config()
        self.prompt = BotPromt()
        self.ai = AIClient(
            tools=get_tools_definition()
        )
        self.tools = Tool(shared_memory)
        self.shared_memory = shared_memory
        self.messages: List[Message] = []
        self.doc = Doc()

    def init_prompt(self):
        """初始化智能体提示"""
        prompt=self.prompt.get_prompt("Bot.txt").format(name=self.config.user.bot_name, user=self.config.user.user_name, user_set=self.config.user.bot_prompt)
        msg = Message(
            role="system",
            content=prompt
        )   
        self._add_message(msg)
        set_msg = self.init_system_prompt()
        self._add_message(set_msg)
    def init_system_prompt(self):
        """初始化系统提示"""
        # 获取当前操作系统为Windows
        if os.name == "nt":
            Os = "Windows"
        elif platform.system() == "Darwin":
            Os = "macOS"
        else:
            Os = "Linux"
        doc_list = str(self.doc.value)
        prompt=self.prompt.get_prompt("Sys.txt").format(
        stop_file=self.config.stop.file,
        time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        os = Os,
        docs=doc_list,
        roles=self.tools.role.role_dict,
        skills=self.tools.skill.skill_dict
        )
        msg = Message(
            role="system",
            content=prompt
        )   
        return msg
    async def chat(self, message: str):
        """与智能体交互"""
        set_msg = self.init_system_prompt()
        self._set_memory(set_msg,1)
        msg = Message(
            role="user",
            content=message
        )
        self.ai.log.add_log(msg)
        
        self._add_message(msg)
        
        messages = self._get_messages()
        response = self.ai.chat(messages)
        
        if response is None:
            return "抱歉，AI 生成失败，请重试。"
        
        assistant_msg = Message(
            role="assistant",
            content=response.content,
            tool_calls=response.tool_calls 
        )
        self._add_message(assistant_msg)
        
        while hasattr(response, 'tool_calls') and response.tool_calls:
            tool_messages = await self.tools.execute(response)
            if tool_messages:
                self._add_messages(tool_messages)
                messages = self._get_messages()
                response = self.ai.chat(messages)
                if response is None:
                    return "抱歉，AI 生成失败，请重试。"
            else:
                break
        
        return response.content
    
    def _add_message(self, message: Message):
        """
        添加消息到记忆
        
        Args:
            message: 要添加的消息
        """
        if self.shared_memory:
            self.shared_memory.add_message(message)
        else:
            self.messages.append(message)
    
    def _add_messages(self, messages: List[Message]):
        """
        批量添加消息到记忆
        
        Args:
            messages: 要添加的消息列表
        """
        if self.shared_memory:
            self.shared_memory.add_messages(messages)
        else:
            self.messages.extend(messages)
    
    def _get_messages(self) -> List[Message]:
        """
        获取所有消息
        
        Returns:
            List[Message]: 消息列表
        """
        if self.shared_memory:
            return self.shared_memory.get_messages()
        else:
            return self.messages
    def _set_memory(self, message: Message,index:int):
        """
        设置记忆
        
        Args:
            message: 要设置的消息
            index: 要设置的消息索引
        """
        if self.shared_memory:
            self.shared_memory.set_message(message,index)
        else:
            self.messages[index] = message
    def clear_memory(self):
        """清空记忆"""
        if self.shared_memory:
            self.shared_memory.clear()
        else:
            self.messages.clear()
    
    def get_message_count(self) -> int:
        """
        获取消息数量
        
        Returns:
            int: 消息数量
        """
        if self.shared_memory:
            return self.shared_memory.get_message_count()
        else:
            return len(self.messages)


async def test_shared_memory():
    print("=" * 60)
    print("Bot 共享记忆测试")
    print("=" * 60)
    
    print("\n【方式1：使用共享记忆】")
    print("-" * 60)
    
    shared_memory = SharedMemory()
    bot1 = Bot(shared_memory=shared_memory)
    bot2 = Bot(shared_memory=shared_memory)
    
    bot1.init_prompt()
    
    print("\nBot1 对话:")
    response1 = await bot1.chat("你好，我叫黎梓轩")
    print(f"  用户: 你好，我叫黎梓轩")
    print(f"  Bot1: {response1}")
    
    print("\nBot2 对话（应该知道黎梓轩的名字）:")
    response2 = await bot2.chat("你好，我叫什么？")
    print(f"  用户: 你好，我叫什么？")
    print(f"  Bot2: {response2}")
    
    print(f"\n当前消息数量: {bot1.get_message_count()}")
    
    print("\n" + "=" * 60)
    print("【方式2：使用全局共享记忆（单例模式）】")
    print("-" * 60)
    
    bot3 = Bot(shared_memory=get_shared_memory())
    bot4 = Bot(shared_memory=get_shared_memory())
    
    bot3.init_prompt()
    
    print("\nBot3 对话:")
    response3 = await bot3.chat("我喜欢编程，特别是 Python")
    print(f"  用户: 我喜欢编程，特别是 Python")
    print(f"  Bot3: {response3}")
    
    print("\nBot4 对话（应该知道编程偏好）:")
    response4 = await bot4.chat("我喜欢什么？")
    print(f"  用户: 我喜欢什么？")
    print(f"  Bot4: {response4}")
    
    print(f"\n当前消息数量: {bot3.get_message_count()}")
    
    print("\n" + "=" * 60)
    print("【方式3：独立记忆（不共享）】")
    print("-" * 60)
    
    bot5 = Bot()
    bot6 = Bot()
    
    bot5.init_prompt()
    bot6.init_prompt()
    
    print("\nBot5 对话:")
    response5 = await bot5.chat("我是张三")
    print(f"  用户: 我是张三")
    print(f"  Bot5: {response5}")
    
    print("\nBot6 对话（不应该知道张三的名字）:")
    response6 = await bot6.chat("我是谁？")
    print(f"  用户: 我是谁？")
    print(f"  Bot6: {response6}")
    
    print(f"\nBot5 消息数量: {bot5.get_message_count()}")
    print(f"Bot6 消息数量: {bot6.get_message_count()}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_shared_memory())
