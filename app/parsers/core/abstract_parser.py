from abc import ABC, abstractmethod

from pydantic import HttpUrl

from api.schemas.source import SourceParseResults


class AbstractParser(ABC):
    @classmethod
    @abstractmethod
    async def parse(self, url: HttpUrl) -> SourceParseResults:
        pass
