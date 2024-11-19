from typing import Optional
from uuid import UUID
from pydantic import BaseModel, HttpUrl


class SourceItem(BaseModel):
    uid: UUID
    url: HttpUrl
    source_type: str
    last_check_ts: Optional[int] = None
    is_publicated: Optional[bool] = False
    price: Optional[str] = None

    class Config:
        from_attributes = True


class SourceParseResults(BaseModel):
    is_publicated: bool
    price: str


class SourceCreateRequest(BaseModel):
    url: HttpUrl
