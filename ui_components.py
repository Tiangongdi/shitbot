"""
ShitBot UI 组件库
提供可复用的终端界面组件
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown  
from rich import box
from config import load_config

class WelcomeScreen:
    """欢迎屏幕组件"""
    
    def __init__(self, title: str = "ShitBot"):
        self.title = title
        self.console = Console()
    
    def show(self):
        """显示欢迎界面"""
        welcome_text = r"""
╔════════════════════════════════════════════════════════════════╗
║                                                              ║
║             _____ _     _ _  ______       _                  ║
║            /  ___| |   (_) | | ___ \     | |                 ║
║            \ `--.| |__  _| |_| |_/ / ___ | |_                ║
║             `--. \ '_ \| | __| ___ \/ _ \| __|               ║
║            /\__/ / | | | | |_| |_/ / (_) | |_                ║
║            \____/|_| |_|_|\__\____/ \___/ \__|               ║
║                                                              ║
║                                                              ║
║                                                              ║
║                                                              ║
╚════════════════════════════════════════════════════════════════╝
"""
        
        self.console.print(Panel(
            Text(welcome_text, justify="center"),
            title=f"欢迎使用 {self.title}",
            subtitle="输入 /help 查看命令帮助",
            box=box.DOUBLE
        ))


class HelpScreen:
    """帮助屏幕组件"""
    
    def __init__(self, commands: list):
        self.commands = commands
        self.console = Console()
    
    def show(self):
        """显示帮助信息"""
        help_text = "可用命令：\n"
        
        for cmd in self.commands:
            help_text += f"{cmd['name']}: {cmd['description']}\n"
        
        help_text += "\n"
        help_text += "直接在输入框中输入命令\n"
        
        self.console.print(Panel(
            Text(help_text, style="green"),
            title="命令帮助"
        ))


class MessagePanel:
    """消息面板组件"""
    
    def __init__(self):
        self.console = Console()
        self.config = load_config()
    
    def error(self, message: str):
        """显示错误消息"""
        self.console.print("[red]error >[/red] "+message)
    
    def system(self, message: str):
        """显示系统消息"""
        self.console.print("[yellow]system >[/yellow] "+message)
    
    def info(self, message: str):
        """显示信息消息"""
        self.console.print(f"[blue]{self.config.user.bot_name} >[/blue]\n", Markdown(message))
    
    def success(self, message: str):
        """显示成功消息"""
        self.console.print("[green]success >[/green] "+message)
    def tool(self, message: str):
        """显示工具消息"""
        self.console.print("[blue]tool >[/blue] "+message) # 工具消息 颜色：蓝色


class CommandHandler:
    """命令处理器基类"""
    
    def __init__(self):
        self.commands = []
        self.console = Console()
    
    def register(self, name: str, description: str, handler):
        """注册命令"""
        self.commands.append({
            "name": name,
            "description": description,
            "handler": handler
        })
    
    async def handle(self, command: str) -> bool:
        """处理命令"""
        command = command.strip()
        
        if not command or not command.startswith('/'):
            return False
        
        cmd = command.split()[0].lower()
        args = command.split()[1:] if len(command.split()) > 1 else []
        
        for registered_cmd in self.commands:
            if registered_cmd["name"] == cmd:
                await registered_cmd["handler"](args)
                return True
        
        self.error(f"未知命令: {cmd}")
        return True
    
    def error(self, message: str):
        """显示错误消息"""
        self.console.print("[red]error >[/red] "+message)


class TerminalUI:
    """终端 UI 组件"""
    
    def __init__(self, title: str = "ShitBot"):
        self.console = Console()
        self.welcome = WelcomeScreen(title)
        self.messages = MessagePanel()
    
    def show_welcome(self):
        """显示欢迎界面"""
        self.welcome.show()
    
    def show_help(self, commands: list):
        """显示帮助信息"""
        help_screen = HelpScreen(commands)
        help_screen.show()
    
    def error(self, message: str):
        """显示错误消息"""
        self.messages.error(message)
    
    def system(self, message: str):
        """显示系统消息"""
        self.messages.system(message)
    
    def info(self, message: str):
        """显示信息消息"""
        self.messages.info(message)
    
    def success(self, message: str):
        """显示成功消息"""
        self.messages.success(message)
    
    def clear(self):
        """清除屏幕"""
        self.console.clear()
    
    def tool(self, message: str):
        """显示工具消息"""
        self.messages.tool(message)
