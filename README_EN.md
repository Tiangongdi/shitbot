# ShitBot 💩

<div align="center">

**💩 A Powerful AI Assistant Terminal Application 💩**


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
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [FAQ](#faq)
- [Contributing](#contributing)

---

## 🎯 Introduction

ShitBot is a powerful AI assistant terminal application that supports multiple AI APIs (ZhipuAI, Bocha), with complete browser automation, file operations, scheduled tasks, email sending, and more. Users can interact naturally with AI through a Claude Code-like terminal interface and instruct AI to complete various complex tasks.

**Key Highlights:**
- 🤖 Multi-AI provider support (ZhipuAI GLM, Bocha Search)
- 🌐 Complete browser automation capabilities
- 📁 Powerful file operation functions
- ⏰ Flexible scheduled task system
- 📧 Email sending functionality
- 💾 Intelligent memory management
- 📚 Built-in documentation system
- 🔧 Extensible Skills System
- 🎭 Flexible Roles System
- 🎨 Modern terminal interface

---

## ✨ Core Features

### 🤖 Multi-AI Provider Support
- **Recommended** ZhipuAI (GLM): Supports GLM-4, GLM-5 and other models
- **Bocha Search**: Professional web search API
- Streaming response support
- Easy provider switching

### 🌐 Browser Automation
- Playwright-based visual browser control
- Web navigation and interaction
- Intelligent content extraction and summarization
- Form filling and searching
- Page screenshot functionality
- JavaScript execution

### 📁 File Operations
- File read/write operations
- File copy and move
- Directory creation and management
- Safe file deletion (requires user confirmation)
- Forbidden path protection mechanism

### ⏰ Scheduled Task System
- One-time delayed execution
- Periodic task execution
- Daily scheduled execution
- Task management (pause, resume, cancel)

### 📧 Email Sending
- SMTP protocol support
- TLS/SSL encryption
- Support for multiple email services

### 💾 Intelligent Memory Management
- Conversation memory saving
- Historical memory retrieval
- Intelligent memory summarization

### 📚 Documentation System
- Built-in tool usage documentation
- Quick reference guides
- Modular documentation management

### 🔧 Skills System
- Support for Claude Code's Skill format
- Custom skill development
- Modular capability extension
- Built-in practical skills

### 🎭 Roles System
- Support for custom role settings
- Flexible role switching
- Professional domain role support
- Role-specific behaviors and tool recommendations

### 🎨 Modern Terminal Interface
- Claude Code-like interaction experience
- Colorful output and formatted display
- Chat history records

---

## 💻 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11 (tested on Windows environment)
- **Browser**: Microsoft Edge (Chromium version)
- **Network**: Stable network connection
- **API Keys**: ZhipuAI and/or Bocha API keys

---

## 🚀 Quick Start

### 1. Clone the Project

```bash
git clone https://github.com/yourusername/ShitBot.git
cd ShitBot
```

### 2. Create Virtual Environment

```bash
# Execute in the project root directory
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

### 5. Configure Project
Execute `init_project.py` to initialize the project, which will prompt for API keys and other information.

### 6. Run the Program

```bash
python main.py
```

---

## ⚙️ Configuration

### Complete Configuration File Structure

```yaml
# AI Provider Configuration
ai:
  api_key: ""           # ZhipuAI API key (required)
  value: ""             # API platform name
  model: "glm-5"        # Model name

# Bocha Search Configuration
bocha:
  api_key: ""           # Bocha API key (required)
  base_url: ""          # API address
  index_name: "news"    # Search index

# Browser Configuration
browser:
  playwright_browsers_path: "D:\\playwright_browsers"  # Playwright browser path

# Default Provider
default_provider: "ai"

# Email Configuration
email:
  email: "your_email@163.com"      # Sender email
  password: "your_password"         # Email authorization code
  smtp_server: "smtp.163.com"       # SMTP server
  smtp_port: 465                    # SMTP port
  use_tls: true                     # Use TLS

# Forbidden Access Paths
stop:
  file: []  # List of forbidden file paths

# User Configuration
user:
  bot_name: "Tomoling"              # AI assistant name
  user_name: "User"                 # User name
  bot_prompt: "You often say gugu gaga (penguin sounds)"  # AI personality setting
```

### API Key Acquisition

**ZhipuAI**
1. Visit [ZhipuAI Open Platform](https://open.bigmodel.cn/)
2. Register an account and apply for an API key
3. Fill the key in the configuration file's `ai.api_key`

**Bocha Search**
1. Visit [Bocha API Official Site](https://api.bocha.com/)
2. Register an account and apply for an API key
3. Fill the key in the configuration file's `bocha.api_key`

---

## 🛠️ Tool Modules

ShitBot provides rich tool modules, each with detailed usage documentation:

### 📚 Documentation List

| Document Name | Description |
|--------------|-------------|
| [ALL_TOOLS_GUIDE](Docs/ALL_TOOLS_GUIDE.md) | Complete Tool Usage Guide |
| [SEARCH_TOOLS](Docs/SEARCH_TOOLS.md) | Search Tools Guide |
| [FILE_TOOLS](Docs/FILE_TOOLS.md) | File Operation Tools Guide |
| [COMMAND_TOOLS](Docs/COMMAND_TOOLS.md) | Command Line Tools Guide |
| [EMAIL_TOOLS](Docs/EMAIL_TOOLS.md) | Email Tools Guide |
| [TIMER_TOOLS](Docs/TIMER_TOOLS.md) | Timer Tools Guide |
| [INPUT_TOOLS](Docs/INPUT_TOOLS.md) | Input Tools Guide |
| [AI_API_Platforms_OpenAI_SDK_Compatible](Docs/AI_API_Platforms_OpenAI_SDK_Compatible.md) | AI API Platform Compatibility Document |

### 🔧 Tool Overview

#### Web Search Module
- `search_web` - Web search
- `browse_page` - Web page browsing and content extraction

#### File Operation Module
- `read_file` - Read file
- `write_file` - Write file
- `copy_file` - Copy file
- `move_file` - Move file
- `delete_file` - Delete file
- `create_dir` - Create directory
- `get_dir_content` - Get directory content

#### System Command Module
- `shell_command` - Execute shell commands

#### Email Sending Module
- `send_email` - Send email

#### Scheduled Task Module
- `once_after` - One-time delayed execution
- `interval` - Periodic execution
- `daily_at` - Daily scheduled execution
- `cancel` - Cancel scheduled task
- `pause` - Pause scheduled task
- `resume` - Resume scheduled task
- `list` - List all scheduled tasks

#### User Interaction Module
- `input` - User input
- `input_y_or_n` - User confirmation

#### Memory Management Module
- `save_memory` - Save current conversation memory
- `get_memory` - Retrieve historical memory

#### Documentation Management Module
- `get_doc_list` - List all readable documents
- `get_doc` - Get document content

---

## 🔧 Skills System

ShitBot supports a modular skill extension system, where each skill is an independent functional package providing professional domain workflows and tool integrations.

### 📦 Built-in Skills List

| Skill Name | Description |
|-----------|-------------|
| **skill-creator** | Create or update AgentSkills, used for designing, structuring, and packaging skills, source: [openclaw](https://github.com/openclaw/openclaw) |
| **role-skill** | Create or update AgentRoles, used for defining role behaviors, skills, and tool recommendations |

### 🎯 Skill Features

- **Modular Design**: Each skill is independently packaged, easy to manage and extend
- **Progressive Loading**: Skill content is loaded only when needed, saving context space
- **Resource Packaging**: Supports packaging of scripts, reference documents, and resource files
- **Custom Development**: Users can create their own skills as needed

### 📝 How to Create Skills

Refer to the `skill-creator` skill documentation to learn how to create custom skills.

---

## 🎭 Roles System

ShitBot supports a flexible role system, where different roles have different professional capabilities and behavior patterns, allowing role switching based on task requirements.

### 👥 Built-in Roles List

| Role Name | Description |
|----------|-------------|
| **GitHubUploader** | GitHub upload assistant role, helping users manage Git repositories and GitHub projects |

### 🎨 Role Features

- **Professional Domains**: Each role focuses on specific domains, providing professional services
- **Behavioral Customization**: Roles have specific behavior patterns and response styles
- **Tool Recommendations**: Recommends the most suitable tools based on role characteristics
- **Flexible Switching**: Roles can be switched at any time based on task requirements

### 📝 How to Create Roles

Refer to the `role-skill` skill documentation to learn how to create custom roles.

---

## 💡 Usage Examples

### Basic Conversation

```
You: Hello, please introduce yourself

AI: Gugu gaga! Hello! I'm Tomoling, an intelligent AI assistant. I can help you:
1. Search web information
2. Operate files
3. Browse web pages
4. Send emails
5. Set up scheduled tasks
6. Use various skills and roles
... and many other features!

How can I help you?
```

### Web Search

```
You: Help me search for the latest AI news

AI: Okay, I'll search for the latest AI news for you.
[Calling search_web tool]
Found the following news:
1. OpenAI releases GPT-5...
2. Google launches Gemini 2.0...
...
```

### File Operations

```
You: Help me read the d:\project\test.txt file

AI: Okay, I'll read this file.
[Calling read_file tool]
File content:
...
```

### Scheduled Tasks

```
You: Help me set up a daily 9 AM reminder

AI: Okay, I'll set up a daily 9 AM reminder for you.
[Calling daily_at tool]
Scheduled task added: Execute reminder task daily at 9:0
```

### Browser Control

```
You: Help me open Baidu and search for "artificial intelligence"

AI: Okay, I'll open Baidu and search for "artificial intelligence".
[Calling browse_page tool]
Visiting Baidu...
Search results obtained...
```

### Using Skills

```
You: Help me create a new skill

AI: Okay, I'll help you create a new skill.
[Using skill-creator skill]
Please tell me the skill name and purpose...
```

### Switching Roles

```
You: I want you to help me analyze the market situation

AI: Okay, let me switch to the market analyst role.
[Switching to MarketAnalyst role]
Now I'm a professional market analyst, I can help you with market research and competitive analysis...
```

---

## 📁 Project Structure

```
ShitBot/
├── Docs/                   # Documentation directory
│   ├── ALL_TOOLS_GUIDE.md  # Complete tools guide
│   ├── SEARCH_TOOLS.md     # Search tools guide
│   ├── FILE_TOOLS.md       # File tools guide
│   ├── COMMAND_TOOLS.md    # Command tools guide
│   ├── EMAIL_TOOLS.md      # Email tools guide
│   ├── TIMER_TOOLS.md      # Timer tools guide
│   ├── INPUT_TOOLS.md      # Input tools guide
│   ├── AI_API_Platforms_OpenAI_SDK_Compatible.md  # AI API Platform Compatibility Document
│   ├── HELLO.md            # Tool usage guide
│   └── Write_Doc.md        # Documentation writing guide
├── Skills/                 # Skills directory
│   ├── skill-creator/      # Skill creation tool
│   ├── role-skill/         # Role creation tool
│   ├── market-research/    # Market research skill
│   └── github-uploader/    # GitHub upload assistant
├── Roles/                  # Roles directory
│   ├── Coder/              # Programmer role
│   ├── MarketAnalyst/      # Market analyst role
│   ├── VideoScriptWriter/  # Video script writer role
│   └── GitHubUploader/     # GitHub upload assistant role
├── memory/                 # Memory storage directory
├── prompt/                 # Prompts directory
├── tools/                  # Tools module directory
├── Logs/                   # Logs directory
├── ai.py                   # AI client
├── bot.py                  # Bot core logic
├── config.py               # Configuration management
├── main.py                 # Main program entry
├── memory.py               # Memory management
├── prompt.py               # Prompt management
├── terminal.py             # Terminal interface
├── tool.py                 # Tool definition and execution
├── ui_components.py        # UI components
├── log.py                  # Log management
├── init_project.py         # Project initialization script
├── config.yaml             # Configuration file
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation
```

---

## ❓ FAQ

### 1. Program Won't Start

**Problem**: Missing dependencies or configuration file doesn't exist

**Solution**:
```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Configuration file will be created automatically if it doesn't exist
# Edit config.yaml and fill in API keys
```

### 2. API Call Failed

**Problem**: Authentication error or connection failure

**Solution**:
1. Check if API key is correct
2. Confirm network connection is normal
3. Check if API quota is sufficient
4. Confirm base_url configuration is correct

### 3. Browser Won't Start

**Problem**: Playwright browser related errors

**Solution**:
```bash
# Install Playwright browser
playwright install chromium

# Or specify browser path in config.yaml
browser:
  playwright_browsers_path: "D:\\playwright_browsers"
```

### 4. File Operation Denied

**Problem**: Prompt says "Operation is in the forbidden list"

**Solution**:
Check the `stop.file` configuration in `config.yaml` to ensure the target path is not in the forbidden list.

### 5. Email Sending Failed

**Problem**: Email sending returns error

**Solution**:
1. Confirm email authorization code is correct (not login password)
2. Check SMTP server configuration
3. Confirm SMTP port and TLS settings are correct

### 6. Scheduled Task Not Executing

**Problem**: Scheduled task set but not executing

**Solution**:
1. Confirm the program is running
2. Use the `list` tool to view task status
3. Check if task is paused

### 7. Skill or Role Cannot Be Loaded

**Problem**: Prompt says skill or role doesn't exist

**Solution**:
1. Check if the corresponding folder exists in Skills or Roles directory
2. Confirm SKILL.md or ROLE.md file format is correct
3. Refer to documentation to learn how to create custom skills and roles

---

## 🤝 Contributing

Contributions and issue reports are welcome!

### Contribution Steps

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

### Code Standards

- Follow PEP 8 coding standards
- Add necessary comments and documentation
- Write unit tests

### Contributing Skills or Roles

Welcome to contribute new skills or roles to ShitBot:

1. **Contribute Skills**: Create new skill folders in the `Skills/` directory
2. **Contribute Roles**: Create new role folders in the `Roles/` directory
3. Develop following the format of existing skills and roles
4. Submit a Pull Request with detailed feature description

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details

---

## 📮 Contact

For questions or suggestions, feel free to contact us through:

- Submit an Issue
- Email: shitbot@163.com

---

<div align="center">

**Made with ❤️ by ShitBot Team**

Gugu gaga! 🐧

</div>
