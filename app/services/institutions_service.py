from uuid import UUID

from app.models import Institution


async def insert_many(institutions: list[Institution]):
    for institution in institutions:
        await Institution.insert_one(institution)


async def find_by_id(uuid: UUID):
    return await Institution.find_one(Institution.uuid == uuid)


async def find_duplicates(uuid: UUID) -> list[Institution]:
    entity = await find_by_id(uuid)
    return await Institution.find(
        Institution.duplication_key == entity.duplication_key,
        Institution.uuid != entity.uuid).to_list() if entity.duplication_key is not None else []


async def mark_for_removal(uuid: UUID, uuids: list[UUID]):
    duplicates = await find_duplicates(uuid)
    for duplicate in duplicates:
        await duplicate.set({Institution.marked_for_removal: duplicate.uuid in uuids})
