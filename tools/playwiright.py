"""
智能网页内容提取器
功能：爬取网页并提取对AI/LLM分析有价值的结构化内容
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

from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup, Comment
from ai import AIClient,Message
from prompt import BotPromt  
from config import load_config
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
            
            # 拦截静态资源以加速
            await context.route("**/*.{png,jpg,jpeg,gif,svg,css,woff,woff2}", 
                              lambda route: route.abort())
            
            page = await context.new_page()
            
            try:
                # 访问页面
                await self._goto_page(page, url)
                
                # 滚动加载懒加载内容
                if self.scroll_to_load:
                    await self._scroll_page(page)
                
                # 获取完整 HTML
                html_content = await page.content()
                page_title = await page.title()
                
                # 解析内容
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
            
            # 等待关键元素
            await page.wait_for_load_state("load")
            await asyncio.sleep(1)  # 额外等待动态内容
            
        except Exception as e:
            print(f"页面加载警告: {e}")
    
    async def _scroll_page(self, page: Page):
        """滚动页面加载懒加载内容"""
        try:
            # 获取页面高度
            height = await page.evaluate("document.body.scrollHeight")
            
            # 分步滚动
            steps = min(height // 1000, 10)  # 最多10步
            for i in range(steps):
                await page.evaluate(f"window.scrollTo(0, {(i + 1) * 1000})")
                await asyncio.sleep(0.3)
            
            # 回滚到顶部
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"滚动警告: {e}")
    
    def _parse_html(self, html: str, url: str, title: str) -> ExtractedContent:
        """解析HTML内容"""
        soup = BeautifulSoup(html, 'lxml')
        
        # 清理脚本和样式
        self._clean_soup(soup)
        
        # 计算哈希
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
        # 移除脚本、样式、注释
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
        """
        智能提取正文内容
        优先查找 article/main 标签，否则基于文本密度算法
        """
        # 尝试语义化标签
        for selector in ["article", "main", '[role="main"]', ".content", "#content"]:
            element = soup.select_one(selector)
            if element:
                return self._clean_text(element.get_text())
        
        # 文本密度算法找正文
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
        
        # JSON-LD
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                structured.append({
                    "type": "json-ld",
                    "data": data
                })
            except:
                pass
        
        # Microdata
        microdata_items = soup.find_all(attrs={"itemscope": True})
        for item in microdata_items[:5]:  # 限制数量
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
            
            # 去重
            if full_url in seen:
                continue
            seen.add(full_url)
            
            # 分类链接
            link_type = self._classify_link(href)
            
            links.append({
                "url": full_url,
                "text": self._clean_text(a.get_text()),
                "title": a.get("title", ""),
                "is_external": not full_url.startswith(base_url.split("/")[2]),
                "type": link_type
            })
        
        return links[:50]  # 限制数量
    
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
            
            # 提取表头
            thead = table.find("thead")
            if thead:
                headers = [th.get_text(strip=True) for th in thead.find_all(["th", "td"])]
            
            # 提取行数据
            for tr in table.find_all("tr"):
                row_data = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if row_data:
                    rows.append(row_data)
            
            tables.append({
                "index": i,
                "headers": headers,
                "rows": rows[:20],  # 限制行数
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
            
            if items and len(items) > 1:  # 过滤空列表
                lists.append({
                    "type": lst.name,  # ul 或 ol
                    "items": items[:15],  # 限制数量
                    "item_count": len(items)
                })
        
        return lists[:10]
    
    def _extract_interactive(self, soup: BeautifulSoup) -> List[Dict]:
        """提取交互元素（表单、按钮等）"""
        elements = []
        
        # 表单
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
        
        # 按钮
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
                # 合并同类型标签的文本
                combined_text = " ".join([
                    self._clean_text(el.get_text())[:500] 
                    for el in elements
                ])
                semantic_tags[tag] = combined_text[:1000]  # 限制长度
        
        return semantic_tags
    
    def _extract_code_blocks(self, soup: BeautifulSoup) -> List[str]:
        """提取代码块"""
        code_blocks = []
        
        # pre > code 结构
        for pre in soup.find_all("pre"):
            code = pre.find("code")
            text = code.get_text() if code else pre.get_text()
            if len(text.strip()) > 20:
                code_blocks.append(text[:2000])  # 限制长度
        
        # 单独 code 标签
        for code in soup.find_all("code"):
            text = code.get_text()
            if len(text.strip()) > 30 and text not in code_blocks:
                code_blocks.append(text[:1000])
        
        return code_blocks[:10]
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符
        text = text.replace('\n', ' ').replace('\t', ' ')
        return text.strip()

class WebBot:
    def __init__(self):
        self.extractor = SmartWebExtractor(
            headless=True,
            wait_for_network_idle=False,
            scroll_to_load=True
        )
        self.prompt = BotPromt()
        self.ai = AIClient()
    async def extract(self, url: str, question: str):
        """提取网页内容"""
        try:
            result =  await self.extractor.extract(url)
            prompt=self.prompt.get_prompt("WebAgent.txt")
            # 调用MiniMax模型
            messages = [
                Message(role="system", content=prompt), 
                Message(role="user", content=question),
                Message(role="user", content=result.to_json())
            ]
            response = self.ai.chat(messages)  
            return response.content
        except Exception as e:
            return f"提取网页内容时出错: {str(e)}"
# ==================== 使用示例 ====================

async def get_web_data(url: str):
    """使用示例"""
    bot = WebBot()
    question = "这个视频的内容大概是什么"
    response = await bot.extract(url, question)
    print(response)
    response = await bot.extract(url, question)
    print(response)


if __name__ == "__main__":
    # 运行示例
    asyncio.run(get_web_data("https://bigmodel.cn/pricing"))
    
    # 或者单URL提取
    # async def single_extract():
    #     extractor = SmartWebExtractor()
    #     result = await extractor.extract("https://example.com")
    #     print(result.to_json())
    # asyncio.run(single_extract())