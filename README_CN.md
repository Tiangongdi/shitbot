# ShitBot 💩

<div align="center">

**💩一个功能强大的 AI 智能助手终端应用💩**


</div>

---

## 📖 目录

- [项目简介](#项目简介)
- [核心特性](#核心特性)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [工具模块](#工具模块)
- [技能系统](#技能系统)
- [角色系统](#角色系统)
- [使用示例](#使用示例)
- [项目结构](#项目结构)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)

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

## ✨ 核心特性

### 🤖 多 AI 提供商支持
- **推荐**智谱AI (GLM)：支持 GLM-4、GLM-5 等模型
- **博查搜索**：专业的网络搜索 API
- 流式响应支持
- 轻松切换提供商

### 🌐 浏览器自动化
- 基于 Playwright 的可视化浏览器控制
- 网页导航和交互
- 智能内容提取和总结
- 表单填写和搜索
- 页面截图功能
- JavaScript 执行

### 📁 文件操作
- 文件读写操作
- 文件复制和移动
- 目录创建和管理
- 安全的文件删除（需用户确认）
- 禁止路径保护机制

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
- 内置工具使用文档
- 快速查阅指南
- 分模块文档管理

### 🔧 技能系统（Skills）
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
- 类 Claude Code 的交互体验
- 彩色输出和格式化显示
- 聊天历史记录

---

## 💻 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10/11（已在 Windows 环境测试）
- **浏览器**: Microsoft Edge (Chromium 版本)
- **网络**: 稳定的网络连接
- **API 密钥**: 智谱AI 和/或 博查 API 密钥

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/ShitBot.git
cd ShitBot
```

### 2. 创建虚拟环境

```bash
# 在项目根目录下执行
python -m venv shitbot_env
```

### 3. 激活虚拟环境

```bash
# Windows
.\shitbot_env\Scripts\activate

# Linux/Mac
source shitbot_env/bin/activate
```

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

# 默认提供商
default_provider: "ai"

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
```

### API 密钥获取

**智谱AI**
1. 访问 [智谱AI 开放平台](https://open.bigmodel.cn/)
2. 注册账号并申请 API 密钥
3. 将密钥填入配置文件的 `ai.api_key`

**博查搜索**
1. 访问 [博查 API 官网](https://api.bocha.com/)
2. 注册账号并申请 API 密钥
3. 将密钥填入配置文件的 `bocha.api_key`

---

## 🛠️ 工具模块

ShitBot 提供了丰富的工具模块，每个模块都有详细的使用文档：

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

### 🎯 技能特点

- **模块化设计**：每个技能独立封装，易于管理和扩展
- **渐进式加载**：只在需要时加载技能内容，节省上下文空间
- **资源打包**：支持脚本、参考文档和资源文件的打包
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

## 💡 使用示例

### 基本对话

```
You: 你好，请介绍一下你自己

AI: 咕咕嘎嘎！你好呀！我是偷摸零，一个智能 AI 助手。我可以帮你：
1. 搜索网络信息
2. 操作文件
3. 浏览网页
4. 发送邮件
5. 设置定时任务
6. 使用各种技能和角色
... 还有很多其他功能！

有什么我可以帮助你的吗？
```

### 网络搜索

```
You: 帮我搜索一下最新的 AI 新闻

AI: 好的，我来帮你搜索最新的 AI 新闻。
[调用 search_web 工具]
找到了以下新闻：
1. OpenAI 发布 GPT-5...
2. Google 推出 Gemini 2.0...
...
```

### 文件操作

```
You: 帮我读取 d:\project\test.txt 文件

AI: 好的，我来读取这个文件。
[调用 read_file 工具]
文件内容如下：
...
```

### 定时任务

```
You: 帮我设置一个每天早上 9 点的提醒

AI: 好的，我来帮你设置每天早上 9 点的提醒。
[调用 daily_at 工具]
定时任务已添加：每天 9:0 执行 提醒任务
```

### 浏览器控制

```
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

## 📁 项目结构

```
ShitBot/
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

## ❓ 常见问题

### 1. 程序无法启动

**问题**：提示缺少依赖或配置文件不存在

**解决**：
```bash
# 确保已安装依赖
pip install -r requirements.txt

# 运行初始化脚本配置环境
python init_project.py

# 然后启动程序
python main.py
```

### 2. API 调用失败

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
1. 确认程序正在运行
2. 使用 `list` 工具查看任务状态
3. 检查任务是否被暂停

### 7. 技能或角色无法加载

**问题**：提示技能或角色不存在

**解决**：
1. 检查 Skills 或 Roles 目录是否存在对应文件夹
2. 确认 SKILL.md 或 ROLE.md 文件格式正确
3. 查看文档了解如何创建自定义技能和角色

---

## 🤝 贡献指南

欢迎贡献代码或报告问题！

### 贡献步骤

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

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

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 📮 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 Issue
- 发送邮件至：shitbot@163.com

---

<div align="center">

**Made with ❤️ by ShitBot Team**

咕咕嘎嘎！🐧

</div>
