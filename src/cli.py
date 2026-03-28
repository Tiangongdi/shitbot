import click
import sys
import asyncio

# 添加项目根目录到 Python 导入路径
from pathlib import Path
project_root = Path(__file__).parent.parent  # src/cli.py → 上级就是项目根
sys.path.insert(0, str(project_root))

from src import main
from config.config import setup_wizard
from src.terminal import check_and_run_setup_wizard
from src.bot import Bot
from src.memory import get_shared_memory


@click.command()
@click.option("-m", "--chat", help="单次对话内容")
def cli(chat):
    """
    ShitBot - 一个功能强大的 AI 智能助手终端应用
    
    不带参数运行时默认启动交互式对话
    使用 -m 参数执行单次对话
    """
    if chat:
        # 执行单次对话
        try:
            # 检查配置
            check_and_run_setup_wizard()
            
            # 初始化 Bot
            bot = Bot(shared_memory=get_shared_memory())
            bot.init_prompt()
            
            # 初始化 MCP 连接
            asyncio.run(bot.init_mcp())
            
            print("思考中...")
            response = asyncio.run(bot.chat(chat))
            print(f"\nBot: {response}\n")
                
        except KeyboardInterrupt:
            print("\n对话已结束")
        except Exception as e:
            print(f"发生错误: {e}")
    else:
        # 启动交互式对话
        try:
            asyncio.run(main.main())
        except KeyboardInterrupt:
            print("\n程序已退出")


@click.command()
def config():
    """
    配置命令，运行配置向导
    """
    setup_wizard()

# 创建命令组
cli_group = click.Group()
cli_group.add_command(cli, name="shitbot")
cli_group.add_command(config)




if __name__ == '__main__':
    cli_group()
