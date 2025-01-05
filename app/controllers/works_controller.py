import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dtos.works import WorkSearchParams
from app.models import Work
from app.services import works_service

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

@router.put("/{uuid}/mark-for-removal")
async def mark_work_duplicates(uuid: UUID, dto: Work):
    return await works_service.mark_for_removal(uuid, dto.uuids)
