from datetime import datetime
from typing import Optional, Annotated
from uuid import uuid4, UUID

import beanie
from pydantic import Field, BaseModel, PlainSerializer

UTCDateTime = Annotated[
    datetime,
    PlainSerializer(lambda _datetime: _datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), return_type=str),
]


class Document(beanie.Document):
    uuid: UUID = Field(default_factory=uuid4)


class EditableDocument(Document):
    imported_at: UTCDateTime = Field(default_factory=datetime.now)
    # TODO set at manual write
    manually_updated_at: Optional[UTCDateTime] = None
    duplication_key: Optional[UUID] = None
    marked_for_removal: bool = False


class SNMEntity(BaseModel):
    snm_key: Optional[str] = None
