# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Commands

### Install Dependencies
```bash
pip install -r requirements.txt
pip install -e .  # Install CLI command
```

### Install Playwright (for browser automation)
```bash
playwright install chromium
```

### Run the App
```bash
shitbot                      # Start interactive terminal (installed CLI)
python src/main.py           # Direct run
shitbot.bat                  # Windows quick start
shitbot -m "your question"   # Single chat mode
shitbot config               # Run configuration wizard
```

### Run Tests
```bash
# Run all tests
pytest test/

# Run specific test
python -m pytest test/test_execute_method.py -v
```

## Project Overview

ShitBot is a powerful AI assistant terminal application that supports 15+ AI API platforms. It provides Claude Code-like interactive terminal experience with capabilities including web search, browser automation, file operations, scheduled tasks, email, code execution, and more.

## Architecture

```
Entry Point → CLI (src/cli.py) → Main (src/main.py) → Terminal (src/terminal.py) → Bot (src/agent/bot.py)
```

### Key Modules

| Module | Purpose |
|--------|---------|
| `src/cli.py` | Command line interface, supports interactive mode and single chat mode |
| `src/main.py` | Program entry, initializes terminal |
| `src/terminal.py` | Interactive terminal UI with prompt_toolkit |
| `src/agent/bot.py` | Core Bot logic - handles chat flow, tool calls, memory |
| `src/agent/subagent.py` | SubAgent implementation for parallel task execution |
| `src/agent/subagent_manager.py` | Manages multiple subAgents, task queue, persistence |
| `src/tool.py` | Tool execution engine - all tools are defined here |
| `src/tool_registry.py` | Tool registry - manages available tools, filters by context |
| `src/ai.py` | AI client wrapper - connects to various AI APIs via litellm |
| `src/memory.py` | Memory management - conversation history and shared memory |
| `src/workflows.py` | Workflow management - different prompt templates for different tasks |
| `tools/` | Individual tool implementations (search, email, browser, timer, etc.) |
| `config/config.py` | Configuration loading and setup wizard |

### Architecture Principles

1. **Modular Tool System**: Tools are registered via `@registry.tool()` decorator in `src/tool.py`. Each tool has a docstring that becomes part of the AI function definition.

2. **SubAgent System**: Main bot can create multiple subAgents with different roles. Tasks run in background threads. SubAgents have isolated memory but can report results back to main agent's shared memory.

   - `create_subagent(role, description)` → creates a new subAgent
   - `subagent_task(task, role_id)` → assigns task to run in background
   - `get_subagent()` → lists all subAgents
   - Security: SubAgents cannot create subAgents (filtered by `tool_registry.py`)

3. **Multiple AI Platforms**: Uses litellm to support 100+ LLM providers. Configured via `config.yaml` or `.env`.

4. **Skills & Roles**: Extensible system - skills stored in `.shitbot/skills/`, roles in `.shitbot/roles/`. Can be installed from community via clawhub skill.

5. **Async First**: All core operations use asyncio for better concurrency.

6. **Safety First**: Multiple layers of security - high-risk operation blocking, file deletion confirmation, forbidden path protection, prompt injection filtering.

## Important Conventions

- All tools are defined in `src/tool.py` using the `@registry.tool()` decorator
- When adding a new tool, update the docstring parameters - they are used for AI function calling
- The `.shitbot/` directory contains runtime data and user configurations, excluded from git
- Configuration (`config.yaml`, `.env`) contains API keys and is excluded from git
- Tests are in the `test/` directory

## Important Files

- `.shitbot/docs/ALL_TOOLS_GUIDE.md` - Complete documentation for all built-in tools
- `config.example.yaml` - Configuration template
- `.env.example` - Environment variables template
- `pyproject.toml` - Project metadata and dependencies
