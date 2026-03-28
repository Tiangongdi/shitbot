. You can also discover more skills from the community via clawhub.

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
├── .env.example                       # Environment variables template
├── config.example.yaml                # Config template (copy to config.yaml)
├── models.json                        # Supported AI platforms list
├── pyproject.toml                     # Project configuration (includes CLI entry definition)
├── requirements.txt                   # Dependencies list
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
│   │   ├── EMAIL_TOOLS.md             # Email tools guide
│   │   ├── EMAIL_READER_GUIDE.md      # Email reader guide
│   │   ├── TIMER_TOOLS.md             # Timer tools guide
│   │   ├── AI_API_Platforms_*.md      # AI API platform compatibility
│   │   └── Write_Doc.md               # Documentation writing guide
│   ├── skills/                        # Skills directory
│   │   ├── skill-creator/             # [Built-in] Skill creation tool
│   │   ├── role-skill/                # [Built-in] Role creation tool
│   │   ├── clawhub/                   # [Built-in] ClawHub skill store
│   │   ├── init_self/                 # [Built-in] Agent initialization
│   │   └── project-update/            # [Built-in] Project update tool
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
├── config/                            # Configuration module
│   ├── __init__.py                    # Configuration initialization
│   └── config.py                      # Configuration loading
│
├── src/                               # Source code directory
│   ├── ai.py                          # AI client
│   ├── bot.py                         # Bot core logic
│   ├── cli.py                         # Command Line Interface (CLI)
│   ├── main.py                        # Main program entry
│   ├── memory.py                      # Memory management
│   ├── prompt.py                      # Prompt management
│   ├── terminal.py                    # Terminal interface
│   ├── tool.py                        # Tool definition and execution
│   ├── ui_components.py               # UI components
│   ├── log.py                         # Log management
│   ├── token_tracker.py               # Token tracking
│   └── workflows.py                   # Workflow management
│
└── init_project.py                    # Project initialization script
```

> **Note**: The following files/directories are excluded from the repository via `.gitignore`:
> - `config.yaml` — Contains sensitive API keys. Use `config.example.yaml` as a template.
> - `.env` — Contains sensitive API keys. Use `.env.example` as a template.
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
