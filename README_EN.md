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
- [Command Line Usage](#command-line-usage)
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
- ⌨️ Command Line Interface (CLI) support, globally accessible after installation

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
git clone https://github.com/Tiangongdi/shitbot.git
cd shitbot
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

### 4. Install Dependencies and CLI Tool

```bash
pip install -r requirements.txt
# Install CLI command (globally accessible `shitbot` command)
pip install -e .
```

### 5. Initialize Configuration

You can choose manual configuration or use the setup wizard:

**Option 1: Using Setup Wizard (Recommended)**

```bash
shitbot config
```

Follow the prompts to select an AI platform, enter API keys, agent info, etc. Configuration files will be generated automatically.

**Option 2: Manual Copy Template**

```bash
# Copy configuration template
cp .env.example .env
# If you prefer YAML format:
cp config.example.yaml config.yaml
# Copy agent info template
cp .shitbot/Self.example.txt .shitbot/Self.txt
```

Then edit the configuration file to fill in your API keys and other settings.

### 6. Run the Program

**Option 1: Using CLI Command (Recommended)**

```bash
shitbot shitbot
```

**Option 2: Run Python Script Directly**

```bash
python src/main.py
```

---

## ⌨️ Command Line Usage

ShitBot provides a complete command line interface (CLI). After installation, you can use the `shitbot` command globally.

### Available Commands

| Command | Description |
|---------|-------------|
| `shitbot shitbot` | Start interactive conversation (default mode) |
| `shitbot shitbot -m "Your question"` | Execute single conversation, output result directly |
| `shitbot config` | Run setup wizard to initialize configuration |

### Command Details

#### 1. Start Interactive Conversation

```bash
shitbot shitbot
```

Enter interactive conversation mode. You can continuously chat with ShitBot just like in Claude Code.

#### 2. Single Conversation Mode

```bash
shitbot shitbot -m "Calculate 1+1 for me"
shitbot shitbot -m "Search today's AI news"
shitbot shitbot -m "Read README.md in current directory and summarize"
```

Suitable for scripting or quick queries. Executes and outputs the result directly, then exits.

#### 3. Setup Wizard

```bash
shitbot config
```

Interactive setup wizard guides you through AI platform selection, API key entry, agent information setup, and automatically generates configuration files.

### Usage Examples

```bash
# Start interactive chat
shitbot shitbot

# Single question
shitbot shitbot -m "What files are in the current directory?"

# Rerun setup wizard
shitbot config
```

---
 is normal
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

## ⚠️ Development Note

Most of the code in this project was generated through AI-assisted programming (Vibe Coding). Human responsibilities include architecture design, requirement definition, and code review.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details

---

<div align="center">

**Made with ❤️ by ShitBot Team**

</div>
