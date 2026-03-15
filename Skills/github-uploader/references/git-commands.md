# Git命令参考手册

## 配置命令

### 初始配置
```bash
# 设置用户名
git config --global user.name "Your Name"

# 设置邮箱
git config --global user.email "your.email@example.com"

# 设置默认编辑器
git config --global core.editor "code --wait"

# 设置默认分支名
git config --global init.defaultBranch main

# 查看所有配置
git config --list
```

### 凭证配置
```bash
# 存储凭证（避免每次输入密码）
git config --global credential.helper store

# 使用缓存（临时存储）
git config --global credential.helper cache

# 设置缓存时间（15分钟）
git config --global credential.helper 'cache --timeout=900'
```

## 仓库操作

### 初始化
```bash
# 在当前目录初始化
git init

# 克隆远程仓库
git clone <url>

# 克隆指定分支
git clone -b <branch> <url>

# 浅克隆（只克隆最近一次提交）
git clone --depth 1 <url>
```

### 远程仓库
```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin <url>

# 修改远程仓库URL
git remote set-url origin <new-url>

# 删除远程仓库
git remote remove origin

# 重命名远程仓库
git remote rename old-name new-name
```

## 文件操作

### 添加文件
```bash
# 添加所有文件
git add .

# 添加特定文件
git add file1.txt file2.txt

# 添加某个目录下所有文件
git add src/

# 交互式添加
git add -p

# 添加所有修改和删除的文件（不包括新文件）
git add -u
```

### 删除文件
```bash
# 删除文件（从工作区和暂存区）
git rm file.txt

# 删除文件（仅从暂存区）
git rm --cached file.txt

# 删除目录
git rm -r directory/

# 删除所有未跟踪的文件
git clean -fd
```

### 移动/重命名
```bash
# 重命名文件
git mv old-name.txt new-name.txt

# 移动文件
git mv file.txt new-directory/
```

## 提交操作

### 基本提交
```bash
# 提交暂存区的文件
git commit -m "Commit message"

# 提交所有已跟踪的文件（跳过暂存）
git commit -a -m "Commit message"

# 修改最后一次提交
git commit --amend -m "New message"

# 修改最后一次提交（不改消息）
git commit --amend --no-edit
```

### 提交信息规范
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type类型：**
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档修改
- `style`: 代码格式修改
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例：**
```
feat(auth): add user login feature

- Add login form component
- Implement JWT authentication
- Add login API endpoint

Closes #123
```

## 分支操作

### 创建分支
```bash
# 创建新分支
git branch new-branch

# 创建并切换分支
git checkout -b new-branch

# 基于远程分支创建
git checkout -b new-branch origin/main

# 创建空分支（无历史）
git checkout --orphan new-branch
```

### 切换分支
```bash
# 切换分支
git checkout branch-name

# 切换到上一个分支
git checkout -

# 切换到main分支
git checkout main
```

### 查看分支
```bash
# 查看本地分支
git branch

# 查看所有分支（包括远程）
git branch -a

# 查看远程分支
git branch -r

# 查看分支详细信息
git branch -vv
```

### 合并分支
```bash
# 合并指定分支到当前分支
git merge branch-name

# 合并但不创建合并提交
git merge --ff-only branch-name

# 强制创建合并提交
git merge --no-ff branch-name

# 中止合并
git merge --abort
```

### 删除分支
```bash
# 删除已合并的分支
git branch -d branch-name

# 强制删除分支
git branch -D branch-name

# 删除远程分支
git push origin --delete branch-name
```

## 推送和拉取

### 推送
```bash
# 推送到远程仓库
git push

# 首次推送并设置上游
git push -u origin main

# 推送所有分支
git push --all

# 推送标签
git push --tags

# 强制推送（谨慎使用）
git push -f

# 强制推送（更安全）
git push --force-with-lease
```

### 拉取
```bash
# 拉取并合并
git pull

# 拉取并变基
git pull --rebase

# 拉取指定分支
git pull origin main

# 拉取所有分支
git fetch --all
```

### 获取
```bash
# 获取远程更新（不合并）
git fetch

# 获取指定远程仓库
git fetch origin

# 获取并清理远程已删除的分支
git fetch -p
```

## 撤销操作

### 撤销暂存
```bash
# 撤销暂存（保留工作区修改）
git reset HEAD file.txt

# 撤销所有暂存
git reset HEAD
```

### 撤销修改
```bash
# 撤销工作区修改
git checkout -- file.txt

# 撤销工作区修改（新语法）
git restore file.txt

# 从暂存区恢复
git restore --staged file.txt
```

### 撤销提交
```bash
# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1

# 撤销最后一次提交（保留工作区修改）
git reset --mixed HEAD~1

# 撤销最后一次提交（丢弃所有修改）
git reset --hard HEAD~1

# 撤销多个提交
git reset --hard HEAD~3
```

### 回退提交
```bash
# 创建新提交来撤销指定提交
git revert <commit-hash>

# 撤销多个提交
git revert <commit1>..<commit2>

# 撤销但不自动提交
git revert --no-commit <commit-hash>
```

## 查看信息

### 状态查看
```bash
# 查看状态
git status

# 简洁状态
git status -s

# 查看被忽略的文件
git status --ignored
```

### 日志查看
```bash
# 查看提交历史
git log

# 简洁日志
git log --oneline

# 图形化日志
git log --graph --oneline --all

# 查看最近N次提交
git log -n 5

# 查看文件修改历史
git log --follow file.txt

# 查看某个作者的提交
git log --author="name"

# 查看某个时间段的提交
git log --since="2024-01-01" --until="2024-12-31"
```

### 差异查看
```bash
# 查看工作区和暂存区的差异
git diff

# 查看暂存区和最后一次提交的差异
git diff --staged

# 查看两个提交之间的差异
git diff commit1 commit2

# 查看文件差异
git diff file.txt

# 查看分支差异
git diff branch1 branch2
```

### 文件查看
```bash
# 查看文件内容（指定版本）
git show commit-hash:file.txt

# 查看提交详情
git show commit-hash

# 查看文件每一行的修改历史
git blame file.txt
```

## 暂存操作

### 基本操作
```bash
# 暂存当前修改
git stash

# 暂存并添加消息
git stash save "message"

# 查看暂存列表
git stash list

# 应用最近一次暂存
git stash apply

# 应用指定暂存
git stash apply stash@{2}

# 应用并删除暂存
git stash pop

# 删除暂存
git stash drop stash@{0}

# 清空所有暂存
git stash clear
```

## 标签操作

### 创建标签
```bash
# 创建轻量标签
git tag v1.0.0

# 创建附注标签
git tag -a v1.0.0 -m "Version 1.0.0"

# 为指定提交创建标签
git tag -a v1.0.0 commit-hash
```

### 管理标签
```bash
# 查看所有标签
git tag

# 查看标签信息
git show v1.0.0

# 删除本地标签
git tag -d v1.0.0

# 删除远程标签
git push origin --delete v1.0.0

# 推送标签到远程
git push origin v1.0.0

# 推送所有标签
git push --tags
```

## 变基操作

### 基本变基
```bash
# 变基到main分支
git rebase main

# 交互式变基（最近3次提交）
git rebase -i HEAD~3

# 中止变基
git rebase --abort

# 继续变基
git rebase --continue

# 跳过当前提交
git rebase --skip
```

## 其他命令

### 归档
```bash
# 创建归档文件
git archive -o project.zip HEAD

# 创建指定目录的归档
git archive -o project.zip HEAD:src/
```

### 清理
```bash
# 删除未跟踪的文件
git clean -f

# 删除未跟踪的文件和目录
git clean -fd

# 预览将被删除的文件
git clean -n

# 删除被忽略的文件
git clean -fX
```

### 子模块
```bash
# 添加子模块
git submodule add <url> path/to/submodule

# 初始化子模块
git submodule init

# 更新子模块
git submodule update

# 克隆包含子模块的项目
git clone --recursive <url>
```

## 常见场景

### 场景1：撤销最后一次提交但保留修改
```bash
git reset --soft HEAD~1
```

### 场景2：修改最后一次提交信息
```bash
git commit --amend -m "New commit message"
```

### 场景3：合并多个提交
```bash
git rebase -i HEAD~3
# 将pick改为squash
```

### 场景4：从其他分支复制文件
```bash
git checkout other-branch -- file.txt
```

### 场景5：查看某个文件的修改历史
```bash
git log --follow -p file.txt
```

### 场景6：撤销已推送的提交
```bash
git revert <commit-hash>
git push
```

### 场景7：解决合并冲突
```bash
# 查看冲突文件
git status

# 手动解决冲突后
git add <resolved-file>
git commit
```

### 场景8：同步fork的仓库
```bash
# 添加上游仓库
git remote add upstream <original-repo-url>

# 获取上游更新
git fetch upstream

# 合并到本地
git merge upstream/main

# 推送到自己的仓库
git push origin main
```
