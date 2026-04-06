# AI Agent Skills Module
# 重构：使用装饰器自动注册工具，消除重复定义
import asyncio
import json
import inspect
import os
from typing import Optional, Dict, Any
from src.tool_registry import registry
from tools.doc import Doc
from src.agent.memory_bot import MemoryBot
from src.agent.webbot import WebBot
from tools.bocha import BochaSearch
from tools.timer import get_timer
from tools.venv_manager import VenvManager
from tools.safe import safe_format
from tools.role import Role
from tools.skill import Skill
from tools.tavily_api import TavilySearch
from tools.email_reader import EmailReader
from tools.mcp_client import MCPClient, MCPServerConfig
from src.agent.ai import Message
from src.agent.subagent_manager import SubAgentManager
from src.ui_components import TerminalUI


class Tool:
    """工具执行类，使用装饰器自动注册工具"""
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
        self.venv_manager = VenvManager()
        self.role = Role()
        self.skill = Skill()
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.tavily_client = TavilySearch()
        self.doc = Doc()
        self.subagent = SubAgentManager()

        # 初始化邮件读取器
        self.email_reader = None
        self._init_email_reader()

        # 初始化 MCP 客户端
        self.mcp_client = MCPClient()
        self._mcp_initialized = False

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

    # ==================== MCP 集成 ====================

    async def init_mcp(self):
        """
        初始化 MCP 连接
        从配置文件读取 MCP Server 列表并连接
        """
        if self._mcp_initialized:
            return

        mcp_config = self.config.mcp
        if not mcp_config.enabled:
            return

        if not mcp_config.servers:
            return

        # 将配置中的 server 项转换为 MCPServerConfig
        server_configs = []
        for srv in mcp_config.servers:
            server_configs.append(MCPServerConfig(
                name=srv.name,
                transport=srv.transport,
                command=srv.command,
                args=srv.args,
                env=srv.env,
                url=srv.url,
                description=srv.description
            ))

        await self.mcp_client.connect_all(server_configs)
        self._mcp_initialized = True

    def get_mcp_tools_definition(self) -> list:
        """
        获取 MCP 工具的 OpenAI function calling 格式定义
        用于合并到 AI 的 tools 参数中
        """
        if not self._mcp_initialized:
            return []
        return self.mcp_client.get_tools_definition()

    def set_terminal_ui(self, terminal_ui):
        """
        设置终端 UI 实例

        Args:
            terminal_ui: TerminalUI 实例
        """
        self.terminal_ui = terminal_ui

    def _load_config(self):
        """加载配置"""
        from config.config import load_config
        return load_config()

    # ==================== 工具方法 - 使用装饰器自动注册 ====================

    @registry.tool("在网络上搜索信息")
    async def search_web(self, query: str, count: int = 5) -> str:
        """
        在网络上搜索信息

        Args:
            query: 搜索查询词
            count: 返回结果数量，默认5
        """
        if self.config.web_search.web_search_ID == "1":
            response = await self.bocha_client.search(query, count=count)
            if response.success:
                return self.bocha_client.format_results(response)
            else:
                return f"✗ 搜索失败: {response.error}"
        else:
            return self.tavily_client.search(query, max_results=count)

    @registry.tool("让WebBot执行任务,WebBot是一个浏览器操作助手,它可以查看网页信息,点击网页,填写表单等浏览器修改功能")
    async def webbot_task(self, query: str) -> str:
        """
        让WebBot执行任务

        Args:
            query: 告诉WebBot要执行的任务
        """
        response = await self.web_bot.execute_task(query)
        return response

    @registry.tool("读取指定文件内容")
    def read_file(self, file_path: str) -> str:
        """
        读取指定文件内容

        Args:
            file_path: 要读取的文件路径
        """
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"读取文件时出错: {str(e)}"

    @registry.tool("给指定文件写入内容")
    def write_file(self, file_path: str, content: str) -> str:
        """
        给指定文件写入内容

        Args:
            file_path: 要写入的文件路径
            content: 要写入的内容
        """
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"成功写入文件: {file_path}"
        except Exception as e:
            return f"写入文件时出错: {str(e)}"

    @registry.tool("复制指定文件,到目标路径")
    def copy_file(self, source_path: str, dest_path: str) -> str:
        """
        复制指定文件到目标路径

        Args:
            source_path: 要复制的文件路径
            dest_path: 要复制到的目标路径
        """
        if source_path in self.stop_file or dest_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        try:
            import shutil
            shutil.copy(source_path, dest_path)
            return f"成功复制文件: {source_path} -> {dest_path}"
        except Exception as e:
            return f"复制文件时出错: {str(e)}"

    @registry.tool("移动指定文件,到目标路径")
    def move_file(self, source_path: str, dest_path: str) -> str:
        """
        移动指定文件到目标路径

        Args:
            source_path: 要移动的文件路径
            dest_path: 要移动到的目标路径
        """
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

    @registry.tool("创建目录")
    def create_dir(self, dir_path: str) -> str:
        """
        创建目录

        Args:
            dir_path: 要创建的目录路径
        """
        if dir_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        try:
            import os
            if os.path.exists(dir_path):
                return f"目录已存在: {dir_path}，请不要重复创建相同的文件夹"
            os.makedirs(dir_path, exist_ok=True)
            return f"成功创建目录: {dir_path}"
        except Exception as e:
            return f"创建目录时出错: {str(e)}"

    @registry.tool("获取目录内容")
    def get_dir_content(self, dir_path: str) -> str:
        """
        获取目录内容

        Args:
            dir_path: 要获取内容的目录路径
        """
        if dir_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        try:
            import os
            content = os.listdir(dir_path)
            return f"目录内容: {content}"
        except Exception as e:
            return f"获取目录内容时出错: {str(e)}"

    @registry.tool("执行 shell 命令")
    def shell_command(self, command: str, use_timeout: bool = True) -> str:
        """
        执行 shell 命令

        Args:
            command: 要执行的 shell 命令
            use_timeout: 是否启用超时限制，默认为true。启用后命令执行超过60秒将自动终止并返回当前输出，防止命令长时间等待用户输入
        """
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

    @registry.tool("发送邮件到指定邮箱")
    def send_email(self, to_email: str, subject: str, body: str) -> str:
        """
        发送邮件到指定邮箱

        Args:
            to_email: 收件人邮箱地址
            subject: 邮件主题
            body: 邮件正文内容
        """
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

    @registry.tool("取消定时任务")
    def cancel_timer(self, task_id: str) -> str:
        """
        取消定时任务

        Args:
            task_id: 任务ID
        """
        self.timer.cancel(task_id)
        return f"定时任务已取消：{task_id}"

    @registry.tool("暂停定时任务")
    def pause_timer(self, task_id: str) -> str:
        """
        暂停定时任务

        Args:
            task_id: 任务ID
        """
        self.timer.pause(task_id)
        return f"定时任务已暂停：{task_id}"

    @registry.tool("恢复定时任务")
    def resume_timer(self, task_id: str) -> str:
        """
        恢复定时任务

        Args:
            task_id: 任务ID
        """
        self.timer.resume(task_id)
        return f"定时任务已恢复：{task_id}"

    @registry.tool("列出所有定时任务")
    def list(self) -> str:
        """
        列出所有定时任务
        """
        tasks = self.timer.get_tasks()
        return f"当前定时任务列表：{tasks}"

    @registry.tool("删除文件")
    async def delete_file(self, file_path: str, if_user: bool = True) -> str:
        """
        删除文件

        Args:
            file_path: 要删除的文件路径
            if_user: 是否为用户操作，定时器操作默认拒绝
        """
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        if not if_user:
            return "为计时器操作，已拒绝，请记录到ERROR日志"

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

    @registry.tool("让memory_bot在以前的对话记录总结信息")
    def get_memory(self, memory_description: str) -> str:
        """
        让memory_bot在以前的对话记录总结信息

        Args:
            memory_description: 让memory_bot总结什么信息
        """
        r = self.memory_bot.get_memory(memory_description)
        return r

    @registry.tool("列出所有可以阅读的doc文档")
    def get_doc_list(self) -> str:
        """
        列出所有可以阅读的doc文档
        """
        return str(self.doc.value)

    @registry.tool("获取doc文档内容,建议先调用get_doc_list获取文档列表")
    def get_doc(self, file_name: str, key: str) -> str:
        """
        获取doc文档内容

        Args:
            file_name: 文档名称
            key: 文档键
        """
        return self.doc.get_data(file_name, key)

    @registry.tool("运行python代码")
    def run_code(self, code: str) -> str:
        """
        运行python代码

        Args:
            code: python代码
        """
        try:
            returncode, stdout, stderr = self.venv_manager.run_python(code)
            return f"代码执行结果: 返回码{returncode}, 输出: {stdout}, 错误: {stderr}"
        except Exception as e:
            return f"代码执行失败：{e}"

    @registry.tool("运行python代码文件")
    def run_code_file(self, code_file: str) -> str:
        """
        运行python代码文件

        Args:
            code_file: python代码文件路径
        """
        if not code_file.endswith(".py"):
            return "代码文件必须是 .py 格式"
        if not os.path.exists(code_file):
            return "代码文件不存在"
        with open(code_file, "r", encoding="utf-8") as f:
            code = f.read()
        returncode, stdout, stderr = self.venv_manager.run_python(code)
        return f"代码执行结果: 返回码{returncode}, 输出: {stdout}, 错误: {stderr}"

    @registry.tool("列出所有可以阅读的角色")
    def get_role(self) -> str:
        """
        列出所有可以阅读的角色
        """
        return str(self.role.role_dict)

    @registry.tool("列出所有可以阅读的技能文档")
    def get_skill(self) -> str:
        """
        列出所有可以阅读的技能文档
        """
        return str(self.skill.skill_dict)


    @registry.tool("列出邮箱中的所有文件夹")
    def list_email_folders(self) -> str:
        """
        列出邮箱中的所有文件夹
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

    @registry.tool("获取邮箱中的邮件列表")
    def get_email_list(self, folder: str = "INBOX", limit: int = 10, unread_only: bool = False) -> str:
        """
        获取邮箱中的邮件列表

        Args:
            folder: 文件夹名称，默认为INBOX
            limit: 返回邮件数量，默认10
            unread_only: 是否只获取未读邮件，默认False
        """
        error = self._ensure_email_connection()
        if error:
            return error

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

    @registry.tool("获取指定邮件的详细内容")
    def get_email_content(self, email_id: str, folder: str = "INBOX") -> str:
        """
        获取指定邮件的详细内容

        Args:
            email_id: 邮件ID
            folder: 文件夹名称，默认为INBOX
        """
        error = self._ensure_email_connection()
        if error:
            return error

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

    @registry.tool("搜索邮件（按主题、发件人、正文搜索）")
    def search_emails(self, criteria: str, folder: str = "INBOX", limit: int = 10) -> str:
        """
        搜索邮件

        Args:
            criteria: 搜索关键词
            folder: 文件夹名称，默认为INBOX
            limit: 返回结果数量，默认10
        """
        error = self._ensure_email_connection()
        if error:
            return error

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

    @registry.tool("标记邮件为已读")
    def mark_email_read(self, email_id: str, folder: str = "INBOX") -> str:
        """
        标记邮件为已读

        Args:
            email_id: 邮件ID
            folder: 文件夹名称，默认为INBOX
        """
        error = self._ensure_email_connection()
        if error:
            return error

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

    @registry.tool("在指定文件末尾追加文本内容")
    def append_to_file(self, file_path: str, content: str) -> str:
        """
        在指定文件末尾追加文本内容

        Args:
            file_path: 要追加内容的文件路径
            content: 要追加的文本内容
        """
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content)
            return f"成功追加内容到文件: {file_path}"
        except Exception as e:
            return f"追加内容时出错: {str(e)}"

    @registry.tool("在指定文件的指定行插入文本")
    def insert_line_at(self, file_path: str, line_number: int, content: str) -> str:
        """
        在指定文件的指定行插入文本

        Args:
            file_path: 要插入内容的文件路径
            line_number: 要插入的行号，从1开始
            content: 要插入的文本内容
        """
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if line_number < 1 or line_number > len(lines) + 1:
                return f"行号超出范围，文件共有{len(lines)}行，有效行号为1-{len(lines)+1}"
            lines.insert(line_number - 1, content + '\n')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return f"成功在第{line_number}行插入内容: {file_path}"
        except Exception as e:
            return f"插入内容时出错: {str(e)}"

    @registry.tool("查看指定文件的指定行文本，可查看单行或多行")
    def read_line_at(self, file_path: str, line_number: int, end_number: int = None) -> str:
        """
        查看指定文件的指定行文本

        Args:
            file_path: 要查看的文件路径
            line_number: 要查看的起始行号，从1开始
            end_number: 要查看的结束行号，从1开始。如果不提供或与line_number相同，则只查看单行
        """
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if line_number < 1 or line_number > len(lines):
                return f"行号超出范围，文件共有{len(lines)}行，有效行号为1-{len(lines)}"

            end = end_number or line_number
            if end < 1 or end > len(lines):
                return f"结束行号超出范围，文件共有{len(lines)}行，有效行号为1-{len(lines)}"

            if line_number == end:
                return f"第{line_number}行内容: {lines[line_number - 1].rstrip()}"
            else:
                selected_lines = lines[line_number - 1:end]
                content = "\n".join([l.rstrip() for l in selected_lines])
                return f"第{line_number}-{end}行内容:\n{content}"
        except Exception as e:
            return f"读取行内容时出错: {str(e)}"

    @registry.tool("删除指定文件的指定行文本，可删除单行或多行")
    def delete_line_at(self, file_path: str, line_number: int, end_number: int = None) -> str:
        """
        删除指定文件的指定行文本

        Args:
            file_path: 要删除行的文件路径
            line_number: 要删除的起始行号，从1开始
            end_number: 要删除的结束行号，从1开始。如果不提供或与line_number相同，则只删除单行
        """
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if line_number < 1 or line_number > len(lines):
                return f"行号超出范围，文件共有{len(lines)}行，有效行号为1-{len(lines)}"

            end = end_number or line_number
            if end < 1 or end > len(lines):
                return f"结束行号超出范围，文件共有{len(lines)}行，有效行号为1-{len(lines)}"

            if line_number == end:
                deleted_line = lines.pop(line_number - 1).rstrip()
                message = f"成功删除第{line_number}行内容: {deleted_line}"
            else:
                deleted_lines = lines[line_number - 1:end]
                del lines[line_number - 1:end]
                deleted_line = "\n".join([l.rstrip() for l in deleted_lines])
                message = f"成功删除第{line_number}-{end}行内容:\n{deleted_line}"

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return message
        except Exception as e:
            return f"删除行内容时出错: {str(e)}"

    @registry.tool("获取文件的行信息：总行数和按关键词搜索匹配的行号")
    def get_line_info(self, file_path: str, keyword: str = "") -> str:
        """
        获取文件的行信息

        Args:
            file_path: 要查看的文件路径
            keyword: 可选，搜索包含该关键词的行号，用于快速定位内容位置
        """
        if file_path in self.stop_file:
            return "操作包含在禁止列表中，已拒绝"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            total_lines = len(lines)
            result = [f"文件: {file_path}"]
            result.append(f"总行数: {total_lines}")
            if keyword:
                matching_lines = []
                for i, line in enumerate(lines, 1):
                    if keyword in line:
                        matching_lines.append(i)
                if matching_lines:
                    result.append(f"包含关键词 '{keyword}' 的行号: {matching_lines}")
                    result.append(f"共找到 {len(matching_lines)} 个匹配")
                else:
                    result.append(f"未找到包含关键词 '{keyword}' 的行")
            return "\n".join(result)
        except Exception as e:
            return f"获取行信息时出错: {str(e)}"

    @registry.tool("定时任务：在指定时间后执行一次")
    def once_after(self, time: int, task: str) -> str:
        """
        定时任务：在指定时间后执行一次

        Args:
            time: 延迟时间（秒）
            task: 任务描述
        """
        self.timer.once_after(description=task, delay_seconds=time)
        return f"定时任务已添加：{time} 秒后执行 {task}"

    @registry.tool("定时任务：周期性执行")
    def interval(self, interval_seconds: int, interval_count: int, task: str) -> str:
        """
        定时任务：周期性执行

        Args:
            interval_seconds: 时间间隔（秒）
            interval_count: 触发次数，-1 表示无限次
            task: 任务描述
        """
        self.timer.interval_every(description=task, interval_seconds=interval_seconds, interval_count=interval_count)
        if interval_count == -1:
            return f"定时任务已添加：每 {interval_seconds} 秒执行 {task} 无限次"
        else:
            return f"定时任务已添加：每 {interval_seconds} 秒执行 {task} {interval_count} 次"

    @registry.tool("定时任务：每天在指定时间执行")
    def daily_at(self, hour: int, task: str, minute: int = 0) -> str:
        """
        定时任务：每天在指定时间执行

        Args:
            hour: 小时（0-23）
            task: 任务描述
            minute: 分钟（0-59），默认为0
        """
        self.timer.daily_at(description=task, hour=hour, minute=minute)
        return f"定时任务已添加：每天 {hour}:{minute} 执行 {task}"

    @registry.tool("发布给子智能体的任务，该工具会创建一个拥有独立记忆的智能体，子智能体会根据任务描述执行任务，执行完任务会返回任务报告")
    def subagent_task(self, task: str, role: str) -> str:
        """
        发布给子智能体的任务

        Args:
            task: 要执行的任务描述
            role: 要执行任务的子智能体的人告诉他在执行任务前阅读哪个role库里面的人设,如果没有相关的人设,那就在role文件夹里面新建一个Role文件,方便重复使用
        """
        if not task:
            return "请提供任务描述"
        if not role:
            return "请提供角色"
        result = self.subagent.run_background_task(role, task, self.shared_memory)
        return result

    # ==================== 私有辅助方法 ====================

    def _ensure_email_connection(self) -> str:
        """确保邮件读取器已连接到服务器，返回错误信息或None"""
        if not self.email_reader:
            return "邮件读取器未初始化，请检查IMAP配置"

        if not self.email_reader.connection:
            result = self.email_reader.connect()
            if not result.get("success"):
                return f"连接邮件服务器失败: {result.get('error')}"

        return None  # 连接成功，返回None表示无错误

    # ==================== 核心执行逻辑 - 动态分发 ====================

    async def execute(self, message, if_user: bool = True):
        """执行工具，动态分发到已注册的方法"""
        msg_list = []
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name.strip()
                arguments = tool_call.function.arguments

                # 尝试清理可能包含 XML 标签的 arguments
 
                try:
                    # 解析 JSON
                    if isinstance(arguments, str):
                        # 清理可能的XML标签
                        import re
                        arguments = re.sub(r'<[^>]*>', '', arguments).strip()
                        args = json.loads(arguments)
                    else:
                        args = arguments
                except json.JSONDecodeError as e:
                    error_msg = f"参数解析失败: {str(e)}, 原始参数: {arguments}"
                    msg_list.append(Message(
                        role="tool",
                        content=error_msg,
                        tool_call_id=tool_call.id
                    ))
                    continue

                # 动态调用已注册的方法
                try:
                    # 获取方法
                    if not hasattr(self, tool_name):
                        error_msg = f"工具不存在: {tool_name}"
                        msg_list.append(Message(
                            role="tool",
                            content=error_msg,
                            tool_call_id=tool_call.id
                        ))
                        continue

                    func = getattr(self, tool_name)
                    
                    # 执行：支持异步和同步方法
                    if inspect.iscoroutinefunction(func):
                        # delete_file 需要特殊处理 if_user 参数
                        if tool_name == "delete_file":
                            args["if_user"] = if_user
                            result = await func(**args)
                        else:
                            result = await func(**args)
                    else:
                        # delete_file 需要特殊处理 if_user 参数
                        if tool_name == "delete_file":
                            args["if_user"] = if_user
                            result = func(**args)
                        else:
                            result = func(**args)

                    # 包装结果返回给AI
                    msg_list.append(Message(
                        role="tool",
                        content=str(result),
                        tool_call_id=tool_call.id
                    ))

                except Exception as e:
                    error_msg = f"执行工具 {tool_name} 时出错: {str(e)}"
                    msg_list.append(Message(
                        role="tool",
                        content=error_msg,
                        tool_call_id=tool_call.id
                    ))

        return msg_list
