import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dtos.duplications import MarkDuplicates
from app.dtos.researchers import ResearcherSearchParams
from app.models import Researcher
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



@router.put("/{uuid}/mark-for-removal")
async def mark_researcher_duplicates(uuid: UUID, dto: MarkDuplicates):
    return await researchers_service.mark_for_removal(uuid, dto.uuids)
