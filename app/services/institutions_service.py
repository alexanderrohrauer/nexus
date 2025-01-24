from uuid import UUID

from app.models import Institution
from app.settings import get_settings

settings = get_settings()


async def insert_many(institutions: list[Institution]):
    for i, institution in enumerate(institutions):
        found_institution = await optimized_find_by_openalex_id(institution.external_id.openalex)
        if found_institution is None:
            await Institution.insert_one(institution)
        else:
            institutions[i] = found_institution


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


async def optimized_find_by_openalex_id(openalex_id: str):
    if settings.optimized_insert:
        return await Institution.find_one(
            Institution.external_id.openalex == openalex_id)
    else:
        return None
