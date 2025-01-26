from datetime import timedelta
from enum import Enum

from beanie import Link, BackLink
from pydantic import Field, BaseModel
from typing_extensions import Optional

from app.db.models import EditableDocument, SNMEntity
from app.models import Institution
from app.settings import get_settings


class ResearcherExternalId(BaseModel):
    openalex: Optional[str] = None
    orcid: Optional[str] = None
    dblp: Optional[str] = None
    scopus: Optional[str] = None
    twitter: Optional[str] = None
    wikipedia: Optional[str] = None

    def openalex_match(self, external_id):
        return self.openalex is not None and external_id.openalex == self.openalex

    def dblp_match(self, external_id):
        return self.dblp is not None and external_id.dblp == self.dblp

    def orcid_match(self, external_id):
        return self.orcid is not None and external_id.orcid == self.orcid

    def matches(self, external_id):
        return self.openalex_match(external_id) or self.dblp_match(external_id) or self.orcid_match(external_id)


class AffiliationType(Enum):
    EDUCATION = "EDUCATION"
    EMPLOYMENT = "EMPLOYMENT"


class Affiliation(EditableDocument):
    years: list[int]
    type: Optional[AffiliationType] = None
    institution: Link[Institution]

    class Settings:
        validate_on_save = True


class Researcher(EditableDocument, SNMEntity):
    external_id: ResearcherExternalId
    full_name: str
    alternative_names: Optional[list[str]] = None
    affiliations: Optional[list[Link[Affiliation]]] = None
    institution: Optional[Link[Institution]] = None
    topic_keywords: Optional[list[str]] = None
    openalex_meta: Optional[dict] = Field(default=None)
    orcid_meta: Optional[dict] = Field(default=None)
    dblp_meta: Optional[dict] = Field(default=None)
    works: list[BackLink["Work"]] = Field(original_field="authors", exclude=True)

    @property
    def normalized_full_name(self):
        # TODO eventually normalize
        return self.full_name.lower()

    class Settings:
        validate_on_save = True
        use_cache = True
        cache_expiration_time = timedelta(minutes=get_settings().mongo_cache_minutes)
