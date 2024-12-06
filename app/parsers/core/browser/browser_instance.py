import os
import asyncio

from fake_useragent import FakeUserAgent
from rebrowser_playwright.async_api import async_playwright, BrowserContext


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class BrowserManager(metaclass=Singleton):
    def __init__(self):
        self.browser = None
        self.context = async_playwright()

    async def launch(self) -> BrowserContext:
        if self.browser is not None:
            return await self._create_new_context()

        self.context = await self.context.__aenter__()
        self.browser = await self.context.chromium.launch(
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-extensions",
                "--disable-infobars",
                "--enable-automation",
                "--no-first-run",
                "--enable-webgl",
            ]
        )

        return await self._create_new_context()

    async def _create_new_context(self) -> BrowserContext:
        context = await self.browser.new_context(user_agent=await self._get_useragent())

        await context.add_init_script(
            path=os.path.join(os.path.dirname(__file__), "stealth.min.js")
        )

        return context

    async def _get_useragent(self) -> str:
        return FakeUserAgent(platforms=["desktop"]).random


if __name__ == "__main__":
    # Check bot detection

    async def main():
        browser = BrowserManager()

        context = await browser.launch()
        page = await context.new_page()

        # https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html
        # https://www.browserscan.net/bot-detection
        # https://bot.sannysoft.com/
        await page.goto("https://www.browserscan.net/bot-detection")
        input()

    asyncio.run(main())
