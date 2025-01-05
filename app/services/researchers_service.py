from uuid import UUID

from beanie import WriteRules

from app.models import Researcher


async def insert_many(researchers: list[Researcher]):
    for researcher in researchers:
        await Researcher.insert_one(researcher, link_rule=WriteRules.WRITE)


async def find_by_id(uuid: UUID):
    return await Researcher.find_one(Researcher.uuid == uuid)

async def find_duplicates(uuid: UUID) -> list[Researcher]:
    entity = await find_by_id(uuid)
    return await Researcher.find(
        Researcher.duplication_key == entity.duplication_key,
        Researcher.uuid != entity.uuid).to_list() if entity.duplication_key is not None else []


async def mark_for_removal(uuid: UUID, uuids: list[UUID]):
    duplicates = await find_duplicates(uuid)
    for duplicate in duplicates:
        await duplicate.set({Researcher.marked_for_removal: duplicate.uuid in uuids})

