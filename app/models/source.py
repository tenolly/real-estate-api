import uuid

from sqlalchemy import UUID, Column, String, Text, BigInteger, Boolean

from . import Base


class SourceModel(Base):
    __tablename__ = "sources"

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, unique=True, nullable=False, index=True)
    source_type = Column(Text, nullable=False)
    last_check_ts = Column(BigInteger)
    is_publicated = Column(Boolean)
    price = Column(Text)
