import os
import json
from re import I
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from config import AIConfig, load_config
from litellm import completion
from prompt import BotPromt  
from dataclasses import asdict
from log import Log


@dataclass
class Message:
    role: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None

# 定义 AI API 的选择数据结构
@dataclass
class Choice:
    index: int
    message: Message
    finish_reason: str # 完成原因，通常是 "stop" 表示正常结束   


@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class ChatCompletion:
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage


class AIClient:
    def __init__(self, config: Optional[AIConfig] = None, tools: Optional[list] = None):
        self.config = config or load_config()
        self.model: str = self.config.ai.value + "/" + self.config.ai.model
        self.tools: Optional[list] = tools
        self.log = Log()
   
    def chat(self, res: List[Message]):
        messages_for_api = []
        for msg in res:
            message_data = {
                "role": msg.role,
                "content": msg.content
            }
            
            if msg.tool_call_id:
                message_data["tool_call_id"] = msg.tool_call_id
            
            if msg.tool_calls:
                message_data["tool_calls"] = msg.tool_calls
            
            messages_for_api.append(message_data)
        
        try:
            kwargs = {
                "model": self.model,
                "messages": messages_for_api,
                "api_key": self.config.ai.api_key,
                "temperature": 0.1
            }
            if self.tools:
                kwargs["tools"] = self.tools
            response = completion(**kwargs)
            self.log.add_log(response.choices[0].message)
            return response.choices[0].message
        except Exception as e:
            print(f"AI生成解析错误: {e}")
            print(f"请求参数: {messages_for_api}")
            return None
if __name__ == "__main__":
    prompt = BotPromt.from_config()
    ai = AIClient(prompt=prompt.get_prompt("WebAgent.txt"))
    ai.init_prompt()
    message = Message(role="user", content="你好")
    print(ai.chat(message))