from enum import Enum

from beanie import Link
from pydantic import Field, BaseModel
from typing_extensions import Optional

from app.db.models import EditableDocument, SNMEntity
from app.models import Institution


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


class Affiliation(BaseModel):
    years: list[int]
    type: Optional[AffiliationType] = None
    institution: Link[Institution]


class Researcher(EditableDocument, SNMEntity):
    external_id: ResearcherExternalId
    full_name: str
    alternative_names: Optional[list[str]] = None
    # TODO normalize affiliations
    affiliations: Optional[list[Affiliation]] = None
    institution: Optional[Link[Institution]] = None
    country: Optional[str] = None
    topic_keywords: Optional[list[str]] = None
    openalex_meta: Optional[dict] = Field(default=None)
    orcid_meta: Optional[dict] = Field(default=None)
    dblp_meta: Optional[dict] = Field(default=None)

    @property
    def normalized_full_name(self):
        # TODO eventually normalize
        return self.full_name.lower()

    def replace_affiliation(self, institution: Institution, replacement: Institution):
        if self.affiliations is not None:
            try:
                found_affiliation = next(filter(lambda a: a.institution.ref.id == institution.id, self.affiliations))
                found_affiliation.institution = replacement
            except StopIteration:
                raise Exception(f"Affiliation with institution {institution.id} was not found in researcher {self.id}")

    class Settings:
        validate_on_save = True
