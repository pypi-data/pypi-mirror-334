import asyncio
from mcp.server.fastmcp import FastMCP
from .crawler import WebCrawler
from .logger import logger

mcp = FastMCP("AIM Crawler")
crawler = None

@mcp.resource("website://status")
def get_website_status() -> str:
    """获取网站状态"""
    global crawler
    if crawler is None:
        return "未初始化"
    return "已连接" if crawler.is_logged_in else "未连接"

@mcp.tool()
async def login() -> str:
    """登录网站"""
    global crawler
    try:
        if crawler is None:
            crawler = WebCrawler()
        success = await crawler.login()
        if success:
            return "登录成功"
        else:
            return "登录失败"
    except Exception as e:
        logger.error(f"登录失败: {str(e)}")
        return f"登录失败: {str(e)}"

@mcp.tool()
async def crawl_content() -> str:
    """爬取网站内容"""
    global crawler
    try:
        if crawler is None:
            return "请先登录"
        if not crawler.is_logged_in:
            return "请先登录"
        return await crawler.crawl()
    except Exception as e:
        logger.error(f"爬取失败: {str(e)}")
        return f"爬取失败: {str(e)}"

@mcp.tool()
async def logout() -> str:
    """登出并关闭浏览器"""
    global crawler
    try:
        if crawler:
            await crawler.close()
            crawler = None
        return "已登出并关闭浏览器"
    except Exception as e:
        logger.error(f"登出失败: {str(e)}")
        return f"登出失败: {str(e)}"

@mcp.prompt()
def help_prompt() -> str:
    """显示帮助信息"""
    return """
    AIM Crawler MCP 服务器
    
    可用工具:
    1. login - 登录网站
    2. crawl_content - 爬取网站内容
    3. logout - 登出并关闭浏览器
    
    可用资源:
    1. website://status - 获取网站连接状态
    """

def main():
    """启动MCP服务器"""
    logger.info("Starting AIM Crawler MCP Server")
    mcp.run()

if __name__ == "__main__":
    main() 