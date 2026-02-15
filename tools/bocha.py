#!/usr/bin/env python3
"""
博查搜索 API
提供网络搜索功能
文档: https://bocha.ai/
"""

import os
import json
import httpx
from typing import Optional, Dict, Any
from dataclasses import dataclass
from config import load_config 

@dataclass
class SearchResult:
    """搜索结果"""
    title: str
    url: str
    content: str
    source: Optional[str] = None
    publish_time: Optional[str] = None


@dataclass
class SearchResponse:
    """搜索响应"""
    success: bool
    query: str
    total_results: int
    results: list
    response_time: float
    error: Optional[str] = None

class BochaSearch:
    """
    博查搜索客户端
    提供网络搜索功能
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化博查搜索客户端
        
        Args:
            api_key: API 密钥，默认从环境变量读取 BOCHA_API_KEY
        """
        self.api_key = api_key or os.environ.get("BOCHA_API_KEY", "")
        self.base_url = "https://api.bocha.cn"
        self.timeout = 30.0
    
    def set_api_key(self, api_key: str) -> None:
        """设置 API 密钥"""
        self.api_key = api_key
    
    async def search(
        self,
        query: str,
        count: int = 10,
        summary: bool = True
    ) -> SearchResponse:
        """
        执行网络搜索
        
        Args:
            query: 搜索关键词
            count: 返回结果数量 (1-20)
            summary: 是否返回摘要
            
        Returns:
            SearchResponse: 搜索结果
        """
        import time
        start_time = time.time()
        
        try:
            if not self.api_key:
                return SearchResponse(
                    success=False,
                    query=query,
                    total_results=0,
                    results=[],
                    response_time=time.time() - start_time,
                    error="请设置博查 API 密钥"
                )
            
            # 构建请求体
            payload = {
                "query": query,
                "count": min(max(count, 1), 20),
                "summary": summary
            }
            
            # 构建请求头
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 发送 POST 请求
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/web-search",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
            
            # 解析结果
            results = []
            if "data" in data and "webPages" in data["data"]:
                for item in data["data"]["webPages"]["value"][:count]:
                    result = SearchResult(
                        title=item.get("name", ""),
                        url=item.get("url", ""),
                        content=item.get("snippet", ""),
                        source=item.get("displayUrl"),
                        publish_time=item.get("dateLastCrawled")
                    )
                    results.append({
                        "title": result.title,
                        "url": result.url,
                        "content": result.content[:200] if result.content else "",
                        "source": result.source,
                        "publish_time": result.publish_time
                    })
            
            response_time = time.time() - start_time
            
            return SearchResponse(
                success=True,
                query=query,
                total_results=len(results),
                results=results,
                response_time=response_time
            )
            
        except httpx.HTTPStatusError as e:
            return SearchResponse(
                success=False,
                query=query,
                total_results=0,
                results=[],
                response_time=time.time() - start_time,
                error=f"API 请求失败: {str(e)}"
            )
        except Exception as e:
            return SearchResponse(
                success=False,
                query=query,
                total_results=0,
                results=[],
                response_time=time.time() - start_time,
                error=f"搜索失败: {str(e)}"
            )
    
    async def search_news(
        self,
        query: str,
        count: int = 10
    ) -> SearchResponse:
        """
        搜索新闻
        
        Args:
            query: 搜索关键词
            count: 返回结果数量
            
        Returns:
            SearchResponse: 搜索结果
        """
        return await self.search(query, count, summary=True)
    
    async def search_tech(
        self,
        query: str,
        count: int = 10
    ) -> SearchResponse:
        """
        搜索技术相关内容
        
        Args:
            query: 搜索关键词
            count: 返回结果数量
            
        Returns:
            SearchResponse: 搜索结果
        """
        return await self.search(query, count, summary=True)
    
    async def search_ai(
        self,
        query: str,
        count: int = 10
    ) -> SearchResponse:
        """
        搜索 AI 相关内容
        
        Args:
            query: 搜索关键词
            count: 返回结果数量
            
        Returns:
            SearchResponse: 搜索结果
        """
        return await self.search(query, count, summary=True)
    
    def format_results(
        self,
        response: SearchResponse,
        max_content_length: int = 150
    ) -> str:
        """
        格式化搜索结果为字符串
        
        Args:
            response: 搜索响应
            max_content_length: 最大内容长度
            
        Returns:
            str: 格式化后的字符串
        """
        if not response.success:
            return f"搜索失败: {response.get('error', '未知错误')}"
        
        lines = [f"搜索关键词: {response.query}"]
        lines.append(f"找到 {response.total_results} 条结果 (耗时 {response.response_time:.2f}秒)")
        lines.append("-" * 60)
        
        for i, result in enumerate(response.results, 1):
            lines.append(f"\n[{i}] {result['title']}")
            lines.append(f"    URL: {result['url']}")
            if result['content']:
                content = result['content'][:max_content_length]
                lines.append(f"    摘要: {content}...")
        
        return "\n".join(lines)
    
    def get_answer_prompt(self, query: str, results: list) -> str:
        """
        生成 AI 回答的提示词
        
        Args:
            query: 用户问题
            results: 搜索结果列表
            
        Returns:
            str: 提示词
        """
        context = "\n\n".join([
            f"来源 {i+1}: {r['title']}\n{r['content']}"
            for i, r in enumerate(results[:5])
        ])
        
        return f"""请根据以下搜索结果回答用户的问题。

用户问题: {query}

搜索结果:
{context}

请用中文回答，引用搜索结果中的信息，确保回答准确可靠。
"""
    
    async def close(self) -> None:
        """
        关闭客户端
        由于使用异步上下文管理，此方法为空实现
        """
        pass


async def create_bocha_search_client() -> BochaSearch:
    """创建博查搜索客户端"""
    return BochaSearch()


if __name__ == "__main__":
    import asyncio
    
    async def test():
        print("=" * 60)
        print("博查搜索 API 测试")
        print("=" * 60)
        print()
        config = load_config()
        bocha_config = config.bocha
        client = BochaSearch(
            api_key=bocha_config.api_key
                    )
        
        # 测试搜索
        print("测试搜索: Python 教程")
        print("-" * 60)
        
        response = await client.search("Python 教程", count=5)
        
        if response.success:
            print(f"✓ 搜索成功，找到 {response.total_results} 条结果")
            print(f"  耗时: {response.response_time:.2f}秒")
            print()
            print(client.format_results(response))
        else:
            print(f"✗ 搜索失败: {response.error}")
        
        print()
        print("=" * 60)
        print("测试完成")
        print("=" * 60)
    
    asyncio.run(test())
