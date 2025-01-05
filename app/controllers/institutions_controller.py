import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dtos.duplications import MarkDuplicates
from app.dtos.institutions import InstitutionSearchParams
from app.models import Institution
from app.services import institutions_service

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
    result = await Institution.find(query, nesting_depth=2, fetch_links=True).limit(params.limit).skip(params.offset).to_list()
    return result


@router.get("/{uuid}")
async def get_institution(uuid: UUID) -> Institution:
    return await institutions_service.find_by_id(uuid)

@router.get("/{uuid}/duplicates")
async def get_institution_duplicates(uuid: UUID) -> list[Institution]:
    return await institutions_service.find_duplicates(uuid)

@router.put("/{uuid}/mark-for-removal")
async def mark_institution_duplicates(uuid: UUID, dto: MarkDuplicates):
    return await institutions_service.mark_for_removal(uuid, dto.uuids)
