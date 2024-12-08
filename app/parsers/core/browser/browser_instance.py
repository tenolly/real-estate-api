import os
import json
import random
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
        self.async_pw = async_playwright()
        self.semaphore = asyncio.Semaphore(10)

        self.proxies = json.loads(
            open(os.path.join(os.path.dirname(__file__), "proxies.json")).read()
        )

    async def launch(self, with_proxy: bool = False) -> BrowserContext:
        if self.browser is not None:
            return await self._create_new_context(with_proxy)

        self.async_pw = await self.async_pw.__aenter__()
        self.browser = await self.async_pw.chromium.launch(
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-extensions",
                "--disable-infobars",
                "--enable-automation",
                "--no-first-run",
                "--enable-webgl",
            ]
        )

        return await self._create_new_context(with_proxy)

    async def _create_new_context(self, with_proxy: bool = False) -> BrowserContext:
        proxy = None
        if with_proxy:
            proxy = random.choice(self.proxies)

        context = await self.browser.new_context(
            user_agent=await self._get_useragent(), proxy=proxy
        )

        await context.add_init_script(
            path=os.path.join(os.path.dirname(__file__), "stealth.min.js")
        )

        return context

    async def _get_useragent(self) -> str:
        return FakeUserAgent(platforms=["desktop"]).random


if __name__ == "__main__":
    # Check browser instance

    async def main():
        browser = BrowserManager()

        context = await browser.launch(True)
        page = await context.new_page()

        # https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html
        # https://www.browserscan.net/bot-detection
        # https://bot.sannysoft.com/
        await page.goto("https://whatismyipaddress.com/")
        input()

    asyncio.run(main())
