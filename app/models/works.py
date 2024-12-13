from datetime import date
from typing import Optional

from beanie import Link
from pydantic import BaseModel, Field

from app.db.models import EditableDocument, SNMEntity
from app.models.researchers import Researcher


class WorkExternalId(BaseModel):
    openalex: Optional[str] = None
    mag: Optional[str] = None
    dblp: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    pmcid: Optional[str] = None


class WorkType(BaseModel):
    openalex: Optional[str] = None
    orcid: Optional[str] = None
    dblp: Optional[str] = None


# TODO maybe related works...
class Work(EditableDocument, SNMEntity):
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

    def replace_author(self, researcher: Researcher, replacement: Researcher):
        if self.authors is not None:
            try:
                found_author_link = next(filter(lambda a: a.ref.id == researcher.id, self.authors))
                index: int = self.authors.index(found_author_link)
                self.authors[index] = replacement
            except StopIteration:
                raise Exception(f"Researcher {researcher.id} was not found in work {self.id}")

    class Settings:
        validate_on_save = True
