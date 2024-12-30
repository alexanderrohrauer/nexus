from pydantic import BaseModel

from app.utils.visualization_utils import SeriesMap


class VisualizationData(BaseModel):
    series: SeriesMap
    generator: str
    chart_template: str
    filters: dict
