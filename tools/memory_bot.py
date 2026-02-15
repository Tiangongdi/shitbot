
from typing import List
from ai import Message,AIClient
from prompt import BotPromt
import json
from datetime import datetime

tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "get_memory_doc",
            "description": "获取所有内存文档的摘要信息",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_memory",
            "description": "获取指定名称的内存文档内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "memory_description": {
                        "type": "string",
                        "description": "内存文档的描述或名称"
                    }
                },
                "required": ["memory_description"]
            }
        }
    }
]
class memrry_tool:
    def __init__(self, memory_file: str = "memory.json"):
        self.memory_file = memory_file
        self.memory_doc = self.load_memory()
    def load_memory(self):
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    def execute(self, message) -> List[Message]:
        """执行技能，返回技能执行结果"""
        msg_list = []
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                if tool_name == "get_memory_doc":
                    m = json.dumps(self.memory_doc, ensure_ascii=False, indent=2)
                elif tool_name == "get_memory":
                    m = json.dumps(self.get_one_memory_doc(tool_args["memory_description"]), ensure_ascii=False, indent=2)
                else:
                    m = f"未知技能：{tool_name}"
                msg_list.append(Message(role="tool", content=m, tool_call_id=tool_call.id))
        return msg_list
    def get_one_memory_doc(self,name):
        """获取指定名称的内存文档"""
        try:
            with open(f"../memory/{name}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
class MemoryBot:
    def __init__(self, memory_file: str = "memory.json"):
        self.memory_file = memory_file
        self.memory_doc = self.load_memory()
        self.prompt = BotPromt()
        self.ai = AIClient(
            tools = tools_definition
        )
        self.memory_tool = memrry_tool()
    def load_memory(self):
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    def save_memory(self,memory:List[Message]):
        if len(memory) == 0:
            return
        old_memory = memory.copy() # 备份原始内存
        memory.extend([
            Message(role="system", content=self.prompt.get_prompt("MemoryBot.txt")),
            Message(role="user", content="Please generate a memory summary based on the above conversation records and prompt requirements.Please do not use any tools, only summarize the above history records.")
        ]) 
        response = self.ai.chat(memory)
        if response is None:
            return
        # 创建一个时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.memory_doc[timestamp]=response.content
        # 将old_memory转换为可序列化的字典格式
        serializable_memory = []
        for msg in old_memory:
            msg_dict = {
                "role": msg.role,
                "content": msg.content
            }
            if msg.tool_calls:
                tool_calls_list = []
                for tool_call in msg.tool_calls:
                    tool_call_dict = {
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }
                    tool_calls_list.append(tool_call_dict)
                msg_dict["tool_calls"] = tool_calls_list
            if msg.tool_call_id:
                msg_dict["tool_call_id"] = msg.tool_call_id
            serializable_memory.append(msg_dict)
        # 保存到./memory/{timestamp}.json
        with open(f"./memory/{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(serializable_memory, f, ensure_ascii=False, indent=4)
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory_doc, f, ensure_ascii=False, indent=4)
    def get_memory(self,q:str):
        """获取指定时间戳的内存"""
        message=[
            Message(role="system", content=self.prompt.get_prompt("MemoryBot.txt")),
            Message(role="user", content=q)
        ]
        response = self.ai.chat(message)
        if response is None:
            return None
        while hasattr(response, 'tool_calls') and response.tool_calls:
            tool_messages = self.memory_tool.execute(response)
            if tool_messages:
                message.extend(tool_messages)
                response = self.ai.chat(message)
            else:
                break
        return response.content

        
        
