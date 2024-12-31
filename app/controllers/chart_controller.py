from fastapi import APIRouter
from pydantic import BaseModel

from app.utils.visualization_utils import ChartType
from app.visualizations import CHARTS

router = APIRouter(
    prefix="/charts",
    tags=["chart"]
)

class ChartInfo(BaseModel):
    value: str
    label: str
@router.get("/mixed")
async def get_mixed_charts() -> list[ChartInfo]:
    mixed_charts = filter(lambda chart: chart.type == ChartType.MIXED, CHARTS)
    return [ChartInfo(value=chart.identifier, label=chart.name) for chart in mixed_charts]
