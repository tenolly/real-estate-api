from playwright_stealth import stealth_async
from playwright.async_api import async_playwright, BrowserContext


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

        self.context = await self.context.start()
        self.browser = await self.context.chromium.launch(headless=False)

        return await self._create_new_context()

    async def _create_new_context(self) -> BrowserContext:
        context = await self.browser.new_context(
            user_agent=await self._create_useragent()
        )
        await stealth_async(context)

        return context

    async def _create_useragent(self) -> str:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.89 Safari/537.36"
