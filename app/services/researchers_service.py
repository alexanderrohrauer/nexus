from uuid import UUID

from app.models import Researcher


async def insert_many(researchers: list[Researcher]):
    for researcher in researchers:
        await Researcher.insert_one(researcher)


async def find_by_id(uuid: UUID):
    return await Researcher.find_one(Researcher.uuid == uuid)
