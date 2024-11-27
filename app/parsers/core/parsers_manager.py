import re
import logging
from typing import Optional, Type, Dict, List, Any, Union

from .abstract_parser import AbstractParser
from parsers.avito import AvitoParser


PARSER_MANAGER_LOGGER = logging.getLogger(__name__)


class ParserManager:
    __parsers: List[Dict[str, Union[str, Type[AbstractParser]]]] = [
        {
            "source_type": "avito",
            "url_pattern": "^https:\/\/www\.avito\.ru(\/[\w\-._~:\/?#[\]@!$&'()*+,;=]*)?$",
            "parser_class": AvitoParser,
        }
    ]

    # For get methods
    __by_source_type: Dict[str, Type[AbstractParser]] = {}
    __by_url_pattern: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def init(cls) -> None:
        for parser_config in cls.__parsers:
            source_type = parser_config["source_type"]
            url_pattern = parser_config["url_pattern"]
            parser_class = parser_config["parser_class"]

            if source_type not in cls.__by_url_pattern.keys():
                cls.__by_url_pattern[url_pattern] = {}

            cls.__by_source_type[source_type] = parser_class
            cls.__by_url_pattern[url_pattern]["class"] = parser_class
            cls.__by_url_pattern[url_pattern]["source_type"] = source_type

    @classmethod
    def get_parser_by_url(cls, url: str) -> Optional[Type[AbstractParser]]:
        for pattern, values in cls.__by_url_pattern.items():
            if re.match(pattern, url):
                return values["class"]

    @classmethod
    def get_source_type_by_url(cls, url: str) -> Optional[str]:
        for pattern, values in cls.__by_url_pattern.items():
            if re.match(pattern, url):
                return values["source_type"]

    @classmethod
    def get_parser_by_source_type(
        cls, source_type: str
    ) -> Optional[Type[AbstractParser]]:
        return cls.__by_source_type.get(source_type)
