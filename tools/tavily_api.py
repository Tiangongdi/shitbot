from tavily import TavilyClient 
from config import load_config




class TavilySearch:
    def __init__(self):
        self.config = load_config()
        self.tavily_client = TavilyClient(api_key=self.config.tavily.key)   
        
    def search(self, query: str,max_results: int = 3):
        results = self.tavily_client.search(query=query,max_results=max_results)['results']   
        # 返回字符串
        results_str = ""
        for result in results:
            results_str += f"标题: {result['title']}\n"
            results_str += f"内容: {result['content']}\n"
            results_str += f"来源: {result['url']}\n\n"
        return results_str
if __name__ == "__main__":
    tavily_search = TavilySearch()
    print(tavily_search.search("tavily是什么"))