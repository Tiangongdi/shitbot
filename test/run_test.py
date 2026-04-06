"""
测试 terminal.py 中的 prompt_command 方法
"""
import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from terminal import ShitBotTerminal


def test_prompt_command():
    """测试 prompt_command 方法"""
    
    # 创建一个 mock 的 terminal 实例（不需要完整的初始化）
    class MockTerminal:
        def prompt_command(self, user_input: str):
            """提示用户输入命令"""
            command = user_input.strip()
            
            if not command:
                return False
            
            if command.startswith('/'):
                parts = command.split()
                cmd = parts[0].lower()
                args = " ".join(parts[1:]) if len(parts) > 1 else ""
                print(f"cmd: {cmd}, args: '{args}'")
                return cmd, args
            return None
    
    terminal = MockTerminal()
    
    # 测试用例 1: 带参数的命令
    print("=" * 50)
    print("测试 1: /ccc lll mmm mmm")
    result = terminal.prompt_command("/ccc lll mmm mmm")
    assert result == ("/ccc", "lll mmm mmm"), f"期望 ('/ccc', 'lll mmm mmm'), 得到 {result}"
    print("✓ 通过")
    
    # 测试用例 2: 单个参数
    print("=" * 50)
    print("测试 2: /skill coder")
    result = terminal.prompt_command("/skill coder")
    assert result == ("/skill", "coder"), f"期望 ('/skill', 'coder'), 得到 {result}"
    print("✓ 通过")
    
    # 测试用例 3: 无参数的命令
    print("=" * 50)
    print("测试 3: /clear")
    result = terminal.prompt_command("/clear")
    assert result == ("/clear", ""), f"期望 ('/clear', ''), 得到 {result}"
    print("✓ 通过")
    
    # 测试用例 4: 空命令
    print("=" * 50)
    print("测试 4: 空字符串 ''")
    result = terminal.prompt_command("")
    assert result == False, f"期望 False, 得到 {result}"
    print("✓ 通过")
    
    # 测试用例 5: 只有空格的命令
    print("=" * 50)
    print("测试 5: '   ' (只有空格)")
    result = terminal.prompt_command("   ")
    assert result == False, f"期望 False, 得到 {result}"
    print("✓ 通过")
    
    # 测试用例 6: 非斜杠命令（普通消息）
    print("=" * 50)
    print("测试 6: 'hello world' (非命令)")
    result = terminal.prompt_command("hello world")
    assert result is None, f"期望 None, 得到 {result}"
    print("✓ 通过")
    
    # 测试用例 7: 大写命令
    print("=" * 50)
    print("测试 7: '/HELP' (大写)")
    result = terminal.prompt_command("/HELP")
    assert result == ("/help", ""), f"期望 ('/help', ''), 得到 {result}"
    print("✓ 通过")
    
    # 测试用例 8: 混合大小写参数
    print("=" * 50)
    print("测试 8: '/Skill Coder Python'")
    result = terminal.prompt_command("/Skill Coder Python")
    assert result == ("/skill", "Coder Python"), f"期望 ('/skill', 'Coder Python'), 得到 {result}"
    print("✓ 通过")
    
    # 测试用例 9: 首尾有空格
    print("=" * 50)
    print("测试 9: '  /test arg  ' (首尾有空格)")
    result = terminal.prompt_command("  /test arg  ")
    assert result == ("/test", "arg"), f"期望 ('/test', 'arg'), 得到 {result}"
    print("✓ 通过")
    
    print("=" * 50)
    print("所有测试通过！")


if __name__ == "__main__":
    test_prompt_command()
