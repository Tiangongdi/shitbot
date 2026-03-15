---
name: github-uploader
description: "GitHub项目上传助手。帮助用户将本地项目上传到GitHub仓库，包括初始化Git仓库、创建提交、关联远程仓库、推送代码等完整流程。当用户需要：(1) 上传项目到GitHub，(2) 初始化Git仓库，(3) 创建GitHub仓库并推送代码，(4) 处理Git上传相关问题，(5) 创建.gitignore和README文件时使用此技能。"
---

# GitHub上传助手 -- 该技能帮助用户将本地项目上传到GitHub仓库

## 功能概述

本技能提供完整的GitHub项目上传流程支持，包括：
- Git仓库初始化
- 文件暂存和提交
- 远程仓库关联
- 代码推送
- 常见问题处理

## 快速开始

### 基本上传流程

```bash
# 1. 初始化Git仓库
git init

# 2. 添加文件到暂存区
git add .

# 3. 创建首次提交
git commit -m "Initial commit"

# 4. 关联远程仓库
git remote add origin <repository-url>

# 5. 推送到GitHub
git branch -M main
git push -u origin main
```

## 详细工作流程

### 步骤1：检查当前环境

在上传前，先检查：
- 当前目录是否已经是Git仓库
- 是否已安装Git
- Git用户配置是否正确

```bash
# 检查Git状态
git status

# 检查Git配置
git config --global user.name
git config --global user.email
```

### 步骤2：创建必要文件

#### .gitignore文件

根据项目类型创建合适的.gitignore文件，常见模板：

**Python项目：**
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env
```

**Node.js项目：**
```
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.env
```

**通用模板：**
```
# 操作系统
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# 环境变量
.env
.env.local
```

#### README.md文件

创建项目说明文档：

```markdown
# 项目名称

## 项目简介
[项目描述]

## 安装
[安装说明]

## 使用方法
[使用说明]

## 许可证
MIT
```

### 步骤3：初始化仓库

如果当前目录不是Git仓库：

```bash
git init
```

### 步骤4：添加文件

```bash
# 添加所有文件
git add .

# 或添加特定文件
git add <file1> <file2>
```

### 步骤5：创建提交

```bash
git commit -m "提交说明"
```

提交信息最佳实践：
- 使用简洁明了的描述
- 使用祈使语气（如"Add feature"而非"Added feature"）
- 首字母大写
- 不以句号结尾

### 步骤6：关联远程仓库

**方式1：已有GitHub仓库**
```bash
git remote add origin https://github.com/username/repository.git
```

**方式2：使用SSH**
```bash
git remote add origin git@github.com:username/repository.git
```

### 步骤7：推送代码

```bash
# 首次推送
git branch -M main
git push -u origin main

# 后续推送
git push
```

## 常见问题处理

### 问题1：认证失败

**症状：** `Authentication failed` 或 `Permission denied`

**解决方案：**
1. 使用Personal Access Token（推荐）
2. 配置SSH密钥
3. 使用GitHub CLI登录

```bash
# 使用GitHub CLI
gh auth login

# 或配置凭证存储
git config --global credential.helper store
```

### 问题2：远程仓库已存在内容

**症状：** `! [rejected] (fetch first)` 或冲突

**解决方案：**
```bash
# 拉取并合并
git pull origin main --allow-unrelated-histories

# 解决冲突后提交
git add .
git commit -m "Merge remote changes"
git push
```

### 问题3：大文件上传失败

**症状：** `File larger than 100MB`

**解决方案：**
1. 使用Git LFS
2. 将大文件添加到.gitignore

```bash
# 安装Git LFS
git lfs install

# 跟踪大文件
git lfs track "*.psd"
git add .gitattributes
```

### 问题4：推送被拒绝

**症状：** `Updates were rejected`

**解决方案：**
```bash
# 强制推送（谨慎使用）
git push -f origin main

# 或先拉取再推送
git pull --rebase origin main
git push origin main
```

## 高级功能

### 分支管理

```bash
# 创建新分支
git checkout -b feature-branch

# 切换分支
git checkout main

# 合并分支
git merge feature-branch

# 删除分支
git branch -d feature-branch
```

### 撤销操作

```bash
# 撤销暂存
git reset HEAD <file>

# 撤销提交（保留修改）
git reset --soft HEAD~1

# 撤销提交（丢弃修改）
git reset --hard HEAD~1

# 修改最后一次提交
git commit --amend
```

### 查看历史

```bash
# 查看提交历史
git log --oneline

# 查看文件修改历史
git log --follow <file>

# 查看差异
git diff
```

## 最佳实践

1. **提交频率**：小步快跑，频繁提交
2. **提交信息**：清晰描述本次修改内容
3. **分支使用**：新功能使用分支开发
4. **忽略文件**：合理配置.gitignore
5. **定期同步**：及时拉取远程更新
6. **备份重要分支**：避免误删

## 工具推荐

- **GitHub CLI (gh)**：命令行工具，简化GitHub操作
- **Git LFS**：大文件支持
- **.gitignore生成器**：https://gitignore.io

## 参考资源

详细命令参考请查看 [references/git-commands.md](references/git-commands.md)
