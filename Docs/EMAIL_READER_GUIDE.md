# 邮件读取工具使用指南

## 功能概述

邮件读取工具（EmailReader）是一个通过IMAP协议读取邮箱内容的工具，支持以下功能：

- 连接到IMAP邮箱服务器
- 列出所有邮件文件夹
- 获取邮件列表（支持未读邮件筛选）
- 搜索邮件（按主题、发件人、正文搜索）
- 读取邮件详细内容
- 标记邮件为已读
- 删除邮件

## 文件说明

### 1. 核心工具文件
- **tools/email_reader.py**: 邮件读取工具核心实现
  - `EmailReader` 类：主要的邮件读取器
  - 支持多种邮箱服务器（QQ、163、Gmail等）

### 2. 测试文件
- **test_email_reader.py**: 交互式测试脚本
  - 提供菜单式操作界面
  - 支持手动输入邮箱信息进行测试
  
- **test_email_reader_auto.py**: 自动化测试脚本
  - 测试基本功能是否正常
  - 不需要真实邮箱信息

### 3. 启动脚本
- **run_email_test.bat**: Windows批处理脚本
  - 自动激活虚拟环境
  - 运行测试脚本

## 快速开始

### 方法1: 使用批处理脚本（推荐）

双击运行 `run_email_test.bat`，会自动：
1. 激活虚拟环境 `shitbot_env`
2. 运行测试脚本

### 方法2: 命令行运行

```bash
# 激活虚拟环境
D:\project\ShitBot_bata\shitbot_env\Scripts\activate

# 运行自动化测试
python test_email_reader_auto.py

# 运行交互式测试
python test_email_reader.py
```

## 使用示例

### 1. 基本使用

```python
from tools.email_reader import EmailReader

# 创建邮件读取器
reader = EmailReader(
    email_address="your_email@qq.com",
    password="your_auth_code",  # QQ邮箱使用授权码
    imap_server="imap.qq.com",
    imap_port=993
)

# 连接到邮箱
result = reader.connect()
if result["success"]:
    print("连接成功！")
    
    # 获取邮件列表
    emails = reader.get_email_list(limit=10)
    print(f"找到 {emails['total']} 封邮件")
    
    # 读取邮件内容
    if emails['emails']:
        email_id = emails['emails'][0]['id']
        content = reader.get_email_content(email_id)
        print(content['email']['subject'])
        print(content['email']['body'])
    
    # 断开连接
    reader.disconnect()
```

### 2. 搜索邮件

```python
# 搜索包含关键词的邮件
result = reader.search_emails(criteria="重要", limit=5)
for email in result['emails']:
    print(f"主题: {email['subject']}")
    print(f"发件人: {email['from']}")
```

### 3. 获取未读邮件

```python
# 只获取未读邮件
result = reader.get_email_list(unread_only=True, limit=10)
print(f"有 {result['total']} 封未读邮件")
```

## 常用邮箱配置

### QQ邮箱
- IMAP服务器: `imap.qq.com`
- 端口: `993`
- 密码: 需要使用**授权码**（不是QQ密码）
- 获取授权码: QQ邮箱设置 → 账户 → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务 → 开启IMAP服务 → 生成授权码

### 163邮箱
- IMAP服务器: `imap.163.com`
- 端口: `993`
- 密码: 需要使用**授权码**
- 获取授权码: 163邮箱设置 → POP3/SMTP/IMAP → 开启IMAP服务 → 设置授权码

### Gmail
- IMAP服务器: `imap.gmail.com`
- 端口: `993`
- 密码: 需要使用**应用专用密码**
- 前提: 开启两步验证
- 获取应用密码: Google账户 → 安全性 → 两步验证 → 应用专用密码

## API参考

### EmailReader类

#### 初始化参数
- `email_address` (str): 邮箱地址
- `password` (str): 邮箱密码或授权码
- `imap_server` (str): IMAP服务器地址
- `imap_port` (int): IMAP服务器端口，默认993

#### 主要方法

##### connect()
连接到IMAP服务器
- 返回: `Dict[str, Any]` - 包含success和message字段

##### disconnect()
断开与IMAP服务器的连接

##### list_folders()
列出所有邮件文件夹
- 返回: `Dict[str, Any]` - 包含folders列表

##### get_email_list(folder="INBOX", limit=10, unread_only=False)
获取邮件列表
- 参数:
  - `folder`: 邮件文件夹，默认"INBOX"
  - `limit`: 返回邮件数量限制
  - `unread_only`: 是否只获取未读邮件
- 返回: `Dict[str, Any]` - 包含emails列表

##### get_email_content(email_id, folder="INBOX")
获取邮件详细内容
- 参数:
  - `email_id`: 邮件ID
  - `folder`: 邮件文件夹
- 返回: `Dict[str, Any]` - 包含email详细信息

##### search_emails(criteria, folder="INBOX", limit=10)
搜索邮件
- 参数:
  - `criteria`: 搜索关键词
  - `folder`: 邮件文件夹
  - `limit`: 返回邮件数量限制
- 返回: `Dict[str, Any]` - 包含匹配的邮件列表

##### mark_as_read(email_id, folder="INBOX")
标记邮件为已读
- 参数:
  - `email_id`: 邮件ID
  - `folder`: 邮件文件夹
- 返回: `Dict[str, Any]` - 操作结果

##### delete_email(email_id, folder="INBOX")
删除邮件
- 参数:
  - `email_id`: 邮件ID
  - `folder`: 邮件文件夹
- 返回: `Dict[str, Any]` - 操作结果

## 注意事项

1. **授权码 vs 密码**: 大多数邮箱服务需要使用授权码而不是登录密码
2. **IMAP服务**: 需要在邮箱设置中开启IMAP服务
3. **安全性**: 不要在代码中硬编码邮箱密码，建议使用配置文件或环境变量
4. **编码问题**: 工具已处理UTF-8编码，支持中文邮件
5. **附件**: 当前版本可以检测附件，但不支持下载附件内容

## 下一步计划

- [ ] 集成到ShitBot主工具系统（tool.py）
- [ ] 添加下载附件功能
- [ ] 支持更多邮箱服务商
- [ ] 添加邮件分类和过滤功能
- [ ] 支持邮件移动和复制

## 故障排查

### 连接失败
- 检查邮箱地址是否正确
- 确认使用的是授权码而不是密码
- 确认IMAP服务已开启
- 检查网络连接

### 中文乱码
- 工具已自动处理UTF-8编码
- 如果仍有乱码，请检查邮件本身的编码

### 找不到邮件
- 确认文件夹名称正确（区分大小写）
- 尝试使用"INBOX"作为默认文件夹

## 更新日志

### v1.0.0 (2026-03-15)
- 初始版本发布
- 支持基本的邮件读取功能
- 支持QQ、163、Gmail等主流邮箱
