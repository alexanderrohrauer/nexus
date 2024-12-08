from enum import Enum

from beanie import Link
from pydantic import Field, BaseModel
from typing_extensions import Optional

from app.db.models import EditableDocument
from app.models import Institution


class ResearcherExternalId(BaseModel):
    openalex: Optional[str] = None
    orcid: Optional[str] = None
    dblp: Optional[str] = None
    scopus: Optional[str] = None
    twitter: Optional[str] = None
    wikipedia: Optional[str] = None


class AffiliationType(Enum):
    EDUCATION = "EDUCATION"
    EMPLOYMENT = "EMPLOYMENT"


class Affiliation(BaseModel):
    years: list[int]
    type: Optional[AffiliationType] = None
    institution: Link[Institution]


class Researcher(EditableDocument):
    external_id: ResearcherExternalId
    full_name: str
    alternative_names: list[str]
    affiliations: list[Affiliation]
    institution: Optional[Link[Institution]] = None
    country: Optional[str] = None
    topic_keywords: list[str]
    openalex_meta: Optional[dict] = Field(default={})
    orcid_meta: Optional[dict] = Field(default={})
    dblp_meta: Optional[dict] = Field(default={})

    class Settings:
        validate_on_save = True
