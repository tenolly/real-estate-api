from pydantic import HttpUrl
from parsers.core import AbstractParser
from api.schemas.source import SourceParseResults


class AvitoParser(AbstractParser):
    @classmethod
    async def parse(self, url: HttpUrl) -> SourceParseResults:
        return SourceParseResults(is_publicated=True, price="23000 рублей/мес")
