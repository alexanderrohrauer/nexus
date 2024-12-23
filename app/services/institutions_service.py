from app.models import Institution


async def insert_many(institutions: list[Institution]):
    for institution in institutions:
        await Institution.insert_one(institution)
