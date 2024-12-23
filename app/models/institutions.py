from typing import Optional, Tuple, Annotated

import pymongo
from beanie import Indexed
from pydantic import Field, HttpUrl, BaseModel

from app.db.models import EditableDocument, SNMEntity


class InstitutionExternalId(BaseModel):
    grid: Optional[str] = None
    mag: Optional[str] = None
    openalex: Optional[str] = None
    ror: Optional[str] = None
    wikipedia: Optional[str] = None
    wikidata: Optional[str] = None

    def ror_match(self, external_id):
        return self.ror is not None and self.ror == external_id.ror

    def openalex_match(self, external_id):
        return self.openalex is not None and self.openalex == external_id.openalex

    def matches(self, external_id):
        return self.openalex_match(external_id) or self.ror_match(external_id)


# TODO maybe do here also Optional everywhere...
class Institution(EditableDocument, SNMEntity):
    external_id: InstitutionExternalId
    name: str
    acronyms: list[str]
    alternative_names: list[str]
    international_names: dict[str, str]
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = Field(description="Is the country code", default=None)
    location: Annotated[Optional[Tuple[float, float]], Indexed(index_type=pymongo.GEOSPHERE)] = Field(default=None,
                                                                                                      description="Long-Lat")
    homepage_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    # TODO maybe do UUIDs some day:
    parent_institutions_ids: list[str]
    type: Optional[str] = None
    topic_keywords: list[str]
    openalex_meta: Optional[dict] = Field(default=None)
    orcid_meta: Optional[dict] = Field(default=None)
    dblp_meta: Optional[dict] = Field(default=None)

    @property
    def normalized_name(self): 
        # TODO normalize eventually
        return self.name.lower()

    class Settings:
        validate_on_save = True
