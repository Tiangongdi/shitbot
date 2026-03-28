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
from config.config import setup_wizard
from src.terminal import check_and_run_setup_wizard
from src.bot import Bot
from src.memory import get_shared_memory


@click.group(invoke_without_command=True)
def cli(ctx):
    """
    ShitBot - 一个功能强大的 AI 智能助手终端应用
    
    不带子命令运行时默认启动交互式对话
    """
    if ctx.invoked_subcommand is None:
        # 如果没有子命令，默认启动主程序
        try:
            asyncio.run(main.main())
        except KeyboardInterrupt:
            print("\n程序已退出")


@cli.command()
def config():
    """
    配置命令，运行配置向导
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


@cli.command('chat')
def chat():
    """
    单次对话模式，用于快速进行一次对话
    """
    run_chat()


@cli.command('-m')
def m():
    """
    单次对话模式（简写），用于快速进行一次对话
    """
    run_chat()


if __name__ == '__main__':
    cli()
