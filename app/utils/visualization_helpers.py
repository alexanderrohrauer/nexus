from fastapi import HTTPException

from app.dtos.visualizations import VisualizationData
from app.utils.visualization_utils import ChartInput


async def parse_visualization_data(chart_cls, queries: dict, query_preset: dict, **kwargs):
    try:
        chart_instance = chart_cls()
        chart_input = ChartInput(queries=queries, pre_filters=query_preset, **kwargs)
        return VisualizationData(
            series=await chart_instance.get_series(chart_input),
            generator=chart_instance.generator,
            chart_template=chart_instance.chart_template,
            filters=chart_input.queries)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Visualization-type not found")
