import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

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
    result = await Researcher.find(query, fetch_links=True).limit(params.limit).skip(params.offset).to_list()
    return result


@router.get("/{uuid}")
async def get_researcher(uuid: UUID) -> Researcher:
    return await researchers_service.find_by_id(uuid)
