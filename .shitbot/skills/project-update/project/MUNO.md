# ShitBot 项目目录说明

## 项目根目录结构

```
ShitBot/
├── config/                 # 配置文件目录
│   ├── __init__.py
│   ├── config.py           # 配置管理模块
│   ├── config.example.yaml # 配置文件模板
│   ├── models.json         # 支持的 AI 平台列表
│   └── common_models.json  # 常用模型列表
├── src/                    # 源代码目录
│   ├── __init__.py
│   ├── ai.py               # AI 客户端
│   ├── bot.py              # 机器人核心逻辑
│   ├── init_project.py     # 项目初始化脚本
│   ├── log.py              # 日志管理
│   ├── main.py             # 主程序入口
│   ├── memory.py           # 记忆管理
│   ├── prompt.py           # 提示词管理
│   ├── read_models.py      # 模型读取
│   ├── terminal.py         # 终端界面
│   ├── token_tracker.py    # Token 追踪
│   ├── tool.py             # 工具定义和执行
│   ├── ui_components.py    # UI 组件
│   └── workflows.py         # 工作流管理
├── tools/                  # 工具模块目录（保持原有结构）
│   ├── bocha.py            # 博查搜索
│   ├── doc.py              # 文档管理
│   ├── email_reader.py     # 邮件读取（IMAP）
│   ├── mcp_client.py        # MCP客户端
│   ├── memory_bot.py       # 记忆机器人
│   ├── playwiright.py      # 浏览器自动化
│   ├── role.py             # 角色管理
│   ├── safe.py             # 安全检查
│   ├── skill.py            # 技能管理
│   ├── tavily_api.py       # Tavily 搜索
│   ├── timer.py            # 定时任务
│   ├── venv_manager.py     # 虚拟环境管理
│   ├── webbot.py           # WebBot浏览器操作
│   └── __init__.py
├── .shitbot/               # ShitBot 核心数据目录
│   ├── docs/               # 内置文档
│   ├── skills/             # 技能目录
│   │   └── project-update/ # 项目更新技能
│   │       └── project/    # 工作文件
│   │           ├── LOG.md  # 更新日志（本文件）
│   │           └── MUNO.md # 目录说明
│   ├── roles/              # 角色目录
│   ├── workfile/           # 工作文件目录
│   ├── memory/             # 记忆存储（运行时生成）
│   ├── logs/               # 运行日志（运行时生成）
│   └── datas/              # 数据文件（运行时生成）
├── cli.py                  # CLI命令行入口
├── pyproject.toml          # 项目配置（包含CLI脚本声明）
├── requirements.txt        # 依赖列表
├── README_CN.md            # 中文说明文档
├── README_EN.md            # 英文说明文档
├── .gitignore              # Git 忽略规则
└── shitbot.bat             # Windows启动脚本
```

## 核心文件说明

### CLI入口
- **cli.py**: 命令行入口，使用Click框架，支持子命令
  - `shitbot` - 默认启动交互式对话
  - `shitbot config` - 运行配置向导
  - `shitbot chat` / `shitbot -m` - 单次对话模式

### 主程序文件（src/）
- **src/main.py**: 程序入口，启动终端界面
- **src/bot.py**: 机器人核心逻辑，处理对话和工具调用
- **src/ai.py**: AI客户端，处理与AI API的通信
- **src/tool.py**: 工具定义和执行，包含所有可用工具的实现

### 配置文件（config/）
- **config/config.py**: 配置管理模块，包含SMTP和IMAP邮件配置
- **config/config.example.yaml**: 配置文件模板
- **config/models.json**: 支持的AI平台和模型列表

### 功能模块
- **src/memory.py**: 共享记忆管理
- **src/prompt.py**: 提示词管理
- **src/terminal.py**: 终端界面
- **src/ui_components.py**: UI组件
- **src/log.py**: 日志管理
- **src/token_tracker.py**: Token使用追踪
- **src/workflows.py**: 工作流管理

### 工具模块（tools/）

### bocha.py
- 博查搜索API客户端
- 提供网络搜索功能

### doc.py
- 文档管理系统
- 管理内置文档的读取和查询

### email_reader.py（新增）
- 邮件读取工具
- 基于IMAP协议读取邮箱内容
- 支持功能：
  - 列出邮箱文件夹
  - 获取邮件列表（支持未读筛选）
  - 读取邮件详细内容
  - 搜索邮件（按主题、发件人、正文）
  - 标记邮件为已读
- 支持QQ、163、Gmail等主流邮箱

### memory_bot.py
- 记忆机器人
- 处理对话记忆的保存和检索

### playwiright.py
- 浏览器自动化
- 基于Playwright的网页操作

### role.py
- 角色管理
- 加载和管理角色配置

### safe.py
- 安全检查
- 路径安全验证

### skill.py
- 技能管理
- 加载和管理技能配置

### tavily_api.py
- Tavily搜索API
- 备用搜索服务

### timer.py
- 定时任务管理
- 支持一次性、周期性、每日任务

### venv_manager.py
- 虚拟环境管理
- Python代码执行环境

### webbot.py
- WebBot浏览器操作助手
- 提供浏览器任务执行功能

---

*最后更新: 2026-03-28*
