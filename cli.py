import click
import sys
import asyncio
import io

# 添加项目根目录到 Python 导入路径
from pathlib import Path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 修复 Windows 控制台中文编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import src.main as main
from config.config import setup_wizard, load_config
from src.terminal import check_and_run_setup_wizard
from src.bot import Bot
from src.memory import get_shared_memory

# 创建命令
@click.command()
def default():
    """
    主命令，用于启动 ShitBot
    """
    try:
        asyncio.run(main.main())
    except KeyboardInterrupt:
        print("\n程序已退出")

@click.command()
def config():
    """
    配置命令，用于配置 ShitBot
    """
    setup_wizard()

def run_chat():
    """
    执行单次对话的核心逻辑
    """
    try:
        # 检查配置
        check_and_run_setup_wizard()
        
        # 初始化 Bot
        bot = Bot(shared_memory=get_shared_memory())
        bot.init_prompt()
        
        # 初始化 MCP 连接
        asyncio.run(bot.init_mcp())
        
        print("进入单次对话模式...")
        print("请输入您的问题，输入 /exit 退出：")
        
        while True:
            user_input = input("> ")
            
            if user_input.strip() == '/exit':
                print("对话已结束")
                break
            
            if not user_input.strip():
                continue
            
            # 执行单次对话
            print("思考中...")
            response = asyncio.run(bot.chat(user_input))
            print(f"\nBot: {response}\n")
            
    except KeyboardInterrupt:
        print("\n对话已结束")
    except Exception as e:
        print(f"发生错误: {e}")

@click.command('chat')
def chat():
    """
    单次对话模式，用于快速进行一次对话
    """
    run_chat()

@click.command('-m')
def m():
    """
    单次对话模式，用于快速进行一次对话
    """
    run_chat()

# 创建命令集合
cli = click.CommandCollection(sources=[default, config, chat, m], invoke_without_command=True)


