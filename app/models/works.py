from datetime import date
from typing import Optional

from beanie import Link
from pydantic import BaseModel, Field

from app.db.models import EditableDocument
from app.models.researchers import Researcher


class ExternalId(BaseModel):
    openalex: Optional[str] = None
    orcid: Optional[str] = None
    dblp: Optional[str] = None
    doi: Optional[str] = None


class WorkType(BaseModel):
    openalex: Optional[str] = None
    orcid: Optional[str] = None
    dblp: Optional[str] = None


# TODO maybe cite information (and take the newer/higher one), doi on root level, related works
class Work(EditableDocument):
    external_id: ExternalId
    title: str
    type: WorkType
    publication_year: int
    publication_date: Optional[date] = None
    keywords: list[str]
    authors: list[Link[Researcher]]
    language: Optional[str] = None
    open_access: Optional[bool] = None
    openalex_meta: Optional[dict] = Field(default={})
    orcid_meta: Optional[dict] = Field(default={})
    dblp_meta: Optional[dict] = Field(default={})

    class Settings:
        validate_on_save = True
