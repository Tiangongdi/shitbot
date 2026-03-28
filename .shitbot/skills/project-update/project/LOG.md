# ShitBot 项目更新日志

## 2026-03-15 更新记录

### 更新时间
2026-03-15 16:45

### 更新内容
1. **添加邮件读取工具**
   - 创建 `tools/email_reader.py` - 邮件读取核心工具
   - 支持IMAP协议连接邮箱
   - 功能包括：
     - 列出邮箱文件夹
     - 获取邮件列表（支持未读筛选）
     - 读取邮件详细内容
     - 搜索邮件（按主题、发件人、正文）
     - 标记邮件为已读

2. **更新配置文件**
   - 在 `config.py` 中添加 `IMAPConfig` 数据类
   - 在 `config.yaml` 中添加IMAP配置项
   - 支持QQ、163、Gmail等主流邮箱

3. **集成到工具系统**
   - 在 `tool.py` 中导入 `EmailReader`
   - 添加邮件读取器初始化方法 `_init_email_reader()`
   - 实现5个邮件读取工具方法：
     - `list_email_folders()` - 列出文件夹
     - `get_email_list()` - 获取邮件列表
     - `get_email_content()` - 读取邮件内容
     - `search_emails()` - 搜索邮件
     - `mark_email_read()` - 标记已读
   - 添加5个工具定义到 `get_tools_definition()`

4. **创建测试文件**
   - `test_email_reader.py` - 交互式测试脚本
   - `test_email_reader_auto.py` - 自动化测试脚本
   - `run_email_test.bat` - Windows启动脚本

5. **创建文档**
   - `Docs/EMAIL_READER_GUIDE.md` - 完整使用指南

### 用户要求
用户要求添加一个获取当前邮箱内容的工具，并集成到tool.py中

### 更新人员
偷摸零 (AI助手)

---

## 2026-03-15 更新记录（上午）

### 更新时间
2026-03-15 15:44

### 更新内容
1. **更新 ALL_TOOLS_GUIDE.md 文档**
   - 添加新工具：`run_code` - 运行Python代码
   - 添加新工具：`run_code_file` - 运行Python代码文件
   - 添加新工具：`append_to_file` - 在文件末尾追加内容
   - 添加新工具：`get_role` - 列出所有角色
   - 添加新工具：`get_skill` - 列出所有技能
   - 更新工具说明：`webbot_task` 替代原来的 `browse_page`
   - 添加新的模块分类：代码执行模块、角色管理模块、技能管理模块
   - 更新注意事项，添加文件写入限制和删除确认说明
   - 更新快速参考表格
   - 文档版本升级到 2.0

2. **更新 README_CN.md 文档**
   - 添加代码执行能力到主要亮点
   - 更新工具模块列表，添加代码执行模块
   - 更新技能系统列表，添加所有内置技能
   - 更新角色系统列表，添加所有内置角色
   - 更新项目结构，添加tools目录下的所有工具文件
   - 添加Python代码执行失败的常见问题
   - 更新使用示例，添加代码执行示例

### 用户要求
用户要求更新doc里面的tools库和README文件

### 更新人员
偷摸零 (AI助手)

---

## 历史更新记录

（之前的更新记录可以在这里添加）

---

## 2026-03-28 更新记录

### 更新时间
2026-03-28 17:30

### 更新内容
1. **配置CLI全局命令功能**
   - 重构 `cli.py` - 使用 Click 的 group 模式，支持子命令
   - `shitbot` - 不带参数默认启动交互式对话
   - `shitbot config` - 运行配置向导
   - `shitbot chat` / `shitbot -m` - 单次对话模式
   - 在 `pyproject.toml` 中配置 `[project.scripts]`，安装后可全局使用 `shitbot` 命令

2. **重构项目目录结构**
   - 将所有核心源码移动到 `src/` 目录下，符合Python打包规范
   - 将配置文件统一放到 `config/` 目录
     - `config/config.py` - 配置管理
     - `config/config.example.yaml` - 配置模板
     - `config/models.json` - 支持的AI模型列表
     - `config/common_models.json` - 常用模型列表
   - `tools/` 保持不动，按用户要求保留原有结构
   - 修复所有导入路径，确保能正常运行

3. **修复代码问题**
   - 修复 `src/main.py` 导入路径问题
   - 修复 `src/terminal.py` 中 `config_path` 路径指向 `config/config.yaml`
   - 修复 `config/config.py` 中 `config_path` 默认路径指向正确位置

4. **创建 .env.example**
   - 添加环境变量配置示例模板
   - 方便使用环境变量管理配置的用户参考

### 用户要求
用户要求配置CLI功能，让用户可以在任何地方使用 `shitbot` 命令启动程序，保持 `tools` 文件夹不动，config.yaml会在第一次使用自动生成。

### 更新人员
大史 (AI助手)

---
