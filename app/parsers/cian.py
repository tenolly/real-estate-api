from pydantic import HttpUrl

from api.schemas.source import SourceParseResults
from parsers.core import AbstractParser
from parsers.exceptions import PriceNotFoundException
from .core.browser.browser_instance import BrowserManager


class CianParser(AbstractParser):
    @classmethod
    async def parse(self, url: HttpUrl) -> SourceParseResults:
        browser_manager = BrowserManager()

        async with browser_manager.semaphore:
            context = await browser_manager.launch()

            page = await context.new_page()
            await page.goto(url, wait_until="domcontentloaded")

            price = " ".join(
                await page.locator(
                    "xpath=//div[@data-name='PriceInfo']/div/span"
                ).first.all_text_contents()
            )

            if not price:
                raise PriceNotFoundException()

            is_publicated = (
                await page.query_selector("//div[@data-name='OfferUnpublished']")
            ) is None

            await page.close()

        return SourceParseResults(is_publicated=is_publicated, price=price)
