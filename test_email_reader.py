# -*- coding: utf-8 -*-
"""
邮件读取工具测试脚本
使用 ShitBot 开发环境进行测试
"""

import sys
import os
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目路径
sys.path.insert(0, r'D:\project\ShitBot_bata')

from tools.email_reader import EmailReader


def test_connection():
    """测试邮箱连接"""
    print("\n" + "=" * 60)
    print("[邮件读取工具测试]")
    print("=" * 60)
    
    # 输入邮箱信息
    print("\n请输入邮箱信息：")
    email_address = input("邮箱地址: ").strip()
    password = input("邮箱授权码/密码: ").strip()
    
    # 选择邮箱服务器
    print("\n常用邮箱服务器：")
    print("1. QQ邮箱 (imap.qq.com)")
    print("2. 163邮箱 (imap.163.com)")
    print("3. Gmail (imap.gmail.com)")
    print("4. 自定义")
    
    choice = input("请选择 (1-4): ").strip()
    
    if choice == "1":
        imap_server = "imap.qq.com"
        imap_port = 993
    elif choice == "2":
        imap_server = "imap.163.com"
        imap_port = 993
    elif choice == "3":
        imap_server = "imap.gmail.com"
        imap_port = 993
    else:
        imap_server = input("IMAP服务器地址: ").strip()
        imap_port = int(input("IMAP端口 (默认993): ").strip() or "993")
    
    # 创建邮件读取器
    reader = EmailReader(email_address, password, imap_server, imap_port)
    
    # 测试连接
    print("\n" + "=" * 60)
    print("[测试连接...]")
    result = reader.connect()
    print(f"连接结果: {result}")
    
    if not result.get("success"):
        print("\n[错误] 连接失败，请检查邮箱地址和授权码是否正确")
        print("\n提示：")
        print("- QQ邮箱需要在设置中开启IMAP服务并获取授权码")
        print("- 163邮箱需要在设置中开启IMAP服务并设置授权码")
        print("- Gmail需要开启两步验证并生成应用专用密码")
        return
    
    print("\n[成功] 连接成功！")
    
    # 测试功能菜单
    while True:
        print("\n" + "=" * 60)
        print("[功能菜单]")
        print("=" * 60)
        print("1. 列出所有文件夹")
        print("2. 获取邮件列表")
        print("3. 获取未读邮件")
        print("4. 搜索邮件")
        print("5. 读取邮件内容")
        print("6. 标记邮件为已读")
        print("7. 删除邮件")
        print("0. 退出")
        
        choice = input("\n请选择功能 (0-7): ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            # 列出文件夹
            print("\n[列出所有文件夹...]")
            result = reader.list_folders()
            if result.get("success"):
                print(f"\n找到 {result['count']} 个文件夹：")
                for i, folder in enumerate(result['folders'], 1):
                    print(f"  {i}. {folder}")
            else:
                print(f"[错误] {result.get('error')}")
        
        elif choice == "2":
            # 获取邮件列表
            folder = input("文件夹名称 (默认INBOX): ").strip() or "INBOX"
            limit = int(input("获取数量 (默认10): ").strip() or "10")
            
            print(f"\n[获取 {folder} 中的邮件列表...]")
            result = reader.get_email_list(folder=folder, limit=limit)
            
            if result.get("success"):
                print(f"\n找到 {result['total']} 封邮件：")
                print("-" * 60)
                for i, email in enumerate(result['emails'], 1):
                    print(f"\n{i}. 主题: {email['subject']}")
                    print(f"   发件人: {email['from']}")
                    print(f"   日期: {email['date']}")
                    print(f"   ID: {email['id']}")
                    if email['has_attachment']:
                        print(f"   [有附件]")
            else:
                print(f"[错误] {result.get('error')}")
        
        elif choice == "3":
            # 获取未读邮件
            folder = input("文件夹名称 (默认INBOX): ").strip() or "INBOX"
            limit = int(input("获取数量 (默认10): ").strip() or "10")
            
            print(f"\n[获取 {folder} 中的未读邮件...]")
            result = reader.get_email_list(folder=folder, limit=limit, unread_only=True)
            
            if result.get("success"):
                print(f"\n找到 {result['total']} 封未读邮件：")
                print("-" * 60)
                for i, email in enumerate(result['emails'], 1):
                    print(f"\n{i}. 主题: {email['subject']}")
                    print(f"   发件人: {email['from']}")
                    print(f"   日期: {email['date']}")
                    print(f"   ID: {email['id']}")
            else:
                print(f"[错误] {result.get('error')}")
        
        elif choice == "4":
            # 搜索邮件
            criteria = input("搜索关键词: ").strip()
            folder = input("文件夹名称 (默认INBOX): ").strip() or "INBOX"
            limit = int(input("返回数量 (默认10): ").strip() or "10")
            
            print(f"\n[搜索包含 '{criteria}' 的邮件...]")
            result = reader.search_emails(criteria=criteria, folder=folder, limit=limit)
            
            if result.get("success"):
                print(f"\n找到 {result['total']} 封匹配的邮件：")
                print("-" * 60)
                for i, email in enumerate(result['emails'], 1):
                    print(f"\n{i}. 主题: {email['subject']}")
                    print(f"   发件人: {email['from']}")
                    print(f"   日期: {email['date']}")
                    print(f"   ID: {email['id']}")
            else:
                print(f"[错误] {result.get('error')}")
        
        elif choice == "5":
            # 读取邮件内容
            email_id = input("邮件ID: ").strip()
            folder = input("文件夹名称 (默认INBOX): ").strip() or "INBOX"
            
            print(f"\n[读取邮件内容...]")
            result = reader.get_email_content(email_id=email_id, folder=folder)
            
            if result.get("success"):
                email = result['email']
                print("\n" + "=" * 60)
                print(f"主题: {email['subject']}")
                print(f"发件人: {email['from']}")
                print(f"收件人: {email['to']}")
                if email['cc']:
                    print(f"抄送: {email['cc']}")
                print(f"日期: {email['date']}")
                print("=" * 60)
                print("\n正文内容：")
                print("-" * 60)
                print(email['body'][:500])  # 只显示前500字符
                if len(email['body']) > 500:
                    print(f"\n... (还有 {len(email['body']) - 500} 字符)")
                
                if email['attachments']:
                    print("\n[附件]：")
                    for att in email['attachments']:
                        print(f"  - {att['filename']} ({att['size']} bytes)")
            else:
                print(f"[错误] {result.get('error')}")
        
        elif choice == "6":
            # 标记为已读
            email_id = input("邮件ID: ").strip()
            folder = input("文件夹名称 (默认INBOX): ").strip() or "INBOX"
            
            print(f"\n[标记邮件为已读...]")
            result = reader.mark_as_read(email_id=email_id, folder=folder)
            
            if result.get("success"):
                print(f"[成功] {result['message']}")
            else:
                print(f"[错误] {result.get('error')}")
        
        elif choice == "7":
            # 删除邮件
            email_id = input("邮件ID: ").strip()
            folder = input("文件夹名称 (默认INBOX): ").strip() or "INBOX"
            
            confirm = input(f"确认删除邮件 {email_id}? (yes/no): ").strip().lower()
            if confirm == 'yes':
                print(f"\n[删除邮件...]")
                result = reader.delete_email(email_id=email_id, folder=folder)
                
                if result.get("success"):
                    print(f"[成功] {result['message']}")
                else:
                    print(f"[错误] {result.get('error')}")
            else:
                print("已取消删除")
    
    # 断开连接
    reader.disconnect()
    print("\n" + "=" * 60)
    print("[已断开连接，测试结束]")
    print("=" * 60)


if __name__ == "__main__":
    test_connection()
