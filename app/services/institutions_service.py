from uuid import UUID

from app.models import Institution


async def insert_many(institutions: list[Institution]):
    for institution in institutions:
        await Institution.insert_one(institution)

async def find_by_id(uuid: UUID):
    return await Institution.find_one(Institution.uuid == uuid)
