from uuid import uuid4, UUID

import beanie
from pydantic import Field


class Document(beanie.Document):
    uuid: UUID = Field(default_factory=uuid4)
