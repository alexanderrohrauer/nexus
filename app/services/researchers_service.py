from uuid import UUID

from beanie import WriteRules

from app.models import Researcher


async def insert_many(researchers: list[Researcher]):
    for researcher in researchers:
        await Researcher.insert_one(researcher, link_rule=WriteRules.WRITE)


async def find_by_id(uuid: UUID):
    return await Researcher.find_one(Researcher.uuid == uuid)
