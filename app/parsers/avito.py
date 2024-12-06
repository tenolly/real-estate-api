from pydantic import HttpUrl
from parsers.core import AbstractParser

from .core.browser.browser_instance import BrowserManager
from api.schemas.source import SourceParseResults


class AvitoParser(AbstractParser):
    @classmethod
    async def parse(self, url: HttpUrl) -> SourceParseResults:
        browser_manager = BrowserManager()

        context = await browser_manager.launch()

        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded")

        price = " ".join(
            await page.locator(
                "xpath=//span[contains(@class, 'style-price-value')]"
            ).first.all_text_contents()
        )

        is_publicated = (
            await page.query_selector("//div[contains(@class, 'closed-warning-block')]")
        ) is None

        await page.close()

        return SourceParseResults(is_publicated=is_publicated, price=price)
