# ShitBot 💩

<div align="center">

**💩 A Powerful AI Assistant Terminal Application 💩**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📖 Table of Contents

- [Introduction](#introduction)
- [Core Features](#core-features)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Tool Modules](#tool-modules)
- [Skills System](#skills-system)
- [Roles System](#roles-system)
- [Security](#security)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [FAQ](#faq)
- [Contributing](#contributing)

---

## 🎯 Introduction

ShitBot is a powerful AI assistant terminal application that supports 15+ mainstream AI API platforms, with complete browser automation, file operations, scheduled tasks, email sending/receiving, code execution, and more. Users can interact naturally with AI through a Claude Code-like terminal interface and instruct AI to complete various complex tasks.

**Key Highlights:**
- 🤖 Supports 15+ AI platforms (ZhipuAI, DeepSeek, Kimi, OpenAI, Claude, Gemini, etc.)
- 🌐 Complete browser automation (Playwright + WebBot)
- 📁 Powerful file operation functions
- ⏰ Flexible scheduled task system
- 📧 Email sending & receiving (SMTP + IMAP)
- 💾 Intelligent memory management
- 📚 Built-in documentation system
- 🔧 Extensible Skills System
- 🎭 Flexible Roles System
- 🐍 Python code execution
- 🛡️ Comprehensive security mechanisms
- 🎨 Modern terminal interface

---

## ✨ Core Features

### 🤖 Multi-AI Provider Support

Supports 15+ mainstream AI platforms worldwide, unified through OpenAI SDK compatible interfaces, easy to switch:

| Type | Platform | Identifier |
|------|----------|------------|
| 🇨🇳 China | ZhipuAI (GLM) | `zai` |
| 🇨🇳 China | DeepSeek | `deepseek` |
| 🇨🇳 China | Moonshot (Kimi) | `moonshot` |
| 🇨🇳 China | MiniMax | `minimax` |
| 🇨🇳 China | Xiaomi (MiMo) | `xiaomi_mimo` |
| 🇨🇳 China | Volcengine | `volcengine` |
| 🇨🇳 China | Alibaba Cloud (DashScope) | `dashscope` |
| 🌍 International | OpenAI (ChatGPT) | `openai` |
| 🌍 International | Anthropic (Claude) | `anthropic` |
| 🌍 International | Google (Gemini) | `gemini` |
| 🌍 International | Cohere | `cohere` |
| 🌍 International | Mistral | `mistral` |
| 🌍 International | Groq | `groq` |
| 🌍 International | Perplexity | `perplexity` |
| 🌍 International | OpenRouter | `openrouter` |

> 💡 All platforms are called through OpenAI SDK compatible interfaces. Just configure the corresponding `api_key`, `base_url`, and `model` to get started. For detailed configuration, refer to the `.shitbot/docs/AI_API_Platforms_OpenAI_SDK_Compatible` document.

### 🌐 Browser Automation
- Playwright-based visual browser control
- Web navigation and interaction
- Intelligent content extraction and summarization
- Form filling and searching
- Page screenshot functionality
- JavaScript execution

### 📁 File Operations
- File read/write operations
- File append content
- File copy and move
- Directory creation and management
- Safe file deletion (requires user confirmation)
- Forbidden path protection mechanism

### 🐍 Code Execution
- Run Python code snippets
- Execute Python code files
- Real-time code testing and validation

### ⏰ Scheduled Task System
- One-time delayed execution
- Periodic task execution
- Daily scheduled execution
- Task management (pause, resume, cancel)

### 📧 Email System
- **Sending**: SMTP protocol with TLS/SSL encryption
- **Reading**: IMAP protocol with folder browsing, email search, content retrieval
- Support for multiple email services (163, Gmail, etc.)

### 💾 Intelligent Memory Management
- Conversation memory saving
- Historical memory retrieval
- Intelligent memory summarization
- Work file system (notes, todos, user profiles)

### 📚 Documentation System
- Built-in tool usage documentation
- Quick reference guides
- Modular documentation management

### 🔧 Skills System
- Modular skill extension with on-demand loading
- Custom skill development
- Built-in skill creation tools
- ClawHub public skill registry support

### 🎭 Roles System
- Custom role settings
- Flexible role switching
- Built-in code writing role
- Role-specific behaviors and tool recommendations

### 🛡️ Security Mechanisms
- High-risk operation blocking (DB deletion, shutdown, privilege escalation)
- Scheduled task security review
- Mandatory file deletion confirmation
- API key protection
- Forbidden path protection
- Prompt injection prevention

### 🎨 Modern Terminal Interface
- Claude Code-like interaction experience
- Colorful output and formatted display
- Chat history records

---

## 💻 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11 (primary test environment)
- **Browser**: Microsoft Edge (Chromium version)
- **Network**: Stable network connection
- **API Keys**: At least one AI platform's API key (see supported platforms above)

---

## 🚀 Quick Start

### 1. Clone the Project

```bash
git clone https://github.com/yourusername/ShitBot.git
cd ShitBot
```

### 2. Create Virtual Environment

```bash
python -m venv shitbot_env
```

### 3. Activate Virtual Environment

```bash
# Windows
.\shitbot_env\Scripts\activate

# Linux/Mac
source shitbot_env/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Initialize Configuration

```bash
# Copy configuration template
cp config.example.yaml config.yaml
# Copy agent info template
cp .shitbot/Self.example.txt .shitbot/Self.txt
```

Edit `config.yaml` to fill in your API keys and email settings. Edit `.shitbot/Self.txt` to set the agent name and personality.

Or run the initialization wizard for automatic setup:

```bash
python init_project.py
```

Follow the prompts to select an AI platform, enter API keys, agent info, etc. Configuration files will be generated automatically.

### 6. Run the Program

```bash
python main.py
```

---

## ⚙️ Configuration

### Configuration File Structure

Refer to `config.example.yaml` for the full configuration template. Key settings:

```yaml
# AI Provider Configuration (supports 15+ platforms, see models.json)
ai:
  api_key: ""           # AI API key (required)
  value: ""             # Platform identifier (e.g. zai/deepseek/moonshot/openai)
  model: ""             # Model name (e.g. glm-5-turbo, deepseek-chat)
  base_url: ""          # Custom API URL (optional, leave empty for default)

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

# Email Sending Configuration (SMTP)
email:
  email: ""             # Sender email
  password: ""          # Email authorization code
  smtp_server: ""       # SMTP server
  smtp_port: 465        # SMTP port
  use_tls: true         # Use TLS

# Email Reading Configuration (IMAP)
imap:
  email: ""             # Email address
  password: ""          # Email authorization code
  imap_server: ""       # IMAP server
  imap_port: 993        # IMAP port
  use_ssl: true         # Use SSL

# Forbidden Access Paths
stop:
  file: []
```

### Agent Information Configuration

Edit `.shitbot/Self.txt` to customize the agent identity:

```
# ShitBot Self-Information File

## Name: Your Agent Name
## Personality: Personality description
## User: Your Username
## User Introduction: User bio
```

### API Key Acquisition

| Platform | URL | Description |
|----------|-----|-------------|
| ZhipuAI | [open.bigmodel.cn](https://open.bigmodel.cn/) | Register and apply for API key |
| DeepSeek | [platform.deepseek.com](https://platform.deepseek.com/) | Register to get API Key |
| Moonshot (Kimi) | [platform.moonshot.cn](https://platform.moonshot.cn/) | Register and apply for API key |
| MiniMax | [platform.minimaxi.com](https://platform.minimaxi.com/) | Register to get API Key |
| Xiaomi (MiMo) | [platform.minimaxi.com](https://platform.minimaxi.com/) | Register to get API Key |
| Volcengine | [console.volcengine.com](https://console.volcengine.com/) | Register and apply for API key |
| Alibaba Cloud (DashScope) | [dashscope.aliyun.com](https://dashscope.aliyun.com/) | Register and apply for API key |
| OpenAI | [platform.openai.com](https://platform.openai.com/) | Register to get API Key |
| Anthropic (Claude) | [console.anthropic.com](https://console.anthropic.com/) | Register to get API Key |
| Google (Gemini) | [ai.google.dev](https://ai.google.dev/) | Register to get API Key |
| Bocha Search | [api.bocha.com](https://api.bocha.com/) | Register and apply for API key |
| Tavily | [tavily.com](https://tavily.com/) | Register to get API Key |

> 💡 For detailed configuration of more platforms (`base_url`, model names, etc.), refer to the `.shitbot/docs/AI_API_Platforms_OpenAI_SDK_Compatible` document.

---

## 🛠️ Tool Modules

ShitBot provides rich tool modules, each with detailed usage documentation:

### 🔧 Tool Overview

#### 🌐 Web Search Module
| Tool | Description |
|------|-------------|
| `search_web` | Web search |
| `webbot_task` | Browser task execution (WebBot) |

#### 📁 File Operation Module
| Tool | Description |
|------|-------------|
| `read_file` | Read file |
| `write_file` | Write file |
| `append_to_file` | Append content to file |
| `copy_file` | Copy file |
| `move_file` | Move file |
| `delete_file` | Delete file (requires confirmation) |
| `create_dir` | Create directory |
| `get_dir_content` | Get directory content |

#### 🐍 Code Execution Module
| Tool | Description |
|------|-------------|
| `run_code` | Run Python code snippet |
| `run_code_file` | Run Python code file |

#### 💻 System Command Module
| Tool | Description |
|------|-------------|
| `shell_command` | Execute shell commands |

#### 📧 Email Module
| Tool | Description |
|------|-------------|
| `send_email` | Send email (SMTP) |
| `list_email_folders` | List email folders |
| `get_email_list` | Get email list |
| `get_email_content` | Get email detail content |
| `search_emails` | Search emails |
| `mark_email_read` | Mark email as read |

#### ⏰ Scheduled Task Module
| Tool | Description |
|------|-------------|
| `once_after` | One-time delayed execution |
| `interval` | Periodic execution |
| `daily_at` | Daily scheduled execution |
| `cancel_timer` | Cancel scheduled task |
| `pause_timer` | Pause scheduled task |
| `resume_timer` | Resume scheduled task |
| `list` | List all scheduled tasks |

#### 💾 Memory Management Module
| Tool | Description |
|------|-------------|
| `save_memory` | Save current conversation memory |
| `get_memory` | Retrieve historical memory |

#### 📚 Documentation Module
| Tool | Description |
|------|-------------|
| `get_doc_list` | List all readable documents |
| `get_doc` | Get document content |

#### 🎭 Roles & Skills Module
| Tool | Description |
|------|-------------|
| `get_role` | List all roles |
| `get_skill` | List all skills |

---

## 🔧 Skills System

ShitBot supports a modular skill extension system, where each skill is an independent functional package providing professional domain workflows and tool integrations. Users can freely create and install skills to extend ShitBot's capabilities.

### 📦 Built-in Skills

| Skill Name | Description |
|-----------|-------------|
| **skill-creator** | Skill creation tool — design, build, and package custom skills |
| **role-skill** | Role creation tool — define role behaviors, skills, and tool recommendations |
| **clawhub** | Skill store — search and install community skills from ClawHub registry |
| **init_self** | Agent initialization — configure agent initial state and parameters |

### 🎯 Skill Features

- **Modular Design**: Each skill is independently packaged
- **Progressive Loading**: Skills loaded only when needed, saving context space
- **Resource Packaging**: Supports scripts, references, and asset files
- **Custom Development**: Create your own skills with `skill-creator`
- **Community Ecosystem**: Discover and install community skills via `clawhub`

### 📝 How to Create Skills

Use the built-in `skill-creator` skill and follow the prompts to create custom skills. You can also discover more skills from the community via `clawhub`.

---

## 🎭 Roles System

ShitBot supports a flexible role system with different professional capabilities and behavior patterns.

### 👥 Built-in Roles

| Role Name | Description |
|----------|-------------|
| **Coder** | General-purpose code writing — supports multiple languages and project types |

### 🎨 Role Features

- **Professional Domains**: Each role focuses on specific domains
- **Behavioral Customization**: Specific behavior patterns and response styles
- **Tool Recommendations**: Recommends suitable tools based on role characteristics
- **Flexible Switching**: Switch roles anytime based on task requirements

### 📝 How to Create Roles

Use the built-in `role-skill` skill and follow the prompts to create custom roles.

---

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

---

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

---

## 📁 Project Structure

```
ShitBot/
├── .gitignore                         # Git ignore rules
├── config.example.yaml                # Config template (copy to config.yaml)
├── models.json                        # Supported AI platforms list
├── requirements.txt                   # Dependencies list
├── README_CN.md                       # Chinese documentation
├── README_EN.md                       # English documentation
│
├── .shitbot/                          # ShitBot core data directory
│   ├── Self.example.txt               # Agent info template (copy to Self.txt)
│   ├── Safe.txt                       # Safety rules
│   ├── docs/                          # Built-in documentation
│   │   ├── ALL_TOOLS_GUIDE.md         # Complete tools guide
│   │   ├── SEARCH_TOOLS.md            # Search tools guide
│   │   ├── FILE_TOOLS.md              # File tools guide
│   │   ├── COMMAND_TOOLS.md           # Command line tools guide
│   │   ├── EMAIL_TOOLS.md             # Email tools guide
│   │   ├── EMAIL_READER_GUIDE.md      # Email reader guide
│   │   ├── TIMER_TOOLS.md             # Timer tools guide
│   │   ├── AI_API_Platforms_*.md      # AI API platform compatibility
│   │   └── Write_Doc.md               # Documentation writing guide
│   ├── skills/                        # Skills directory
│   │   ├── skill-creator/             # [Built-in] Skill creation tool
│   │   ├── role-skill/                # [Built-in] Role creation tool
│   │   ├── clawhub/                   # [Built-in] ClawHub skill store
│   │   └── init_self/                 # [Built-in] Agent initialization
│   ├── roles/                         # Roles directory
│   │   └── Coder/                     # [Built-in] Code writing role
│   ├── workfile/                      # Work files (placeholder files, auto-filled at runtime)
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
├── ai.py                              # AI client
├── bot.py                             # Bot core logic
├── config.py                          # Configuration management
├── main.py                            # Main program entry
├── memory.py                          # Memory management
├── prompt.py                          # Prompt management
├── terminal.py                        # Terminal interface
├── tool.py                            # Tool definition and execution
├── ui_components.py                   # UI components
├── log.py                             # Log management
├── token_tracker.py                   # Token tracking
├── workflows.py                       # Workflow management
└── init_project.py                    # Project initialization script
```

> **Note**: The following files/directories are excluded from the repository via `.gitignore`:
> - `config.yaml` — Contains sensitive API keys. Use `config.example.yaml` as a template.
> - `.shitbot/Self.txt` — User's personalized agent config. Use `Self.example.txt` as a template.
> - `.shitbot/workfile/` — Runtime work files (empty placeholders are provided).
> - `.shitbot/memory/`, `.shitbot/logs/`, `.shitbot/datas/` — Auto-generated at runtime.
> - `shitbot_env/`, `code_venv/` — Python virtual environments.
> - User-installed skills and user-created roles.

---

## ❓ FAQ

### 1. Program Won't Start
```bash
# Ensure dependencies are installed
pip install -r requirements.txt
# Ensure config file exists
cp config.example.yaml config.yaml
# Edit config.yaml and fill in your API keys
# Run initialization script
python init_project.py
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
3. Confirm port and encryption settings
4. For 163 email: enable IMAP/SMTP service in settings

### 5. Scheduled Task Not Executing
1. Confirm the program is running
2. Use the `list` tool to view task status
3. Check if task is paused

### 6. How to Install More Skills
Use the built-in `clawhub` skill to search and install community skills, or use `skill-creator` to create custom skills.

### 7. File Operation Denied
Check the `stop.file` configuration in `config.yaml` to ensure the target path is not in the forbidden list.

---

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

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details

---

<div align="center">

**Made with ❤️ by ShitBot Team**

</div>
