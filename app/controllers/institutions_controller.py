import json
import logging
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.dtos.duplications import MarkDuplicates
from app.dtos.institutions import InstitutionSearchParams
from app.dtos.visualizations import VisualizationData
from app.models import Institution
from app.services import institutions_service
from app.utils.visualization_helpers import parse_visualization_data
from app.visualizations import CHARTS

router = APIRouter(
    prefix="/institutions",
    tags=["institution"]
)

logger = logging.getLogger("uvicorn.error")


@router.get("")
async def get_institutions(params: Annotated[InstitutionSearchParams, Depends(InstitutionSearchParams)]) -> list[
    Institution]:
    query = params.get_filter()
    logger.debug(query)
    result = await Institution.find(query, nesting_depth=3, fetch_links=True).limit(params.limit).skip(
        params.offset).to_list()
    return result


@router.get("/{uuid}")
async def get_institution(uuid: UUID) -> Institution:
    return await institutions_service.find_by_id(uuid)


@router.get("/{uuid}/duplicates")
async def get_institution_duplicates(uuid: UUID) -> list[Institution]:
    return await institutions_service.find_duplicates(uuid)


@router.get("/{uuid}/visualizations/{chart_identifier}")
async def get_institution_visualization_data(uuid: UUID, chart_identifier: str,
                                            q: Optional[str] = "{}") -> VisualizationData:
    institution = await institutions_service.find_by_id(uuid)
    try:
        chart_cls = next(chart for chart in CHARTS if chart.identifier == chart_identifier)
        return await parse_visualization_data(chart_cls, json.loads(q), {}, institution=institution)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Visualization not found")


@router.put("/{uuid}/mark-for-removal")
async def mark_institution_duplicates(uuid: UUID, dto: MarkDuplicates):
    return await institutions_service.mark_for_removal(uuid, dto.uuids)
