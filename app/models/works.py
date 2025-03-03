from datetime import date, timedelta
from typing import Optional

from beanie import Link
from pydantic import BaseModel, Field

from app.db.models import EditableDocument, SNMEntity
from app.models.researchers import Researcher
from app.settings import get_settings


class WorkExternalId(BaseModel):
    openalex: Optional[str] = None
    mag: Optional[str] = None
    dblp: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    pmcid: Optional[str] = None

    def openalex_match(self, external_id):
        return self.openalex is not None and self.openalex == external_id.openalex

    def dblp_match(self, external_id):
        return self.dblp is not None and self.dblp == external_id.dblp

    def doi_match(self, external_id):
        return self.doi is not None and self.doi == external_id.doi

    def matches(self, external_id):
        return self.openalex_match(external_id) or self.dblp_match(external_id) or self.doi_match(external_id)


class WorkType(BaseModel):
    openalex: Optional[str] = None
    orcid: Optional[str] = None
    dblp: Optional[str] = None


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

    @property
    def normalized_title(self):
        return self.title.lower()

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
        use_cache = get_settings().mongo_cache_enabled
        cache_expiration_time = timedelta(minutes=get_settings().mongo_cache_minutes)
