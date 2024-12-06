from datetime import datetime
from typing import Optional

from beanie import Link
from pydantic import BaseModel, Field

from app.db.models import EditableDocument
from app.models.researchers import Researcher


class ExternalId(BaseModel):
    openalex: Optional[str]
    orcid: Optional[str]
    dblp: Optional[str]
    doi: Optional[str]


class WorkType(BaseModel):
    openalex: Optional[str]
    orcid: Optional[str]
    dblp: Optional[str]


class Work(EditableDocument):
    external_id: ExternalId
    title: str
    type: WorkType
    publication_year: int
    publication_date: Optional[datetime]
    keywords: list[str]
    authors: list[Link[Researcher]]
    language: Optional[str]
    open_access: Optional[bool]
    openalex_meta: Optional[dict] = Field(default={})
    orcid_meta: Optional[dict] = Field(default={})
    dblp_meta: Optional[dict] = Field(default={})
    imported_at: datetime = Field(default_factory=datetime.now)
    manually_updated_at: Optional[datetime]
