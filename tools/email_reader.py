"""
邮件读取工具
功能：通过IMAP协议读取邮箱中的邮件内容
支持：获取邮件列表、读取邮件详情、搜索邮件等
"""

import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
import imaplib


import base64


def imap_utf7_encode(s: str) -> str:
    """
    将字符串编码为 IMAP UTF-7 格式
    IMAP 使用修改版的 UTF-7 编码来支持非 ASCII 字符
    """
    result = []
    utf16_buffer = []
    
    for char in s:
        if ord(char) < 128:
            # ASCII 字符
            if utf16_buffer:
                # 先处理缓冲区中的 UTF-16 字符
                utf16_bytes = ''.join(utf16_buffer).encode('utf-16be')
                b64 = base64.b64encode(utf16_bytes).decode('ascii')
                b64 = b64.rstrip('=')  # 移除填充
                result.append('&' + b64 + '-')
                utf16_buffer = []
            if char == '&':
                result.append('&-')
            else:
                result.append(char)
        else:
            # 非 ASCII 字符，加入缓冲区
            utf16_buffer.append(char)
    
    # 处理剩余的 UTF-16 字符
    if utf16_buffer:
        utf16_bytes = ''.join(utf16_buffer).encode('utf-16be')
        b64 = base64.b64encode(utf16_bytes).decode('ascii')
        b64 = b64.rstrip('=')
        result.append('&' + b64 + '-')
    
    return ''.join(result)


def imap_utf7_decode(s: str) -> str:
    """
    解码 IMAP UTF-7 编码的字符串
    IMAP 使用修改版的 UTF-7 编码来支持非 ASCII 字符
    """
    result = []
    i = 0
    while i < len(s):
        if s[i] == '&':
            end = s.find('-', i)
            if end == -1:
                result.append(s[i])
                i += 1
            elif end == i + 1:
                result.append('&')
                i = end + 1
            else:
                base64_part = s[i+1:end]
                try:
                    padding = 4 - len(base64_part) % 4
                    if padding != 4:
                        base64_part += '=' * padding
                    decoded_bytes = base64_part.encode('ascii')
                    bytes_data = base64.b64decode(decoded_bytes)
                    result.append(bytes_data.decode('utf-16be'))
                except Exception:
                    result.append(s[i:end+1])
                i = end + 1
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)


class EmailReader:
    """邮件读取器"""
    
    def __init__(self, email_address: str, password: str, 
                 imap_server: str = "imap.qq.com", 
                 imap_port: int = 993):
        """
        初始化邮件读取器
        
        Args:
            email_address: 邮箱地址
            password: 邮箱密码或授权码
            imap_server: IMAP服务器地址
            imap_port: IMAP服务器端口
        """
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.connection = None
    
    def connect(self) -> Dict[str, Any]:
        """
        连接到IMAP服务器
        
        Returns:
            连接结果
        """
        try:
            # 添加 ID 命令到 imaplib（163邮箱需要）
            imaplib.Commands["ID"] = "AUTH"
            
            # 创建IMAP连接
            self.connection = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            # 登录
            self.connection.login(self.email_address, self.password)
            
            # 发送 IMAP ID 命令（163邮箱需要，否则会报 Unsafe Login 错误）
            args = ("name", "ShitBot", "contact", self.email_address, "version", "1.0.0", "vendor", "shitbot")
            typ, dat = self.connection._simple_command('ID', '("' + '" "'.join(args) + '")')
            self.connection._untagged_response(typ, dat, 'ID')
            
            return {
                "success": True,
                "message": f"成功连接到 {self.imap_server}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"连接失败: {str(e)}"
            }
    
    def disconnect(self):
        """断开连接"""
        try:
            if self.connection:
                self.connection.close()
                self.connection.logout()
        except Exception:
            pass
    
    def _decode_str(self, s: str) -> str:
        """解码邮件头字符串"""
        if s is None:
            return ""
        
        decoded_list = decode_header(s)
        result = []
        for content, charset in decoded_list:
            if isinstance(content, bytes):
                if charset:
                    try:
                        result.append(content.decode(charset))
                    except:
                        result.append(content.decode('utf-8', errors='ignore'))
                else:
                    result.append(content.decode('utf-8', errors='ignore'))
            else:
                result.append(str(content))
        
        return ''.join(result)
    
    def _get_email_body(self, msg) -> str:
        """获取邮件正文"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # 跳过附件
                if "attachment" in content_disposition:
                    continue
                
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        try:
                            body = payload.decode(charset, errors='ignore')
                        except:
                            body = payload.decode('utf-8', errors='ignore')
                        
                        # 如果是HTML，提取纯文本
                        if content_type == "text/html":
                            body = re.sub(r'<[^>]+>', '', body)
                        
                        if body.strip():
                            break
                except Exception:
                    continue
        else:
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    charset = msg.get_content_charset() or 'utf-8'
                    body = payload.decode(charset, errors='ignore')
                    
                    content_type = msg.get_content_type()
                    if content_type == "text/html":
                        body = re.sub(r'<[^>]+>', '', body)
            except Exception:
                pass
        
        return body.strip()
    
    def list_folders(self) -> Dict[str, Any]:
        """
        列出所有邮件文件夹
        
        Returns:
            文件夹列表
        """
        try:
            if not self.connection:
                return {"success": False, "error": "未连接到服务器"}
            
            status, folders = self.connection.list()
            
            if status != 'OK':
                return {"success": False, "error": "获取文件夹列表失败"}
            
            folder_list = []
            raw_folders = []  # 保存原始文件夹名称用于选择
            for folder in folders:
                folder_str = folder.decode('utf-8')
                # 提取文件夹名称
                # IMAP 文件夹格式: (\HasNoChildren) "/" "文件夹名"
                # 或: (\HasNoChildren) "." "文件夹名"
                parts = folder_str.split('"')
                if len(parts) >= 3:
                    folder_name = parts[-2]
                    raw_folders.append(folder_name)
                    # 解码 UTF-7 编码
                    decoded_name = imap_utf7_decode(folder_name)
                    folder_list.append(decoded_name)
            
            return {
                "success": True,
                "folders": folder_list,
                "raw_folders": raw_folders,
                "count": len(folder_list)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_email_list(self, folder: str = "INBOX", limit: int = 10, 
                       unread_only: bool = False) -> Dict[str, Any]:
        """
        获取邮件列表
        
        Args:
            folder: 邮件文件夹，默认为收件箱
            limit: 返回邮件数量限制
            unread_only: 是否只获取未读邮件
        
        Returns:
            邮件列表
        """
        try:
            if not self.connection:
                return {"success": False, "error": "未连接到服务器"}
            
            # 选择文件夹
            status, data = self.connection.select(folder)
            if status != 'OK':
                error_msg = data[0].decode('utf-8') if data else "未知错误"
                return {"success": False, "error": f"无法打开文件夹 '{folder}': {error_msg}"}
            
            # 搜索邮件
            if unread_only:
                status, messages = self.connection.search(None, 'UNSEEN')
            else:
                status, messages = self.connection.search(None, 'ALL')
            
            if status != 'OK':
                return {"success": False, "error": "搜索邮件失败"}
            
            email_ids = messages[0].split()
            
            # 获取最新的N封邮件
            email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            email_ids = list(reversed(email_ids))  # 最新的在前面
            
            email_list = []
            for email_id in email_ids:
                status, msg_data = self.connection.fetch(email_id, '(RFC822)')
                
                if status != 'OK':
                    continue
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # 解析邮件信息
                        subject = self._decode_str(msg.get('Subject', ''))
                        from_addr = self._decode_str(msg.get('From', ''))
                        to_addr = self._decode_str(msg.get('To', ''))
                        date_str = msg.get('Date', '')
                        
                        # 解析发件人
                        _, from_email = parseaddr(from_addr)
                        
                        email_info = {
                            "id": email_id.decode('utf-8'),
                            "subject": subject,
                            "from": from_addr,
                            "from_email": from_email,
                            "to": to_addr,
                            "date": date_str,
                            "has_attachment": self._has_attachment(msg)
                        }
                        
                        email_list.append(email_info)
            
            return {
                "success": True,
                "folder": folder,
                "total": len(email_ids),
                "emails": email_list
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _has_attachment(self, msg) -> bool:
        """检查邮件是否有附件"""
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                return True
        return False
    
    def get_email_content(self, email_id: str, folder: str = "INBOX") -> Dict[str, Any]:
        """
        获取邮件详细内容
        
        Args:
            email_id: 邮件ID
            folder: 邮件文件夹
        
        Returns:
            邮件详细内容
        """
        try:
            if not self.connection:
                return {"success": False, "error": "未连接到服务器"}
            
            # 选择文件夹
            status, data = self.connection.select(folder)
            if status != 'OK':
                return {"success": False, "error": f"无法打开文件夹: {folder}"}
            
            # 获取邮件
            status, msg_data = self.connection.fetch(email_id.encode(), '(RFC822)')
            
            if status != 'OK':
                return {"success": False, "error": "获取邮件失败"}
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # 解析邮件信息
                    subject = self._decode_str(msg.get('Subject', ''))
                    from_addr = self._decode_str(msg.get('From', ''))
                    to_addr = self._decode_str(msg.get('To', ''))
                    cc_addr = self._decode_str(msg.get('Cc', ''))
                    date_str = msg.get('Date', '')
                    
                    # 解析发件人
                    from_name, from_email = parseaddr(from_addr)
                    
                    # 获取邮件正文
                    body = self._get_email_body(msg)
                    
                    # 获取附件信息
                    attachments = []
                    for part in msg.walk():
                        if part.get_content_disposition() == 'attachment':
                            filename = self._decode_str(part.get_filename())
                            if filename:
                                attachments.append({
                                    "filename": filename,
                                    "content_type": part.get_content_type(),
                                    "size": len(part.get_payload(decode=True))
                                })
                    
                    return {
                        "success": True,
                        "email": {
                            "id": email_id,
                            "subject": subject,
                            "from": from_addr,
                            "from_name": self._decode_str(from_name),
                            "from_email": from_email,
                            "to": to_addr,
                            "cc": cc_addr,
                            "date": date_str,
                            "body": body,
                            "attachments": attachments,
                            "has_attachment": len(attachments) > 0
                        }
                    }
            
            return {"success": False, "error": "未找到邮件"}
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_emails(self, criteria: str, folder: str = "INBOX", 
                      limit: int = 10) -> Dict[str, Any]:
        """
        搜索邮件
        
        Args:
            criteria: 搜索条件（支持主题、发件人等）
            folder: 邮件文件夹
            limit: 返回邮件数量限制
        
        Returns:
            搜索结果
        """
        try:
            if not self.connection:
                return {"success": False, "error": "未连接到服务器"}
            
            # 选择文件夹
            status, data = self.connection.select(folder)
            if status != 'OK':
                return {"success": False, "error": f"无法打开文件夹: {folder}"}
            
            # 构建搜索条件
            # 支持搜索主题、发件人、正文
            search_criteria = f'(OR OR SUBJECT "{criteria}" FROM "{criteria}" BODY "{criteria}")'
            
            status, messages = self.connection.search(None, search_criteria)
            
            if status != 'OK':
                return {"success": False, "error": "搜索失败"}
            
            email_ids = messages[0].split()
            
            # 限制返回数量
            email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            email_ids = list(reversed(email_ids))
            
            email_list = []
            for email_id in email_ids:
                status, msg_data = self.connection.fetch(email_id, '(RFC822)')
                
                if status != 'OK':
                    continue
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        subject = self._decode_str(msg.get('Subject', ''))
                        from_addr = self._decode_str(msg.get('From', ''))
                        _, from_email = parseaddr(from_addr)
                        date_str = msg.get('Date', '')
                        
                        email_info = {
                            "id": email_id.decode('utf-8'),
                            "subject": subject,
                            "from": from_addr,
                            "from_email": from_email,
                            "to": self._decode_str(msg.get('To', '')),
                            "date": date_str
                        }
                        
                        email_list.append(email_info)
            
            return {
                "success": True,
                "criteria": criteria,
                "folder": folder,
                "total": len(email_ids),
                "emails": email_list
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_email(self, email_id: str, folder: str = "INBOX") -> Dict[str, Any]:
        """
        删除邮件
        
        Args:
            email_id: 邮件ID
            folder: 邮件文件夹
        
        Returns:
            删除结果
        """
        try:
            if not self.connection:
                return {"success": False, "error": "未连接到服务器"}
            
            # 选择文件夹
            status, data = self.connection.select(folder)
            if status != 'OK':
                return {"success": False, "error": f"无法打开文件夹: {folder}"}
            
            # 标记为删除
            self.connection.store(email_id.encode(), '+FLAGS', '\\Deleted')
            
            # 执行删除
            self.connection.expunge()
            
            return {
                "success": True,
                "message": f"邮件 {email_id} 已删除"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def mark_as_read(self, email_id: str, folder: str = "INBOX") -> Dict[str, Any]:
        """
        标记邮件为已读
        
        Args:
            email_id: 邮件ID
            folder: 邮件文件夹
        
        Returns:
            操作结果
        """
        try:
            if not self.connection:
                return {"success": False, "error": "未连接到服务器"}
            
            # 选择文件夹
            status, data = self.connection.select(folder)
            if status != 'OK':
                return {"success": False, "error": f"无法打开文件夹: {folder}"}
            
            # 标记为已读
            self.connection.store(email_id.encode(), '-FLAGS', '\\Seen')
            
            return {
                "success": True,
                "message": f"邮件 {email_id} 已标记为已读"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


def test_email_reader():
    """测试邮件读取功能"""
    # 这里需要填写实际的邮箱信息
    email_address = "your_email@qq.com"  # 替换为实际邮箱
    password = "your_auth_code"  # 替换为授权码
    
    reader = EmailReader(email_address, password)
    
    # 测试连接
    print("=" * 50)
    print("测试连接...")
    result = reader.connect()
    print(f"连接结果: {result}")
    
    if not result.get("success"):
        print("连接失败，测试终止")
        return
    
    # 测试列出文件夹
    print("\n" + "=" * 50)
    print("测试列出文件夹...")
    result = reader.list_folders()
    print(f"文件夹列表: {result}")
    
    # 测试获取邮件列表
    print("\n" + "=" * 50)
    print("测试获取邮件列表...")
    result = reader.get_email_list(limit=5)
    print(f"邮件列表: {result}")
    
    # 测试搜索邮件
    print("\n" + "=" * 50)
    print("测试搜索邮件...")
    result = reader.search_emails("测试", limit=3)
    print(f"搜索结果: {result}")
    
    # 断开连接
    reader.disconnect()
    print("\n" + "=" * 50)
    print("测试完成，已断开连接")


if __name__ == "__main__":
    test_email_reader()
