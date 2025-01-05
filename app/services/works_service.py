from uuid import UUID

from app.models import Work


async def insert_many(works: list[Work]):
    for work in works:
        await Work.insert_one(work)

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
