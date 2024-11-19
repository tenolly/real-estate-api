from sqlalchemy.orm import declarative_base

Base = declarative_base()


from .source import SourceModel


__all__ = ["SourceModel"]
