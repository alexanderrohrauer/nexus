from typing import Optional, Tuple, Annotated

import pymongo
from beanie import Indexed
from pydantic import Field, HttpUrl, BaseModel

from app.db.models import EditableDocument


class InstitutionExternalId(BaseModel):
    grid: Optional[str] = None
    mag: Optional[str] = None
    openalex: Optional[str] = None
    ror: Optional[str] = None
    wikipedia: Optional[str] = None
    wikidata: Optional[str] = None

class Institution(EditableDocument):
    external_id: InstitutionExternalId
    name: str
    acronyms: list[str]
    alternative_names: list[str]
    international_names: dict[str, str]
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = Field(description="Is the country code", default=None)
    location: Annotated[Optional[Tuple[float, float]], Indexed(index_type=pymongo.GEO2D)] = Field(default=None, description="Long-Lat")
    homepage_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    # TODO maybe do UUIDs some day:
    parent_institutions_ids: list[str]
    type: str
    openalex_meta: Optional[dict] = Field(default={})
    orcid_meta: Optional[dict] = Field(default={})
    dblp_meta: Optional[dict] = Field(default={})


    class Settings:
        validate_on_save = True
