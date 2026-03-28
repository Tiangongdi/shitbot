"""
浏览器操作工具
功能：
1. SmartWebExtractor - 智能网页内容提取器
2. BrowserTools - 底层浏览器操作工具（导航、点击、表单）
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import json
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from urllib.parse import urljoin, urlparse
import hashlib

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from bs4 import BeautifulSoup, Comment
from config.config import load_config

config = load_config()
if config.browser.playwright_browsers_path:
    os.environ['PLAYWRIGHT_BROWSERS_PATH'] = config.browser.playwright_browsers_path


@dataclass
class ExtractedContent:
    url: str
    title: str
    meta_description: str
    main_text: str
    structured_data: List[Dict]
    headings_outline: List[Dict]
    links: List[Dict]
    images: List[Dict]
    tables: List[Dict]
    lists: List[Dict]
    interactive_elements: List[Dict]
    semantic_html5_tags: Dict[str, str]
    code_blocks: List[str]
    raw_html_hash: str
    raw_html: str = ""
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


class SmartWebExtractor:
    """
    智能网页提取器
    使用 Playwright 获取渲染后的内容，并提取语义化结构
    """
    
    def __init__(self, 
                 headless: bool = True,
                 wait_for_network_idle: bool = True,
                 scroll_to_load: bool = True,
                 timeout: int = 30000):
        self.headless = headless
        self.wait_for_network_idle = wait_for_network_idle
        self.scroll_to_load = scroll_to_load
        self.timeout = timeout
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    async def extract(self, url: str) -> ExtractedContent:
        """主提取方法"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                user_agent=self.user_agent,
                viewport={"width": 1920, "height": 1080}
            )
            
            await context.route("**/*.{png,jpg,jpeg,gif,svg,css,woff,woff2}", 
                              lambda route: route.abort())
            
            page = await context.new_page()
            
            try:
                await self._goto_page(page, url)
                
                if self.scroll_to_load:
                    await self._scroll_page(page)
                
                html_content = await page.content()
                page_title = await page.title()
                
                extracted = self._parse_html(
                    html=html_content,
                    url=url,
                    title=page_title
                )
                
                return extracted
                
            finally:
                await browser.close()
    
    async def _goto_page(self, page: Page, url: str):
        """安全访问页面"""
        try:
            if self.wait_for_network_idle:
                await page.goto(url, wait_until="networkidle", timeout=self.timeout)
            else:
                await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
            
            await page.wait_for_load_state("load")
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"页面加载警告: {e}")
    
    async def _scroll_page(self, page: Page):
        """滚动页面加载懒加载内容"""
        try:
            height = await page.evaluate("document.body.scrollHeight")
            steps = min(height // 1000, 10)
            for i in range(steps):
                await page.evaluate(f"window.scrollTo(0, {(i + 1) * 1000})")
                await asyncio.sleep(0.3)
            
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"滚动警告: {e}")
    
    def _parse_html(self, html: str, url: str, title: str) -> ExtractedContent:
        """解析HTML内容"""
        soup = BeautifulSoup(html, 'lxml')
        self._clean_soup(soup)
        raw_hash = hashlib.md5(html.encode()).hexdigest()
        
        return ExtractedContent(
            url=url,
            title=title,
            meta_description=self._extract_meta(soup),
            main_text=self._extract_main_text(soup),
            structured_data=self._extract_structured_data(soup),
            headings_outline=self._extract_headings(soup),
            links=self._extract_links(soup, url),
            images=self._extract_images(soup, url),
            tables=self._extract_tables(soup),
            lists=self._extract_lists(soup),
            interactive_elements=self._extract_interactive(soup),
            semantic_html5_tags=self._extract_semantic_tags(soup),
            code_blocks=self._extract_code_blocks(soup),
            raw_html_hash=raw_hash,
            raw_html=html
        )
    
    def _clean_soup(self, soup: BeautifulSoup):
        """清理无关标签"""
        for element in soup(["script", "style", "noscript", "iframe", "canvas", "svg"]):
            element.decompose()
        
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
    
    def _extract_meta(self, soup: BeautifulSoup) -> str:
        """提取元描述"""
        meta = soup.find("meta", attrs={"name": "description"}) or \
               soup.find("meta", attrs={"property": "og:description"})
        return meta.get("content", "") if meta else ""
    
    def _extract_main_text(self, soup: BeautifulSoup) -> str:
        """智能提取正文内容"""
        for selector in ["article", "main", '[role="main"]', ".content", "#content"]:
            element = soup.select_one(selector)
            if element:
                return self._clean_text(element.get_text())
        
        paragraphs = soup.find_all("p")
        best_text = ""
        max_density = 0
        
        for p in paragraphs:
            parent = p.parent
            text = parent.get_text()
            text_len = len(text.strip())
            link_len = sum(len(a.get_text()) for a in parent.find_all("a"))
            
            if text_len > 0:
                density = (text_len - link_len) / text_len
                if text_len > 200 and density > max_density:
                    max_density = density
                    best_text = text
        
        return self._clean_text(best_text) if best_text else self._clean_text(soup.get_text())
    
    def _extract_structured_data(self, soup: BeautifulSoup) -> List[Dict]:
        """提取 JSON-LD 等结构化数据"""
        structured = []
        
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                structured.append({"type": "json-ld", "data": data})
            except:
                pass
        
        microdata_items = soup.find_all(attrs={"itemscope": True})
        for item in microdata_items[:5]:
            item_data = {"type": "microdata", "properties": {}}
            for prop in item.find_all(attrs={"itemprop": True}):
                item_data["properties"][prop["itemprop"]] = prop.get_text(strip=True)
            structured.append(item_data)
        
        return structured
    
    def _extract_headings(self, soup: BeautifulSoup) -> List[Dict]:
        """提取标题层级结构"""
        headings = []
        for i in range(1, 7):
            for h in soup.find_all(f"h{i}"):
                headings.append({
                    "level": i,
                    "text": self._clean_text(h.get_text()),
                    "id": h.get("id", "")
                })
        return headings
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """提取链接信息"""
        links = []
        seen = set()
        
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full_url = urljoin(base_url, href)
            
            if full_url in seen:
                continue
            seen.add(full_url)
            
            link_type = self._classify_link(href)
            
            links.append({
                "url": full_url,
                "text": self._clean_text(a.get_text()),
                "title": a.get("title", ""),
                "is_external": not full_url.startswith(base_url.split("/")[2]),
                "type": link_type
            })
        
        return links[:50]
    
    def _classify_link(self, href: str) -> str:
        """分类链接类型"""
        if href.startswith("#"):
            return "anchor"
        elif any(x in href.lower() for x in [".pdf", ".doc", ".zip"]):
            return "document"
        elif "mailto:" in href:
            return "email"
        elif re.search(r"/(tag|category|topic)/", href):
            return "taxonomy"
        else:
            return "page"
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """提取图片信息"""
        images = []
        
        for img in soup.find_all("img"):
            src = img.get("src", img.get("data-src", ""))
            if not src:
                continue
            
            images.append({
                "url": urljoin(base_url, src),
                "alt": img.get("alt", ""),
                "title": img.get("title", ""),
                "width": img.get("width", ""),
                "height": img.get("height", ""),
                "is_lazy": "lazy" in str(img.get("loading", ""))
            })
        
        return images[:30]
    
    def _extract_tables(self, soup: BeautifulSoup) -> List[Dict]:
        """提取表格数据"""
        tables = []
        
        for i, table in enumerate(soup.find_all("table")):
            rows = []
            headers = []
            
            thead = table.find("thead")
            if thead:
                headers = [th.get_text(strip=True) for th in thead.find_all(["th", "td"])]
            
            for tr in table.find_all("tr"):
                row_data = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if row_data:
                    rows.append(row_data)
            
            tables.append({
                "index": i,
                "headers": headers,
                "rows": rows[:20],
                "row_count": len(rows)
            })
        
        return tables[:5]
    
    def _extract_lists(self, soup: BeautifulSoup) -> List[Dict]:
        """提取列表结构（ul/ol）"""
        lists = []
        
        for i, lst in enumerate(soup.find_all(["ul", "ol"])):
            items = [
                self._clean_text(li.get_text()) 
                for li in lst.find_all("li", recursive=False)
            ]
            
            if items and len(items) > 1:
                lists.append({
                    "type": lst.name,
                    "items": items[:15],
                    "item_count": len(items)
                })
        
        return lists[:10]
    
    def _extract_interactive(self, soup: BeautifulSoup) -> List[Dict]:
        """提取交互元素（表单、按钮等）"""
        elements = []
        
        for form in soup.find_all("form"):
            inputs = []
            for inp in form.find_all(["input", "textarea", "select"]):
                inputs.append({
                    "type": inp.get("type", inp.name),
                    "name": inp.get("name", ""),
                    "placeholder": inp.get("placeholder", ""),
                    "required": bool(inp.get("required"))
                })
            
            elements.append({
                "tag": "form",
                "action": form.get("action", ""),
                "method": form.get("method", "get"),
                "inputs": inputs
            })
        
        for btn in soup.find_all(["button", "a"], class_=re.compile(r"btn|button", re.I)):
            elements.append({
                "tag": btn.name,
                "text": self._clean_text(btn.get_text()),
                "classes": btn.get("class", [])
            })
        
        return elements[:20]
    
    def _extract_semantic_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """提取 HTML5 语义化标签内容"""
        semantic_tags = {}
        
        for tag in ["article", "section", "aside", "nav", "header", "footer"]:
            elements = soup.find_all(tag)
            if elements:
                combined_text = " ".join([
                    self._clean_text(el.get_text())[:500] 
                    for el in elements
                ])
                semantic_tags[tag] = combined_text[:1000]
        
        return semantic_tags
    
    def _extract_code_blocks(self, soup: BeautifulSoup) -> List[str]:
        """提取代码块"""
        code_blocks = []
        
        for pre in soup.find_all("pre"):
            code = pre.find("code")
            text = code.get_text() if code else pre.get_text()
            if len(text.strip()) > 20:
                code_blocks.append(text[:2000])
        
        for code in soup.find_all("code"):
            text = code.get_text()
            if len(text.strip()) > 30 and text not in code_blocks:
                code_blocks.append(text[:1000])
        
        return code_blocks[:10]
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('\n', ' ').replace('\t', ' ')
        return text.strip()


class BrowserTools:
    """
    底层浏览器操作工具
    提供导航、点击、表单填写等基础操作
    """
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
    
    async def _ensure_browser(self) -> Page:
        """确保浏览器已启动"""
        if self._page is None:
            p = await async_playwright().start()
            self._browser = await p.chromium.launch(headless=self.headless)
            self._context = await self._browser.new_context(
                user_agent=self.user_agent,
                viewport={"width": 1920, "height": 1080}
            )
            self._page = await self._context.new_page()
        return self._page
    
    async def close(self):
        """关闭浏览器"""
        if self._browser:
            await self._browser.close()
            self._browser = None
            self._context = None
            self._page = None
    
    async def navigate(self, url: str, wait_until: str = "networkidle") -> Dict[str, Any]:
        """
        导航到指定URL
        Args:
            url: 目标URL
            wait_until: 等待状态 (networkidle, domcontentloaded, load)
        Returns:
            操作结果
        """
        try:
            page = await self._ensure_browser()
            await page.goto(url, wait_until=wait_until, timeout=self.timeout)
            await page.wait_for_load_state("load")
            
            title = await page.title()
            current_url = page.url
            
            return {
                "success": True,
                "url": current_url,
                "title": title,
                "message": f"成功导航到: {current_url}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"导航失败: {str(e)}"
            }
    
    async def click(self, selector: str, wait_after: float = 1.0) -> Dict[str, Any]:
        """
        点击页面元素
        Args:
            selector: CSS选择器
            wait_after: 点击后等待时间（秒）
        Returns:
            操作结果
        """
        try:
            page = await self._ensure_browser()
            await page.wait_for_selector(selector, timeout=self.timeout)
            await page.click(selector)
            await asyncio.sleep(wait_after)
            
            return {
                "success": True,
                "selector": selector,
                "current_url": page.url,
                "message": f"成功点击元素: {selector}"
            }
        except Exception as e:
            return {
                "success": False,
                "selector": selector,
                "error": str(e),
                "message": f"点击失败: {str(e)}"
            }
    
    async def fill(self, selector: str, value: str, clear_first: bool = True) -> Dict[str, Any]:
        """
        填写输入框
        Args:
            selector: CSS选择器
            value: 要填写的值
            clear_first: 是否先清空
        Returns:
            操作结果
        """
        try:
            page = await self._ensure_browser()
            await page.wait_for_selector(selector, timeout=self.timeout)
            
            if clear_first:
                await page.fill(selector, value)
            else:
                await page.type(selector, value)
            
            return {
                "success": True,
                "selector": selector,
                "value": value,
                "message": f"成功填写: {selector}"
            }
        except Exception as e:
            return {
                "success": False,
                "selector": selector,
                "error": str(e),
                "message": f"填写失败: {str(e)}"
            }
    
    async def fill_form(self, form_data: Dict[str, str]) -> Dict[str, Any]:
        """
        批量填写表单
        Args:
            form_data: 表单数据 {"selector": "value"}
        Returns:
            操作结果
        """
        try:
            page = await self._ensure_browser()
            filled_fields = []
            errors = []
            
            for selector, value in form_data.items():
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    await page.fill(selector, value)
                    filled_fields.append(selector)
                except Exception as e:
                    errors.append({"selector": selector, "error": str(e)})
            
            return {
                "success": len(errors) == 0,
                "filled_fields": filled_fields,
                "errors": errors,
                "message": f"成功填写 {len(filled_fields)}/{len(form_data)} 个字段"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"表单填写失败: {str(e)}"
            }
    
    async def submit(self, selector: Optional[str] = None) -> Dict[str, Any]:
        """
        提交表单
        Args:
            selector: 提交按钮选择器（可选，默认按Enter）
        Returns:
            操作结果
        """
        try:
            page = await self._ensure_browser()
            
            if selector:
                await page.click(selector)
            else:
                await page.keyboard.press("Enter")
            
            await asyncio.sleep(2)
            
            return {
                "success": True,
                "current_url": page.url,
                "message": "表单已提交"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"提交失败: {str(e)}"
            }
    
    async def get_content(self) -> Dict[str, Any]:
        """
        获取当前页面内容
        Returns:
            页面内容信息
        """
        try:
            page = await self._ensure_browser()
            
            html = await page.content()
            title = await page.title()
            url = page.url
            text = await page.evaluate("() => document.body.innerText")
            
            return {
                "success": True,
                "url": url,
                "title": title,
                "html_length": len(html),
                "text": text[:5000],
                "message": "成功获取页面内容"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"获取内容失败: {str(e)}"
            }
    
    async def get_text(self) -> str:
        """
        获取当前页面纯文本
        Returns:
            页面文本内容
        """
        try:
            page = await self._ensure_browser()
            text = await page.evaluate("() => document.body.innerText")
            return text
        except Exception as e:
            return f"获取文本失败: {str(e)}"
    
    async def screenshot(self, path: str = "screenshot.png", full_page: bool = False) -> Dict[str, Any]:
        """
        截取页面截图
        Args:
            path: 保存路径
            full_page: 是否全页面截图
        Returns:
            操作结果
        """
        try:
            page = await self._ensure_browser()
            await page.screenshot(path=path, full_page=full_page)
            
            return {
                "success": True,
                "path": path,
                "message": f"截图已保存: {path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"截图失败: {str(e)}"
            }
    
    async def wait_for_selector(self, selector: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        等待元素出现
        Args:
            selector: CSS选择器
            timeout: 超时时间
        Returns:
            操作结果
        """
        try:
            page = await self._ensure_browser()
            await page.wait_for_selector(selector, timeout=timeout or self.timeout)
            
            return {
                "success": True,
                "selector": selector,
                "message": f"元素已出现: {selector}"
            }
        except Exception as e:
            return {
                "success": False,
                "selector": selector,
                "error": str(e),
                "message": f"等待超时: {str(e)}"
            }
    
    async def evaluate(self, script: str) -> Any:
        """
        执行JavaScript脚本
        Args:
            script: JavaScript代码
        Returns:
            执行结果
        """
        try:
            page = await self._ensure_browser()
            result = await page.evaluate(script)
            return result
        except Exception as e:
            return f"脚本执行失败: {str(e)}"
    
    async def scroll(self, distance: int = 500, steps: int = 1) -> Dict[str, Any]:
        """
        滚动页面
        Args:
            distance: 每步滚动距离
            steps: 滚动步数
        Returns:
            操作结果
        """
        try:
            page = await self._ensure_browser()
            
            for i in range(steps):
                await page.evaluate(f"window.scrollBy(0, {distance})")
                await asyncio.sleep(0.3)
            
            return {
                "success": True,
                "message": f"已滚动 {distance * steps} 像素"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"滚动失败: {str(e)}"
            }
    
    async def get_current_url(self) -> str:
        """获取当前URL"""
        try:
            page = await self._ensure_browser()
            return page.url
        except:
            return ""


async def get_web_data(url: str):
    """使用示例"""
    extractor = SmartWebExtractor()
    result = await extractor.extract(url)
    print("提取的网页内容:")
    print(f"标题: {result.title}")
    print(f"元描述: {result.meta_description}")
    print(f"正文长度: {len(result.main_text)} 字符")
    print(f"链接数量: {len(result.links)}")
    print(f"图片数量: {len(result.images)}")


if __name__ == "__main__":
    asyncio.run(get_web_data("https://bigmodel.cn/pricing"))
