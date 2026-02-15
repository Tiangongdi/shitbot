# browser-use + GLM 使用指南

## 概述

browser-use 是一个专为 AI Agent 设计的浏览器自动化工具，可以理解网页结构并执行复杂的浏览器操作。

## 快速开始

### 1. 基本使用

```python
import asyncio
from browser_use import Agent, ChatOpenAI
from config import load_config


async def simple_example():
    config = load_config()
    
    llm = ChatOpenAI(
        model=config.browser.model,
        api_key=config.browser.api_key,
        base_url=config.browser.base_url,
        temperature=0.7
    )
    
    agent = Agent(
        task="访问 https://www.baidu.com 并搜索'人工智能'",
        llm=llm
    )
    
    result = await agent.run()
    print(result)


if __name__ == "__main__":
    asyncio.run(simple_example())
```

### 2. 使用 GLMBrowserAgent 类

```python
from browser_use_glm import GLMBrowserAgent


async def example():
    agent = GLMBrowserAgent()
    
    result = await agent.browse(
        task="访问 https://www.example.com 并提取所有链接"
    )
    
    print(result)


asyncio.run(example())
```

## 常见任务示例

### 搜索并提取信息

```python
task = """
访问 https://www.baidu.com
搜索'Python教程'
提取前5个搜索结果的标题和链接
"""
```

### 填写表单

```python
task = """
访问 https://example.com/login
在用户名输入框输入 'testuser'
在密码输入框输入 'password123'
点击登录按钮
等待页面加载完成
告诉我登录是否成功
"""
```

### 爬取数据

```python
task = """
访问 https://news.ycombinator.com
提取前10条新闻的标题、链接和分数
以JSON格式返回结果
"""
```

### 截图

```python
task = """
访问 https://www.example.com
等待页面完全加载
截图保存到 screenshot.png
"""
```

## 高级用法

### 自定义浏览器配置

```python
from browser_use import Agent, ChatOpenAI, BrowserSession


async def advanced_example():
    config = load_config()
    
    llm = ChatOpenAI(
        model=config.browser.model,
        api_key=config.browser.api_key,
        base_url=config.browser.base_url
    )
    
    browser = BrowserSession(
        headless=False,  # 显示浏览器窗口
        disable_security=True
    )
    
    agent = Agent(
        task="访问 https://www.example.com",
        llm=llm,
        browser=browser
    )
    
    result = await agent.run()
    await browser.close()
```

### 多步骤任务

```python
task = """
1. 访问 https://www.google.com
2. 搜索'browser-use python'
3. 点击第一个搜索结果
4. 滚动到页面底部
5. 提取页面主要内容
6. 返回摘要
"""
```

## 运行示例

### 测试基本功能

```bash
.\shitbot_env\Scripts\python browser_use_glm.py
```

### 在 ShitBot 中使用

```python
from browser_use_glm import GLMBrowserAgent


async def handle_browse_command(url, query):
    agent = GLMBrowserAgent()
    
    task = f"访问 {url} 并搜索 '{query}'，提取前3条结果"
    result = await agent.browse(task)
    
    return result
```

## 注意事项

1. **API 密钥**: 确保 config.yaml 中配置了正确的 GLM API 密钥
2. **网络连接**: 需要稳定的网络连接
3. **浏览器依赖**: 首次运行会自动下载 Playwright 浏览器
4. **资源占用**: 浏览器自动化会占用较多系统资源

## 故障排除

### Playwright 浏览器未安装

```bash
.\shitbot_env\Scripts\playwright install chromium
```

### API 密钥错误

检查 config.yaml 中的 browser 配置：

```yaml
browser:
  model: "glm-4.7"
  api_key: "your-api-key"
  base_url: "https://open.bigmodel.cn/api/paas/v4/"
```

### 网络超时

增加超时时间：

```python
llm = ChatOpenAI(
    model=config.browser.model,
    api_key=config.browser.api_key,
    base_url=config.browser.base_url,
    timeout=60  # 60秒超时
)
```

## 性能优化

1. **使用无头模式**: `headless=True`（默认）
2. **缓存浏览器实例**: 复用浏览器会话
3. **限制并发**: 避免同时运行多个浏览器实例
4. **清理资源**: 及时关闭浏览器

## 相关资源

- [browser-use 官方文档](https://github.com/browser-use/browser-use)
- [Playwright 文档](https://playwright.dev/python/)
- [GLM API 文档](https://open.bigmodel.cn/)
