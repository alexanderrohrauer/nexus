from uuid import UUID

from fastapi import HTTPException

from app.dtos.visualizations import VisualizationData
from app.models import Dashboard
from app.utils.visualization_utils import ChartInput
from app.visualizations import CHARTS


async def get_visualization_data(dashboard: Dashboard, visualization_uuid: UUID, queries: dict) -> VisualizationData:
    try:
        visualization = next(v for v in dashboard.visualizations if v.uuid == visualization_uuid)
        chart_cls = next(chart for chart in CHARTS if chart.identifier == visualization.chart)
        chart_instance = chart_cls()
        chart_input = ChartInput(queries=queries, pre_filters=visualization.query_preset)
        return VisualizationData(
            series=await chart_instance.get_series(chart_input),
            generator=chart_instance.generator,
            chart_template=chart_instance.chart_template,
            filters=chart_input.queries)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Visualization/Type not found")
