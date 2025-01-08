import logging
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dtos.duplications import MarkDuplicates
from app.dtos.researchers import ResearcherSearchParams
from app.models import Researcher, Affiliation
from app.services import researchers_service

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
    return await researchers_service.find_by_id(uuid)

@router.get("/{uuid}/duplicates")
async def get_researcher_duplicates(uuid: UUID) -> list[Researcher]:
    return await researchers_service.find_duplicates(uuid)

class ResearcherVisualizations(BaseModel):
    affiliations: Optional[list[Affiliation]] = None

@router.get("/{uuid}/visualizations")
async def get_researcher_visualizations(uuid: UUID) -> ResearcherVisualizations:
    result = ResearcherVisualizations()
    researcher = await researchers_service.find_by_id(uuid, fetch_links=True)
    result.affiliations = researcher.affiliations
    return result


@router.put("/{uuid}/mark-for-removal")
async def mark_researcher_duplicates(uuid: UUID, dto: MarkDuplicates):
    return await researchers_service.mark_for_removal(uuid, dto.uuids)
