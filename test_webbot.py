"""
WebBot 测试文件
测试 WebBot 智能体的基本功能
"""

import asyncio
import json
from tools.webbot import WebBot

async def test_basic_functionality():
    """测试 WebBot 的基本功能"""
    print("=" * 60)
    print("WebBot 基本功能测试")
    print("=" * 60)
    
    bot = WebBot(headless=True)
    
    try:
        # 测试导航功能
        print("\n1. 测试导航功能")
        navigate_result = await bot.navigate({"url": "https://www.baidu.com"})
        print(f"   导航结果: {json.loads(navigate_result)['success']}")
        
        # 测试获取内容
        print("\n2. 测试获取页面内容")
        content_result = await bot.get_content({})
        content_data = json.loads(content_result)
        print(f"   页面标题: {content_data.get('title', 'N/A')}")
        print(f"   内容长度: {len(content_data.get('text', ''))} 字符")
        
        # 测试滚动功能
        print("\n3. 测试滚动功能")
        scroll_result = await bot.scroll({"distance": 500, "steps": 2})
        print(f"   滚动结果: {json.loads(scroll_result)['success']}")
        
        # 测试截图功能
        print("\n4. 测试截图功能")
        screenshot_result = await bot.screenshot({"path": "test_screenshot.png", "full_page": False})
        print(f"   截图结果: {json.loads(screenshot_result)['success']}")
        print(f"   截图路径: {json.loads(screenshot_result)['path']}")
        
        # 测试提取功能
        print("\n5. 测试提取功能")
        extract_result = await bot.extract({"url": "https://www.baidu.com"})
        extract_data = json.loads(extract_result)
        print(f"   提取结果类型: {type(extract_data).__name__}")
        print(f"   页面标题: {extract_data.get('title', 'N/A')}")
        
        # 测试获取链接
        print("\n6. 测试获取链接")
        links_result = await bot.get_links({"url": "https://www.baidu.com"})
        links_data = json.loads(links_result)
        print(f"   链接数量: {len(links_data)}")
        if links_data:
            print(f"   第一个链接: {links_data[0].get('text', 'N/A')} -> {links_data[0].get('href', 'N/A')}")
        
        # 测试获取图片
        print("\n7. 测试获取图片")
        images_result = await bot.get_images({"url": "https://www.baidu.com"})
        images_data = json.loads(images_result)
        print(f"   图片数量: {len(images_data)}")
        if images_data:
            print(f"   第一个图片: {images_data[0].get('alt', 'N/A')} -> {images_data[0].get('src', 'N/A')}")
        
        # 测试获取表单
        print("\n8. 测试获取表单")
        forms_result = await bot.get_forms({"url": "https://www.baidu.com"})
        forms_data = json.loads(forms_result)
        print(f"   表单元素数量: {len(forms_data)}")
        
        print("\n" + "=" * 60)
        print("测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
    finally:
        await bot.close()

async def test_search_functionality():
    """测试搜索功能"""
    print("\n" + "=" * 60)
    print("WebBot 搜索功能测试")
    print("=" * 60)
    
    bot = WebBot(headless=True)
    
    try:
        # 测试搜索功能
        print("\n1. 测试搜索功能")
        search_result = await bot.search_and_extract({
            "search_url": "https://www.baidu.com",
            "query": "Python",
            "result_selector": "#content_left"
        })
        print(f"   搜索结果长度: {len(search_result)} 字符")
        print(f"   搜索结果前100字符: {search_result[:100]}...")
        
        print("\n" + "=" * 60)
        print("搜索测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"搜索测试失败: {str(e)}")
    finally:
        await bot.close()

async def test_bilibili_search():
    """测试哔哩哔哩搜索功能"""
    print("\n" + "=" * 60)
    print("WebBot 哔哩哔哩搜索测试")
    print("=" * 60)
    
    bot = WebBot(headless=True)
    
    try:
        # 导航到哔哩哔哩
        print("\n1. 导航到哔哩哔哩")
        navigate_result = await bot.navigate({"url": "https://www.bilibili.com"})
        print(f"   导航结果: {json.loads(navigate_result)['success']}")
        
        # 等待页面加载
        await asyncio.sleep(2)
        
        # 点击搜索框
        print("\n2. 点击搜索框")
        click_result = await bot.click({"selector": "#nav-searchform > div > input"})
        print(f"   点击结果: {json.loads(click_result)['success']}")
        
        # 输入搜索关键词
        print("\n3. 输入搜索关键词")
        fill_result = await bot.fill({"selector": "#nav-searchform > div > input", "value": "火影忍者"})
        print(f"   填写结果: {json.loads(fill_result)['success']}")
        
        # 点击搜索按钮
        print("\n4. 点击搜索按钮")
        # 尝试不同的选择器
        selectors = [
            "#nav-searchform > div > button",
            ".nav-search-btn",
            "button[type='submit']",
            "#nav-searchform button"
        ]
        
        click_success = False
        for selector in selectors:
            try:
                click_result = await bot.click({"selector": selector})
                if json.loads(click_result)['success']:
                    click_success = True
                    print(f"   点击结果: True (使用选择器: {selector})")
                    break
            except Exception:
                continue
        
        if not click_success:
            print("   点击结果: False (所有选择器都失败)")
        
        # 等待搜索结果加载
        await asyncio.sleep(3)
        
        # 获取搜索结果页面内容
        print("\n5. 获取搜索结果")
        content_result = await bot.get_content({})
        content_data = json.loads(content_result)
        print(f"   页面标题: {content_data.get('title', 'N/A')}")
        print(f"   内容长度: {len(content_data.get('text', ''))} 字符")
        
        # 截图保存
        print("\n6. 截图保存")
        screenshot_result = await bot.screenshot({"path": "bilibili_search.png", "full_page": True})
        print(f"   截图结果: {json.loads(screenshot_result)['success']}")
        print(f"   截图路径: {json.loads(screenshot_result)['path']}")
        
        print("\n" + "=" * 60)
        print("哔哩哔哩搜索测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"哔哩哔哩搜索测试失败: {str(e)}")
    finally:
        await bot.close()

async def main():
    """运行 WebBot 能力测试"""
    # 只运行哔哩哔哩搜索测试，验证 WebBot 的核心能力
    await test_bilibili_search()

if __name__ == "__main__":
    asyncio.run(main())
