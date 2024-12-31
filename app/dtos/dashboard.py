from uuid import UUID

from pydantic import BaseModel, Field

from app.models import Dashboard
from app.utils.api_utils import ResponseModel


class UpdateVisualizationRequest(BaseModel):
    title: str = Field(min_length=1)
    rows: int = Field(gt=1)
    columns: int = Field(gt=1)
    query_preset: dict


class CreateVisualizationRequest(UpdateVisualizationRequest):
    chart: str = Field(min_length=1)


class CreateDashboardRequest(BaseModel):
    title: str = Field(min_length=1)
    visualizations: list[CreateVisualizationRequest]


class DashboardMinimal(ResponseModel):
    uuid: UUID
    title: str

    @classmethod
    def from_model(cls, model: Dashboard):
        return DashboardMinimal(**model.model_dump())
