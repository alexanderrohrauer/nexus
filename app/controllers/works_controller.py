import json
import logging
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.dtos.visualizations import VisualizationData
from app.dtos.works import WorkSearchParams
from app.models import Work
from app.services import works_service
from app.utils.visualization_helpers import parse_visualization_data
from app.visualizations import CHARTS

router = APIRouter(
    prefix="/works",
    tags=["work"]
)

logger = logging.getLogger("uvicorn.error")


@router.get("")
async def get_works(params: Annotated[WorkSearchParams, Depends(WorkSearchParams)]) -> list[Work]:
    query = params.get_filter()
    logger.debug(query)
    result = await Work.find(query, nesting_depth=2, fetch_links=True).limit(params.limit).skip(params.offset).to_list()
    return result


@router.get("/{uuid}")
async def get_work(uuid: UUID) -> Work:
    return await works_service.find_by_id(uuid)


@router.get("/{uuid}/duplicates")
async def get_work_duplicates(uuid: UUID) -> list[Work]:
    return await works_service.find_duplicates(uuid)


@router.get("/{uuid}/visualizations/{chart_identifier}")
async def get_institution_visualization_data(uuid: UUID, chart_identifier: str,
                                             q: Optional[str] = "{}") -> VisualizationData:
    work = await works_service.find_by_id(uuid)
    try:
        chart_cls = next(chart for chart in CHARTS if chart.identifier == chart_identifier)
        return await parse_visualization_data(chart_cls, json.loads(q), {}, work=work)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Visualization not found")


@router.put("/{uuid}/mark-for-removal")
async def mark_work_duplicates(uuid: UUID, dto: Work):
    return await works_service.mark_for_removal(uuid, dto.uuids)
