"""
WebBot 智能体
功能：接收任务、处理任务、调用浏览器工具、AI分析
作为ShitBot的Web调查助手，负责执行网页相关的自动化任务
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import json
from typing import Dict, Any, Optional, List
from tools.playwiright import SmartWebExtractor, BrowserTools, ExtractedContent
from ai import AIClient, Message
from prompt import BotPromt


class WebBot:
    """
    WebBot智能体
    负责接收ShitBot的指令，执行网页自动化任务
    """
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.extractor = SmartWebExtractor(
            headless=headless,
            wait_for_network_idle=False,
            scroll_to_load=True
        )
        self.browser = BrowserTools(headless=headless)
        self.prompt = BotPromt()
        self.ai = AIClient()
        self._task_history: List[Dict] = []
    
    async def close(self):
        """关闭资源"""
        try:
            await self.browser.close()
        except Exception:
            pass
    
    async def execute_task(self, task: str, context: Optional[Dict] = None) -> str:
        """
        执行Web任务（主入口）- 支持工具调用
        Args:
            task: 任务描述
            context: 上下文信息
        Returns:
            任务执行结果
        """
        try:
            # 构建系统提示词，包含工具调用格式说明
            system_prompt = self._build_system_prompt()
            
            messages = [
                Message(role="system", content=system_prompt),
                Message(role="user", content=task)
            ]
            
            # 最多执行10轮工具调用
            max_iterations = 10
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                
                # 调用AI获取响应
                response = self.ai.chat(messages)
                
                if response is None:
                    return "抱歉，AI 生成失败，请重试。"
                
                # 检查是否需要调用工具
                tool_calls = self._parse_tool_calls(response.content)
                
                if not tool_calls:
                    # 没有工具调用，直接返回结果
                    self._task_history.append({
                        "task": task,
                        "response": response.content,
                        "iterations": iteration
                    })
                    return response.content
                
                # 执行工具调用
                tool_results = []
                for tool_call in tool_calls:
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("args", {})
                    
                    result = await self._execute_tool(tool_name, tool_args)
                    tool_results.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "result": result
                    })
                    
                    # 添加工具执行结果到消息历史
                    messages.append(Message(role="assistant", content=response.content))
                    messages.append(Message(
                        role="user", 
                        content=f"工具执行结果:\n{json.dumps(tool_results, ensure_ascii=False)}"
                    ))
            
            return f"任务执行完成，共执行 {iteration} 轮工具调用"
            
        except Exception as e:
            return f"任务执行失败: {str(e)}"
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词，包含工具调用格式说明"""
        base_prompt = self.prompt.get_prompt("WebAgent.txt")
        
        tool_instructions = """

# 工具调用格式
你可以通过以下格式调用工具来执行任务：

```tool
{
    "name": "工具名称",
    "args": {
        "参数名": "参数值"
    }
}
```

可用工具列表：
- navigate: 导航到指定URL，参数: {"url": "https://example.com"}
- click: 点击页面元素，参数: {"selector": "css选择器"}
- fill: 填写输入框，参数: {"selector": "css选择器", "value": "填写内容"}
- fill_form: 批量填写表单，参数: {"form_data": {"selector1": "value1", "selector2": "value2"}}
- submit: 提交表单，参数: {"selector": "提交按钮选择器(可选)"}
- get_content: 获取当前页面内容，参数: {}
- extract: 提取网页结构化内容，参数: {"url": "https://example.com"}
- scroll: 滚动页面，参数: {"distance": 500, "steps": 1}
- screenshot: 截图，参数: {"path": "screenshot.png", "full_page": false}

如果需要调用多个工具，请按顺序列出多个工具调用块。
当任务完成时，直接返回最终结果，不需要工具调用块。
"""
        
        return base_prompt + tool_instructions
    
    def _parse_tool_calls(self, content: str) -> List[Dict]:
        """解析AI响应中的工具调用"""
        tool_calls = []
        
        # 查找所有工具调用块
        import re
        pattern = r'```tool\s*\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            try:
                tool_data = json.loads(match.strip())
                if "name" in tool_data:
                    tool_calls.append(tool_data)
            except json.JSONDecodeError:
                continue
        
        return tool_calls
    
    async def _execute_tool(self, tool_name: str, tool_args: Dict) -> str:
        """执行指定的工具"""
        tool_map = {
            "navigate": self.navigate,
            "click": self.click,
            "fill": self.fill,
            "fill_form": self.fill_form,
            "submit": self.submit,
            "get_content": self.get_content,
            "extract": self.extract,
            "scroll": self.scroll,
            "screenshot": self.screenshot,
        }
        
        if tool_name not in tool_map:
            return f"未知工具: {tool_name}"
        
        try:
            result = await tool_map[tool_name](tool_args)
            return result
        except Exception as e:
            return f"工具执行失败: {str(e)}"
    
    async def navigate(self, args: Dict[str, Any]) -> str:
        """
        导航到指定URL
        Args:
            args: 包含url的字典
        Returns:
            导航结果
        """
        try:
            url = args.get("url", "")
            result = await self.browser.navigate(url)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"导航失败: {str(e)}"
    
    async def click(self, args: Dict[str, Any]) -> str:
        """
        点击页面元素
        Args:
            args: 包含selector的字典
        Returns:
            点击结果
        """
        try:
            selector = args.get("selector", "")
            result = await self.browser.click(selector)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"点击失败: {str(e)}"
    
    async def fill(self, args: Dict[str, Any]) -> str:
        """
        填写输入框
        Args:
            args: 包含selector和value的字典
        Returns:
            填写结果
        """
        try:
            selector = args.get("selector", "")
            value = args.get("value", "")
            result = await self.browser.fill(selector, value)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"填写失败: {str(e)}"
    
    async def fill_form(self, args: Dict[str, Any]) -> str:
        """
        批量填写表单
        Args:
            args: 包含form_data的字典
        Returns:
            填写结果
        """
        try:
            form_data = args.get("form_data", {})
            result = await self.browser.fill_form(form_data)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"表单填写失败: {str(e)}"
    
    async def submit(self, args: Dict[str, Any]) -> str:
        """
        提交表单
        Args:
            args: 包含selector的字典（可选）
        Returns:
            提交结果
        """
        try:
            selector = args.get("selector", None)
            result = await self.browser.submit(selector)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"提交失败: {str(e)}"
    
    async def get_content(self, args: Dict[str, Any]) -> str:
        """
        获取当前页面内容
        Args:
            args: 空字典
        Returns:
            页面内容
        """
        try:
            result = await self.browser.get_content()
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"获取内容失败: {str(e)}"
    
    async def extract(self, args: Dict[str, Any]) -> str:
        """
        提取网页结构化内容
        Args:
            args: 包含url的字典
        Returns:
            提取的内容
        """
        try:
            url = args.get("url", "")
            result = await self.extractor.extract(url)
            return result.to_json()
        except Exception as e:
            return f"提取失败: {str(e)}"
    
    async def extract_and_analyze(self, args: Dict[str, Any]) -> str:
        """
        提取网页内容并用AI分析
        Args:
            args: 包含url和question的字典
        Returns:
            AI分析结果
        """
        try:
            url = args.get("url", "")
            question = args.get("question", "")
            result = await self.extractor.extract(url)
            
            system_prompt = self.prompt.get_prompt("WebAgent.txt")
            messages = [
                Message(role="system", content=system_prompt),
                Message(role="user", content=question),
                Message(role="user", content=f"网页内容:\n{result.to_json()}")
            ]
            
            response = self.ai.chat(messages)
            return response.content
            
        except Exception as e:
            return f"提取分析失败: {str(e)}"
    
    async def scroll(self, args: Dict[str, Any]) -> str:
        """
        滚动页面
        Args:
            args: 包含distance和steps的字典
        Returns:
            滚动结果
        """
        try:
            distance = args.get("distance", 500)
            steps = args.get("steps", 1)
            result = await self.browser.scroll(distance, steps)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"滚动失败: {str(e)}"
    
    async def screenshot(self, args: Dict[str, Any]) -> str:
        """
        截取页面截图
        Args:
            args: 包含path和full_page的字典
        Returns:
            截图结果
        """
        try:
            path = args.get("path", "screenshot.png")
            full_page = args.get("full_page", False)
            result = await self.browser.screenshot(path, full_page)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"截图失败: {str(e)}"
    
    async def search_and_extract(self, args: Dict[str, Any]) -> str:
        """
        搜索并提取结果
        Args:
            args: 包含search_url, query, result_selector的字典
        Returns:
            搜索结果
        """
        try:
            search_url = args.get("search_url", "")
            query = args.get("query", "")
            result_selector = args.get("result_selector", "")
            
            await self.browser.navigate(search_url)
            
            search_input = "input[type='search'], input[name='q'], input[name='query'], input[placeholder*='搜索']"
            await self.browser.fill(search_input, query)
            await self.browser.submit()
            
            await asyncio.sleep(2)
            
            content = await self.browser.get_content()
            return content.get("text", "")
            
        except Exception as e:
            return f"搜索失败: {str(e)}"
    
    async def login(self, args: Dict[str, Any]) -> str:
        """
        执行登录操作
        Args:
            args: 包含login_url, username, password等的字典
        Returns:
            登录结果
        """
        try:
            login_url = args.get("login_url", "")
            username = args.get("username", "")
            password = args.get("password", "")
            username_selector = args.get("username_selector", "input[type='text'], input[name='username'], input[name='email']")
            password_selector = args.get("password_selector", "input[type='password']")
            
            await self.browser.navigate(login_url)
            await self.browser.fill(username_selector, username)
            await self.browser.fill(password_selector, password)
            
            result = await self.browser.submit()
            
            return json.dumps({
                "success": True,
                "current_url": result.get("current_url", ""),
                "message": "登录操作已执行"
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": str(e),
                "message": f"登录失败: {str(e)}"
            }, ensure_ascii=False)
    
    async def get_links(self, args: Dict[str, Any]) -> str:
        """
        获取页面所有链接
        Args:
            args: 包含url的字典
        Returns:
            链接列表
        """
        try:
            url = args.get("url", "")
            result = await self.extractor.extract(url)
            return json.dumps(result.links, ensure_ascii=False)
        except Exception as e:
            return f"获取链接失败: {str(e)}"
    
    async def get_images(self, args: Dict[str, Any]) -> str:
        """
        获取页面所有图片
        Args:
            args: 包含url的字典
        Returns:
            图片列表
        """
        try:
            url = args.get("url", "")
            result = await self.extractor.extract(url)
            return json.dumps(result.images, ensure_ascii=False)
        except Exception as e:
            return f"获取图片失败: {str(e)}"
    
    async def get_forms(self, args: Dict[str, Any]) -> str:
        """
        获取页面所有表单
        Args:
            args: 包含url的字典
        Returns:
            表单列表
        """
        try:
            url = args.get("url", "")
            result = await self.extractor.extract(url)
            return json.dumps(result.interactive_elements, ensure_ascii=False)
        except Exception as e:
            return f"获取表单失败: {str(e)}"
    
    def get_task_history(self) -> List[Dict]:
        """获取任务历史"""
        return self._task_history


async def demo():
    """使用示例"""
    bot = WebBot(headless=True)
    
    try:
        result = await bot.execute_task("打开哔哩哔哩搜索影视飓风，并且把UP页面的页面截图")
        print(result)
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(demo())
