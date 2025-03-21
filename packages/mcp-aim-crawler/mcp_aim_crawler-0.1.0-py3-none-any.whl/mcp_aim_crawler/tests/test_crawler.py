import asyncio
from mcp_aim_crawler.crawler import WebCrawler

async def main():
    """测试爬虫功能"""
    crawler = WebCrawler()
    try:
        print("正在登录...")
        if await crawler.login():
            print("登录成功，开始爬取内容...")
            content = await crawler.crawl()
            print(f"爬取成功，内容长度: {len(content)}")
            # 保存内容到文件
            with open("output.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("内容已保存到 output.html")
        else:
            print("登录失败")
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        print("正在关闭浏览器...")
        await crawler.close()
        print("浏览器已关闭")

if __name__ == "__main__":
    asyncio.run(main()) 