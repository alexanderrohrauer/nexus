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
@router.get("/{chart_type}")
async def get_mixed_charts(chart_type: ChartType) -> list[ChartInfo]:
    mixed_charts = filter(lambda chart: chart.type == chart_type, CHARTS)
    return [ChartInfo(value=chart.identifier, label=chart.name) for chart in mixed_charts]
