import os
import json

from pydantic import HttpUrl
from rebrowser_playwright.async_api import BrowserContext

from api.schemas.source import SourceParseResults
from parsers.core import AbstractParser
from parsers.exceptions import PriceNotFoundException
from .core.browser.browser_instance import BrowserManager


class AvitoParser(AbstractParser):
    cookies_path = os.path.join(os.path.dirname(__file__), "cookies", "avito.json")
    cookies = json.loads(open(cookies_path).read())

    @classmethod
    async def parse(cls, url: HttpUrl) -> SourceParseResults:
        browser_manager = BrowserManager()

        async with browser_manager.semaphore:
            context = await browser_manager.launch(cookies=cls.cookies)

            try:
                page = await context.new_page()
                await page.goto(url, wait_until="domcontentloaded")
                await page.wait_for_selector(
                    "xpath=//span[contains(@class, 'style-price-value')]", timeout=10000
                )

                price = " ".join(
                    await page.locator(
                        "xpath=//span[contains(@class, 'style-price-value')]"
                    ).first.all_text_contents()
                )

                if not price:
                    raise PriceNotFoundException()

                is_publicated = (
                    await page.query_selector(
                        "//div[contains(@class, 'closed-warning-block')]"
                    )
                ) is None

                await page.close()
            finally:
                cls.cookies = await context.cookies()
                with open(cls.cookies_path, mode="w") as file:
                    file.write(json.dumps(cls.cookies))

                await context.close()

        return SourceParseResults(is_publicated=is_publicated, price=price)
