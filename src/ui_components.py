"""
ShitBot UI 组件库
提供可复用的终端界面组件
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown  
from rich import box
from rich.live import Live
from rich.spinner import Spinner

class WelcomeScreen:
    """欢迎屏幕组件"""

    def __init__(self, title: str = "ShitBot"):
        self.title = title
        self.console = Console()

    def show(self):
        """显示欢迎界面"""
        # 使用纯 ASCII art，兼容所有编码
        # S H I T B O T
        ascii_art = r"""
███████╗██╗  ██╗██╗████████╗██████╗  ██████╗ ████████╗
██╔════╝██║  ██║██║╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝
███████╗███████║██║   ██║   ██████╔╝██║   ██║   ██║   
╚════██║██╔══██║██║   ██║   ██╔══██╗██║   ██║   ██║   
███████║██║  ██║██║   ██║   ██████╔╝╚██████╔╝   ██║   
╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═════╝  ╚═════╝    ╚═╝   
                                                      
"""
        welcome_text = f"""[bold green]{ascii_art}[/bold green]

[bold cyan]ShitBot - 你的 AI 编程助手[/bold cyan]

[dim white] * 输入 [/dim white][yellow bold]/help[/yellow bold][dim white] 查看所有可用命令[/dim white]
[dim white] * 输入 [/dim white][yellow bold]/workflow[/yellow bold][dim white] 切换工作模式[/dim white]
[dim white] * 按 [/dim white][yellow bold]Esc[/yellow bold][dim white] 终止当前任务[/dim white]
"""

        # 使用 Panel 美化显示
        panel = Panel(
            welcome_text,
            border_style="green",
            box=box.ROUNDED
        )
        self.console.print(panel)


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
        self._thinking_live = None
    
    def error(self, message: str):
        """显示错误消息"""
        self.console.print("[red]error >[/red] "+message)
    
    def system(self, message: str):
        """显示系统消息"""
        self.console.print("[yellow]system >[/yellow] "+message)
    
    def info(self, message: str):
        """显示信息消息"""
        self.console.print("[blue]ShitBot >[/blue]\n", Markdown(message))
    
    def success(self, message: str):
        """显示成功消息"""
        self.console.print("[green]success >[/green] "+message)
    
    def tool(self, message: str):
        """显示工具消息"""
        self.console.print("[blue]tool >[/blue] "+message)
    
    def start_thinking(self, tool_name: str = None):
        """开始思考动画 - 使用Rich Spinner"""
        # 根据是否提供工具名称来显示不同的文字
        if tool_name:
            text = f"[cyan white]Use tool {tool_name}[/cyan white]"
        else:
            text = "[cyan white]Thinks[/cyan white]"
        
        # 创建Spinner，使用dots样式
        spinner = Spinner("dots", text=text)
        
        # 创建Live显示
        self._thinking_live = Live(
            spinner,
            console=self.console,
            refresh_per_second=10,
            transient=True
        )
        self._thinking_live.start()
    
    def stop_thinking(self):
        """停止思考动画"""
        if self._thinking_live:
            self._thinking_live.stop()
            self._thinking_live = None
    
    def save_and_show_response(self, message: str):
        """保存并显示AI回复"""
        self.stop_thinking()
        # 先打印加粗的·和空格，然后打印markdown，使用同一个console实例
        self.console.print("[white]●[/white] ", end="")
        self.console.print(Markdown(message))


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
    
    def start_thinking(self, tool_name: str = None):
        """开始思考动画"""
        self.messages.start_thinking(tool_name)
    
    def stop_thinking(self):
        """停止思考动画"""
        self.messages.stop_thinking()
    
    def save_and_show_response(self, message: str):
        """保存并显示AI回复"""
        self.messages.save_and_show_response(message)
