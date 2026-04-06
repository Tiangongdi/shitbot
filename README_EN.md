# ShitBot 💩



**💩 A powerful AI intelligent assistant terminal application 💩**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



***

## 📖 Table of Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Command Line Usage](#command-line-usage)
- [Configuration](#configuration)
- [Tools Module](#tools-module)
- [Skills System](#skills-system)
- [Roles System](#roles-system)
- [Security](#security)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [FAQ](#faq)
- [Contributing](#contributing)

***

## 🎯 Introduction

ShitBot is a powerful AI intelligent assistant terminal application that supports 15+ mainstream AI API platforms, with complete browser automation, file operations, scheduled tasks, email sending/receiving, code execution capabilities. Users can have natural conversations with AI through a Claude Code-like terminal interface and instruct AI to complete various complex tasks.

**Highlights:**

- 🤖 Supports 15+ AI platforms (Zhipu AI, DeepSeek, Kimi, OpenAI, Claude, Gemini, etc.)
- 🌐 Complete browser automation (Playwright + WebBot)
- 📁 Powerful file operation capabilities
- ⏰ Flexible scheduled task system
- 📧 Email functionality (SMTP sending + IMAP reading)
- 💾 Intelligent memory management
- 📚 Built-in documentation system
- 🔧 Extensible skills system
- 🎭 Flexible roles system
- 🐍 Python code execution capability
- 🛡️ Comprehensive security protection
- 🎨 Modern terminal interface
- ⌨️ Command Line Interface (CLI) support, globally usable after installation
- 🔌 MCP protocol support (Model Context Protocol)

***

## ✨ Key Features

### 🤖 Multi-AI Provider Support

Supports 15+ mainstream AI platforms from China and abroad, uniformly called through OpenAI SDK compatible interface, easy to switch:

| Type      | Platform             | Identifier      |
| --------- | -------------------- | --------------- |
| 🇨🇳 China  | 智谱AI (GLM)          | `zai`           |
| 🇨🇳 China  | DeepSeek             | `deepseek`      |
| 🇨🇳 China  | Moonshot (Kimi)      | `moonshot`      |
| 🇨🇳 China  | MiniMax              | `minimax`       |
| 🇨🇳 China  | Xiaomi (MiMo)        | `xiaomi_mimo`   |
| 🇨🇳 China  | Volcengine           | `volcengine`    |
| 🇨🇳 China  | Aliyun (DashScope)   | `dashscope`     |
| 🌍 Global | OpenAI (ChatGPT)     | `openai`        |
| 🌍 Global | Anthropic (Claude)   | `anthropic`     |
| 🌍 Global | Google (Gemini)      | `gemini`        |
| 🌍 Global | Cohere               | `cohere`        |
| 🌍 Global | Mistral              | `mistral`       |
| 🌍 Global | Groq                 | `groq`          |
| 🌍 Global | Perplexity           | `perplexity`    |
| 🌍 Global | OpenRouter           | `openrouter`    |

> 💡 All platforms are called through OpenAI SDK compatible interface. Just configure `api_key`, `base_url`, and `model` to use. See `.shitbot/docs/AI_API_Platforms_OpenAI_SDK_Compatible` for detailed configuration.

### 🌐 Browser Automation

- Visual browser control based on Playwright
- Web navigation and interaction
- Intelligent content extraction and summarization
- Form filling and search
- Page screenshot functionality
- JavaScript execution

### 📁 File Operations

- File read/write operations
- Append content to files
- File copy and move
- Directory creation and management
- Secure file deletion (requires user confirmation)
- Forbidden path protection mechanism

### 🐍 Code Execution

- Run Python code snippets
- Execute Python code files
- Real-time code testing and validation

### ⏰ Scheduled Task System

- One-time delayed execution
- Periodic execution
- Daily scheduled execution
- Task management (pause, resume, cancel)

### 📧 Email System

- **Send**: SMTP protocol, supports TLS/SSL encryption
- **Read**: IMAP protocol, supports folder browsing, email search, content retrieval
- Supports multiple email services (163, Gmail, etc.)

### 💾 Intelligent Memory Management

- Conversation memory saving
- Historical memory retrieval
- Intelligent memory summarization
- Work file system (notes, todos, user profile)

### 📚 Documentation System

- Built-in tool usage documentation
- Quick reference guide
- Modular document management

### 🔧 Skills System

- Modular skill extension, loaded on demand
- Custom skill development
- Built-in skill creation tools
- Supports searching and installing from ClawHub public skill registry

### 🎭 Roles System

- Custom role settings
- Flexible switching between roles
- Multiple built-in professional roles
- Role-specific behaviors and tool recommendations

### 🛡️ Security

- High-risk operation blocking
- Scheduled task security review
- File deletion forced confirmation
- API key protection
- Forbidden path protection
- Prompt injection prevention

### 🎨 Modern Terminal Interface

- Claude Code-like interaction experience
- Colored output and formatted display
- Chat history

***

## 💻 Requirements

- **Python**: 3.8 or higher
- **OS**: Windows 10/11 (primary test environment)
- **Browser**: Microsoft Edge (Chromium version)
- **Network**: Stable network connection
- **API Key**: At least one AI platform API key (see list above)

***

## 🚀 Quick Start

### 1. Clone the project

```bash
git clone https://github.com/Tiangongdi/shitbot.git
cd shitbot
```

### 2. Create virtual environment

```bash
python -m venv shitbot_env
```

### 3. Activate virtual environment

```bash
# Windows
.\shitbot_env\Scripts\activate

# Linux/Mac
source shitbot_env/bin/activate
```

### 4. Install dependencies and CLI tool

```bash
pip install -r requirements.txt
# Install CLI command (globally usable shitbot command)
pip install -e .
```

### 5. Initialize configuration

You can choose manual configuration or use the configuration wizard:

**Method 1: Use configuration wizard (Recommended)**

```bash
shitbot config
```

After execution, it will prompt you to select AI platform, enter API key, agent information, etc., automatically generate the configuration file.

**Method 2: Manually copy configuration template**

```bash
# Copy configuration template
cp .env.example .env
# If you use config.yaml format:
cp config.example.yaml config.yaml
# Copy agent information template
cp .shitbot/Self.example.txt .shitbot/Self.txt
```

Then edit the configuration file to fill in your API key and other configurations.

### 6. Start the program

**Method 1: Use CLI command (Recommended)**

```bash
shitbot shitbot
```

**Method 2: Run Python script directly**

```bash
python src/main.py
```

***

## ⌨️ Command Line Usage

ShitBot provides a complete command line interface (CLI), globally usable with `shitbot` command after installation.

### Available Commands

| Command | Description |
|---------|-------------|
| `shitbot shitbot` | Start interactive conversation (default) |
| `shitbot shitbot -m "Your question"` | Execute single conversation, output result directly |
| `shitbot config` | Run configuration wizard, initialize configuration |

### Command Details

#### 1. Start interactive conversation

```bash
shitbot shitbot
```

Enter interactive conversation mode, you can continuously converse with ShitBot, just like in Claude Code.

#### 2. Single conversation mode

```bash
shitbot shitbot -m "Help me calculate 1+1"
shitbot shitbot -m "Search today's AI news"
shitbot shitbot -m "Read README.md in current directory and summarize"
```

Suitable for script calls or quick queries, outputs result directly and exits after execution.

#### 3. Configuration wizard

```bash
shitbot config
```

Interactive configuration wizard, guides you through AI platform selection, API key input, agent information setup, automatically generates configuration file.

### Usage Examples

```bash
# Start interactive chat
shitbot shitbot

# Single question
shitbot shitbot -m "What files are in the current directory?"

# Rerun configuration wizard
shitbot config
```

***

## ⚙️ Configuration

### Configuration Methods

ShitBot supports two configuration methods:

**1. Environment variables (Recommended, generated via `shitbot config`)**
- Uses `.env` file for configuration storage
- More aligned with modern development practices, convenient for container deployment

**2. YAML configuration file**
- Uses `config.yaml` for configuration storage
- Compatible with older version configuration formats

### Complete Configuration Items

Main configuration items:

```env
# AI Provider Configuration
AI_API_KEY=your-api-key-here
AI_VALUE=deepseek
AI_MODEL=deepseek-chat
AI_BASE_URL=

# Bocha Search Configuration
BOCHA_API_KEY=
BOCHA_BASE_URL=

# Tavily Search Configuration
TAVILY_KEY=

# Web Search Configuration
WEB_SEARCH_ID=2

# Email Send Configuration (SMTP)
EMAIL_FROM=your-email@example.com
EMAIL_PASSWORD=your-email-password
EMAIL_SMTP_SERVER=smtp.example.com
EMAIL_SMTP_PORT=465
EMAIL_USE_TLS=true

# Email Read Configuration (IMAP)
IMAP_EMAIL=your-email@example.com
IMAP_PASSWORD=your-email-password
IMAP_SERVER=imap.example.com
IMAP_PORT=993
IMAP_USE_SSL=true
```

Or in YAML format:

```yaml
# AI Provider Configuration (supports 15+ platforms, see models.json)
ai:
  api_key: ""           # AI API key (required)
  value: ""             # API platform identifier (zai/deepseek/moonshot/openai, etc.)
  model: ""             # Model name (glm-5-turbo, deepseek-chat, etc.)
  base_url: ""          # Custom API address (optional, leave empty for default)

# Bocha Search Configuration
bocha:
  api_key: ""           # Bocha API key
  base_url: ""          # API address
  index_name: "news"    # Search index

# Tavily Search Configuration
tavily:
  key: ""               # Tavily API key

# Web Search Configuration
web_search:
  web_search_ID: 2      # Search engine selection (1=Bocha, 2=Tavily)

# Browser Configuration
browser:
  playwright_browsers_path: ""  # Playwright browser path

# Default Provider
default_provider: "ai"

# Email Send Configuration (SMTP)
email:
  email: ""             # From email
  password: ""          # Email authorization code
  smtp_server: ""       # SMTP server
  smtp_port: 465        # SMTP port
  use_tls: true         # Use TLS

# Email Read Configuration (IMAP)
imap:
  email: ""             # Email address
  password: ""          # Email authorization code
  imap_server: ""       # IMAP server
  imap_port: 993        # IMAP port
  use_ssl: true         # Use SSL

# Forbidden access paths
stop:
  file: []
```

### Agent Information Configuration

Edit `.shitbot/Self.txt` to customize agent identity:

```
# ShitBot Self-Information File

## Name: Your agent name
## Personality: Personality description
## User: Your username
## User Introduction: User introduction
```

### API Key Acquisition

| Platform             | URL                                                         | Notes                     |
| -------------------- | ----------------------------------------------------------- | ------------------------- |
| 智谱AI               | [open.bigmodel.cn](https://open.bigmodel.cn/)             | Apply for API key after registration |
| DeepSeek             | [platform.deepseek.com](https://platform.deepseek.com/)   | Get API Key after registration |
| Moonshot (Kimi)      | [platform.moonshot.cn](https://platform.moonshot.cn/)     | Apply for API key after registration |
| MiniMax              | [platform.minimaxi.com](https://platform.minimaxi.com/)   | Get API Key after registration |
| Xiaomi (MiMo)        | [platform.mimaji.com](https://platform.mimaji.com/)       | Get API Key after registration |
| Volcengine           | [console.volcengine.com](https://console.volcengine.com/) | Apply for API key after registration |
| Aliyun (DashScope)   | [dashscope.aliyun.com](https://dashscope.aliyun.com/)     | Apply for API key after registration |
| OpenAI             | [platform.openai.com](https://platform.openai.com/)       | Get API Key after registration |
| Anthropic (Claude) | [console.anthropic.com](https://console.anthropic.com/)   | Get API Key after registration |
| Google (Gemini)    | [ai.google.dev](https://ai.google.dev/)                   | Get API Key after registration |
| Bocha Search         | [api.bocha.com](https://api.bocha.com/)                   | Apply for API key after registration |
| Tavily             | [tavily.com](https://tavily.com/)                         | Get API Key after registration |

> 💡 For detailed configuration (`base_url`, model name, etc.) please refer to `.shitbot/docs/AI_API_Platforms_OpenAI_SDK_Compatible` documentation.

***
## 🛠️ Tools Module

ShitBot provides rich tool modules, each with detailed usage documentation:

### 🔧 Tool Overview

#### 🌐 Web Search Module

| Tool            | Description               |
| --------------- | ----------------------- |
| `search_web`    | Web search              |
| `webbot_task`   | Browser task execution (WebBot) |

#### 📁 File Operation Module

| Tool                | Description           |
| ------------------- | ------------------- |
| `read_file`         | Read file           |
| `write_file`        | Write file          |
| `append_to_file`    | Append content to file |
| `copy_file`         | Copy file           |
| `move_file`         | Move file           |
| `delete_file`       | Delete file (requires confirmation) |
| `create_dir`        | Create directory    |
| `get_dir_content`   | Get directory content |

#### 🐍 Code Execution Module

| Tool              | Description             |
| --------------- | ---------------------- |
| `run_code`      | Run Python code snippet |
| `run_code_file` | Run Python code file   |

#### 💻 System Command Module

| Tool              | Description         |
| --------------- | ----------------- |
| `shell_command` | Execute shell command |

#### 📧 Email Module

| Tool                   | Description        |
| -------------------- | ---------------- |
| `send_email`         | Send email (SMTP) |
| `list_email_folders` | List email folders |
| `get_email_list`     | Get email list   |
| `get_email_content`  | Get email content |
| `search_emails`      | Search emails    |
| `mark_email_read`    | Mark email as read |

#### ⏰ Scheduled Task Module

| Tool             | Description    |
| -------------- | ------------ |
| `once_after`   | One-time delayed execution |
| `interval`     | Periodic execution |
| `daily_at`     | Daily scheduled execution |
| `cancel_timer` | Cancel scheduled task |
| `pause_timer`  | Pause scheduled task |
| `resume_timer` | Resume scheduled task |
| `list`         | List all scheduled tasks |

#### 💾 Memory Management Module

| Tool            | Description   |
| ------------- | ----------- |
| `get_memory`  | Get historical memory |

#### 📚 Documentation Management Module

| Tool             | Description             |
| -------------- | --------------------- |
| `get_doc_list` | List all readable documents |
| `get_doc`      | Get document content  |

#### 🎭 Roles & Skills Module

| Tool          | Description      |
| ----------- | -------------- |
| `get_role`  | List all roles  |
| `get_skill` | List all skills |

***

## 🔧 Skills System

ShitBot supports a modular skill extension system. Each skill is an independent functional package that provides professional workflows and tool integration. Users can freely create and install skills to extend ShitBot's capabilities.

### 📦 Built-in Skills

| Skill Name        | Description                              |
| Skill Name        | Description                              |
| ----------------- | ---------------------------------------- |
| **clawhub**       | Skill Store — Search and install community skills from ClawHub public registry |
| **init_self**     | Agent Initialization — Configure agent initial state and basic parameters |
| **project-update**| Project Update Tool — Standardize project code update process |
| **role-skill**    | Role Creation Tool — Define role behaviors, skills and tool recommendations |
| **skill-creator** | Skill Creation Tool — Design, build and package custom skills |

- **Modular Design**: Each skill is independently packaged, easy to manage and extend
- **Lazy Loading**: Only load skill content when needed, saves context space
- **Resource Packaging**: Supports packaging of scripts, reference documents and assets
- **Custom Development**: Create your own skills using `skill-creator`
- **Community Ecosystem**: Discover and install community skills via `clawhub`

### 📝 How to Create Skills

Use the built-in `skill-creator` skill, follow the prompts to create custom skills. You can also get more skills from the community via `clawhub`.

***
## 🎭 Roles System

ShitBot supports a flexible role system with different roles having different professional capabilities and behavior patterns.

### 👥 Built-in Roles

| Role Name      | Description                        |
| ------------- | ---------------------------------- |
| **Coder** | General-purpose code writing — supports multiple programming languages and project types |
| Role Name      | Description                        |
| **VideoScriptWriter** | Professional Video Script Writer — Creates engaging scripts for various video formats |
### 🎨 Role Features

- **Professional Domains**: Each role focuses on specific domains
- **Behavioral Customization**: Roles have specific behavior patterns and response styles
- **Tool Recommendations**: Recommends most suitable tools based on role characteristics
- **Flexible Switching**: Switch roles anytime based on task requirements

### 📝 How to Create Roles

Use the built-in `role-skill` skill, follow the prompts to create custom roles.

***

## 🛡️ Security

ShitBot includes a comprehensive security protection system:

| Security Layer | Description |
|---------------|-------------|
| **High-Risk Operation Blocking** | Blocks DB deletion, shutdown, privilege escalation, remote pipe execution |
| **Scheduled Task Review** | Pre-execution whitelist check, interval validation, resource monitoring |
| **File Deletion Protection** | Any deletion requires explicit user confirmation; forbidden in scheduled tasks |
| **API Key Protection** | Configuration secrets never disclosed to users |
| **Forbidden Path Protection** | User-configurable forbidden file paths |
| **Prompt Injection Prevention** | Filters directive content from external input |
| **Audit Logging** | Critical operations logged to ERROR.md for traceability |

***

## 💡 Usage Examples

### Basic Conversation
```
You: Hello, please introduce yourself

AI: Hello! I'm ShitBot, an intelligent AI assistant. I can help you
    search information, operate files, browse web pages, send/receive emails,
    set scheduled tasks, run code... How can I help you?
```

### Web Search
```
You: Help me search for the latest AI news
AI: [Calling search_web tool] Found the following news...
```

### File Operations
```
You: Help me read d:\project\test.txt
AI: [Calling read_file tool] File content...
```

### Email Reading
```
You: Check if I have any unread emails
AI: [Calling get_email_list tool] You have 3 unread emails...
```

### Code Execution
```
You: Run a Python code to calculate Fibonacci sequence
AI: [Calling run_code tool] Results...
```

### Scheduled Tasks
```
You: Set up a daily 9 AM email check
AI: [Calling daily_at tool] Scheduled task set...
```

### Browser Control
```
You: Open Baidu and search for "artificial intelligence"
AI: [Calling webbot_task tool] Visiting Baidu...
```

### Install Community Skills
```
You: Search for a PPT generation skill
AI: [Using clawhub skill] Found the following related skills...
```

### Create Custom Skills
```
You: Help me create a new skill
AI: [Using skill-creator skill] Please tell me the skill name and purpose...
```

***

## 📁 Project Structure

```
ShitBot/
├── .gitignore                         # Git ignore rules
├── .env.example                       # Environment variables template
├── config.example.yaml                # Config template (copy to config.yaml)
├── models.json                        # Supported AI platforms list
├── pyproject.toml                     # Project configuration (includes CLI entry definition)
├── requirements.txt                   # Dependencies list
├── README.md                          # Main README
├── README_CN.md                       # Chinese documentation
├── README_EN.md                       # English documentation
├── shitbot.bat                        # Windows quick start script
├── skills-lock.json                   # Skills lock file
│
├── .shitbot/                          # ShitBot core data directory
│   ├── Self.example.txt               # Agent info template (copy to Self.txt)
│   ├── Safe.txt                       # Safety rules
│   ├── docs/                          # Built-in documentation
│   │   ├── ALL_TOOLS_GUIDE.md         # Complete tools guide
│   │   ├── SEARCH_TOOLS.md            # Search tools guide
│   │   ├── FILE_TOOLS.md              # File tools guide
│   │   ├── COMMAND_TOOLS.md           # Command line tools guide
│   │   ├── TIMER_TOOLS.md             # Timer tools guide
│   │   ├── AI_API_Platforms_*.md      # AI API platform compatibility
│   │   └── Write_Doc.md               # Documentation writing guide
│   ├── skills/                        # Skills directory (only built-in base skills, more skills installable via clawhub)
│   │   ├── clawhub/                   # [Built-in] ClawHub skill store
│   │   ├── init_self/                 # [Built-in] Agent initialization
│   │   ├── project-update/            # [Built-in] Project update tool
│   │   ├── role-skill/                # [Built-in] Role creation tool
│   │   └── skill-creator/             # [Built-in] Skill creation tool
│   ├── roles/                         # Roles directory (only built-in base role, more roles can be custom created)
│   │   └── Coder/                     # [Built-in] Code writing role
│   │   ├── EMAIL_TOOLS.md             # Email tools guide
│   │   ├── NOTE.md                    # Notes
│   │   ├── TODO.md                    # Long-term todos
│   │   ├── DAYTODO.md                 # Daily todos
│   │   ├── USER.md                    # User info
│   │   ├── ERROR.md                   # Error logs
│   │   ├── BLACKLIST.md               # Command blacklist
│   │   └── temp/                      # Temporary files
│   ├── memory/                        # Memory storage (auto-generated at runtime)
│   ├── logs/                          # Runtime logs (auto-generated at runtime)
│   └── datas/                         # Data files (auto-generated at runtime)
│
├── tools/                             # Tools module directory
│   ├── bocha.py                       # Bocha search
│   ├── tavily_api.py                  # Tavily search
│   ├── email_reader.py                # Email reader (IMAP)
│   ├── mcp_client.py                  # MCP protocol client (Model Context Protocol)
│   ├── doc.py                         # Document management
│   ├── memory_bot.py                  # Memory bot
│   ├── playwiright.py                 # Browser automation
│   ├── webbot.py                      # WebBot
│   ├── role.py                        # Role management
│   ├── skill.py                       # Skill management
│   ├── safe.py                        # Security check
│   ├── timer.py                       # Scheduled tasks
│   └── venv_manager.py                # Virtual environment manager
│
├── config/                            # Configuration module
│   ├── __init__.py                    # Configuration initialization
│   └── config.py                      # Configuration loading
│
├── src/                               # Source code directory
│   ├── agent/                         # Agent module
│   ├── ai.py                          # AI client
│   ├── bot.py                         # Bot core logic
│   ├── cli.py                         # Command Line Interface (CLI)
│   ├── main.py                        # Main program entry
│   ├── memory.py                      # Memory management
│   ├── prompt.py                      # Prompt management
│   ├── terminal.py                    # Terminal interface
│   ├── tool.py                        # Tool definition and execution
│   ├── tools/                         # Tools registry
│   ├── tool_registry.py               # Tool registry
│   ├── ui_components.py               # UI components
│   ├── log.py                         # Log management
│   ├── token_tracker.py               # Token tracking
│   └── workflows.py                   # Workflow management
│
├── init_project.py                    # Project initialization script
└── test/                              # Test files directory
```

> **Note**: The following files/directories are excluded from the repository via `.gitignore`:
> - `config.yaml` — Contains sensitive API keys. Use `config.example.yaml` as a template.
> - `.env` — Contains sensitive API keys. Use `.env.example` as a template.
> - `.shitbot/Self.txt` — User's personalized agent config. Use `Self.example.txt` as a template.
> - `.shitbot/workfile/` — Runtime work files (empty placeholders are provided).
> - `.shitbot/memory/`, `.shitbot/logs/`, `.shitbot/datas/` — Auto-generated at runtime.
> - `shitbot_env/`, `code_venv/` — Python virtual environments.
> - User-installed skills and user-created roles.

***
## ❓ FAQ

### 1. Program Won't Start
```bash
# Ensure dependencies are installed
pip install -r requirements.txt
# Ensure CLI is installed
pip install -e .
# Ensure config file exists
cp .env.example .env
# Edit .env and fill in your API keys
# Run setup wizard
shitbot config
```

### 2. API Call Failed
1. Check if API key is correct
2. Confirm network connection is normal
3. Check if API quota is sufficient
4. Confirm `base_url` and `model` configuration is correct
5. Refer to `.shitbot/docs/AI_API_Platforms_OpenAI_SDK_Compatible` for platform-specific settings

### 3. Browser Won't Start
```bash
# Install Playwright browser
playwright install chromium
# Or specify browser path in config.yaml
```

### 4. Email Sending/Reading Failed
1. Confirm using **email authorization code** (not login password)
2. Check SMTP/IMAP server configuration
3. Confirm port and encryption settings correct
4. For 163 email: enable IMAP/SMTP service in settings

### 5. Scheduled Task Not Executing
1. Confirm the program is running
2. Use the `list` tool to view task status
3. Check if task is paused

### 6. How to Install More Skills
Use the built-in `clawhub` skill to search and install community skills, or use `skill-creator` to create custom skills.

### 7. File Operation Denied
Check the `stop.file` configuration in `config.yaml` to ensure the target path is not in the forbidden list.

***

## 🤝 Contributing

Contributions of code, skills, roles, or issue reports are welcome!

### Contribution Steps

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

### Contributing Skills or Roles

1. **Skills**: Create new folder in `.shitbot/skills/` with `SKILL.md`
2. **Roles**: Create new folder in `.shitbot/roles/` with `ROLE.md`
3. Follow the format of existing skills and roles

***

## ⚠️ Development Note

Most of the code in this project was generated through AI-assisted programming (Vibe Coding). Human responsibilities include architecture design, requirement definition, and code review.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details

***



**Made with ❤️ by ShitBot Team**


