#!/usr/bin/env python3
"""
ShitBot - AI 智能助手
支持 MiniMax API、博查搜索API，具备浏览器自动化能力
"""

import asyncio
import sys
import os
from pathlib import Path
from terminal import ShitBotTerminal



async def main():
    terminal = ShitBotTerminal()
    await terminal.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已退出")
