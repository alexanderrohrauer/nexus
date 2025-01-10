from datetime import datetime
from typing import Optional, Annotated
from uuid import uuid4, UUID

import beanie
import pytz
from pydantic import Field, BaseModel, PlainSerializer

UTCDateTime = Annotated[
    datetime,
    PlainSerializer(
        lambda _datetime: _datetime.strftime("%Y-%m-%dT%H:%M:%SZ") if isinstance(_datetime, datetime) else _datetime,
        return_type=str),
]


class Document(beanie.Document):
    uuid: UUID = Field(default_factory=uuid4)


class EditableDocument(Document):
    imported_at: UTCDateTime = Field(default_factory=lambda: datetime.now(tz=pytz.UTC))


class SNMEntity(BaseModel):
    snm_key: Optional[str] = None
    duplication_key: Optional[UUID] = None
    marked_for_removal: bool = False
