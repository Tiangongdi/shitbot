# AI Agent Skills Module
import asyncio
import json
import os
from dataclasses import dataclass
from tools.doc import Doc
from statistics import quantiles
from typing import Optional, Dict, Any
from tools.memory_bot import MemoryBot
from tools.webbot import WebBot
from tools.bocha import BochaSearch
from tools.timer import get_timer
from tools.venv_manager import VenvManager
from tools.safe import safe_format
from tools.role import Role
from tools.skill import Skill
from tools.tavily_api import TavilySearch
from tools.email_reader import EmailReader
from ai import Message
from ui_components import TerminalUI
class Tool:
    """工具基类"""
    def __init__(self, shared_memory: Dict[str, Any]):
        self.config = self._load_config()
        self.bocha_config = self.config.bocha
        self.stop_file = self.config.stop.file  
        self.bocha_client = BochaSearch(api_key=self.bocha_config.api_key)
        self.web_bot = WebBot() 
        self.timer = get_timer()
        self.terminal_ui = None  # 暂时设为 None，稍后从外部设置
        self.shared_memory = shared_memory
        self.memory_bot = MemoryBot()
        self.tools = {}
        self.venv_manager = VenvManager()
        self.role = Role()
        self.skill = Skill()
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.tavily_client = TavilySearch()
        self.doc = Doc()

        # 初始化邮件读取器
        self.email_reader = None
        self._init_email_reader()
    
    def _init_email_reader(self):
        """初始化邮件读取器"""
        try:
            imap_config = self.config.imap
            if imap_config.email and imap_config.password:
                self.email_reader = EmailReader(
                    email_address=imap_config.email,
                    password=imap_config.password,
                    imap_server=imap_config.imap_server,
                    imap_port=imap_config.imap_port
                )
        except Exception as e:
            pass
    
    def set_terminal_ui(self, terminal_ui):
        """
        设置终端 UI 实例
        
        Args:
            terminal_ui: TerminalUI 实例
        """
        self.terminal_ui = terminal_ui
    def _load_config(self):
        """加载配置"""
        from config import load_config
        return load_config()
    async def execute(self, message,if_user: bool = True) :
        """执行技能，返回技能执行结果"""
        msg_list = []
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name.strip()  # 去除函数名前后的空格
                arguments = tool_call.function.arguments
                
                # 尝试清理可能包含 XML 标签的 arguments
                if '</arg_key>' in arguments or '</arg_value>' in arguments or '</tool_call>' in arguments:
                    import re
                    # 提取 query 字段的内容
                    query_match = re.search(r'<arg_value>(.*?)</arg_value>', arguments, re.DOTALL)
                    if query_match:
                        query_value = query_match.group(1)
                        arguments = f'{{"query": "{query_value}"}}'
                
                try:
                    tool_args = json.loads(arguments)
                except json.JSONDecodeError as e:
                    error_msg = f"JSON解析错误: {e}, arguments: {arguments}"
                    self.terminal_ui.error(error_msg)
                    msg_list.append(Message(role="tool", content=error_msg, tool_call_id=tool_call.id))
                    continue
                if tool_name == "search_web":
                    m = await self._search_web(tool_args)
                elif tool_name == "webbot_task":
                    m = await self.webbot_task(tool_args)
                elif tool_name == "read_file":
                    m = self.read_file_content(tool_args)   
                elif tool_name == "write_file":
                    m = self.write_file_content(tool_args)   
                elif tool_name == "shell_command":
                    m = self.shell_command(tool_args)
                elif tool_name == "copy_file":
                    m = self.copy_file(tool_args)
                elif tool_name == "move_file":
                    m = self.move_file(tool_args)
                elif tool_name == "create_dir":
                    m = self.create_dir(tool_args)
                elif tool_name == "get_dir_content":
                    m = self.get_dir_content(tool_args)
                elif tool_name == "send_email":
                    m = self.send_email(tool_args)
                elif tool_name == "once_after":
                    m = self.once_after(tool_args)  
                elif tool_name == "interval":
                    m = self.interval(tool_args)
                elif tool_name == "daily_at":
                    m = self.daily_at(tool_args)
                elif tool_name == "cancel_timer":
                    m = self.cancel(tool_args)
                elif tool_name == "pause_timer":
                    m = self.pause(tool_args)
                elif tool_name == "resume_timer":
                    m = self.resume(tool_args)
                elif tool_name == "list":
                    m = self.list(tool_args)    
                elif tool_name == "delete_file":
                    m = await self.delete_file(tool_args, if_user)
                elif tool_name == "get_memory":
                    m = self.get_memory(tool_args)
                elif tool_name == "get_doc_list":
                    m = str(self.doc.value)
                elif tool_name == "get_doc":
                    file_name = tool_args.get("file_name", "")
                    key = tool_args.get("key", "")
                    m = self.doc.get_data(file_name,key)
                elif tool_name == "get_role":
                    m = str(self.role.role_dict)
                elif tool_name == "get_skill":
                    m = str(self.skill.skill_dict)   
                elif tool_name == "run_code":
                    m = self.run_code(tool_args)
                elif tool_name == "run_code_file":
                    m = self.run_code_file(tool_args)
                elif tool_name == "append_to_file":
                    m = self.append_to_file(tool_args)
                elif tool_name == "list_email_folders":
                    m = self.list_email_folders(tool_args)
                elif tool_name == "get_email_list":
                    m = self.get_email_list(tool_args)
                elif tool_name == "get_email_content":
                    m = self.get_email_content(tool_args)
                elif tool_name == "search_emails":
                    m = self.search_emails(tool_args)
                elif tool_name == "mark_email_read":
                    m = self.mark_email_read(tool_args)

                else:
                    m = f"未知技能：{tool_name}"
                # 创建Message对象并添加到msg_list
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
        response = await self.web_bot.extract({"url": url})
        return response
    async def webbot_task(self, args: Dict[str, Any]) -> str:
        """打开指定的网页"""
        query = args.get("query", "")
        response = await self.web_bot.execute_task(query)
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
        import os
        if not os.path.exists(source_path):
            return f"源文件不存在: {source_path}"
        if not os.path.exists(dest_path):
            return f"目标文件不存在: {dest_path}"
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
            if os.path.exists(dir_path):
                return f"目录已存在: {dir_path}，请不要重复使用这个工具重复创建相同的文件夹"
            os.makedirs(dir_path, exist_ok=True)
            return f"成功创建目录: {dir_path},请不要重复使用这个工具重复创建相同的文件夹"
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
    async def delete_file(self, args: Dict[str, Any],if_user: bool) -> str:
        """删除文件"""
        file_path = args.get("file_path", "")
        
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"   
        if not if_user:
            return "为计时器操作，已拒绝,请记录到ERROR日志"
        
        try:
            import os
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return f"文件不存在: {file_path}"
            
            # 检查是否为文件
            if not os.path.isfile(file_path):
                return f"{file_path} 不是一个文件"
            
            os.remove(file_path)
            return f"成功删除文件: {file_path}"
        except Exception as e:
            return f"删除文件时出错: {str(e)}"
    def shell_command(self, args: Dict[str, Any]) -> str:
        """执行 shell 命令"""
        command = args.get("command", "")
        use_timeout = args.get("use_timeout", True)
        try:
            import subprocess
            timeout_seconds = 60 if use_timeout else None
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True, encoding='utf-8', errors='replace', timeout=timeout_seconds)
            return result.stdout
        except subprocess.TimeoutExpired as e:
            output = (e.stdout or "") + (e.stderr or "")
            return f"命令执行超时（超过60秒），已终止命令。\n当前输出:\n{output}"
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
        self.timer.once_after(description=task, delay_seconds=delay_seconds)
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
        self.timer.interval_every(description=task, interval_seconds=interval_seconds, interval_count=interval_count)
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
        self.timer.daily_at(description=task, hour=hour, minute=minute)
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
    def run_code_file(self, args: Dict[str, Any]) -> str:
        """
        运行代码文件
        Args:
            args: 包含代码文件路径的字典
        Returns:
            str: 执行结果
        """
        code_file = args.get("code_file", "")
        try:
            if not code_file.endswith(".py"):
                return "代码文件必须是 .py 格式"
            if not os.path.exists(code_file):
                return "代码文件不存在"
            with open(code_file, "r", encoding="utf-8") as f:
                code = f.read()
            returncode,stdout,stderr = self.venv_manager.run_python(code)
            return f"代码执行结果: 返回码{returncode}, 输出: {stdout}, 错误: {stderr}"
        except Exception as e:
            return f"代码执行失败：{e}"
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


    def _ensure_email_connection(self) -> str:
        """确保邮件读取器已连接到服务器"""
        if not self.email_reader:
            return "邮件读取器未初始化，请检查IMAP配置"
        
        if not self.email_reader.connection:
            result = self.email_reader.connect()
            if not result.get("success"):
                return f"连接邮件服务器失败: {result.get('error')}"
        
        return None  # 连接成功，返回None表示无错误

    def list_email_folders(self, args: Dict[str, Any]) -> str:
        """
        列出邮箱文件夹
        
        Args:
            args: 空字典
            
        Returns:
            str: 文件夹列表
        """
        error = self._ensure_email_connection()
        if error:
            return error
        
        try:
            result = self.email_reader.list_folders()
            if result.get("success"):
                folders = result.get("folders", [])
                return f"邮箱文件夹列表：\n" + "\n".join([f"  - {f}" for f in folders])
            else:
                return f"获取文件夹列表失败: {result.get('error')}"
        except Exception as e:
            return f"操作失败: {str(e)}"
    
    def get_email_list(self, args: Dict[str, Any]) -> str:
        """
        获取邮件列表
        
        Args:
            args: 包含folder和limit的字典
            
        Returns:
            str: 邮件列表
        """
        error = self._ensure_email_connection()
        if error:
            return error
        
        folder = args.get("folder", "INBOX")
        limit = args.get("limit", 10)
        unread_only = args.get("unread_only", False)
        
        try:
            result = self.email_reader.get_email_list(
                folder=folder, 
                limit=limit, 
                unread_only=unread_only
            )
            
            if result.get("success"):
                emails = result.get("emails", [])
                if not emails:
                    return f"文件夹 {folder} 中没有邮件"
                
                output = [f"文件夹 {folder} 中的邮件（共{result['total']}封）：\n"]
                for i, email in enumerate(emails, 1):
                    output.append(f"{i}. 主题: {email['subject']}")
                    output.append(f"   发件人: {email['from']}")
                    output.append(f"   日期: {email['date']}")
                    output.append(f"   ID: {email['id']}")
                    if email.get('has_attachment'):
                        output.append("   [有附件]")
                    output.append("")
                
                return "\n".join(output)
            else:
                return f"获取邮件列表失败: {result.get('error')}"
        except Exception as e:
            return f"操作失败: {str(e)}"
    
    def get_email_content(self, args: Dict[str, Any]) -> str:
        """
        获取邮件内容
        
        Args:
            args: 包含email_id和folder的字典
            
        Returns:
            str: 邮件内容
        """
        error = self._ensure_email_connection()
        if error:
            return error
        
        email_id = args.get("email_id", "")
        folder = args.get("folder", "INBOX")
        
        if not email_id:
            return "请提供邮件ID"
        
        try:
            result = self.email_reader.get_email_content(email_id=email_id, folder=folder)
            
            if result.get("success"):
                email = result['email']
                output = [
                    "=" * 60,
                    f"主题: {email['subject']}",
                    f"发件人: {email['from']}",
                    f"收件人: {email['to']}",
                ]
                
                if email.get('cc'):
                    output.append(f"抄送: {email['cc']}")
                
                output.append(f"日期: {email['date']}")
                output.append("=" * 60)
                output.append("\n正文内容：")
                output.append("-" * 60)
                output.append(email['body'][:1000])  # 限制显示1000字符
                
                if len(email['body']) > 1000:
                    output.append(f"\n... (还有 {len(email['body']) - 1000} 字符)")
                
                if email.get('attachments'):
                    output.append("\n附件：")
                    for att in email['attachments']:
                        output.append(f"  - {att['filename']} ({att['size']} bytes)")
                
                return "\n".join(output)
            else:
                return f"获取邮件内容失败: {result.get('error')}"
        except Exception as e:
            return f"操作失败: {str(e)}"
    
    def search_emails(self, args: Dict[str, Any]) -> str:
        """
        搜索邮件
        
        Args:
            args: 包含criteria、folder和limit的字典
            
        Returns:
            str: 搜索结果
        """
        error = self._ensure_email_connection()
        if error:
            return error
        
        criteria = args.get("criteria", "")
        folder = args.get("folder", "INBOX")
        limit = args.get("limit", 10)
        
        if not criteria:
            return "请提供搜索关键词"
        
        try:
            result = self.email_reader.search_emails(
                criteria=criteria, 
                folder=folder, 
                limit=limit
            )
            
            if result.get("success"):
                emails = result.get("emails", [])
                if not emails:
                    return f"没有找到包含 '{criteria}' 的邮件"
                
                output = [f"搜索 '{criteria}' 的结果（共{result['total']}封）：\n"]
                for i, email in enumerate(emails, 1):
                    output.append(f"{i}. 主题: {email['subject']}")
                    output.append(f"   发件人: {email['from']}")
                    output.append(f"   日期: {email['date']}")
                    output.append(f"   ID: {email['id']}")
                    output.append("")
                
                return "\n".join(output)
            else:
                return f"搜索失败: {result.get('error')}"
        except Exception as e:
            return f"操作失败: {str(e)}"
    
    def mark_email_read(self, args: Dict[str, Any]) -> str:
        """
        标记邮件为已读
        
        Args:
            args: 包含email_id和folder的字典
            
        Returns:
            str: 操作结果
        """
        error = self._ensure_email_connection()
        if error:
            return error
        
        email_id = args.get("email_id", "")
        folder = args.get("folder", "INBOX")
        
        if not email_id:
            return "请提供邮件ID"
        
        try:
            result = self.email_reader.mark_as_read(email_id=email_id, folder=folder)
            
            if result.get("success"):
                return f"邮件 {email_id} 已标记为已读"
            else:
                return f"标记失败: {result.get('error')}"
        except Exception as e:
            return f"操作失败: {str(e)}"
    def append_to_file(self, args: Dict[str, Any]) -> str:
        """
        在文件末尾追加文本
        Args:
            args: 包含文件路径和要追加内容的字典
        Returns:
            str: 执行结果
        """
        file_path = args.get("file_path", "")
        content = args.get("content", "")
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content)
            return f"成功追加内容到文件: {file_path}"
        except Exception as e:
            return f"追加内容时出错: {str(e)}"
        
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
                "name": "webbot_task",
                "description": "让WebBot执行任务,WebBot是一个浏览器操作助手,它可以查看网页信息,点击网页,填写表单等浏览器修改功能",    
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "告诉WebBot要执行的任务"
                        }
                    },
                    "required": ["query"]                                   
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
                        },
                        "use_timeout": {
                            "type": "boolean",
                            "description": "是否启用超时限制，默认为true。启用后命令执行超过60秒将自动终止并返回当前输出，防止命令长时间等待用户输入",
                            "default": True
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
                "name": "cancel_timer",
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
                "name": "pause_timer",
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
                "name": "resume_timer",
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
                "name": "run_code_file",
                "description": "运行python代码文件",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code_file": {
                            "type": "string",
                            "description": "python代码文件路径"
                        },
                    },
                    "required": ["code_file"]
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
                "name": "get_skill",
                "description": "列出所有可以阅读的技能文档",
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
                "name": "list_email_folders",
                "description": "列出邮箱中的所有文件夹",
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
                "name": "get_email_list",
                "description": "获取邮箱中的邮件列表",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "folder": {
                            "type": "string",
                            "description": "文件夹名称，默认为INBOX",
                            "default": "INBOX"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "返回邮件数量，默认10",
                            "default": 10
                        },
                        "unread_only": {
                            "type": "boolean",
                            "description": "是否只获取未读邮件，默认False",
                            "default": False
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_email_content",
                "description": "获取指定邮件的详细内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email_id": {
                            "type": "string",
                            "description": "邮件ID"
                        },
                        "folder": {
                            "type": "string",
                            "description": "文件夹名称，默认为INBOX",
                            "default": "INBOX"
                        }
                    },
                    "required": ["email_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_emails",
                "description": "搜索邮件（按主题、发件人、正文搜索）",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "criteria": {
                            "type": "string",
                            "description": "搜索关键词"
                        },
                        "folder": {
                            "type": "string",
                            "description": "文件夹名称，默认为INBOX",
                            "default": "INBOX"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "返回邮件数量，默认10",
                            "default": 10
                        }
                    },
                    "required": ["criteria"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "mark_email_read",
                "description": "标记邮件为已读",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email_id": {
                            "type": "string",
                            "description": "邮件ID"
                        },
                        "folder": {
                            "type": "string",
                            "description": "文件夹名称，默认为INBOX",
                            "default": "INBOX"
                        }
                    },
                    "required": ["email_id"]
                }
            }
        },
        {
             "type": "function",
            "function": {
                    "name": "append_to_file",
                "description": "在指定文件末尾追加文本内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "要追加内容的文件路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "要追加的文本内容"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            }
        },

    ]
