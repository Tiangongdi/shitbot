# ShitBot 项目目录说明

## 项目根目录结构

```
ShitBot/
├── Docs/                   # 文档目录
├── Skills/                 # 技能目录
├── Roles/                  # 角色目录
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

## 核心文件说明

### 主程序文件
- **main.py**: 程序入口，启动终端界面
- **bot.py**: 机器人核心逻辑，处理对话和工具调用
- **ai.py**: AI客户端，处理与AI API的通信
- **tool.py**: 工具定义和执行，包含所有可用工具的实现

### 配置文件
- **config.py**: 配置管理模块
- **config.yaml**: 配置文件，包含API密钥、用户设置等

### 功能模块
- **memory.py**: 记忆管理
- **prompt.py**: 提示词管理
- **terminal.py**: 终端界面
- **ui_components.py**: UI组件
- **log.py**: 日志管理

## Docs 目录结构

```
Docs/
├── ALL_TOOLS_GUIDE.md              # 完整工具使用指南
├── SEARCH_TOOLS.md                 # 搜索工具使用指南
├── FILE_TOOLS.md                   # 文件操作工具使用指南
├── COMMAND_TOOLS.md                # 命令行工具使用指南
├── EMAIL_TOOLS.md                  # 邮件工具使用指南
├── TIMER_TOOLS.md                  # 计时器工具使用指南
├── INPUT_TOOLS.md                  # 输入工具使用指南
├── AI_API_Platforms_OpenAI_SDK_Compatible.md  # AI API 平台兼容性文档
├── HELLO.md                        # 工具使用指南
└── Write_Doc.md                    # 文档编写指南
```

## Skills 目录结构

```
Skills/
├── bilibili-update-viewer/         # B站更新查看器
├── clawhub/                        # ClawHub技能库
├── docx/                           # Word文档操作
├── find_skill/                     # 技能发现
├── github-uploader/                # GitHub上传助手
├── idea-expander/                  # 项目灵感扩展
├── market-research/                # 市场调研
├── ppt-generator/                  # PPT生成器
├── proj-pilot/                     # 项目管理助手
├── project-update/                 # 项目更新流程
│   ├── SKILL.md                    # 技能说明
│   └── project/                    # 工作文件
│       ├── LOG.md                  # 更新日志
│       └── MUNO.md                 # 目录说明
├── role-skill/                     # 角色创建
├── self-improving-agent/           # 自我改进
├── skill-creator/                  # 技能创建
├── skill-vetter-1.0.0/             # 技能审查
├── tech-selection-report/          # 技术选型报告
├── ui-ux-pro-max/                  # UI/UX设计
└── user-profile-generator/         # 用户画像生成器
```

## Roles 目录结构

```
Roles/
├── Coder/                          # 代码编写角色
├── GitHubUploader/                 # GitHub上传助手角色
├── MarketAnalyst/                  # 市场分析师角色
├── SpringBootCoder/                # SpringBoot开发者角色
├── UserProfiler/                   # 用户画像分析师角色
└── VideoScriptWriter/              # 视频脚本编写角色
```

## tools 目录结构

```
tools/
├── bocha.py                        # 博查搜索API
├── doc.py                          # 文档管理
├── memory_bot.py                   # 记忆机器人
├── playwiright.py                  # 浏览器自动化
├── role.py                         # 角色管理
├── safe.py                         # 安全检查
├── skill.py                        # 技能管理
├── tavily_api.py                   # Tavily搜索API
├── timer.py                        # 定时任务
├── venv_manager.py                 # 虚拟环境管理
├── webbot.py                       # WebBot浏览器操作
└── __init__.py                     # 模块初始化
```

## 工具模块说明

### bocha.py
- 博查搜索API客户端
- 提供网络搜索功能

### doc.py
- 文档管理系统
- 管理内置文档的读取和查询

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

*最后更新: 2026-03-15*
