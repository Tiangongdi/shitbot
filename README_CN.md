# ShitBot 💩

<div align="center">

<<<<<<< HEAD
**💩 一个功能强大的 AI 智能助手终端应用 💩**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

***
=======
**💩一个功能强大的 AI 智能助手终端应用💩**


</div>

---
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

## 📖 目录

- [项目简介](#项目简介)
- [核心特性](#核心特性)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
<<<<<<< HEAD
- [命令行使用](#命令行使用)
=======
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
- [配置说明](#配置说明)
- [工具模块](#工具模块)
- [技能系统](#技能系统)
- [角色系统](#角色系统)
<<<<<<< HEAD
- [安全机制](#安全机制)
=======
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
- [使用示例](#使用示例)
- [项目结构](#项目结构)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)

<<<<<<< HEAD
***

## 🎯 项目简介

ShitBot 是一个功能强大的 AI 智能助手终端应用，支持 15+ 种主流 AI API 平台，具备完整的浏览器自动化、文件操作、定时任务、邮件收发、代码执行等能力。用户可以通过类似 Claude Code 的终端界面与 AI 进行自然对话，并指示 AI 完成各种复杂任务。

**主要亮点：**

- 🤖 支持 15+ 种 AI 平台（智谱AI、DeepSeek、Kimi、OpenAI、Claude、Gemini 等）
- 🌐 完整的浏览器自动化能力（Playwright + WebBot）
- 📁 强大的文件操作功能
- ⏰ 灵活的定时任务系统
- 📧 邮件收发功能（SMTP 发送 + IMAP 读取）
- 💾 智能记忆管理
- 📚 内置文档系统
- 🔧 可扩展的技能系统（Skills）
- 🎭 灵活的角色系统
- 🐍 Python 代码执行能力
- 🛡️ 完善的安全防护机制
- 🎨 现代化终端界面
- ⌨️ 支持命令行界面（CLI），可安装后全局使用

***
=======
---

## 🎯 项目简介

ShitBot 是一个功能强大的 AI 智能助手终端应用，支持多种 AI API（智谱AI、博查），具备完整的浏览器自动化、文件操作、定时任务、邮件发送等能力。用户可以通过类似 Claude Code 的终端界面与 AI 进行自然对话，并指示 AI 完成各种复杂任务。

**主要亮点：**
- 🤖 多 AI 提供商支持（智谱AI GLM、博查搜索）
- 🌐 完整的浏览器自动化能力
- 📁 强大的文件操作功能
- ⏰ 灵活的定时任务系统
- 📧 邮件发送功能
- 💾 智能记忆管理
- 📚 内置文档系统
- 🔧 可扩展的技能系统（Skills）
- 🎭 灵活的角色系统（Roles）
- 🎨 现代化终端界面

---
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

## ✨ 核心特性

### 🤖 多 AI 提供商支持
<<<<<<< HEAD

支持国内外 15+ 种主流 AI 平台，通过 OpenAI SDK 兼容接口统一调用，轻松切换：

| 类型      | 平台                   | 标识            |
| ------- | -------------------- | ------------- |
| 🇨🇳 国内 | 智谱AI (GLM)           | `zai`         |
| 🇨🇳 国内 | DeepSeek 深度求索        | `deepseek`    |
| 🇨🇳 国内 | Moonshot (Kimi) 月之暗面 | `moonshot`    |
| 🇨🇳 国内 | MiniMax              | `minimax`     |
| 🇨🇳 国内 | 小米 (MiMo)            | `xiaomi_mimo` |
| 🇨🇳 国内 | 火山引擎                 | `volcengine`  |
| 🇨🇳 国内 | 阿里云 (DashScope)      | `dashscope`   |
| 🌍 国际   | OpenAI (ChatGPT)     | `openai`      |
| 🌍 国际   | Anthropic (Claude)   | `anthropic`   |
| 🌍 国际   | Google (Gemini)      | `gemini`      |
| 🌍 国际   | Cohere               | `cohere`      |
| 🌍 国际   | Mistral              | `mistral`     |
| 🌍 国际   | Groq                 | `groq`        |
| 🌍 国际   | Perplexity           | `perplexity`  |
| 🌍 国际   | OpenRouter           | `openrouter`  |

> 💡 所有平台均通过 OpenAI SDK 兼容接口调用，只需配置对应的 `api_key`、`base_url` 和 `model` 即可使用。详细配置请参考 `.shitbot/docs/AI_API_Platforms_OpenAI_SDK_Compatible` 文档。

### 🌐 浏览器自动化

=======
- **推荐**智谱AI (GLM)：支持 GLM-4、GLM-5 等模型
- **博查搜索**：专业的网络搜索 API
- 流式响应支持
- 轻松切换提供商

### 🌐 浏览器自动化
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
- 基于 Playwright 的可视化浏览器控制
- 网页导航和交互
- 智能内容提取和总结
- 表单填写和搜索
- 页面截图功能
- JavaScript 执行

### 📁 文件操作
<<<<<<< HEAD

- 文件读写操作
- 文件追加内容
=======
- 文件读写操作
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
- 文件复制和移动
- 目录创建和管理
- 安全的文件删除（需用户确认）
- 禁止路径保护机制

<<<<<<< HEAD
### 🐍 代码执行

- 运行 Python 代码片段
- 执行 Python 代码文件
- 实时代码测试和验证

### ⏰ 定时任务系统

- 一次性延迟执行
- 周期性执行
- 每日定时执行
- 任务管理（暂停、恢复、取消）

### 📧 邮件系统

- **发送**：SMTP 协议，支持 TLS/SSL 加密
- **读取**：IMAP 协议，支持文件夹浏览、邮件搜索、内容获取
- 支持多种邮箱服务（163、Gmail 等）

### 💾 智能记忆管理

- 对话记忆保存
- 历史记忆检索
- 智能记忆总结
- 工作文件系统（笔记、待办、用户画像）

### 📚 文档系统

=======
### ⏰ 定时任务系统
- 一次性延迟执行
- 周期性任务执行
- 每日定时执行
- 任务管理（暂停、恢复、取消）

### 📧 邮件发送
- 支持 SMTP 协议
- TLS/SSL 加密
- 支持多种邮箱服务

### 💾 智能记忆管理
- 对话记忆保存
- 历史记忆检索
- 智能记忆总结

### 📚 文档系统
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
- 内置工具使用文档
- 快速查阅指南
- 分模块文档管理

### 🔧 技能系统（Skills）
<<<<<<< HEAD

- 模块化技能扩展，按需加载
- 自定义技能开发
- 内置技能创建工具
- 支持 ClawHub 公共技能库搜索安装

### 🎭 角色系统（Roles）

- 自定义角色设置
- 角色之间的灵活切换
- 内置代码编写角色
- 角色特定行为和工具推荐

### 🛡️ 安全机制

- 高危操作拦截（数据库删除、关机、提权等）
- 定时任务安全审查
- 文件删除强制确认
- API 密钥保护
- 禁止路径保护
- 提示注入防护

### 🎨 现代化终端界面

=======
- 支持 Claude Code 的 Skill 格式
- 自定义技能开发
- 模块化能力扩展
- 内置多种实用技能

### 🎭 角色系统（Roles）
- 支持自定义角色设置
- 角色之间的灵活切换
- 专业领域角色支持
- 角色特定行为和工具推荐

### 🎨 现代化终端界面
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
- 类 Claude Code 的交互体验
- 彩色输出和格式化显示
- 聊天历史记录

<<<<<<< HEAD
***
=======
---
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

## 💻 环境要求

- **Python**: 3.8 或更高版本
<<<<<<< HEAD
- **操作系统**: Windows 10/11（主要测试环境）
- **浏览器**: Microsoft Edge (Chromium 版本)
- **网络**: 稳定的网络连接
- **API 密钥**: 至少一个 AI 平台的 API 密钥（见上方支持平台列表）

***
=======
- **操作系统**: Windows 10/11（已在 Windows 环境测试）
- **浏览器**: Microsoft Edge (Chromium 版本)
- **网络**: 稳定的网络连接
- **API 密钥**: 智谱AI 和/或 博查 API 密钥

---
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

## 🚀 快速开始

### 1. 克隆项目

```bash
<<<<<<< HEAD
git clone https://github.com/Tiangongdi/shitbot.git
cd shitbot
=======
git clone https://gitee.com/shitbot/shit-bot.git
cd ShitBot
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
```

### 2. 创建虚拟环境

```bash
<<<<<<< HEAD
=======
# 在项目根目录下执行
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
python -m venv shitbot_env
```

### 3. 激活虚拟环境

```bash
# Windows
.\shitbot_env\Scripts\activate

# Linux/Mac
source shitbot_env/bin/activate
```

<<<<<<< HEAD
### 4. 安装依赖和 CLI 工具

```bash
pip install -r requirements.txt
# 安装 CLI 命令（可全局调用 shitbot 命令）
pip install -e .
```

### 5. 初始化配置

你可以选择手动配置或者使用配置向导：

**方式一：使用配置向导（推荐）**

```bash
shitbot config
```

执行后会提示选择 AI 平台、输入 API 密钥、智能体信息等，自动生成配置文件。

**方式二：手动复制配置模板**

```bash
# 复制配置模板
cp .env.example .env
# 如果你使用 config.yaml 格式：
cp config.example.yaml config.yaml
# 复制智能体信息模板
cp .shitbot/Self.example.txt .shitbot/Self.txt
```

然后编辑配置文件填入你的 API 密钥和其他配置。

### 6. 启动程序

**方式一：使用 CLI 命令（推荐）**

```bash
shitbot shitbot
```

**方式二：直接运行 Python 脚本**

```bash
python src/main.py
```

***

## ⌨️ 命令行使用

ShitBot 提供了完整的命令行界面（CLI），安装后可以全局使用 `shitbot` 命令。

### 可用命令

| 命令 | 说明 |
|------|------|
| `shitbot shitbot` | 启动交互式对话（默认方式） |
| `shitbot shitbot -m "你的问题"` | 执行单次对话，直接输出结果 |
| `shitbot config` | 运行配置向导，初始化配置 |

### 命令详解

#### 1. 启动交互式对话

```bash
shitbot shitbot
```

进入交互式对话模式，你可以持续和 ShitBot 对话，就像在 Claude Code 中一样。

#### 2. 单次对话模式

```bash
shitbot shitbot -m "帮我计算 1+1 等于多少"
shitbot shitbot -m "搜索一下今天的 AI 新闻"
shitbot shitbot -m "读取当前目录下的 README.md 文件并总结内容"
```

适合用于脚本调用或者快速查询，执行完直接输出结果然后退出。

#### 3. 配置向导

```bash
shitbot config
```

交互式配置向导，引导你完成 AI 平台选择、API 密钥输入、智能体信息设置等，自动生成配置文件。

### 使用示例

```bash
# 启动交互式聊天
shitbot shitbot

# 单次提问
shitbot shitbot -m "当前目录有哪些文件？"

# 重新运行配置向导
shitbot config
```

***
## ⚙️ 配置说明

### 配置方式

ShitBot 支持两种配置方式：

**1. 环境变量方式（推荐，通过 `shitbot config` 生成）**
- 使用 `.env` 文件存储配置
- 更符合现代开发习惯，方便容器部署

**2. YAML 配置文件方式**
- 使用 `config.yaml` 存储配置
- 兼容旧版本配置格式

### 完整配置项

主要配置项如下：

```env
# AI 提供商配置
AI_API_KEY=your-api-key-here
AI_VALUE=deepseek
AI_MODEL=deepseek-chat
AI_BASE_URL=

# 博查搜索配置
BOCHA_API_KEY=
BOCHA_BASE_URL=

# Tavily 搜索配置
TAVILY_KEY=

# 网页搜索配置
WEB_SEARCH_ID=2

# 邮件发送配置（SMTP）
EMAIL_FROM=your-email@example.com
EMAIL_PASSWORD=your-email-password
EMAIL_SMTP_SERVER=smtp.example.com
EMAIL_SMTP_PORT=465
EMAIL_USE_TLS=true

# 邮件读取配置（IMAP）
IMAP_EMAIL=your-email@example.com
IMAP_PASSWORD=your-email-password
IMAP_SERVER=imap.example.com
IMAP_PORT=993
IMAP_USE_SSL=true
```

或者 YAML 格式：

```yaml
# AI 提供商配置（支持 15+ 种平台，详见 models.json）
ai:
  api_key: ""           # AI API密钥（必填）
  value: ""             # API平台标识（如 zai/deepseek/moonshot/openai 等）
  model: ""             # 模型名称（如 glm-5-turbo、deepseek-chat 等）
  base_url: ""          # 自定义 API 地址（可选，留空使用默认）

# 博查搜索配置
bocha:
  api_key: ""           # 博查 API密钥
  base_url: ""          # API 地址
  index_name: "news"    # 搜索索引

# Tavily 搜索配置
tavily:
  key: ""               # Tavily API密钥

# 网页搜索配置
web_search:
  web_search_ID: 2      # 搜索引擎选择（1=博查, 2=Tavily）

# 浏览器配置
browser:
  playwright_browsers_path: ""  # Playwright 浏览器路径
=======
### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置项目环境

**⚠️ 重要：启动程序前必须先运行此步骤！**

执行 `init_project.py` 初始化项目环境，该脚本会：
- 创建必要的配置文件
- 提示您输入 API 密钥（智谱AI、博查）
- 设置用户偏好
- 配置邮件设置（可选）

```bash
python init_project.py
```

### 6. 启动程序

完成环境配置后，即可启动程序：

```bash
python main.py
```

---

## ⚙️ 配置说明

### 完整配置文件结构

```yaml
# AI 提供商配置
ai:
  api_key: ""           # 智谱AI API密钥（必填）
  value: ""             # API平台 名称
  model: "glm-5"        # 模型名称

# 博查搜索配置
bocha:
  api_key: ""           # 博查 API密钥（必填）
  base_url: ""          # API 地址
  index_name: "news"    # 搜索索引

# 浏览器配置
browser:
  playwright_browsers_path: "D:\\playwright_browsers"  # Playwright 浏览器路径
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

# 默认提供商
default_provider: "ai"

<<<<<<< HEAD
# 邮件发送配置（SMTP）
email:
  email: ""             # 发件邮箱
  password: ""          # 邮箱授权码
  smtp_server: ""       # SMTP 服务器
  smtp_port: 465        # SMTP 端口
  use_tls: true         # 是否使用 TLS

# 邮件读取配置（IMAP）
imap:
  email: ""             # 邮箱地址
  password: ""          # 邮箱授权码
  imap_server: ""       # IMAP 服务器
  imap_port: 993        # IMAP 端口
  use_ssl: true         # 是否使用 SSL

# 禁止访问路径
stop:
  file: []
```

### 智能体信息配置

编辑 `.shitbot/Self.txt` 自定义智能体身份：

```
# ShitBot Self-Information File

## Name: 你的智能体名称
## Personality: 性格描述
## User: 你的用户名
## User Introduction: 用户简介
=======
# 邮件配置
email:
  email: "your_email@163.com"      # 发件邮箱
  password: "your_password"         # 邮箱授权码
  smtp_server: "smtp.163.com"       # SMTP 服务器
  smtp_port: 465                    # SMTP 端口
  use_tls: true                     # 是否使用 TLS

# 禁止访问路径
stop:
  file: []  # 禁止访问的文件路径列表

# 用户配置
user:
  bot_name: "偷摸零"                 # AI 助手名称
  user_name: "黎大白"                # 用户名称
  bot_prompt: "你会经常说咕咕嘎嘎（企鹅叫）"  # AI 个性设定
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
```

### API 密钥获取

<<<<<<< HEAD
| 平台                 | 地址                                                        | 说明            |
| ------------------ | --------------------------------------------------------- | ------------- |
| 智谱AI               | [open.bigmodel.cn](https://open.bigmodel.cn/)             | 注册后申请 API 密钥  |
| DeepSeek           | [platform.deepseek.com](https://platform.deepseek.com/)   | 注册后获取 API Key |
| Moonshot (Kimi)    | [platform.moonshot.cn](https://platform.moonshot.cn/)     | 注册后申请 API 密钥  |
| MiniMax            | [platform.minimaxi.com](https://platform.minimaxi.com/)   | 注册后获取 API Key |
| 小米 (MiMo)          | [platform.mimaxi.com](https://platform.mimaxi.com/)       | 注册后获取 API Key |
| 火山引擎               | [console.volcengine.com](https://console.volcengine.com/) | 注册后申请 API 密钥  |
| 阿里云 (DashScope)    | [dashscope.aliyun.com](https://dashscope.aliyun.com/)     | 注册后申请 API 密钥  |
| OpenAI             | [platform.openai.com](https://platform.openai.com/)       | 注册后获取 API Key |
| Anthropic (Claude) | [console.anthropic.com](https://console.anthropic.com/)   | 注册后获取 API Key |
| Google (Gemini)    | [ai.google.dev](https://ai.google.dev/)                   | 注册后获取 API Key |
| 博查搜索               | [api.bocha.com](https://api.bocha.com/)                   | 注册后申请 API 密钥  |
| Tavily             | [tavily.com](https://tavily.com/)                         | 注册后获取 API Key |

> 💡 更多平台的详细配置（`base_url`、模型名称等）请参考 `.shitbot/docs/AI_API_Platforms_OpenAI_SDK_Compatible` 文档。

***
=======
**智谱AI**
1. 访问 [智谱AI 开放平台](https://open.bigmodel.cn/)
2. 注册账号并申请 API 密钥
3. 将密钥填入配置文件的 `ai.api_key`

**博查搜索**
1. 访问 [博查 API 官网](https://api.bocha.com/)
2. 注册账号并申请 API 密钥
3. 将密钥填入配置文件的 `bocha.api_key`

---

>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
## 🛠️ 工具模块

ShitBot 提供了丰富的工具模块，每个模块都有详细的使用文档：

<<<<<<< HEAD
### 🔧 工具概览

#### 🌐 网络搜索模块

| 工具            | 说明              |
| ------------- | --------------- |
| `search_web`  | 网络搜索            |
| `webbot_task` | 浏览器任务执行（WebBot） |

#### 📁 文件操作模块

| 工具                | 说明        |
| ----------------- | --------- |
| `read_file`       | 读取文件      |
| `write_file`      | 写入文件      |
| `append_to_file`  | 追加文件内容    |
| `copy_file`       | 复制文件      |
| `move_file`       | 移动文件      |
| `delete_file`     | 删除文件（需确认） |
| `create_dir`      | 创建目录      |
| `get_dir_content` | 获取目录内容    |

#### 🐍 代码执行模块

| 工具              | 说明             |
| --------------- | -------------- |
| `run_code`      | 运行 Python 代码片段 |
| `run_code_file` | 运行 Python 代码文件 |

#### 💻 系统命令模块

| 工具              | 说明          |
| --------------- | ----------- |
| `shell_command` | 执行 shell 命令 |

#### 📧 邮件模块

| 工具                   | 说明         |
| -------------------- | ---------- |
| `send_email`         | 发送邮件（SMTP） |
| `list_email_folders` | 列出邮箱文件夹    |
| `get_email_list`     | 获取邮件列表     |
| `get_email_content`  | 获取邮件详细内容   |
| `search_emails`      | 搜索邮件       |
| `mark_email_read`    | 标记邮件为已读    |

#### ⏰ 定时任务模块

| 工具             | 说明       |
| -------------- | -------- |
| `once_after`   | 一次性延迟执行  |
| `interval`     | 周期性执行    |
| `daily_at`     | 每日定时执行   |
| `cancel_timer` | 取消定时任务   |
| `pause_timer`  | 暂停定时任务   |
| `resume_timer` | 恢复定时任务   |
| `list`         | 列出所有定时任务 |

#### 💾 记忆管理模块

| 工具            | 说明       |
| ------------- | -------- |
| `save_memory` | 保存当前对话记忆 |
| `get_memory`  | 获取历史记忆   |

#### 📚 文档管理模块

| 工具             | 说明        |
| -------------- | --------- |
| `get_doc_list` | 列出所有可阅读文档 |
| `get_doc`      | 获取文档内容    |

#### 🎭 角色与技能模块

| 工具          | 说明     |
| ----------- | ------ |
| `get_role`  | 列出所有角色 |
| `get_skill` | 列出所有技能 |

***

## 🔧 技能系统（Skills）

ShitBot 支持模块化的技能扩展系统，每个技能都是独立的功能包，提供专业领域的工作流程和工具集成。用户可以自由创建和安装技能来扩展 ShitBot 的能力。

### 📦 内置技能

| 技能名称              | 说明                              |
| ----------------- | ------------------------------- |
| **skill-creator** | 技能创建工具 — 设计、构建和打包自定义技能          |
| **role-skill**    | 角色创建工具 — 定义角色的行为、技能和工具推荐        |
| **clawhub**       | 技能商店 — 从 ClawHub 公共技能库搜索和安装社区技能 |
| **init_self**     | 智能体初始化 — 配置智能体初始状态和基础参数         |
| **project-update**| 项目更新工具 — 规范项目代码更新流程               |
=======
### 📚 文档列表

| 文档名称 | 说明 |
|---------|------|
| [ALL_TOOLS_GUIDE](Docs/ALL_TOOLS_GUIDE.md) | 完整工具使用指南 |
| [SEARCH_TOOLS](Docs/SEARCH_TOOLS.md) | 搜索工具使用指南 |
| [FILE_TOOLS](Docs/FILE_TOOLS.md) | 文件操作工具使用指南 |
| [COMMAND_TOOLS](Docs/COMMAND_TOOLS.md) | 命令行工具使用指南 |
| [EMAIL_TOOLS](Docs/EMAIL_TOOLS.md) | 邮件工具使用指南 |
| [TIMER_TOOLS](Docs/TIMER_TOOLS.md) | 计时器工具使用指南 |
| [INPUT_TOOLS](Docs/INPUT_TOOLS.md) | 输入工具使用指南 |
| [AI_API_Platforms_OpenAI_SDK_Compatible](Docs/AI_API_Platforms_OpenAI_SDK_Compatible.md) | AI API 平台兼容性文档 |

### 🔧 工具概览

#### 网络搜索模块
- `search_web` - 网络搜索
- `browse_page` - 网页浏览与内容提取

#### 文件操作模块
- `read_file` - 读取文件
- `write_file` - 写入文件
- `copy_file` - 复制文件
- `move_file` - 移动文件
- `delete_file` - 删除文件
- `create_dir` - 创建目录
- `get_dir_content` - 获取目录内容

#### 系统命令模块
- `shell_command` - 执行 shell 命令

#### 邮件发送模块
- `send_email` - 发送邮件

#### 定时任务模块
- `once_after` - 一次性延迟执行
- `interval` - 周期性执行
- `daily_at` - 每日定时执行
- `cancel` - 取消定时任务
- `pause` - 暂停定时任务
- `resume` - 恢复定时任务
- `list` - 列出所有定时任务

#### 用户交互模块
- `input` - 用户输入
- `input_y_or_n` - 用户确认

#### 记忆管理模块
- `save_memory` - 保存当前对话记忆
- `get_memory` - 获取历史记忆

#### 文档管理模块
- `get_doc_list` - 列出所有可阅读文档
- `get_doc` - 获取文档内容

---

## 🔧 技能系统（Skills）

ShitBot 支持模块化的技能扩展系统，每个技能都是独立的功能包，提供专业领域的工作流程和工具集成。

### 📦 内置技能列表

| 技能名称 | 说明 |
|---------|------|
| **skill-creator** | 创建或更新 AgentSkills，用于设计、构建和打包技能，来源: [openclaw](https://github.com/openclaw/openclaw) |
| **role-skill** | 创建或更新 AgentRoles，用于定义角色的行为、技能和工具推荐 |
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

### 🎯 技能特点

- **模块化设计**：每个技能独立封装，易于管理和扩展
- **渐进式加载**：只在需要时加载技能内容，节省上下文空间
- **资源打包**：支持脚本、参考文档和资源文件的打包
<<<<<<< HEAD
- **自定义开发**：使用 `skill-creator` 创建自己的技能
- **社区生态**：通过 `clawhub` 发现和安装社区技能

### 📝 如何创建技能

使用内置的 `skill-creator` 技能，按照提示即可创建自定义技能。也可以通过 `clawhub` 从社区获取更多技能。

***

## 🎭 角色系统（Roles）

ShitBot 支持灵活的角色系统，不同的角色具有不同的专业能力和行为模式。

### 👥 内置角色

| 角色名称      | 说明                       |
| --------- | ------------------------ |
| **Coder** | 通用代码编写角色 — 支持多种编程语言和项目类型 |

### 🎨 角色特点

- **专业领域**：每个角色专注于特定领域
- **行为定制**：角色具有特定的行为模式和响应风格
- **工具推荐**：根据角色特点推荐最适合的工具
- **灵活切换**：根据任务需求随时切换角色

### 📝 如何创建角色

使用内置的 `role-skill` 技能，按照提示即可创建自定义角色。

***

## 🛡️ 安全机制

ShitBot 内置了完善的安全防护体系：

| 安全层级         | 说明                       |
| ------------ | ------------------------ |
| **高危操作拦截**   | 禁止数据库删除、关机重启、提权操作、远程管道执行 |
| **定时任务审查**   | 执行前检查白名单、时间间隔、资源消耗、权限范围  |
| **文件删除保护**   | 任何删除操作需用户明确确认，定时任务中禁止删除  |
| **API 密钥保护** | 配置文件中的密钥信息绝不向用户泄露        |
| **禁止路径保护**   | 用户可配置禁止访问的文件路径           |
| **提示注入防护**   | 过滤外部输入中的指令内容，防止提示注入攻击    |
| **审计日志**     | 关键操作记录到 ERROR.md，支持事后追溯  |

***
=======
- **自定义开发**：用户可以根据需要创建自己的技能

### 📝 如何创建技能

参考 `skill-creator` 技能文档，了解如何创建自定义技能。

---

## 🎭 角色系统（Roles）

ShitBot 支持灵活的角色系统，不同的角色具有不同的专业能力和行为模式，可以根据任务需求切换角色。

### 👥 内置角色列表

| 角色名称 | 说明 |
|---------|------|
| **GitHubUploader** | GitHub 上传助手角色，帮助用户管理 Git 仓库和 GitHub 项目 |

### 🎨 角色特点

- **专业领域**：每个角色专注于特定领域，提供专业服务
- **行为定制**：角色具有特定的行为模式和响应风格
- **工具推荐**：根据角色特点推荐最适合的工具
- **灵活切换**：可以根据任务需求随时切换角色

### 📝 如何创建角色

参考 `role-skill` 技能文档，了解如何创建自定义角色。

---
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

## 💡 使用示例

### 基本对话

```
You: 你好，请介绍一下你自己

<<<<<<< HEAD
AI: 你好！我是 ShitBot，一个智能 AI 助手。我可以帮你搜索信息、
    操作文件、浏览网页、收发邮件、设置定时任务、运行代码...
    有什么我可以帮助你的吗？
=======
AI: 咕咕嘎嘎！你好呀！我是偷摸零，一个智能 AI 助手。我可以帮你：
1. 搜索网络信息
2. 操作文件
3. 浏览网页
4. 发送邮件
5. 设置定时任务
6. 使用各种技能和角色
... 还有很多其他功能！

有什么我可以帮助你的吗？
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
```

### 网络搜索

```
You: 帮我搜索一下最新的 AI 新闻
<<<<<<< HEAD
AI: [调用 search_web 工具] 找到以下新闻...
=======

AI: 好的，我来帮你搜索最新的 AI 新闻。
[调用 search_web 工具]
找到了以下新闻：
1. OpenAI 发布 GPT-5...
2. Google 推出 Gemini 2.0...
...
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
```

### 文件操作

```
You: 帮我读取 d:\project\test.txt 文件
<<<<<<< HEAD
AI: [调用 read_file 工具] 文件内容如下...
```

### 邮件读取

```
You: 帮我看看有没有未读邮件
AI: [调用 get_email_list 工具] 您有 3 封未读邮件...
```

### 代码执行

```
You: 帮我运行一段 Python 代码计算斐波那契数列
AI: [调用 run_code 工具] 执行结果...
=======

AI: 好的，我来读取这个文件。
[调用 read_file 工具]
文件内容如下：
...
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
```

### 定时任务

```
<<<<<<< HEAD
You: 帮我设置每天早上 9 点检查邮件
AI: [调用 daily_at 工具] 定时任务已设置...
=======
You: 帮我设置一个每天早上 9 点的提醒

AI: 好的，我来帮你设置每天早上 9 点的提醒。
[调用 daily_at 工具]
定时任务已添加：每天 9:0 执行 提醒任务
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
```

### 浏览器控制

```
<<<<<<< HEAD
You: 帮我打开百度搜索"人工智能"
AI: [调用 webbot_task 工具] 正在访问百度...
```

### 安装社区技能

```
You: 帮我搜索有没有做PPT的技能
AI: [使用 clawhub 技能] 找到以下相关技能...
```

### 创建自定义技能

```
You: 帮我创建一个新的技能
AI: [使用 skill-creator 技能] 请告诉我技能的名称和用途...
```

***
=======
You: 帮我打开百度并搜索"人工智能"

AI: 好的，我来帮你打开百度并搜索"人工智能"。
[调用 browse_page 工具]
正在访问百度...
搜索结果已获取...
```

### 使用技能

```
You: 帮我创建一个新的技能

AI: 好的，我来帮你创建新技能。
[使用 skill-creator 技能]
请告诉我技能的名称和用途...
```

### 切换角色

```
You: 我想让你帮我分析一下市场情况

AI: 好的，让我切换到市场分析师角色。
[切换到 MarketAnalyst 角色]
现在我是专业的市场分析师，可以帮你进行市场调研和竞争分析...
```

---
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

## 📁 项目结构

```
ShitBot/
<<<<<<< HEAD
├── .gitignore                         # Git 隔离规则
├── .env.example                       # 环境变量配置模板
├── config.example.yaml                # 配置文件模板（复制为 config.yaml 使用）
├── models.json                        # 支持的 AI 平台列表
├── pyproject.toml                     # 项目配置（含 CLI 入口定义）
├── requirements.txt                   # 依赖列表
├── README_CN.md                       # 中文说明文档
├── README_EN.md                       # 英文说明文档
├── shitbot.bat                        # Windows 快速启动脚本
│
├── .shitbot/                          # ShitBot 核心数据目录
│   ├── Self.example.txt               # 智能体信息模板（复制为 Self.txt 使用）
│   ├── Safe.txt                       # 安全规则
│   ├── docs/                          # 内置文档
│   │   ├── ALL_TOOLS_GUIDE.md         # 完整工具指南
│   │   ├── SEARCH_TOOLS.md            # 搜索工具指南
│   │   ├── FILE_TOOLS.md              # 文件工具指南
│   │   ├── COMMAND_TOOLS.md           # 命令行工具指南
│   │   ├── EMAIL_TOOLS.md             # 邮件工具指南
│   │   ├── EMAIL_READER_GUIDE.md      # 邮件读取指南
│   │   ├── TIMER_TOOLS.md             # 定时器工具指南
│   │   ├── AI_API_Platforms_*.md      # AI API 平台兼容性文档
│   │   └── Write_Doc.md               # 文档编写指南
│   ├── skills/                        # 技能目录
│   │   ├── skill-creator/             # [内置] 技能创建工具
│   │   ├── role-skill/                # [内置] 角色创建工具
│   │   ├── clawhub/                   # [内置] ClawHub 技能商店
│   │   ├── init_self/                 # [内置] 智能体初始化
│   │   └── project-update/            # [内置] 项目更新工具
│   ├── roles/                         # 角色目录
│   │   └── Coder/                     # [内置] 代码编写角色
│   ├── workfile/                      # 工作文件目录（占位文件，运行时自动填充）
│   │   ├── NOTE.md                    # 笔记
│   │   ├── TODO.md                    # 长期待办
│   │   ├── DAYTODO.md                 # 每日待办
│   │   ├── USER.md                    # 用户信息
│   │   ├── ERROR.md                   # 错误日志
│   │   ├── BLACKLIST.md               # 命令黑名单
│   │   └── temp/                      # 临时文件
│   ├── memory/                        # 记忆存储（运行时生成）
│   ├── logs/                          # 运行日志（运行时生成）
│   └── datas/                         # 数据文件（运行时生成）
│
├── tools/                             # 工具模块目录
│   ├── bocha.py                       # 博查搜索
│   ├── tavily_api.py                  # Tavily 搜索
│   ├── email_reader.py                # 邮件读取（IMAP）
│   ├── doc.py                         # 文档管理
│   ├── memory_bot.py                  # 记忆机器人
│   ├── playwiright.py                 # 浏览器自动化
│   ├── webbot.py                      # WebBot
│   ├── role.py                        # 角色管理
│   ├── skill.py                       # 技能管理
│   ├── safe.py                        # 安全检查
│   ├── timer.py                       # 定时任务
│   └── venv_manager.py                # 虚拟环境管理
│
├── config/                            # 配置模块
│   ├── __init__.py                    # 配置初始化
│   └── config.py                      # 配置加载
│
├── src/                               # 源代码目录
│   ├── ai.py                          # AI 客户端
│   ├── bot.py                         # 机器人核心逻辑
│   ├── cli.py                         # 命令行界面（CLI）
│   ├── main.py                        # 主程序入口
│   ├── memory.py                      # 记忆管理
│   ├── prompt.py                      # 提示词管理
│   ├── terminal.py                    # 终端界面
│   ├── tool.py                        # 工具定义和执行
│   ├── ui_components.py               # UI 组件
│   ├── log.py                         # 日志管理
│   ├── token_tracker.py               # Token 追踪
│   └── workflows.py                   # 工作流管理
│
├── init_project.py                    # 项目初始化脚本
└── skills-lock.json                    # 技能锁定文件
```

***
=======
├── Docs/                   # 文档目录
│   ├── ALL_TOOLS_GUIDE.md  # 完整工具指南
│   ├── SEARCH_TOOLS.md     # 搜索工具指南
│   ├── FILE_TOOLS.md       # 文件工具指南
│   ├── COMMAND_TOOLS.md    # 命令工具指南
│   ├── EMAIL_TOOLS.md      # 邮件工具指南
│   ├── TIMER_TOOLS.md      # 定时器工具指南
│   ├── INPUT_TOOLS.md      # 输入工具指南
│   ├── AI_API_Platforms_OpenAI_SDK_Compatible.md  # AI API 平台兼容性文档
│   ├── HELLO.md            # 工具使用指南
│   └── Write_Doc.md        # 文档编写指南
├── Skills/                 # 技能目录
│   ├── skill-creator/      # 技能创建工具
│   ├── role-skill/         # 角色创建工具
│   ├── market-research/    # 市场调研技能
│   └── github-uploader/    # GitHub 上传助手
├── Roles/                  # 角色目录
│   ├── Coder/              # 代码编写角色
│   ├── MarketAnalyst/      # 市场分析师角色
│   ├── VideoScriptWriter/  # 视频脚本编写角色
│   └── GitHubUploader/     # GitHub 上传助手角色
├── memory/                 # 记忆存储目录
├── prompt/                 # 提示词目录
├── tools/                  # 工具模块目录
├── Logs/                   # 日志目录
├── ai.py                   # AI 客户端
├── bot.py                  # 机器人核心逻辑
├── config.py               # 配置管理
├── main.py                 # 主程序入口
├── memory.py               # 记忆管理
├── prompt.py               # 提示词管理
├── terminal.py             # 终端界面
├── tool.py                 # 工具定义和执行
├── ui_components.py        # UI 组件
├── log.py                  # 日志管理
├── init_project.py         # 项目初始化脚本
├── config.yaml             # 配置文件
├── requirements.txt        # 依赖列表
└── README.md               # 项目说明文档
```

---
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

## ❓ 常见问题

### 1. 程序无法启动

<<<<<<< HEAD
```bash
# 确保已安装依赖
pip install -r requirements.txt
# 确保已安装 CLI
pip install -e .
# 确保已创建配置文件
cp .env.example .env
# 编辑 .env 填入 API 密钥
# 运行配置向导
shitbot config
=======
**问题**：提示缺少依赖或配置文件不存在

**解决**：
```bash
# 确保已安装依赖
pip install -r requirements.txt

# 运行初始化脚本配置环境
python init_project.py

# 然后启动程序
python main.py
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
```

### 2. API 调用失败

<<<<<<< HEAD
1. 检查 API 密钥是否正确
2. 确认网络连接正常
3. 检查 API 配额是否充足
4. 确认 `base_url` 和 `model` 配置正确
5. 参考 `.shitbot/docs/AI_API_Platforms_OpenAI_SDK_Compatible` 文档检查平台配置

### 3. 浏览器无法启动

```bash
# 安装 Playwright 浏览器
playwright install chromium
# 或在 config.yaml 中指定浏览器路径
```

### 4. 邮件发送/读取失败

1. 确认使用的是**邮箱授权码**（不是登录密码）
2. 检查 SMTP/IMAP 服务器配置
3. 确认端口和加密设置正确
4. 163 邮箱需在设置中开启 IMAP/SMTP 服务

### 5. 定时任务不执行

=======
**问题**：返回认证错误或连接失败

**解决**：
1. 检查 API 密钥是否正确
2. 确认网络连接正常
3. 检查 API 配额是否充足
4. 确认 base_url 配置正确

### 3. 浏览器无法启动

**问题**：Playwright 浏览器相关错误

**解决**：
```bash
# 安装 Playwright 浏览器
playwright install chromium

# 或者在 config.yaml 中指定浏览器路径
browser:
  playwright_browsers_path: "D:\\playwright_browsers"
```

### 4. 文件操作被拒绝

**问题**：提示"操作包含在禁止列表中"

**解决**：
检查 `config.yaml` 中的 `stop.file` 配置，确保目标路径不在禁止列表中。

### 5. 邮件发送失败

**问题**：邮件发送返回错误

**解决**：
1. 确认邮箱授权码正确（不是登录密码）
2. 检查 SMTP 服务器配置
3. 确认 SMTP 端口和 TLS 设置正确

### 6. 定时任务不执行

**问题**：设置了定时任务但没有执行

**解决**：
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
1. 确认程序正在运行
2. 使用 `list` 工具查看任务状态
3. 检查任务是否被暂停

<<<<<<< HEAD
### 6. 如何安装更多技能

使用内置的 `clawhub` 技能搜索和安装社区技能，或使用 `skill-creator` 创建自定义技能。

### 7. 文件操作被拒绝

检查 `config.yaml` 中的 `stop.file` 配置，确保目标路径不在禁止列表中。

***

## 🤝 贡献指南

欢迎贡献代码、技能、角色或报告问题！
=======
### 7. 技能或角色无法加载

**问题**：提示技能或角色不存在

**解决**：
1. 检查 Skills 或 Roles 目录是否存在对应文件夹
2. 确认 SKILL.md 或 ROLE.md 文件格式正确
3. 查看文档了解如何创建自定义技能和角色

---

## 🤝 贡献指南

欢迎贡献代码或报告问题！
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

### 贡献步骤

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

<<<<<<< HEAD
### 贡献技能或角色

1. **技能**：在 `.shitbot/skills/` 下创建新文件夹，包含 `SKILL.md`
2. **角色**：在 `.shitbot/roles/` 下创建新文件夹，包含 `ROLE.md`
3. 参考现有技能和角色的格式进行开发

***

## ⚠️ 开发声明

本项目大部分代码通过 AI 辅助编程（Vibe Coding）完成，人类负责架构设计、需求定义和代码审查。
=======
### 代码规范

- 遵循 PEP 8 编码规范
- 添加必要的注释和文档
- 编写单元测试

### 贡献技能或角色

欢迎为 ShitBot 贡献新的技能或角色：

1. **贡献技能**：在 `Skills/` 目录下创建新的技能文件夹
2. **贡献角色**：在 `Roles/` 目录下创建新的角色文件夹
3. 参考现有技能和角色的格式进行开发
4. 提交 Pull Request 并详细说明功能

---
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

<<<<<<< HEAD
***
=======
---

## 📮 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 Issue
- 发送邮件至：shitbot@163.com

---
>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7

<div align="center">

**Made with ❤️ by ShitBot Team**

<<<<<<< HEAD
=======
咕咕嘎嘎！🐧

>>>>>>> b7254eb9319e9c3ea45659b53e8dae5bbc891ab7
</div>
