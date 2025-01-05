from uuid import UUID

from pydantic import BaseModel


class MarkDuplicates(BaseModel):
    uuids: list[UUID]
