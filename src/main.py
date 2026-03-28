#!/usr/bin/env python3
"""
ShitBot - AI 智能助手
支持 MiniMax API、博查搜索API，具备浏览器自动化能力
"""

import asyncio
import sys
import io
import os
from pathlib import Path

# 添加项目根目录到 Python 导入路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 修复 Windows 控制台中文编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.terminal import ShitBotTerminal



async def main():
    terminal = ShitBotTerminal()
    await terminal.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已退出")
