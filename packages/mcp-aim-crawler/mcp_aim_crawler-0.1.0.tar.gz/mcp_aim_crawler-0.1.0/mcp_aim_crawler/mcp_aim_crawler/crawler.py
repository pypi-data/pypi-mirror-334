import os
import asyncio
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError

# 设置日志
logger = logging.getLogger('mcp_aim_crawler')
logger.setLevel(logging.DEBUG)  # 改为DEBUG级别以获取更多信息
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class WebCrawler:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://app.datatist.com"
        self.login_url = f"{self.base_url}/aimarketer/login"
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        
        if not all([self.username, self.password]):
            raise ValueError("Missing required environment variables: USERNAME, PASSWORD")
        
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.is_logged_in = False
        logger.info("WebCrawler initialized")
    
    async def _setup_browser(self):
        """初始化浏览器"""
        if self.browser is None:
            logger.info("Starting browser...")
            playwright = await async_playwright().start()
            # 使用chromium，设置headless模式，添加更多选项以提高稳定性
            self.browser = await playwright.chromium.launch(
                headless=False,  # 设置为False以便于调试
                args=[
                    '--disable-dev-shm-usage',  # 禁用/dev/shm使用
                    '--no-sandbox',  # 禁用沙箱
                    '--disable-setuid-sandbox',  # 禁用setuid沙箱
                    '--disable-gpu',  # 禁用GPU硬件加速
                ]
            )
            self.page = await self.browser.new_page()
            # 设置视窗大小
            await self.page.set_viewport_size({"width": 1920, "height": 1080})
            # 启用请求拦截
            await self.page.route("**/*", self._handle_route)
            logger.info("Browser started successfully")
    
    async def _handle_route(self, route):
        """处理请求拦截"""
        # 记录所有请求
        logger.debug(f"Request: {route.request.method} {route.request.url}")
        await route.continue_()
    
    async def login(self) -> bool:
        """
        登录datatist.com
        
        Returns:
            bool: 登录是否成功
        """
        if self.is_logged_in:
            logger.info("Already logged in")
            return True
            
        try:
            await self._setup_browser()
            if not self.page:
                raise ValueError("Browser not initialized")
            
            logger.info(f"Navigating to login page: {self.login_url}")
            # 访问登录页面
            await self.page.goto(self.login_url)
            
            # 等待登录表单加载
            logger.info("Waiting for login form...")
            # 等待页面加载完成
            await self.page.wait_for_load_state("networkidle")
            
            # 获取页面HTML以进行调试
            html = await self.page.content()
            logger.debug(f"Page HTML: {html}")
            
            # 等待输入框出现，增加超时时间
            logger.info("Waiting for email input...")
            email_input = await self.page.wait_for_selector('input[type="text"]', timeout=30000)
            logger.info("Waiting for password input...")
            password_input = await self.page.wait_for_selector('input[type="password"]', timeout=30000)
            
            if not email_input or not password_input:
                raise ValueError("Login form not found")
            
            # 输入用户名和密码
            logger.info("Filling login form...")
            await email_input.fill(self.username)
            await password_input.fill(self.password)
            
            # 点击登录按钮
            logger.info("Clicking login button...")
            # 尝试多个可能的选择器
            login_button = None
            for selector in [
                'button:has-text("登录")',
                'button[type="submit"]',
                '.ant-btn-primary',
                'button.ant-btn-primary',
            ]:
                try:
                    logger.debug(f"Trying selector: {selector}")
                    login_button = await self.page.wait_for_selector(selector, timeout=5000)
                    if login_button:
                        logger.info(f"Found login button with selector: {selector}")
                        break
                except PlaywrightTimeoutError:
                    logger.debug(f"Selector not found: {selector}")
                    continue
            
            if login_button:
                await login_button.click()
            else:
                raise ValueError("Login button not found")
            
            # 等待登录完成，检查是否重定向到仪表板
            try:
                logger.info("Waiting for login completion...")
                await self.page.wait_for_url(f"{self.base_url}/aimarketer/dashboard", timeout=30000)
                self.is_logged_in = True
                logger.info("Login successful")
                return True
            except PlaywrightTimeoutError:
                # 如果超时，检查是否有错误消息
                error_message = await self.page.evaluate("""() => {
                    const errorElement = document.querySelector('.ant-message-error');
                    return errorElement ? errorElement.textContent : null;
                }""")
                if error_message:
                    logger.error(f"Login failed: {error_message}")
                else:
                    logger.error("Login failed: Timeout waiting for dashboard redirect")
                self.is_logged_in = False
                return False
            
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            self.is_logged_in = False
            raise
    
    async def crawl(self) -> str:
        """
        爬取网站内容
        
        Returns:
            str: 爬取到的内容
        """
        if not self.is_logged_in:
            raise ValueError("Not logged in")
            
        try:
            if not self.page:
                raise ValueError("Browser not initialized")
                
            # 获取AI Marketer仪表板内容
            logger.info("Navigating to productcenter...")
            await self.page.goto(f"{self.base_url}/aimarketer/usercenter/productcenter")
            
            # 等待页面加载完成
            logger.info("Waiting for page load...")
            await self.page.wait_for_load_state("networkidle")
            
            # 获取页面内容
            logger.info("Getting page content...")
            content = await self.page.content()
            logger.info("Content crawled successfully")
            return content
            
        except Exception as e:
            logger.error(f"Crawl failed: {str(e)}")
            raise
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            logger.info("Closing browser...")
            await self.browser.close()
            self.browser = None
            self.page = None
            self.is_logged_in = False
            logger.info("Browser closed")

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