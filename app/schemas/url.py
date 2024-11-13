from typing import Optional
from uuid import UUID
from pydantic import BaseModel, HttpUrl


class SourceItem(BaseModel):
    uid: UUID
    url: HttpUrl
    source_type: Optional[str] = None
    last_check_ts: Optional[int] = None
    is_publicated: Optional[bool] = False

    class Config:
        from_attributes = True


class SourceCreateRequest(BaseModel):
    url: HttpUrl
