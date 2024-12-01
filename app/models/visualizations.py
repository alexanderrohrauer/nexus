from uuid import UUID, uuid4

from pydantic import Field, BaseModel

from app.db.models import Document


class Visualization(BaseModel):
    uuid: UUID = Field(default=uuid4())
    title: str = Field(min_length=1)
    rows: int = Field(gt=1)
    columns: int = Field(gt=1)
    visualization: str = Field(min_length=1)
    default_query: list | dict = Field(default={})


class Dashboard(Document):
    title: str = Field(min_length=1)
    visualizations: list[Visualization] = Field(default=[])

    class Settings:
        validate_on_save = True
