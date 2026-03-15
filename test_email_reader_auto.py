# -*- coding: utf-8 -*-
"""
邮件读取工具自动化测试
测试基本功能是否正常
"""

import sys
import os
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目路径
sys.path.insert(0, r'D:\project\ShitBot_bata')

from tools.email_reader import EmailReader


def test_basic_functions():
    """测试基本功能"""
    print("\n" + "=" * 60)
    print("[邮件读取工具 - 基本功能测试]")
    print("=" * 60)
    
    # 测试1: 创建EmailReader实例
    print("\n[测试1] 创建EmailReader实例...")
    try:
        reader = EmailReader(
            email_address="test@example.com",
            password="test_password",
            imap_server="imap.qq.com",
            imap_port=993
        )
        print("[成功] EmailReader实例创建成功")
    except Exception as e:
        print(f"[失败] {str(e)}")
        return False
    
    # 测试2: 测试字符串解码功能
    print("\n[测试2] 测试字符串解码功能...")
    try:
        test_str = "=?utf-8?B?5rWL6K+V6YKu5Lu2?="  # "测试主题"的编码
        decoded = reader._decode_str(test_str)
        print(f"[成功] 解码结果: {decoded}")
    except Exception as e:
        print(f"[失败] {str(e)}")
    
    # 测试3: 测试连接功能（会失败，但测试代码逻辑）
    print("\n[测试3] 测试连接功能...")
    result = reader.connect()
    if not result.get("success"):
        print(f"[预期失败] {result.get('error')}")
        print("[说明] 这是正常的，因为使用了测试邮箱地址")
    else:
        print("[成功] 连接成功")
    
    # 测试4: 测试断开连接
    print("\n[测试4] 测试断开连接...")
    try:
        reader.disconnect()
        print("[成功] 断开连接成功")
    except Exception as e:
        print(f"[失败] {str(e)}")
    
    print("\n" + "=" * 60)
    print("[测试完成]")
    print("=" * 60)
    print("\n提示：")
    print("1. 要测试实际邮箱功能，请运行 test_email_reader.py")
    print("2. 需要提供真实的邮箱地址和授权码")
    print("3. QQ邮箱需要在设置中开启IMAP服务并获取授权码")
    
    return True


if __name__ == "__main__":
    test_basic_functions()
