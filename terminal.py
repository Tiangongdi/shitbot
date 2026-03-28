import asyncio
import sys
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style as PromptStyle
from prompt_toolkit.formatted_text import FormattedText
from bot import Bot
from config import load_config, setup_wizard
from ui_components import TerminalUI
from memory import SharedMemory, get_shared_memory

def check_and_run_setup_wizard() -> bool:
    """
    检查配置，如果需要则运行配置向导
    返回 True 表示可以继续运行，False 表示需要退出
    """
    config_path = Path("config.yaml")
    
    if not config_path.exists():
        print("\n[yellow]未找到配置文件，正在启动首次运行配置向导...[/yellow]\n")
        setup_wizard("config.yaml")
        return True
    
    try:
        config = load_config()
        
        needs_setup = False
        
        if not config.ai.api_key:
            print("\n[yellow]检测到 AI API 密钥未配置[/yellow]")
            needs_setup = True
        
        if config.web_search.web_search_ID == 0:
            print("\n[yellow]检测到 Web 搜索 API 未配置[/yellow]")
            needs_setup = True
        
        if needs_setup:
            print("\n[cyan]部分配置缺失，是否重新运行配置向导？[/cyan]")
            from rich.prompt import Prompt
            
            if Prompt.ask("输入 y 重新配置，其他键跳过", default="y").lower() == "y":
                setup_wizard("config.yaml")
        
        return True
        
    except Exception as e:
        print(f"\n[yellow]配置文件读取失败: {e}[/yellow]")
        print("[cyan]是否重新创建配置文件？[/cyan]")
        from rich.prompt import Prompt
        
        if Prompt.ask("输入 y 重新创建", default="y").lower() == "y":
            setup_wizard("config.yaml")
        
        return True


class ShitBotTerminal:
    def __init__(self, title: str = "ShitBot"):
        self.ui = TerminalUI(title)
        self.session = PromptSession()
        self.browser_manager = None
        self.config = load_config()
        self.config_path = Path("config.yaml")
        self.bot = Bot(shared_memory=get_shared_memory())
        self.bot.init_prompt()
    async def handle_command(self, command: str) -> bool:
        command = command.strip()
        
        if not command:
            return False
        
        if command.startswith('/'):
            cmd = command.split()[0].lower()
            args = command.split()[1:] if len(command.split()) > 1 else []
            
            if cmd == '/help':
                self.ui.show_help([
                    {"name": "/help", "description": "显示此帮助信息"},
                    {"name": "/clear", "description": "清除屏幕"},
                    {"name": "/exit", "description": "退出程序"}
                ])
                return True
            
            elif cmd == '/clear':
                self.ui.clear()
                self.ui.show_welcome()
                return True
            
            elif cmd == '/exit':
                self.bot.shared_memory.clear()
                self.ui.system("再见！")
                await self.cleanup()
                sys.exit(0)
            
            elif cmd == '/add':
                if not args:
                    self.ui.error("请提供文件路径")
                    return True
                file_path = args[0]
                self._add_stop_file(file_path)
                return True
            
            elif cmd == '/remove':
                if not args:
                    self.ui.error("请提供文件路径")
                    return True
                file_path = args[0]
                self._remove_stop_file(file_path)
                return True
            
            elif cmd == '/list':
                self._list_stop_files()
                return True
            
            elif cmd == '/clear_memory':
                self.bot.shared_memory.clear()
                self.ui.success("记忆已清空")
                return True
            
            else:
                self.ui.error(f"未知命令: {cmd}")
                return True
        
        return False
    
    async def cleanup(self):
        if self.browser_manager:
            self.browser_manager.close()
    
    def _add_stop_file(self, file_path: str):
        """添加文件到停止列表"""
        if file_path in self.config.stop.file:
            self.ui.warning(f"文件已在列表中: {file_path}")
            return
        
        self.config.stop.file.append(file_path)
        self._save_config()
        self.ui.success(f"已添加到禁止列表: {file_path}")
    
    def _remove_stop_file(self, file_path: str):
        """从停止列表中删除文件"""
        if file_path not in self.config.stop.file:
            self.ui.warning(f"文件不在列表中: {file_path}")
            return
        
        self.config.stop.file.remove(file_path)
        self._save_config()
        self.ui.success(f"已从禁止列表移除: {file_path}")
    
    def _list_stop_files(self):
        """列出所有禁止文件"""
        if not self.config.stop.file:
            self.ui.system("禁止列表为空")
            return
        
        self.ui.system("禁止文件列表:")
        for i, file_path in enumerate(self.config.stop.file, 1):
            self.ui.info(f"  {i}. {file_path}")
    
    def _save_config(self):
        """保存配置到文件"""
        import yaml
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump({
                'user': {
                    'user_name': self.config.user.user_name,
                    'bot_name': self.config.user.bot_name,
                    'bot_prompt': self.config.user.bot_prompt
                },
                'ai': {
                    'api_key': self.config.ai.api_key,
                    'value': self.config.ai.value,
                    'model': self.config.ai.model
                },
                'bocha': {
                    'api_key': self.config.bocha.api_key,
                    'base_url': self.config.bocha.base_url,
                    'index_name': self.config.bocha.index_name
                },
                'browser': {
                    'playwright_browsers_path': self.config.browser.playwright_browsers_path or ''
                },
                'email': {
                    'smtp_server': self.config.email.smtp_server,
                    'smtp_port': self.config.email.smtp_port,
                    'email': self.config.email.email,
                    'password': self.config.email.password,
                    'use_tls': self.config.email.use_tls
                },
                'stop': {
                    'file': self.config.stop.file
                },
                'tavily': {
                    'key': self.config.tavily.key
                },
                'web_search': {
                    'web_search_ID': self.config.web_search.web_search_ID
                },
                'default_provider': self.config.default_provider
            }, f, default_flow_style=False, allow_unicode=True)
    
    async def run(self):
        check_and_run_setup_wizard()
        
        self.ui.show_welcome()
        self.ui.show_help([
            {"name": "/help", "description": "显示此帮助信息"},
            {"name": "/clear", "description": "清除屏幕"},
            {"name": "/clear_memory", "description": "清空对话记忆"},
            {"name": "/add", "description": "添加文件到禁止列表 (例: /add /path/to/file)"},
            {"name": "/remove", "description": "从禁止列表删除文件 (例: /remove /path/to/file)"},
            {"name": "/list", "description": "查看禁止文件列表"},  
            {"name": "/exit", "description": "退出程序"}
        ])
        
        while True:
            try:
                user_input = await self.session.prompt_async(
                   FormattedText([("class:user", "> ")]),
                    style=PromptStyle.from_dict({
                        "user": "ansigreen bold",
                    })
                ) 
                if not user_input.strip(): # 忽略空输入
                    continue
                
                elif await self.handle_command(user_input):
                    continue
                else:
                    res = await self.bot.chat(user_input)
                    self.ui.info(res) 
            except KeyboardInterrupt:
                self.bot.shared_memory.clear()
                self.ui.system("\n检测到中断信号，输入 /exit 退出")
            except Exception as e:
                self.ui.error(f"发生错误: {e}")

