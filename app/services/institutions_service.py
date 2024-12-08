from app.models import Institution


async def upsert_many(institutions: list[Institution]):
    # TODO do find logic here for upsert
    for institution in institutions:
        await Institution.insert_one(institution)

