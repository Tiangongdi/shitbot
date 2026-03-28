# AI Agent Skills Module
import asyncio
import json
import os
from dataclasses import dataclass
from tools.doc import Doc
from statistics import quantiles
from typing import Optional, Dict, Any
from tools.memory_bot import MemoryBot
from tools.playwiright import WebBot
from tools.bocha import BochaSearch
from tools.timer import Timer
from tools.venv_manager import VenvManager
from tools.safe import safe_format
from tools.role import Role
from tools.skill import Skill
from tools.tavily_api import TavilySearch
from ai import Message
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style as PromptStyle
from prompt_toolkit.formatted_text import FormattedText
from ui_components import TerminalUI
class Tool:
    """工具基类"""
    def __init__(self, shared_memory: Dict[str, Any]):
        self.config = self._load_config()
        self.bocha_config = self.config.bocha
        self.stop_file = self.config.stop.file  
        self.bocha_client = BochaSearch(api_key=self.bocha_config.api_key)
        self.web_bot = WebBot() 
        self.timer = Timer()
        self.session = PromptSession()
        self.terminal_ui = TerminalUI()
        self.shared_memory = shared_memory
        self.memory_bot = MemoryBot()
        self.tools = {}
        self.venv_manager = VenvManager()
        self.role = Role()
        self.skill = Skill()
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.tavily_client = TavilySearch()
        self.doc = Doc()
    def _load_config(self):
        """加载配置"""
        from config import load_config
        return load_config()
    async def execute(self, message) -> str:
        """执行技能，返回技能执行结果"""
        msg_list = []
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                if tool_name == "search_web":
                    self.terminal_ui.tool(f"搜索网页：{tool_args['query']}")
                    m = await self._search_web(tool_args)
                elif tool_name == "browse_page":
                    self.terminal_ui.tool(f"浏览网页：{tool_args['url']}")
                    m = await self._browse_page(tool_args) 
                elif tool_name == "read_file":
                    self.terminal_ui.tool(f"读取文件：{tool_args['file_path']}")
                    m = self.read_file_content(tool_args)   
                elif tool_name == "write_file":
                    self.terminal_ui.tool(f"写入文件：{tool_args['file_path']}")
                    m = self.write_file_content(tool_args)   
                elif tool_name == "shell_command":
                    self.terminal_ui.tool(f"执行shell命令：{tool_args['command']}")
                    m = self.shell_command(tool_args)
                elif tool_name == "copy_file":
                    source_path = tool_args.get("source_path", "")
                    dest_path = tool_args.get("dest_path", "") 
                    self.terminal_ui.tool(f"复制文件：{source_path} -> {dest_path}")
                    m = self.copy_file(tool_args)
                elif tool_name == "move_file":
                    self.terminal_ui.tool(f"移动文件：{tool_args['source_path']} -> {tool_args['dest_path']}")
                    m = self.move_file(tool_args)
                elif tool_name == "create_dir":
                    self.terminal_ui.tool(f"创建目录：{tool_args['dir_path']}")
                    m = self.create_dir(tool_args)
                elif tool_name == "delete_file":
                    self.terminal_ui.tool(f"删除文件：{tool_args['file_path']}")
                    m = await self.delete_file(tool_args) 
                elif tool_name == "get_dir_content":
                    self.terminal_ui.tool(f"获取目录内容：{tool_args['dir_path']}")
                    m = self.get_dir_content(tool_args)
                elif tool_name == "send_email":
                    self.terminal_ui.tool(f"发送邮件：{tool_args['to']}，主题：{tool_args['subject']}")
                    m = self.send_email(tool_args)
                elif tool_name == "once_after":
                    self.terminal_ui.tool(f"设置延迟执行")
                    m = self.once_after(tool_args)  
                elif tool_name == "interval":
                    self.terminal_ui.tool(f"设置间隔执行")
                    m = self.interval(tool_args)
                elif tool_name == "daily_at":
                    self.terminal_ui.tool(f"设置每天执行")
                    m = self.daily_at(tool_args)
                elif tool_name == "cancel_timer":
                    self.terminal_ui.tool(f"取消定时器：{tool_args['timer_id']}")
                    m = self.cancel(tool_args)
                elif tool_name == "pause_timer":
                    self.terminal_ui.tool(f"暂停定时器：{tool_args['timer_id']}")
                    m = self.pause(tool_args)
                elif tool_name == "resume_timer":
                    self.terminal_ui.tool(f"恢复定时器：{tool_args['timer_id']}")
                    m = self.resume(tool_args)
                elif tool_name == "list":
                    self.terminal_ui.tool(f"列出所有定时器")
                    m = self.list(tool_args)    
                elif tool_name == "input_y_or_n":
                    m = await self.input_y_or_n(tool_args)
                elif tool_name == "input":
                    m = await self.input(tool_args)
                elif tool_name == "save_memory":
                    m = self.save_memory(tool_args)
                    self.terminal_ui.tool(f"保存记忆")
                elif tool_name == "get_memory":
                    m = self.get_memory(tool_args)
                    self.terminal_ui.tool(f"获取记忆")
                elif tool_name == "get_doc_list":
                    self.terminal_ui.tool(f"获取文档列表")
                    m = str(self.doc.value)
                elif tool_name == "get_doc":
                    file_name = tool_args.get("file_name", "")
                    key = tool_args.get("key", "")
                    self.terminal_ui.tool(f"获取文档：{file_name}，键：{key}")
                    m = self.doc.get_data(file_name,key)
                elif tool_name == "get_role":
                    self.terminal_ui.tool(f"获取角色")
                    m = self.role.role_dict
                elif tool_name == "get_skill":
                    self.terminal_ui.tool(f"获取技能")
                    m = self.skill.skill_dict   
                elif tool_name == "run_code":
                    self.terminal_ui.tool(f"运行代码")
                    m = self.run_code(tool_args)
                else:
                    m = f"未知技能：{tool_name}"
                msg_list.append(Message(role="tool", content=m, tool_call_id=tool_call.id))
        return msg_list 
    
    async def _search_web(self, args: Dict[str, Any]) -> str:
        """网络搜索"""
        query = args.get("query", "")
        count = args.get("count", 5)
        if self.config.web_search.web_search_ID == "1":
            response = await self.bocha_client.search(query, count=count)
            if response.success:
                return self.bocha_client.format_results(response)
            else:
                return f"✗ 搜索失败: {response.error}"
        else:
            return self.tavily_client.search(query, max_results=count)
    
    async def _browse_page(self, args: Dict[str, Any]) -> str:
        """打开指定的网页"""
        url = args.get("url", "")
        query = args.get("query", "")
        response = await self.web_bot.extract(url, query)
        return response
    def read_file_content(self, args: Dict[str, Any]) -> str:
        """获取文件内容"""
        file_path = args.get("file_path", "")
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"       
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"读取文件时出错: {str(e)}"
    def write_file_content(self, args: Dict[str, Any]) -> str:
        """写入文件内容"""
        file_path = args.get("file_path", "")
        content = args.get("content", "")
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"   
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"成功写入文件: {file_path}"
        except Exception as e:
            return f"写入文件时出错: {str(e)}"
    def copy_file(self, args: Dict[str, Any]) -> str:
        """复制文件"""
        source_path = args.get("source_path", "")
        dest_path = args.get("dest_path", "")
        if source_path in self.stop_file or dest_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"   
        try:
            import shutil
            shutil.copy(source_path, dest_path)
            return f"成功复制文件: {source_path} -> {dest_path}"
        except Exception as e:
            return f"复制文件时出错: {str(e)}"
    def move_file(self, args: Dict[str, Any]) -> str:
        """移动文件"""
        source_path = args.get("source_path", "")
        dest_path = args.get("dest_path", "")
        if source_path in self.stop_file or dest_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"   
        try:
            import shutil
            shutil.move(source_path, dest_path)
            return f"成功移动文件: {source_path} -> {dest_path}"
        except Exception as e:
            return f"移动文件时出错: {str(e)}"
    def create_dir(self, args: Dict[str, Any]) -> str:
        """创建目录"""
        dir_path = args.get("dir_path", "")
        if dir_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"   
        try:
            import os
            os.makedirs(dir_path, exist_ok=True)
            return f"成功创建目录: {dir_path}"
        except Exception as e:
            return f"创建目录时出错: {str(e)}"  
    def get_dir_content(self, args: Dict[str, Any]) -> str:
        """获取目录内容"""
        dir_path = args.get("dir_path", "")
        if dir_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"   
        try:
            import os
            content = os.listdir(dir_path)
            return f"目录内容: {content}"
        except Exception as e:
            return f"获取目录内容时出错: {str(e)}"
    async def delete_file(self, args: Dict[str, Any]) -> str:
        """删除文件"""
        file_path = args.get("file_path", "")
        
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"   
        user_input = await self.session.prompt_async(
                   FormattedText([("class:user", f"确认删除文件 {file_path}？[y/n]")]),
                    style=PromptStyle.from_dict({
                        "user": "ansired bold",
                    })
                ) 
        if user_input.lower() in ["n","N"]:
            return user_input
        try:
            import os
            os.remove(file_path)
            return f"成功删除文件: {file_path}"
        except Exception as e:
            return f"删除文件时出错: {str(e)}"
    def shell_command(self, args: Dict[str, Any]) -> str:
        """执行 shell 命令"""
        command = args.get("command", "")
        try:
            import subprocess
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"命令执行失败: {e.stderr}"
    
    def send_email(self, args: Dict[str, Any]) -> str:
        """发送邮件"""
        to_email = args.get("to_email", "")
        subject = args.get("subject", "")
        body = args.get("body", "")
        from_email = self.config.email.email
        password = self.config.email.password
        smtp_server = self.config.email.smtp_server
        smtp_port = self.config.email.smtp_port
        use_tls = self.config.email.use_tls 
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            if smtp_port == 465:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            else:
                server = smtplib.SMTP(smtp_server, smtp_port)
                if use_tls:
                    server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            
            return f"✓ 邮件发送成功\n收件人: {to_email}\n主题: {subject}"
        except Exception as e:
            return f"✗ 邮件发送失败: {str(e)}"
    def once_after(self, args: Dict[str, Any]) -> str:
        """
        定时任务：在指定时间后执行一次
        Args:
            args: 包含时间和任务描述的字典
        Returns:
            str: 执行结果
        """
        delay_seconds = args.get("time", 0)
        task = args.get("task", "")
        self.timer.once_after(message=task, delay_seconds=delay_seconds)
        return f"定时任务已添加：{delay_seconds} 后执行 {task}"
    def interval(self, args: Dict[str, Any]) -> str:
        """
        定时任务：周期性执行
        Args:
            args: 包含时间间隔、触发次数和任务描述的字典
        Returns:
            str: 执行结果
        """
        interval_seconds = args.get("interval_seconds", 0)
        interval_count = args.get("interval_count", -1)
        task = args.get("task", "")
        self.timer.interval(message=task, interval_seconds=interval_seconds, interval_count=interval_count)
        if interval_count == -1:
            return f"定时任务已添加：每 {interval_seconds} 秒执行 {task} 无限次"
        else:
            return f"定时任务已添加：每 {interval_seconds} 秒执行 {task} {interval_count} 次"
    def daily_at(self, args: Dict[str, Any]) -> str:
        """
        定时任务：每天在指定时间执行
        Args:
            args: 包含时间和任务描述的字典
        Returns:
            str: 执行结果
        """
        hour = args.get("hour", 0)
        task = args.get("task", "")
        minute = args.get("minute", 0)
        self.timer.daily_at(message=task, hour=hour, minute=minute)
        return f"定时任务已添加：每天 {hour}:{minute} 执行 {task}"
    def cancel(self, args: Dict[str, Any]) -> str:
        """
        取消定时任务
        Args:
            args: 包含任务ID的字典
        Returns:
            str: 执行结果
        """
        task_id = args.get("task_id", "")
        self.timer.cancel(task_id)
        return f"定时任务已取消：{task_id}"
    def pause(self, args: Dict[str, Any]) -> str:
        """
        暂停定时任务
        Args:
            args: 包含任务ID的字典
        Returns:
            str: 执行结果
        """
        task_id = args.get("task_id", "")
        self.timer.pause(task_id)
        return f"定时任务已暂停：{task_id}"
    def resume(self, args: Dict[str, Any]) -> str:
        """
        恢复定时任务
        Args:
            args: 包含任务ID的字典
        Returns:
            str: 执行结果
        """
        task_id = args.get("task_id", "")
        self.timer.resume(task_id)
        return f"定时任务已恢复：{task_id}" 
    def list(self, args: Dict[str, Any]) -> str:
        """
        列出所有定时任务
        Args:
            args: 空字典
        Returns:
            str: 执行结果
        """
        tasks = self.timer.get_tasks()
        return f"当前定时任务列表：{tasks}"
    async def input(self, args: Dict[str, Any]) -> str:
        """
        输入提示
        Args:
            args: 包含提示信息的字典
        Returns:
            str: 用户输入
        """
        prompt = args.get("prompt", "")
        user_input = await self.session.prompt_async(
                   FormattedText([("class:user", prompt+" > ")]),
                    style=PromptStyle.from_dict({
                        "user": "ansired bold",
                    })
                ) 
        return user_input
    async def input_y_or_n(self, args: Dict[str, Any]) -> str:
        """
        输入提示
        Args:
            args: 包含提示信息的字典
        Returns:
            str: 用户输入
        """
        prompt = args.get("prompt", "")
        user_input = await self.session.prompt_async(
                   FormattedText([("class:user", prompt+"[y/n]")]),
                    style=PromptStyle.from_dict({
                        "user": "ansired bold",
                    })
                ) 
        if user_input.lower() not in ["y", "n", "", " ","Y","N"]:
            return user_input
        elif user_input.lower() in ["N", "n"]:
            return "用户拒绝，请不要执行这一操作"
        else:
            return "用户同意"
    def get_tools(self) -> str:
        """
        获取工具信息
        
        Args:
            name: 工具名
        Returns:
            dict: 工具信息
        """
        list = [
            {
                "name": name,
                "purpose": tool["purpose"]
            }
            for name, tool in self.tools.items()
        ]
        return str(list)
    def run_code(self, args: Dict[str, Any]) -> str:
        """
        运行代码
        Args:
            args: 包含代码的字典
        Returns:
            str: 执行结果
        """
        code = args.get("code", "")
        try:
            returncode,stdout,stderr = self.venv_manager.run_python(code)
            return f"代码执行结果: 返回码{returncode}, 输出: {stdout}, 错误: {stderr}"
        except Exception as e:
            return f"代码执行失败：{e}"
    def save_memory(self, args: Dict[str, Any]):
        """
        保存记忆
        Args:
            memory: 记忆内容
        Returns:
            None
        """
        self.shared_memory.clear()
    def get_memory(self, args: Dict[str, Any]) -> str:
        """
        获取记忆
        Args:
            args: 空字典
        Returns:
            str: 记忆内容
        """
        memory_description = args.get("memory_description", "")
        r = self.memory_bot.get_memory(memory_description)
        return r
        
def get_tools_definition() -> list:
    """获取技能定义列表，用于 AI 调用"""
    return [
        {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "在网络上搜索信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索查询词"
                        },
                        "count": {
                            "type": "integer",
                            "description": "返回结果数量",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "browse_page",
                "description": "打开指定的网页",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "要访问的网页 URL"
                        },
                        "query": {
                            "type": "string",
                            "description": "告诉网站提取总结助手要在这个网站里面提取和总结的内容"
                        }
                    },
                    "required": ["url", "query"]                                   
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "给指定文件写入内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "要写入的文件路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "要写入的内容"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "读取指定文件内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "要读取的文件路径"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "copy_file",
                "description": "复制指定文件,到目标路径",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source_path": {
                            "type": "string",
                            "description": "要复制的文件路径"
                        },
                        "dest_path": {
                            "type": "string",
                            "description": "要复制到的目标路径"
                        }
                    },
                    "required": ["source_path", "dest_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "move_file",
                "description": "移动指定文件,到目标路径",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source_path": {
                            "type": "string",
                            "description": "要移动的文件路径"
                        },
                        "dest_path": {
                            "type": "string",
                            "description": "要移动到的目标路径"
                        }
                    },
                    "required": ["source_path", "dest_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_dir",
                "description": "创建目录",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dir_path": {
                            "type": "string",
                            "description": "要创建的目录路径"
                        }
                    },
                    "required": ["dir_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_dir_content",
                "description": "获取目录内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dir_path": {
                            "type": "string",
                            "description": "要获取内容的目录路径"
                        }
                    },
                    "required": ["dir_path"]
                }
            }
        },  
        {
            "type": "function",
            "function": {
                "name": "delete_file",
                "description": "删除文件",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "要删除的文件路径"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        },  
        {
            "type": "function",
            "function": {
                "name": "shell_command",
                "description": "执行 shell 命令",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "要执行的 shell 命令"
                        }
                    },
                    "required": ["command"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "发送邮件到指定邮箱",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to_email": {
                            "type": "string",
                            "description": "收件人邮箱地址"
                        },
                        "subject": {
                            "type": "string",
                            "description": "邮件主题"
                        },
                        "body": {
                            "type": "string",
                            "description": "邮件正文内容"
                        }
                    },
                    "required": ["to_email", "subject", "body"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "once_after",
                "description": "定时任务：在指定时间后执行一次",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "time": {
                            "type": "integer",
                            "description": "延迟时间（秒）"
                        },
                        "task": {
                            "type": "string",
                            "description": "任务描述"
                        }
                    },
                    "required": ["time", "task"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "interval",
                "description": "定时任务：周期性执行",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "interval_seconds": {
                            "type": "integer",
                            "description": "时间间隔（秒）"
                        },
                        "interval_count": {
                            "type": "integer",
                            "description": "触发次数，-1 表示无限次"
                        },
                        "task": {
                            "type": "string",
                            "description": "任务描述"
                        }
                    },
                    "required": ["interval_seconds", "interval_count", "task"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "daily_at",
                "description": "定时任务：每天在指定时间执行",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "hour": {
                            "type": "integer",
                            "description": "小时（0-23）"
                        },
                        "minute": {
                            "type": "integer",
                            "description": "分钟（0-59）"
                        },
                        "task": {
                            "type": "string",
                            "description": "任务描述"
                        }
                    },
                    "required": ["hour", "task"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "cancel",
                "description": "取消定时任务",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "任务ID"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "pause",
                "description": "暂停定时任务",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "任务ID"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "resume",
                "description": "恢复定时任务",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "任务ID"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list",
                "description": "列出所有定时任务",
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
                "name": "input_y_or_n",
                "description": "用户输入确认",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "向用户提出确认提示，如：你喜欢吃披萨吗？"
                        }
                    },
                    "required": ["prompt"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "input",
                "description": "用户输入",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "向用户提出输入提示"
                        }
                    },
                    "required": ["prompt"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "save_memory",
                "description": "保存当前对话记忆",
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
                "description": "让memory_bot在以前的对话记录总结信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "memory_description": {
                            "type": "string",
                            "description": "让memory_bot的总结信息"
                        }
                    },
                    "required": ["memory_description"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_doc_list",
                "description": "列出所有可以阅读的doc文档",
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
                "name": "get_doc",
                "description": "获取doc文档内容,建议先调用get_doc_list获取文档列表",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "文档名称"
                        },
                        "key": {
                            "type": "string",
                            "description": "文档键"
                        }
                    },
                    "required": ["file_name", "key"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "run_code",
                "description": "运行python代码",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {   
                            "type": "string",
                            "description": "python代码"
                        },
                    },
                    "required": ["code"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_role",
                "description": "列出所有可以阅读的角色",
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
                "name": "get_doc_list",
                "description": "列出所有可以阅读的技能文档",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },

    ]
