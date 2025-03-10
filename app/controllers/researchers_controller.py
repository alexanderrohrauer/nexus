import json
import logging
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.dtos.duplications import MarkDuplicates
from app.dtos.researchers import ResearcherSearchParams
from app.dtos.visualizations import VisualizationData
from app.models import Researcher
from app.services import researchers_service
from app.utils.visualization_helpers import parse_visualization_data
from app.visualizations import CHARTS

router = APIRouter(
    prefix="/researchers",
    tags=["researcher"]
)

logger = logging.getLogger("uvicorn.error")


@router.get("")
async def get_researchers(params: Annotated[ResearcherSearchParams, Depends(ResearcherSearchParams)]) -> list[Researcher]:
    query = params.get_filter()
    logger.debug(query)
    result = await Researcher.find(query, nesting_depth=2, fetch_links=True).limit(params.limit).skip(params.offset).to_list()
    return result


@router.get("/{uuid}")
async def get_researcher(uuid: UUID) -> Researcher:
    return await researchers_service.find_by_id(uuid, fetch_links=True, nesting_depth=2)

@router.get("/{uuid}/duplicates")
async def get_researcher_duplicates(uuid: UUID) -> list[Researcher]:
    return await researchers_service.find_duplicates(uuid)

@router.get("/{uuid}/visualizations/{chart_identifier}")
async def get_researcher_visualization_data(uuid: UUID, chart_identifier: str, q: Optional[str] = "{}") -> VisualizationData:
    researcher = await researchers_service.find_by_id(uuid)
    try:
        chart_cls = next(chart for chart in CHARTS if chart.identifier == chart_identifier)
        return await parse_visualization_data(chart_cls, json.loads(q), {}, researcher=researcher)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Visualization not found")


@router.put("/{uuid}/mark-for-removal")
async def mark_researcher_duplicates(uuid: UUID, dto: MarkDuplicates):
    return await researchers_service.mark_for_removal(uuid, dto.uuids)
