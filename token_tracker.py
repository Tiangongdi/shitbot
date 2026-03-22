import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class TokenTracker:
    def __init__(self, token_file_path: Optional[str] = None):
        if token_file_path is None:
            self.token_file_path = os.path.join(
                os.path.dirname(__file__), 
                ".shitbot", "datas", "token.json"
            )
        else:
            self.token_file_path = token_file_path
        
        self.current_session = TokenUsage()
        self.cumulative_data = self._load_cumulative_data()
    
    def _load_cumulative_data(self) -> Dict[str, Any]:
        if os.path.exists(self.token_file_path):
            try:
                with open(self.token_file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
            except (json.JSONDecodeError, IOError):
                pass
        
        return {
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_tokens": 0,
            "sessions": []
        }
    
    def add_usage(self, usage: Any) -> None:
        if hasattr(usage, 'prompt_tokens'):
            self.current_session.prompt_tokens += usage.prompt_tokens
            self.current_session.completion_tokens += usage.completion_tokens
            self.current_session.total_tokens += usage.total_tokens
        elif isinstance(usage, dict):
            self.current_session.prompt_tokens += usage.get('prompt_tokens', 0)
            self.current_session.completion_tokens += usage.get('completion_tokens', 0)
            self.current_session.total_tokens += usage.get('total_tokens', 0)
    
    def save_and_reset(self, session_name: Optional[str] = None) -> Dict[str, Any]:
        if self.current_session.total_tokens == 0:
            return self.cumulative_data
        
        session_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "session_name": session_name or "unnamed_session",
            "prompt_tokens": self.current_session.prompt_tokens,
            "completion_tokens": self.current_session.completion_tokens,
            "total_tokens": self.current_session.total_tokens
        }
        
        self.cumulative_data["total_prompt_tokens"] += self.current_session.prompt_tokens
        self.cumulative_data["total_completion_tokens"] += self.current_session.completion_tokens
        self.cumulative_data["total_tokens"] += self.current_session.total_tokens
        self.cumulative_data["sessions"].append(session_record)
        
        self._save_to_file()
        
        self.current_session = TokenUsage()
        
        return self.cumulative_data
    
    def _save_to_file(self) -> None:
        os.makedirs(os.path.dirname(self.token_file_path), exist_ok=True)
        
        with open(self.token_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.cumulative_data, f, ensure_ascii=False, indent=4)
    
    def get_current_session_usage(self) -> TokenUsage:
        return self.current_session
    
    def get_cumulative_usage(self) -> Dict[str, Any]:
        return self.cumulative_data
    
    def reset_current_session(self) -> None:
        self.current_session = TokenUsage()
    
    def get_session_count(self) -> int:
        return len(self.cumulative_data.get("sessions", []))
    
    def get_summary(self) -> str:
        return (
            f"当前会话: {self.current_session.total_tokens} tokens "
            f"(输入: {self.current_session.prompt_tokens}, 输出: {self.current_session.completion_tokens})\n"
            f"累计总量: {self.cumulative_data['total_tokens']} tokens "
            f"(输入: {self.cumulative_data['total_prompt_tokens']}, 输出: {self.cumulative_data['total_completion_tokens']})\n"
            f"历史会话数: {self.get_session_count()}"
        )
