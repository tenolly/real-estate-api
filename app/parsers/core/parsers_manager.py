import re
import yaml
import logging
import importlib
from typing import Optional, Type, Dict, Any

from .abstract_parser import AbstractParser


PARSER_MANAGER_LOGGER = logging.getLogger(__name__)


class ParserManager:
    by_source_type: Dict[str, Type[AbstractParser]] = {}
    by_url_pattern: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def load_parsers_from_yaml(cls, yaml_path: str) -> None:
        with open(yaml_path, "r") as file:
            config = yaml.safe_load(file)

        for parser_config in config.get("parsers", []):
            source_type = parser_config["source_type"]
            url_pattern = parser_config["url_pattern"]
            parser_class_path = parser_config["parser_class"]

            module_name, class_name = parser_class_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            parser_class = getattr(module, class_name)

            if source_type not in cls.by_url_pattern.keys():
                cls.by_url_pattern[url_pattern] = {}

            cls.by_source_type[source_type] = parser_class
            cls.by_url_pattern[url_pattern]["class"] = parser_class
            cls.by_url_pattern[url_pattern]["source_type"] = source_type

    @classmethod
    def get_parser_by_url(cls, url: str) -> Optional[Type[AbstractParser]]:
        for pattern, values in cls.by_url_pattern.items():
            if re.match(pattern, url):
                return values["class"]

    @classmethod
    def get_source_type_by_url(cls, url: str) -> Optional[str]:
        for pattern, values in cls.by_url_pattern.items():
            if re.match(pattern, url):
                return values["source_type"]

    @classmethod
    def get_parser_by_source_type(
        cls, source_type: str
    ) -> Optional[Type[AbstractParser]]:
        return cls.by_source_type.get(source_type)
