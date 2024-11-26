from datetime import datetime

from models.source import SourceModel
from api.schemas.source import SourceParseResults


async def update_source_with_parsing_results(
    source: SourceModel, parsing_results: SourceParseResults
) -> None:
    source.is_publicated = parsing_results.is_publicated
    source.price = parsing_results.price
    source.last_check_ts = int(datetime.now().timestamp())
    return source
