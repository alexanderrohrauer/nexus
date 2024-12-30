from uuid import UUID, uuid4

from pydantic import Field, BaseModel

from app.db.models import Document


class Visualization(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    title: str = Field(min_length=1)
    # TODO max 12
    rows: int = Field(gt=1)
    columns: int = Field(gt=1)
    chart: str = Field(min_length=1)
    query_preset: dict = Field(default={})


class Dashboard(Document):
    title: str = Field(min_length=1)
    visualizations: list[Visualization] = Field()

    class Settings:
        validate_on_save = True
