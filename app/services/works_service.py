from uuid import UUID

from app.models import Work


async def insert_many(works: list[Work]):
    for work in works:
        await Work.insert_one(work)

async def find_by_id(uuid: UUID):
    return await Work.find_one(Work.uuid == uuid)
