import logging
from uuid import UUID

from app.models import Work

WORKS_AUTHORS_MAX_LENGTH = 30

logger = logging.getLogger("uvicorn.error")


async def insert_many(works: list[Work]):
    for work in works:
        if len(work.authors) > WORKS_AUTHORS_MAX_LENGTH:
            await Work.insert_one(work)
        else:
            logger.error(f"Error while inserting work {work.external_id}: Validation failed")


async def find_by_id(uuid: UUID):
    return await Work.find_one(Work.uuid == uuid)


async def find_duplicates(uuid: UUID) -> list[Work]:
    entity = await find_by_id(uuid)
    return await Work.find(
        Work.duplication_key == entity.duplication_key,
        Work.uuid != entity.uuid).to_list() if entity.duplication_key is not None else []


async def mark_for_removal(uuid: UUID, uuids: list[UUID]):
    duplicates = await find_duplicates(uuid)
    for duplicate in duplicates:
        await duplicate.set({Work.marked_for_removal: duplicate.uuid in uuids})
