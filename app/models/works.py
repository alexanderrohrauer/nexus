from datetime import date
from typing import Optional

from beanie import Link
from pydantic import BaseModel, Field

from app.db.models import EditableDocument
from app.models.researchers import Researcher


class WorkExternalId(BaseModel):
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
    external_id: WorkExternalId
    title: str
    type: WorkType
    publication_year: int
    publication_date: Optional[date] = None
    keywords: Optional[list[str]] = None
    authors: Optional[list[Link[Researcher]]] = None
    language: Optional[str] = None
    open_access: Optional[bool] = None
    openalex_meta: Optional[dict] = Field(default=None)
    orcid_meta: Optional[dict] = Field(default=None)
    dblp_meta: Optional[dict] = Field(default=None)

    class Settings:
        validate_on_save = True
